from enum import Enum


class CommonResource(object):

    class OutputName(Enum):
        BUCKET_NAME = 'SampleBucketName'
        BUCKET_ARN = 'SampleBucketArn'
        CLOUD_FORMATION_SERVICE_ROLE_ARN = 'SampleCloudFormationServiceRoleArn'
        CODE_BUILD_SERVICE_ROLE_ARN = 'SampleCodeBuildServiceRoleArn'
        CODE_PIPELINE_SERVICE_ROLE_ARN = 'SampleCodePipelineServiceRoleArn'
        LAMBDA_SERVICE_ROLE_ARN = 'SampleLambdaServiceRoleArn'
        LAMBDA_EDGE_SERVICE_ROLE_ARN = 'SampleLambdaEdgeServiceRoleArn'
        VPC_ID = 'SampleVpcId'
        PUBLIC_SUBNET_A_ID = 'SamplePublicSubnetAId'
        PUBLIC_SUBNET_B_ID = 'SamplePublicSubnetBId'
        PRIVATE_SUBNET_A_ID = 'SamplePrivateSubnetAId'
        PRIVATE_SUBNET_B_ID = 'SamplePrivateSubnetBId'

    class ExportName(Enum):
        BUCKET_NAME = 'sample-bucket-name'
        BUCKET_ARN = 'sample-bucket-arn'
        CLOUD_FORMATION_SERVICE_ROLE_ARN = 'sample-cloud-formation-service-role-arn'
        CODE_BUILD_SERVICE_ROLE_ARN = 'sample-code-build-service-role-arn'
        CODE_PIPELINE_SERVICE_ROLE_ARN = 'sample-code-pipeline-service-role-arn'
        LAMBDA_SERVICE_ROLE_ARN = 'sample-lambda-service-role-arn'
        LAMBDA_EDGE_SERVICE_ROLE_ARN = 'sample-lambda-edge-service-role-arn'
        VPC_ID = 'sample-vpc-id'
        PUBLIC_SUBNET_A_ID = 'sample-public-subnet-a-id'
        PUBLIC_SUBNET_B_ID = 'sample-public-subnet-b-id'
        PRIVATE_SUBNET_A_ID = 'sample-private-subnet-a-id'
        PRIVATE_SUBNET_B_ID = 'sample-private-subnet-b-id'
