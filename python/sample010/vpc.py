from troposphere import Parameter, Template, Ref
from troposphere.ec2 import VPC, Subnet, RouteTable, \
    SubnetRouteTableAssociation, InternetGateway, VPCGatewayAttachment, Route


def create_vpc_template():
    template = Template()

    vpc_cidr = template.add_parameter(
        parameter=Parameter(
            title='VpcCidr',
            Type='String',
            Default='192.168.0.0/16'
        )
    )

    subnet_cidr_a = template.add_parameter(
        parameter=Parameter(
            title='SubnetCidr1',
            Type='String',
            Default='192.168.1.0/24'
        )
    )

    subnet_cidr_b = template.add_parameter(
        parameter=Parameter(
            title='SubnetCidr2',
            Type='String',
            Default='192.168.2.0/24'
        )
    )

    vpc = template.add_resource(
        resource=VPC(
            title='SampleVpc',
            CidrBlock=Ref(vpc_cidr),
            EnableDnsHostnames=True
        )
    )

    igw = template.add_resource(
        resource=InternetGateway(
            title='SampleIgw'
        )
    )

    template.add_resource(
        resource=VPCGatewayAttachment(
            title='SampleAttachment',
            VpcId=Ref(vpc),
            InternetGatewayId=Ref(igw)
        )
    )

    subnet_a = template.add_resource(
        resource=Subnet(
            title='SampleSubnetA',
            AvailabilityZone='us-east-1a',
            CidrBlock=Ref(subnet_cidr_a),
            MapPublicIpOnLaunch=True,
            VpcId=Ref(vpc)
        )
    )

    subnet_b = template.add_resource(
        resource=Subnet(
            title='SampleSubnetB',
            AvailabilityZone='us-east-1b',
            CidrBlock=Ref(subnet_cidr_b),
            MapPublicIpOnLaunch=True,
            VpcId=Ref(vpc)
        )
    )

    route_table = template.add_resource(
        resource=RouteTable(
            title='SampleRoteTable',
            VpcId=Ref(vpc)
        )
    )

    template.add_resource(
        resource=SubnetRouteTableAssociation(
            title='SampleRoteTableAssociationA',
            RouteTableId=Ref(route_table),
            SubnetId=Ref(subnet_a)
        )
    )

    template.add_resource(
        resource=SubnetRouteTableAssociation(
            title='SampleRoteTableAssociationB',
            RouteTableId=Ref(route_table),
            SubnetId=Ref(subnet_b)
        )
    )

    template.add_resource(
        resource=Route(
            title='SampleRoute',
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=Ref(igw),
            RouteTableId=Ref(route_table)
        )
    )

    with open('./vpc.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_vpc_template()
