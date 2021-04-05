import * as aws from 'aws-sdk';

/**
 *
 * @param region      スタックが存在するリージョン
 * @param stackName   スタック名
 * @param resourceId  リソース名
 */
const main = async (region: string, stackName: string, resourceId: string): Promise<any> => {
  const cfn = new aws.CloudFormation({ region });
  const data = await cfn.listStackResources({ StackName: stackName }).promise();

  if (!data.StackResourceSummaries) return null;

  for (const resource of data.StackResourceSummaries) {
    if (resource.PhysicalResourceId &&
      resource.PhysicalResourceId.includes(resourceId) &&
      resource.ResourceType === 'AWS::Lambda::Version') {
      console.log(resource)
      console.log(resource.PhysicalResourceId)
      console.log(resource.ResourceType)
      const ary = resource.PhysicalResourceId.split(':');

      return ary.pop();
    }
  }
};

const region = 'us-east-1';
const stackName = 'study-lambda-edge';
const resourceId = 'study-web-viewer-request';

main(region, stackName, resourceId)
  .then(res => console.log('Version:', res))
  .catch(err => console.error(err));