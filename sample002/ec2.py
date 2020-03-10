from troposphere import Template, Parameter, Ref
from troposphere.ec2 import Instance, SecurityGroup


def create_ec2_template():
    template = Template()

    vpc = template.add_parameter(
        parameter=Parameter(
            title='Vpc',
            Type='String'
        )
    )

    subnet = template.add_parameter(
        parameter=Parameter(
            title='Subnet',
            Type='String'
        )
    )

    ami_image = template.add_parameter(
        parameter=Parameter(
            title='AmiImage',
            Default='ami-0e2ff28bfb72a4e45',
            Type='String'
        )
    )

    key_name = template.add_parameter(
        parameter=Parameter(
            title='KeyName',
            Type='String'
        )
    )

    my_ip = template.add_parameter(
        parameter=Parameter(
            title='MyIp',
            Type='String'
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
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'CidrIp': Ref(my_ip),
                }
            ]
        )
    )

    template.add_resource(
        resource=Instance(
            title='SampleEc2Instance',
            SubnetId=Ref(subnet),
            SecurityGroupIds=[Ref(security_group)],
            InstanceType='t2.micro',
            ImageId=Ref(ami_image),
            KeyName=Ref(key_name),
        )
    )

    with open('./ec2.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_ec2_template()
