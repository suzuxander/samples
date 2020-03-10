import re
from enum import Enum

from troposphere import Template, Output, Export, GetAtt, Sub, Ref
from troposphere.iam import Policy, Role
from troposphere.s3 import Bucket

EXPORT_RESOURCE_LIST = []


def __create_common_resource():
    template = Template()

    __create_bucket(template)
    __create_lambda_function_service_role(template)
    __create_codebuild_service_role(template)

    with open('./common.yml', mode='w') as file:
        file.write(template.to_yaml())


def __add_export(template, title, value):
    # title = bucket.title + 'Name'
    export_name = __camel_to_kebab(title)
    template.add_output(
        output=Output(
            title=title,
            Export=Export(export_name),
            Value=value
        )
    )
    EXPORT_RESOURCE_LIST.append(export_name)


def __create_bucket(template):
    bucket = template.add_resource(
        resource=Bucket(
            title='SampleBucket',
            BucketName=Sub('sample-bucket-${AWS::AccountId}'),
        )
    )
    __add_export(template, bucket.title + 'Name', Ref(bucket))
    __add_export(template, bucket.title + 'Arn', GetAtt(bucket, 'Arn'))


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

    __add_export(template, role.title + 'Arn', GetAtt(role, 'Arn'))


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
    __add_export(template, role.title + 'Arn', GetAtt(role, 'Arn'))


def __camel_to_kebab(target: str) -> str:
    result = re.sub('([A-Z])', lambda x: '-' + x.group(1).lower(), target)
    if result[0] == '-':
        result = result[1:]
    return result


# def __kebab_to_upper_camel(target: str) -> str:
#     result = re.sub('-(.)', lambda x: x.group(1).upper(), target)
#     return result[0].upper() + result[1:]


def __import_export_resource_enum():
    text = 'from enum import Enum\n\n\n'
    text = text + 'class ExportResourceEnum(Enum):\n'
    for name in EXPORT_RESOURCE_LIST:
        text = text + "    {} = '{}'\n".format(name.replace('sample-', '').replace('-', '_').upper(), name)

    with open('./export.py', mode='w') as file:
        file.write(text)


if __name__ == '__main__':
    __create_common_resource()
    __import_export_resource_enum()
