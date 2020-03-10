from troposphere import Template, Ref, ImportValue, Parameter
from troposphere.codebuild import Project, Artifacts, Source, Environment, EnvironmentVariable, ProjectTriggers, \
    SourceAuth, WebhookFilter

from sample000.export import ExportResourceEnum


def create_build():
    template = Template()

    build_spec = template.add_parameter(
        parameter=Parameter(
            title='BuildSpecPath',
            Default='buildspec.yml',
            Type='String'
        )
    )

    github_url = template.add_parameter(
        parameter=Parameter(
            title='GitHubUrl',
            Type='String'
        )
    )

    template.add_resource(
        resource=Project(
            title='SampleBuildProject',
            Name='sample-codepipeline-project',
            Artifacts=Artifacts(
                Type='NO_ARTIFACTS',
            ),
            Source=Source(
                Auth=SourceAuth(
                    Type='OAUTH'
                ),
                BuildSpec=Ref(build_spec),
                Location=Ref(github_url),
                ReportBuildStatus=True,
                Type='GITHUB',
            ),
            Environment=Environment(
                ComputeType='BUILD_GENERAL1_SMALL',
                Image='aws/codebuild/amazonlinux2-x86_64-standard:1.0',
                Type='LINUX_CONTAINER',
            ),
            Triggers=ProjectTriggers(
                Webhook=True,
                FilterGroups=[
                    [
                        WebhookFilter(
                            Pattern='PULL_REQUEST_CREATED, PULL_REQUEST_UPDATED',
                            Type='EVENT'
                        )
                    ]
                ]
            ),
            ServiceRole=ImportValue(ExportResourceEnum.CODE_BUILD_SERVICE_ROLE_ARN.value)
        )
    )

    with open('./build.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_build()
