from troposphere import Template, Parameter, Ref, Sub, GetAtt, Join
from troposphere.cloudfront import CloudFrontOriginAccessIdentity, CloudFrontOriginAccessIdentityConfig, Distribution, \
    DistributionConfig, Origin, S3OriginConfig, DefaultCacheBehavior, ForwardedValues, Cookies, \
    CustomErrorResponse, ViewerCertificate
from troposphere.route53 import RecordSetType, AliasTarget
from troposphere.s3 import Bucket, BucketPolicy


def create_cloudfront_template():
    template = Template()

    cname = template.add_parameter(
        parameter=Parameter(
            title='Cname',
            Type='String'
        )
    )

    acm_certificate_arn = template.add_parameter(
        parameter=Parameter(
            title='AcmCertificateArn',
            Type='String'
        )
    )

    host_zone_id = template.add_parameter(
        parameter=Parameter(
            title='HostZoneId',
            Type='String'
        )
    )

    bucket = template.add_resource(
        resource=Bucket(
            title='SampleBucket',
            BucketName=Sub('sample-bucket-${AWS::AccountId}')
        )
    )

    identity = template.add_resource(
        resource=CloudFrontOriginAccessIdentity(
            title='SampleOriginAccessIdentity',
            CloudFrontOriginAccessIdentityConfig=CloudFrontOriginAccessIdentityConfig(
                Comment='sample'
            )
        )
    )

    template.add_resource(
        resource=BucketPolicy(
            title='SampleBucketPolicy',
            Bucket=Ref(bucket),
            PolicyDocument={
                'Statement': [{
                    'Action': 's3:GetObject',
                    'Effect': 'Allow',
                    'Resource': Join(delimiter='/', values=[GetAtt(bucket, 'Arn'), '*']),
                    'Principal': {
                        'CanonicalUser': GetAtt(logicalName=identity, attrName='S3CanonicalUserId')
                    }
                }]
            }
        )
    )

    distribution = template.add_resource(
        resource=Distribution(
            title='SampleDistribution',
            DistributionConfig=DistributionConfig(
                Aliases=[Ref(cname)],
                # CustomErrorResponses=[
                #     CustomErrorResponse(
                #         ErrorCode=403,
                #         ResponseCode=200,
                #         ResponsePagePath='/404.html',
                #         ErrorCachingMinTTL=30
                #     )
                # ],
                DefaultCacheBehavior=DefaultCacheBehavior(
                    ForwardedValues=ForwardedValues(
                        QueryString=True,
                    ),
                    TargetOriginId=Sub('S3-${' + bucket.title + '}'),
                    ViewerProtocolPolicy='redirect-to-https',
                ),
                # DefaultRootObject='index.html',
                Enabled=True,
                Origins=[
                    Origin(
                        Id=Sub('S3-${' + bucket.title + '}'),
                        DomainName=Sub('${' + bucket.title + '}.s3.amazonaws.com'),
                        S3OriginConfig=S3OriginConfig(
                            OriginAccessIdentity=Sub('origin-access-identity/cloudfront/${' + identity.title + '}')
                        )
                    )
                ],
                ViewerCertificate=ViewerCertificate(
                    AcmCertificateArn=Ref(acm_certificate_arn),
                    SslSupportMethod='sni-only'
                )
            )
        )
    )

    template.add_resource(
        resource=RecordSetType(
            title='SampleRecordSet',
            AliasTarget=AliasTarget(
                HostedZoneId='Z2FDTNDATAQYW2',
                DNSName=GetAtt(logicalName=distribution, attrName='DomainName')
            ),
            HostedZoneId=Ref(host_zone_id),
            Name=Ref(cname),
            Type='A'
        )
    )

    with open('./cloudfront.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_cloudfront_template()
