from troposphere import Template, Parameter, Ref, Sub, GetAtt, Join
from troposphere.cloudfront import CloudFrontOriginAccessIdentity, CloudFrontOriginAccessIdentityConfig, Distribution, \
    DistributionConfig, Origin, S3OriginConfig, DefaultCacheBehavior, ForwardedValues, Cookies, \
    CustomErrorResponse, ViewerCertificate
from troposphere.s3 import Bucket, BucketPolicy


def create_cloud_front_template():
    template = Template()

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

    template.add_resource(
        resource=Distribution(
            title='SampleDistribution',
            DistributionConfig=DistributionConfig(
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
                DefaultCacheBehavior=DefaultCacheBehavior(
                    ForwardedValues=ForwardedValues(
                        QueryString=True,
                    ),
                    TargetOriginId=Sub('S3-${' + bucket.title + '}'),
                    ViewerProtocolPolicy='redirect-to-https',
                ),
                DefaultRootObject='index.html',
                CustomErrorResponses=[
                    CustomErrorResponse(
                        ErrorCode=403,
                        ResponseCode=200,
                        ResponsePagePath='/404.html',
                        ErrorCachingMinTTL=30
                    )
                ]
            )
        )
    )

    with open('./cloudfront.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_cloud_front_template()
