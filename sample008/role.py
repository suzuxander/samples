from enum import Enum

from troposphere import Template, Output, Export, GetAtt
from troposphere.iam import Role, Policy


class ServiceRoleExportName(Enum):
    CODEBUILD = 'sample-codebuild-service-role-arn'
    CODEPIPELINE = 'sample-codepipeline-service-role-arn'
    CLOUDFORMATION = 'sample-cloudformation-service-role-arn'


def create_service_role_template():
    template = Template()

    service_role = template.add_resource(
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
            title=service_role.title,
            Export=Export(name=ServiceRoleExportName.CODEBUILD.value),
            Value=GetAtt(service_role, 'Arn')
        )
    )

    service_role = template.add_resource(
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
    template.add_output(
        output=Output(
            title=service_role.title,
            Export=Export(name=ServiceRoleExportName.CODEPIPELINE.value),
            Value=GetAtt(service_role, 'Arn')
        )
    )

    service_role = template.add_resource(
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
    template.add_output(
        output=Output(
            title=service_role.title,
            Export=Export(name=ServiceRoleExportName.CLOUDFORMATION.value),
            Value=GetAtt(service_role, 'Arn')
        )
    )

    with open('./role.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_service_role_template()
