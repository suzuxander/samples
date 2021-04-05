from troposphere import Template, Parameter, Sub, GetAtt, Join, Ref
from troposphere.cloudfront import Distribution, \
    DistributionConfig, Origin, S3OriginConfig, DefaultCacheBehavior, ForwardedValues, LambdaFunctionAssociation
from troposphere.iam import Role, Policy
from troposphere.serverless import Function


def create_cloud_front_template():
    template = Template()
    template.set_transform('AWS::Serverless-2016-10-31')

    service_role = template.add_resource(
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

    template.add_resource(
        resource=Function(
            title='SampleLambdaFunction',
            AutoPublishAlias='sample',
            CodeUri='.',
            FunctionName='sample-lambda-function',
            Handler='lambda_function.lambda_handler',
            Role=GetAtt(logicalName=service_role, attrName='Arn'),
            Runtime='python3.7',
        )
    )

    with open('./function.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_cloud_front_template()
