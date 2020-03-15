from enum import Enum

from troposphere import Template, Ref, Parameter, ImportValue, Sub, Output, Export
from troposphere.ec2 import SecurityGroup
from troposphere.ecs import Cluster, Service, NetworkConfiguration, AwsvpcConfiguration, \
    LoadBalancer as EcsLoadBalancer, \
    TaskDefinition, ContainerDefinition, LogConfiguration, PortMapping
from troposphere.elasticloadbalancingv2 import TargetGroup, LoadBalancer, Listener, Action
from troposphere.logs import LogGroup

from sample000.resource import CommonResource


class ExportName(Enum):
    ALB_SECURITY_GROUP = 'sample-fargate-alb-security-group'
    TASK_SECURITY_GROUP = 'sample-fargate-task-security-group'
    TARGET_GROUP = 'sample-fargate-alb-target-group'
    # ALB_SECURITY_GROUP = 'sample-fargate-alb-security-group'


def create_fargate_template():
    __create_security_group()

    __create_load_balancer()

    __create_ecs()


def __create_security_group():
    template = Template()

    alb_security_group = template.add_resource(
        resource=SecurityGroup(
            title='SampleAlbSecurityGroup',
            GroupDescription='sample-fargate',
            SecurityGroupIngress=[
                {
                    'IpProtocol': 'tcp',
                    'ToPort': 80,
                    'FromPort': 80,
                    'CidrIp': '0.0.0.0/0'
                }
            ],
            VpcId=ImportValue(CommonResource.ExportName.VPC_ID.value)
        )
    )
    template.add_output(
        output=Output(
            title=alb_security_group.title,
            Value=Ref(alb_security_group),
            Export=Export(name=ExportName.ALB_SECURITY_GROUP.value)
        )
    )

    task_security_group = template.add_resource(
        resource=SecurityGroup(
            title='SampleTaskSecurityGroup',
            GroupDescription='sample-fargate',
            SecurityGroupIngress=[
                # {
                #     'IpProtocol': 'tcp',
                #     'ToPort': 80,
                #     'FromPort': 80,
                #     'SourceSecurityGroupId': Ref(alb_security_group),
                # },
                {
                    'IpProtocol': 'tcp',
                    'ToPort': 80,
                    'FromPort': 80,
                    'CidrIp': '0.0.0.0/0'
                },
                # {
                #     'SourceSecurityGroupId': Ref(alb_security_group),
                #     'IpProtocol': -1,
                # }
            ],
            VpcId=ImportValue(CommonResource.ExportName.VPC_ID.value)
        )
    )
    template.add_output(
        output=Output(
            title=task_security_group.title,
            Value=Ref(task_security_group),
            Export=Export(name=ExportName.TASK_SECURITY_GROUP.value)
        )
    )

    with open('./sg.yml', mode='w') as file:
        file.write(template.to_yaml())

    return alb_security_group, task_security_group


def __create_load_balancer():
    template = Template()
    load_balancer = template.add_resource(
        resource=LoadBalancer(
            title='SampleFargateLoadBalancer',
            Name='sample-fargate-load-balancer',
            Subnets=[
                ImportValue(CommonResource.ExportName.PUBLIC_SUBNET_A_ID.value),
                ImportValue(CommonResource.ExportName.PUBLIC_SUBNET_B_ID.value)
            ],
            SecurityGroups=[
                ImportValue(ExportName.ALB_SECURITY_GROUP.value)
            ],
            Scheme='internet-facing'
        )
    )

    target_group = template.add_resource(
        resource=TargetGroup(
            title='SampleFargateTargetGroup',
            Port=80,
            Protocol='HTTP',
            TargetType='ip',
            VpcId=ImportValue(CommonResource.ExportName.VPC_ID.value)
        )
    )
    template.add_output(
        output=Output(
            title=target_group.title,
            Value=Ref(target_group),
            Export=Export(name=ExportName.TARGET_GROUP.value)
        )
    )

    template.add_resource(
        resource=Listener(
            title='SampleFargateListener',
            DefaultActions=[
                Action(
                    Type='forward',
                    TargetGroupArn=Ref(target_group)
                )
            ],
            LoadBalancerArn=Ref(load_balancer),
            Port=80,
            Protocol='HTTP'
        )
    )

    with open('./alb.yml', mode='w') as file:
        file.write(template.to_yaml())

    return target_group


def __create_ecs():
    template = Template()

    desired_count = template.add_parameter(
        parameter=Parameter(
            title='DesiredCount',
            Default=1,
            Type='Number'
        )
    )

    cpu = template.add_parameter(
        parameter=Parameter(
            title='Cpu',
            Default=256,
            Type='Number'
        )
    )

    memory = template.add_parameter(
        parameter=Parameter(
            title='Memory',
            Default=512,
            Type='Number'
        )
    )

    cluster = template.add_resource(
        resource=Cluster(
            title='SampleCluster',
        )
    )

    log_group = template.add_resource(
        resource=LogGroup(
            title='SampleLogGroup',
            LogGroupName='/aws/ecs/sample'
        )
    )

    container_name = 'sample-nginx'

    task_definition = template.add_resource(
        resource=TaskDefinition(
            title='SampleTaskDefinition',
            Cpu=Ref(cpu),
            Family='sample-fargate-task',
            RequiresCompatibilities=['FARGATE'],
            Memory=Ref(memory),
            NetworkMode='awsvpc',
            ExecutionRoleArn=Sub('arn:aws:iam::${AWS::AccountId}:role/ecsTaskExecutionRole'),
            ContainerDefinitions=[
                ContainerDefinition(
                    Image='nginx:latest',
                    Name=container_name,
                    PortMappings=[
                        PortMapping(
                            ContainerPort=80,
                            HostPort=80,
                            Protocol='tcp'
                        )
                    ],
                    LogConfiguration=LogConfiguration(
                        LogDriver='awslogs',
                        Options={
                            'awslogs-region': Ref('AWS::Region'),
                            'awslogs-group': Ref(log_group),
                            'awslogs-stream-prefix': 'nginx'
                        }
                    )
                )
            ]
        )
    )

    template.add_resource(
        resource=Service(
            title='SampleService',
            ServiceName='sample-fargate',
            Cluster=Ref(cluster),
            DesiredCount=Ref(desired_count),
            TaskDefinition=Ref(task_definition),
            LaunchType='FARGATE',
            NetworkConfiguration=NetworkConfiguration(
                AwsvpcConfiguration=AwsvpcConfiguration(
                    AssignPublicIp='ENABLED',
                    SecurityGroups=[
                        ImportValue(ExportName.TASK_SECURITY_GROUP.value)
                    ],
                    Subnets=[
                        ImportValue(CommonResource.ExportName.PUBLIC_SUBNET_A_ID.value),
                        ImportValue(CommonResource.ExportName.PUBLIC_SUBNET_B_ID.value),
                        # ImportValue(CommonResource.ExportName.PRIVATE_SUBNET_A_ID.value),
                        # ImportValue(CommonResource.ExportName.PRIVATE_SUBNET_B_ID.value),
                    ]
                )
            ),
            LoadBalancers=[
                EcsLoadBalancer(
                    ContainerName=container_name,
                    ContainerPort=80,
                    TargetGroupArn=ImportValue(ExportName.TARGET_GROUP.value)
                )
            ]
        )
    )

    with open('./ecs.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_fargate_template()
