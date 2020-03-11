from troposphere import GetAtt, Template
from troposphere.iam import Role, Policy

from sample000.common import add_export


def create_service_role() -> Template:
    template = Template()
    __create_lambda_function_service_role(template)
    __create_codebuild_service_role(template)
    __create_codepipeline_service_role(template)
    __create_cloudformation_service_role(template)
    return template


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

    add_export(template, role.title + 'Arn', GetAtt(role, 'Arn'))


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
    add_export(template, role.title + 'Arn', GetAtt(role, 'Arn'))


def __create_codepipeline_service_role(template):
    role = template.add_resource(
        resource=Role(
            title='SampleCodePipelineServiceRole',
            RoleName='sample-codepipeline-service-role',
            Path='/',
            AssumeRolePolicyDocument={
                'Statement': [{
                    'Effect': 'Allow',
                    'Principal': {
                        'Service': 'codepipeline.amazonaws.com'
                    },
                    'Action': ['sts:AssumeRole']
                }]
            },
            Policies=[
                Policy(
                    PolicyName='sample-codepipeline-policy',
                    PolicyDocument={
                        'Version': '2012-10-17',
                        'Statement': [
                            {
                                "Action": [
                                    'cloudformation:*',
                                    'codebuild:*',
                                    'iam:*',
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
    add_export(template, role.title + 'Arn', GetAtt(role, 'Arn'))


def __create_cloudformation_service_role(template):
    role = template.add_resource(
        resource=Role(
            title='SampleCloudFormationServiceRole',
            RoleName='sample-cloudformation-service-role',
            Path='/',
            AssumeRolePolicyDocument={
                'Statement': [{
                    'Effect': 'Allow',
                    'Principal': {
                        'Service': 'cloudformation.amazonaws.com'
                    },
                    'Action': ['sts:AssumeRole']
                }]
            },
            Policies=[
                Policy(
                    PolicyName='sample-cloudformation-policy',
                    PolicyDocument={
                        'Version': '2012-10-17',
                        'Statement': [
                            {
                                "Action": [
                                    'cloudformation:*',
                                    'iam:*',
                                    'lambda:*',
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
    add_export(template, role.title + 'Arn', GetAtt(role, 'Arn'))
