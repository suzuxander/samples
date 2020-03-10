from troposphere import Template, Parameter, Sub, GetAtt, Join, Ref
from troposphere.cloudfront import Distribution, \
    DistributionConfig, Origin, S3OriginConfig, DefaultCacheBehavior, ForwardedValues, LambdaFunctionAssociation
from troposphere.iam import Role, Policy
from troposphere.serverless import Function


def create_cloud_front_template():
    template = Template()
    template.set_transform('AWS::Serverless-2016-10-31')

    bucket = template.add_parameter(
        parameter=Parameter(
            title='Bucket',
            Type='String'
        )
    )

    identity = template.add_parameter(
        parameter=Parameter(
            title='OriginAccessIdentity',
            Type='String'
        )
    )

    service_role = template.add_resource(
        resource=Role(
            title='SampleLambdaServiceRole',
            RoleName='sample-lambda-edge-service-role',
            Path='/',
            AssumeRolePolicyDocument={
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {
                        "Service": ['lambda.amazonaws.com', 'edgelambda.amazonaws.com']
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

    lambda_function = template.add_resource(
        resource=Function(
            title='SampleLambdaFunction',
            AutoPublishAlias='sample',
            CodeUri='.',
            FunctionName='sample-lambda-edge-function-1',
            Handler='lambda_function.lambda_handler',
            Role=GetAtt(logicalName=service_role, attrName='Arn'),
            Runtime='python3.7',
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
                            LambdaFunctionARN=Join(delimiter=':', values=[
                                GetAtt(logicalName=lambda_function, attrName='Arn'),
                                '1'
                            ]),
                            # LambdaFunctionARN=Sub('${' + lambda_function_arn.title + '}:1')
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
