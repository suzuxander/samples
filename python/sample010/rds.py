from troposphere import Template, Ref, Parameter, GetAtt
from troposphere.ec2 import SecurityGroup
from troposphere.rds import DBSubnetGroup, DBInstance


def create_rds_template():
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

    master_user_name = template.add_parameter(
        parameter=Parameter(
            title='DBMasterUserName',
            Type='String'
        )
    )

    master_user_password = template.add_parameter(
        parameter=Parameter(
            title='DBMasterUserPassword',
            Type='String'
        )
    )

    storage_size = template.add_parameter(
        parameter=Parameter(
            title='StorageSize',
            Default='20',
            Type='String'
        )
    )

    instance_class = template.add_parameter(
        parameter=Parameter(
            title='InstanceClass',
            Default='db.t2.micro',
            Type='String'
        )
    )

    engine_version = template.add_parameter(
        parameter=Parameter(
            title='EngineVersion',
            Default='5.7.26',
            Type='String'
        )
    )

    security_group = template.add_resource(
        resource=SecurityGroup(
            title='SampleSecurityGroup',
            GroupDescription='sample-rds',
            SecurityGroupIngress=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 3306,
                    'ToPort': 3306,
                    'CidrIp': '0.0.0.0/0',
                }
            ],
            VpcId=Ref(vpc)
        )
    )

    db_subnet_group = template.add_resource(
        resource=DBSubnetGroup(
            title='SampleDBSubnetGroup',
            DBSubnetGroupDescription='sample-rds',
            DBSubnetGroupName='sample-rds',
            SubnetIds=[Ref(subnet_a), Ref(subnet_b)]
        )
    )

    template.add_resource(
        resource=DBInstance(
            title='SampleDBInstance',
            DBSubnetGroupName=Ref(db_subnet_group),
            # VPCSecurityGroups=[Ref(security_group)],
            VPCSecurityGroups=[GetAtt(security_group, 'GroupId')],
            AllocatedStorage=Ref(storage_size),
            DBInstanceClass=Ref(instance_class),
            DBInstanceIdentifier='sample-rds',
            DBName='sample_rds',
            Engine='mysql',
            EngineVersion=Ref(engine_version),
            MasterUsername=Ref(master_user_name),
            MasterUserPassword=Ref(master_user_password),
            PubliclyAccessible=True
        )
    )

    with open('./rds.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_rds_template()
