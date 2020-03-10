from troposphere import Template, Parameter, Ref
from troposphere.ec2 import Instance, SecurityGroup
from troposphere.elasticloadbalancingv2 import LoadBalancer, TargetGroup, TargetDescription, Listener, Action


def create_alb_template():
    template = Template()

    vpc = template.add_parameter(
        parameter=Parameter(
            title='Vpc',
            Type='String'
        )
    )
    subnet_a = template.add_parameter(
        parameter=Parameter(
            title='SubnetA',
            Type='String'
        )
    )
    subnet_b = template.add_parameter(
        parameter=Parameter(
            title='SubnetB',
            Type='String'
        )
    )
    ec2_instance = template.add_parameter(
        parameter=Parameter(
            title='Ec2Instance',
            Type='String'
        )
    )

    security_group = template.add_resource(
        resource=SecurityGroup(
            title='SampleSecurityGroup',
            GroupDescription='sample-security-group',
            SecurityGroupIngress=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'CidrIp': '0.0.0.0/0'
                }
            ],
            VpcId=Ref(vpc)
        )
    )

    load_balancer = template.add_resource(
        resource=LoadBalancer(
            title='SampleLoadBalancer',
            Name='sample-alb',
            Subnets=[Ref(subnet_a), Ref(subnet_b)],
            SecurityGroups=[Ref(security_group)],
        )
    )

    target_group = template.add_resource(
        resource=TargetGroup(
            title='SampleTargetGroup',
            Targets=[
                TargetDescription(
                    Id=Ref(ec2_instance),
                    Port=80,
                )
            ],
            VpcId=Ref(vpc),
            Name='sample-target-group',
            Port=80,
            Protocol='HTTP',
        )
    )

    template.add_resource(
        resource=Listener(
            title='SampleListener',
            DefaultActions=[
                Action(
                    TargetGroupArn=Ref(target_group),
                    Type='forward'
                )
            ],
            LoadBalancerArn=Ref(load_balancer),
            Port=80,
            Protocol='HTTP',
        )
    )

    with open('./alb.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_alb_template()
