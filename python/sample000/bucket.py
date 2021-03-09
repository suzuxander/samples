from troposphere import Template, Sub, Ref, GetAtt
from troposphere.s3 import Bucket

from sample000.common import add_export


def create_bucket_template() -> Template:
    template = Template()
    bucket = template.add_resource(
        resource=Bucket(
            title='SampleBucket',
            BucketName=Sub('sample-bucket-${AWS::AccountId}'),
        )
    )
    add_export(template, bucket.title + 'Name', Ref(bucket))
    add_export(template, bucket.title + 'Arn', GetAtt(bucket, 'Arn'))
    return template
