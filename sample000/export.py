from enum import Enum


class ExportResourceEnum(Enum):
    BUCKET_NAME = 'sample-bucket-name'
    BUCKET_ARN = 'sample-bucket-arn'
    LAMBDA_SERVICE_ROLE_ARN = 'sample-lambda-service-role-arn'
    CODE_BUILD_SERVICE_ROLE_ARN = 'sample-code-build-service-role-arn'
    CODE_PIPELINE_SERVICE_ROLE_ARN = 'sample-code-pipeline-service-role-arn'
    CLOUD_FORMATION_SERVICE_ROLE_ARN = 'sample-cloud-formation-service-role-arn'
