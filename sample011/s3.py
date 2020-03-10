from troposphere import Template, Ref, Sub, GetAtt, Join
from troposphere.cloudfront import CloudFrontOriginAccessIdentity, CloudFrontOriginAccessIdentityConfig
from troposphere.s3 import Bucket, BucketPolicy


def create_driver_template():
    template = Template()

    bucket = template.add_resource(
        resource=Bucket(
            title='SampleBucket',
            BucketName=Sub('lambda-edge-sample-bucket-${AWS::AccountId}')
        )
    )

    identity = template.add_resource(
        resource=CloudFrontOriginAccessIdentity(
            title='SampleOriginAccessIdentity',
            CloudFrontOriginAccessIdentityConfig=CloudFrontOriginAccessIdentityConfig(
                Comment='lambda-edge-sample'
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

    with open('s3.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_driver_template()
