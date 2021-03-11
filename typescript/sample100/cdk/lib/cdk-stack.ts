import * as cdk from '@aws-cdk/core';
import * as sam from '@aws-cdk/aws-sam';

export class CdkStack extends cdk.Stack {

  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const apiResourceId = 'Api';
    const restApi = new sam.CfnApi(this, apiResourceId, {
      stageName: 'sample',
      name: 'sample-api',
      definitionUri: '../openapi.yml',
    });

    const serviceRole = new cdk.CfnParameter(this, 'LambdaServiceRole');
    new sam.CfnFunction(this, 'GetFunction',
      {
        functionName: 'sample-api-get-function',
        codeUri: '../../dist/',
        handler: 'get.handler',
        runtime: 'nodejs10.x',
        role: serviceRole.valueAsString,  // deploy実行時に渡す
        timeout: 5,
        events: {
          ApiEvent: {
            type: 'Api',
            properties: {
              method: 'GET',
              path: '/item',
              restApiId: cdk.Fn.ref(restApi.logicalId)
            }
          }
        },
      }
    );

    new sam.CfnFunction(this, 'PostFunction',
      {
        functionName: 'sample-api-post-function',
        codeUri: '../../dist/',
        handler: 'post.handler',
        runtime: 'nodejs10.x',
        role: serviceRole.valueAsString,
        timeout: 5,
        events: {
          ApiEvent: {
            type: 'Api',
            properties: {
              method: 'POST',
              path: '/item',
              restApiId: cdk.Fn.ref(restApi.logicalId)
            }
          }
        }
      }
    );
  }
}
