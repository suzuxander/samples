from troposphere import Parameter, Template, Ref, GetAtt, Sub
from troposphere.ec2 import VPC, InternetGateway, VPCGatewayAttachment, Route, Subnet, RouteTable, \
    SubnetRouteTableAssociation, NatGateway, EIP


def create_vpc_template() -> Template:
    template = Template()

    vpc_cidr = template.add_parameter(
        parameter=Parameter(
            title='VpcCidr',
            Type='String',
            Default='10.0.0.0/16'
        )
    )

    vpc = template.add_resource(
        resource=VPC(
            title='SampleVpc',
            CidrBlock=Ref(vpc_cidr)
        )
    )

    public_subnet = __create_public_subnet(template, vpc)
    __create_private_subnet(template, vpc)
    __create_dmz_subnet(template, vpc, public_subnet)

    return template


def __create_public_subnet(template: Template, vpc) -> Subnet:
    public_subnet_cidr = template.add_parameter(
        parameter=Parameter(
            title='PublicSubnetCidr',
            Type='String',
            Default='10.0.1.0/24'
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

    public_route_table = template.add_resource(
        resource=RouteTable(
            title='SamplePublicRoteTable',
            VpcId=Ref(vpc)
        )
    )

    for suffix in ['A', 'B']:
        public_subnet = template.add_resource(
            resource=Subnet(
                title='SamplePublicSubnet' + suffix,
                AvailabilityZone=Sub('${AWS::Region}' + suffix.lower()),
                CidrBlock=Ref(public_subnet_cidr),
                MapPublicIpOnLaunch=True,
                VpcId=Ref(vpc)
            )
        )

        template.add_resource(
            resource=SubnetRouteTableAssociation(
                title='SamplePublicRoteTableAssociation' + suffix,
                RouteTableId=Ref(public_route_table),
                SubnetId=Ref(public_subnet)
            )
        )

    template.add_resource(
        resource=Route(
            title='SamplePublicRoute',
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=Ref(igw),
            RouteTableId=Ref(public_route_table)
        )
    )

    return public_subnet


def __create_private_subnet(template: Template, vpc):
    private_subnet_cidr = template.add_parameter(
        parameter=Parameter(
            title='PrivateSubnetCidr',
            Type='String',
            Default='10.0.2.0/24'
        )
    )

    private_route_table = template.add_resource(
        resource=RouteTable(
            title='SamplePrivateRoteTable',
            VpcId=Ref(vpc)
        )
    )

    for suffix in ['A', 'B']:
        private_subnet = template.add_resource(
            resource=Subnet(
                title='SamplePrivateSubnet' + suffix,
                AvailabilityZone=Sub('${AWS::Region}' + suffix.lower()),
                CidrBlock=Ref(private_subnet_cidr),
                VpcId=Ref(vpc)
            )
        )

        template.add_resource(
            resource=SubnetRouteTableAssociation(
                title='SamplePrivateRoteTableAssociation' + suffix,
                RouteTableId=Ref(private_route_table),
                SubnetId=Ref(private_subnet)
            )
        )


def __create_dmz_subnet(template: Template, vpc, public_subnet):
    dmz_subnet_cidr = template.add_parameter(
        parameter=Parameter(
            title='DmzSubnetCidr',
            Type='String',
            Default='10.0.3.0/24'
        )
    )

    dmz_route_table = template.add_resource(
        resource=RouteTable(
            title='SampleDmzRoteTable',
            VpcId=Ref(vpc)
        )
    )

    dmz_subnet = template.add_resource(
        resource=Subnet(
            title='SampleDmzSubnet',
            CidrBlock=Ref(dmz_subnet_cidr),
            VpcId=Ref(vpc)
        )
    )

    template.add_resource(
        resource=SubnetRouteTableAssociation(
            title='SampleDmzRoteTableAssociation',
            RouteTableId=Ref(dmz_route_table),
            SubnetId=Ref(dmz_subnet)
        )
    )

    eip = template.add_resource(
        resource=EIP(
            title='SampleEip',
        )
    )

    ngw = template.add_resource(
        resource=NatGateway(
            title='SampleNatGateway',
            AllocationId=GetAtt(eip, "AllocationId"),
            SubnetId=Ref(public_subnet)
        )
    )

    template.add_resource(
        resource=Route(
            title='SampleDmzRoute',
            DestinationCidrBlock='0.0.0.0/0',
            NatGatewayId=Ref(ngw),
            RouteTableId=Ref(dmz_route_table)
        )
    )


if __name__ == '__main__':
    create_vpc_template()
