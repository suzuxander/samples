from troposphere import Template, Sub, GetAtt, Join, Ref, ImportValue
from troposphere.cloudfront import Distribution, \
    DistributionConfig, Origin, S3OriginConfig, DefaultCacheBehavior, ForwardedValues, LambdaFunctionAssociation, \
    CloudFrontOriginAccessIdentity, CloudFrontOriginAccessIdentityConfig
from troposphere.s3 import Bucket, BucketPolicy

from sample011.function import get_export_name


def create_cloud_front_template():
    template = Template()
    template.set_transform('AWS::Serverless-2016-10-31')

    bucket = template.add_resource(
        resource=Bucket(
            title='SampleOriginBucket',
            BucketName=Sub('sample-origin-bucket-${AWS::AccountId}')
        )
    )

    identity = template.add_resource(
        resource=CloudFrontOriginAccessIdentity(
            title='SampleOriginAccessIdentity',
            CloudFrontOriginAccessIdentityConfig=CloudFrontOriginAccessIdentityConfig(
                Comment='sample-lambda-edge'
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
                DefaultCacheBehavior=DefaultCacheBehavior(
                    ForwardedValues=ForwardedValues(
                        QueryString=True,
                    ),
                    LambdaFunctionAssociations=[
                        LambdaFunctionAssociation(
                            EventType='viewer-request',
                            LambdaFunctionARN=Sub([
                                '${FUNCTION_ARN}:8', {'FUNCTION_ARN': ImportValue(get_export_name())}
                            ]),
                        )
                    ],
                    TargetOriginId=Sub('S3-${' + bucket.title + '}'),
                    ViewerProtocolPolicy='redirect-to-https',
                ),
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
            )
        )
    )

    with open('./cloudfront.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_cloud_front_template()
