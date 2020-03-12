from troposphere import Template, ImportValue, Output, GetAtt, Export
from troposphere.serverless import Function

from sample000.resource import CommonResource


def create_function_template():
    template = Template()
    template.set_transform('AWS::Serverless-2016-10-31')

    bucket = template.add_resource(
        resource=Function(
            title='SampleLambdaFunction',
            AutoPublishAlias='sample',
            CodeUri='.',
            FunctionName='sample-lambda-edge-function',
            Handler='lambda_function.lambda_handler',
            Role=ImportValue(CommonResource.ExportName.LAMBDA_EDGE_SERVICE_ROLE_ARN.value),
            Runtime='python3.7',
        )
    )

    template.add_output(
        output=Output(
            title=bucket.title,
            Value=GetAtt(bucket, 'Arn'),
            Export=Export(name=get_export_name())
        )
    )

    with open('./function.yml', mode='w') as file:
        file.write(template.to_yaml())


def get_export_name() -> str:
    return 'sample-lambda-edge-function-arn'


if __name__ == '__main__':
    create_function_template()
