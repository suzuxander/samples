import sys

from troposphere import Template, Ref, Parameter, ImportValue
from troposphere.awslambda import Permission
from troposphere.serverless import Api, Function

URI = 'arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/arn:aws:lambda:{region}:' \
      '{account_id}:function:{function_name}/invocations '


def create_aurora_template(region, account_id):
    template = Template()
    template.set_transform('AWS::Serverless-2016-10-31')

    api_name = template.add_parameter(
        parameter=Parameter(
            title='ApiName',
            Default='sample-api',
            Type='String',
        )
    )

    function_name = template.add_parameter(
        parameter=Parameter(
            title='FunctionName',
            Default='sample-lambda-function',
            Type='String',
        )
    )

    # swagger_path = template.add_parameter(
    #     parameter=Parameter(
    #         title='SwaggerPath',
    #         Default='./swagger.yml',
    #         Type='String',
    #     )
    # )

    stage_name = template.add_parameter(
        parameter=Parameter(
            title='StageName',
            Default='prod',
            Type='String',
        )
    )

    api = template.add_resource(
        resource=Api(
            title='SampleApi',
            Name=Ref(api_name),
            # DefinitionUri=Ref(swagger_path),
            DefinitionUri='./swagger.yml',
            StageName=Ref(stage_name),
        )
    )

    path = '/sample/'
    method = 'get'
    function = template.add_resource(
        resource=Function(
            title='SampleLambdaFunction',
            AutoPublishAlias='sample',
            CodeUri='.',
            FunctionName=Ref(function_name),
            Handler='lambda_function.lambda_handler',
            Role=ImportValue('sample-lambda-service-role-arn'),
            Runtime='python3.7',
            Events={
                'ApiTrigger': {
                    'Type': 'Api',
                    'Properties': {
                        'Path': path,
                        'Method': method,
                        'RestApiId': Ref(api)
                    }
                }
            }
        )
    )

    template.add_resource(
        resource=Permission(
            title='SampleLambdaFunctionPermission',
            Action='lambda:InvokeFunction',
            FunctionName=Ref(function),
            Principal='apigateway.amazonaws.com'
        )
    )

    with open('swagger_template.yml') as f:
        swagger_yaml = f.read()

    uri = URI.replace('{region}', region).replace('{account_id}', account_id) \
        .replace('{function_name}', function_name.Default)  # TODO:
    swagger = swagger_yaml.replace('{path}', path).replace('{method}', method).replace('{uri}', uri)

    with open('./api.yml', mode='w') as file:
        file.write(template.to_yaml())

    with open('./swagger.yml', mode='w') as file:
        file.write(swagger)


if __name__ == '__main__':
    create_aurora_template(sys.argv[1], sys.argv[2])
