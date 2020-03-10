from troposphere import Parameter, Template, Ref, Sub, ImportValue
from troposphere.codebuild import Project, Artifacts, Source, Environment, EnvironmentVariable
from troposphere.codepipeline import Pipeline, ArtifactStore, Stages, Actions, ActionTypeId, OutputArtifacts, \
    InputArtifacts
from troposphere.s3 import Bucket

from sample008.role import ServiceRoleExportName


def create_pipeline_template():
    template = Template()

    artifact_bucket = template.add_resource(
        resource=Bucket(
            title='SampleArtifactBucket',
            BucketName=Sub('sample-codepipeline-artifact-bucket-${AWS::AccountId}')
        )
    )

    build_project = __create_build_project(template, artifact_bucket)

    __create_pipeline(template, artifact_bucket, build_project)

    with open('./pipeline.yml', mode='w') as file:
        file.write(template.to_yaml())


def __create_build_project(template: Template, artifact_bucket: Bucket) -> Project:
    build_spec = template.add_parameter(
        parameter=Parameter(
            title='BuildSpecPath',
            Default='buildspec.yml',
            Type='String'
        )
    )

    build_project = template.add_resource(
        resource=Project(
            title='SampleBuildProject',
            Name='sample-codepipeline-project',
            Artifacts=Artifacts(
                Name='sample',
                Type='S3',
                Location=Ref(artifact_bucket)
            ),
            Source=Source(
                BuildSpec=Ref(build_spec),
                Type='S3',
                Location=Sub('${' + artifact_bucket.title + '}/sample.zip')
            ),
            Environment=Environment(
                ComputeType='BUILD_GENERAL1_SMALL',
                Image='aws/codebuild/amazonlinux2-x86_64-standard:1.0',
                Type='LINUX_CONTAINER',
                EnvironmentVariables=[
                    EnvironmentVariable(
                        Name='S3_BUCKET', Value=Ref(artifact_bucket)
                    )
                ]
            ),
            ServiceRole=ImportValue(ServiceRoleExportName.CODEBUILD.value)
        )
    )
    return build_project


def __create_pipeline(template: Template, artifact_bucket: Bucket, build_project: Project):
    github_owner = template.add_parameter(
        parameter=Parameter(
            title='GitHubOwner',
            Type='String'
        )
    )
    github_repo = template.add_parameter(
        parameter=Parameter(
            title='GitHubRepo',
            Type='String'
        )
    )
    github_branch = template.add_parameter(
        parameter=Parameter(
            title='GitHubBranch',
            Type='String',
            Default='master'
        )
    )
    github_token = template.add_parameter(
        parameter=Parameter(
            title='GitHubToken',
            Type='String'
        )
    )

    source_artifact = 'MyApp'
    build_artifact = 'MyBuild'
    stack_name = 'pipeline-sample-function'
    change_set_name = 'pipeline-sample-function-change-set'

    template.add_resource(
        resource=Pipeline(
            title='SamplePipeline',
            ArtifactStore=ArtifactStore(
                Type='S3',
                Location=Ref(artifact_bucket),
            ),
            RoleArn=ImportValue(ServiceRoleExportName.CODEPIPELINE.value),
            Stages=[
                Stages(
                    Name="Source",
                    Actions=[
                        Actions(
                            Name="App",
                            ActionTypeId=ActionTypeId(
                                Category="Source",
                                Owner="ThirdParty",
                                Provider="GitHub",
                                Version="1"
                            ),
                            Configuration={
                                "Owner": Ref(github_owner),
                                "Repo": Ref(github_repo),
                                "Branch": Ref(github_branch),
                                "OAuthToken": Ref(github_token),
                            },
                            OutputArtifacts=[
                                OutputArtifacts(Name=source_artifact)
                            ]
                        )
                    ]
                ),
                Stages(
                    Name="Build",
                    Actions=[
                        Actions(
                            Name="Build",
                            ActionTypeId=ActionTypeId(
                                Category="Build",
                                Owner="AWS",
                                Provider="CodeBuild",
                                Version="1"
                            ),
                            Configuration={
                                'ProjectName': Ref(build_project)
                            },
                            InputArtifacts=[
                                InputArtifacts(Name=source_artifact)
                            ],
                            OutputArtifacts=[
                                OutputArtifacts(Name=build_artifact)
                            ],
                            RunOrder=1
                        )
                    ]
                ),
                Stages(
                    Name='Deploy',
                    Actions=[
                        Actions(
                            Name="ChangeSetReplace",
                            ActionTypeId=ActionTypeId(
                                Category="Deploy",
                                Owner="AWS",
                                Provider="CloudFormation",
                                Version="1"
                            ),
                            Configuration={
                                "ActionMode": "CHANGE_SET_REPLACE",
                                "Capabilities": "CAPABILITY_NAMED_IAM,CAPABILITY_AUTO_EXPAND",
                                "ChangeSetName": change_set_name,
                                "StackName": stack_name,
                                "RoleArn": ImportValue(ServiceRoleExportName.CLOUDFORMATION.value),
                                "TemplatePath": build_artifact + '::function.yml'
                            },
                            InputArtifacts=[
                                InputArtifacts(Name=build_artifact)
                            ],
                            RunOrder=1
                        ),
                        Actions(
                            Name="ChangeSetExecute",
                            ActionTypeId=ActionTypeId(
                                Category="Deploy",
                                Owner="AWS",
                                Provider="CloudFormation",
                                Version="1"
                            ),
                            Configuration={
                                "ActionMode": "CHANGE_SET_EXECUTE",
                                "ChangeSetName": change_set_name,
                                "StackName": stack_name,
                            },
                            RunOrder=2
                        )
                    ]
                )
            ],
        )
    )


if __name__ == '__main__':
    create_pipeline_template()
