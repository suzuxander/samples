from troposphere import Parameter, Template, Ref
from troposphere.ec2 import VPC, InternetGateway, VPCGatewayAttachment, Route, Subnet, RouteTable, \
    SubnetRouteTableAssociation


def create_vpc_template():
    template = Template()

    vpc_cidr = template.add_parameter(
        parameter=Parameter(
            title='VpcCidr',
            Type='String',
            Default='192.168.0.0/16'
        )
    )

    subnet_cidr = template.add_parameter(
        parameter=Parameter(
            title='SubnetCidr',
            Type='String',
            Default='192.168.1.0/24'
        )
    )

    vpc = template.add_resource(
        resource=VPC(
            title='SampleVpc',
            CidrBlock=Ref(vpc_cidr)
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

    subnet = template.add_resource(
        resource=Subnet(
            title='SampleSubnet',
            CidrBlock=Ref(subnet_cidr),
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
            title='SampleRoteTableAssociation',
            RouteTableId=Ref(route_table),
            SubnetId=Ref(subnet)
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
