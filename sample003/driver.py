from troposphere import Parameter, Template, Ref
from troposphere.ec2 import Subnet, Instance, SecurityGroup


def create_template():
    template = Template()

    vpc = template.add_parameter(
        parameter=Parameter(
            title='Vpc',
            Type='String'
        )
    )

    key_name = template.add_parameter(
        parameter=Parameter(
            title='KeyName',
            Type='String'
        )
    )

    subnet_a = template.add_resource(
        resource=Subnet(
            title='SampleSubnetA',
            AvailabilityZone='us-east-1a',
            CidrBlock='192.168.10.0/24',
            MapPublicIpOnLaunch=True,
            VpcId=Ref(vpc)
        )
    )
    template.add_resource(
        resource=Subnet(
            title='SampleSubnetB',
            AvailabilityZone='us-east-1b',
            CidrBlock='192.168.11.0/24',
            MapPublicIpOnLaunch=True,
            VpcId=Ref(vpc)
        )
    )

    security_group = template.add_resource(
        resource=SecurityGroup(
            title='SampleSecurityGroup',
            GroupDescription='sample',
            VpcId=Ref(vpc),
            SecurityGroupIngress=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'CidrIp': '0.0.0.0/0',
                }
            ]
        )
    )

    template.add_resource(
        resource=Instance(
            title='SampleEc2Instance',
            SubnetId=Ref(subnet_a),
            SecurityGroupIds=[Ref(security_group)],
            InstanceType='t2.micro',
            ImageId='ami-0e2ff28bfb72a4e45',
            KeyName=Ref(key_name),
        )
    )

    with open('./driver.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_template()
