import re

from troposphere import Template, Output, Export, GetAtt, Sub
from troposphere.iam import Policy, Role
from troposphere.s3 import Bucket


def create_common_resource():
    template = Template()

    __create_bucket(template)
    __create_lambda_function_service_role(template)
    __create_codebuild_service_role(template)

    with open('./common.yml', mode='w') as file:
        file.write(template.to_yaml())


def __create_bucket(template):
    bucket = template.add_resource(
        resource=Bucket(
            title='SampleBucket',
            BucketName=Sub('sample-bucket-${AWS::AccountId}'),
        )
    )
    template.add_output(
        output=Output(
            title=bucket.title,
            Export=Export(name=__camel_to_kebab(bucket.title + 'Arn')),
            Value=GetAtt(bucket, 'Arn')
        )
    )


def __create_lambda_function_service_role(template):
    role = template.add_resource(
        resource=Role(
            title='SampleLambdaServiceRole',
            RoleName='sample-lambda-service-role',
            Path='/',
            AssumeRolePolicyDocument={
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {
                        "Service": ['lambda.amazonaws.com']
                    },
                    "Action": ["sts:AssumeRole"]
                }]
            },
            Policies=[
                Policy(
                    PolicyName="sample-policy",
                    PolicyDocument={
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Action": 'lambda:*',
                                "Resource": '*',
                                "Effect": "Allow"
                            }
                        ]
                    }
                )
            ]
        )
    )

    template.add_output(
        output=Output(
            title=role.title,
            Export=Export(name=__camel_to_kebab(role.title + 'Arn')),
            Value=GetAtt(role, 'Arn')
        )
    )


def __create_codebuild_service_role(template):
    role = template.add_resource(
        resource=Role(
            title='SampleCodeBuildServiceRole',
            RoleName='sample-codebuild-service-role',
            Path='/',
            AssumeRolePolicyDocument={
                'Statement': [{
                    'Effect': 'Allow',
                    'Principal': {
                        'Service': 'codebuild.amazonaws.com'
                    },
                    'Action': ['sts:AssumeRole']
                }]
            },
            Policies=[
                Policy(
                    PolicyName='sample-codebuild-policy',
                    PolicyDocument={
                        'Version': '2012-10-17',
                        'Statement': [
                            {
                                "Action": [
                                    'logs:*',
                                    's3:*',
                                ],
                                "Resource": [
                                    '*'
                                ],
                                "Effect": "Allow"
                            }
                        ]
                    }
                )
            ]
        )
    )

    template.add_output(
        output=Output(
            title=role.title,
            Export=Export(name=__camel_to_kebab(role.title + 'Arn')),
            Value=GetAtt(role, 'Arn')
        )
    )


def __camel_to_kebab(target: str) -> str:
    result = re.sub("([A-Z])", lambda x: "-" + x.group(1).lower(), target)
    if result[0] == '-':
        result = result[1:]
    return result


if __name__ == '__main__':
    create_common_resource()
