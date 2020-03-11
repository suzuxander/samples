from troposphere import Template, GetAtt, ImportValue
from troposphere.iam import Role, Policy
from troposphere.serverless import Function

from sample000.export import ExportResourceEnum


def create_function_template():
    template = Template()
    template.set_transform('AWS::Serverless-2016-10-31')

    template.add_resource(
        resource=Function(
            title='SampleLambdaFunction',
            CodeUri='.',
            FunctionName='sample-lambda-function',
            Handler='lambda_function.lambda_handler',
            # Role=GetAtt(logicalName=service_role, attrName='Arn'),
            Role=ImportValue(ExportResourceEnum.LAMBDA_SERVICE_ROLE_ARN.value),
            Runtime='python3.7',
        )
    )

    with open('./function.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_function_template()
