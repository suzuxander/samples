from troposphere import Template, Ref, Parameter, GetAtt
from troposphere.ec2 import SecurityGroup
from troposphere.rds import DBSubnetGroup, DBInstance, DBCluster, DBClusterParameterGroup


def create_aurora_template():
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

    instance_class = template.add_parameter(
        parameter=Parameter(
            title='InstanceClass',
            Default='db.t2.small',
            Type='String'
        )
    )

    engine_version = template.add_parameter(
        parameter=Parameter(
            title='EngineVersion',
            Default='5.7.12',
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
            DBSubnetGroupDescription='sample-aurora',
            DBSubnetGroupName='sample-aurora',
            SubnetIds=[Ref(subnet_a), Ref(subnet_b)]
        )
    )

    db_cluster_parameter_group = template.add_resource(
        DBClusterParameterGroup(
            title='SampleDBClusterParameterGroup',
            Description='sample-aurora',
            Family='aurora-mysql5.7',
            Parameters={'time_zone': 'Asia/Tokyo'}
        )
    )

    cluster = template.add_resource(
        resource=DBCluster(
            title='SampleDBCluster',
            DatabaseName='sample_aurora',
            DBClusterIdentifier='sample-aurora',
            DBClusterParameterGroupName=Ref(db_cluster_parameter_group),
            DBSubnetGroupName=Ref(db_subnet_group),
            Engine='aurora-mysql',
            EngineVersion=Ref(engine_version),
            MasterUsername=Ref(master_user_name),
            MasterUserPassword=Ref(master_user_password),
            VpcSecurityGroupIds=[GetAtt(security_group, 'GroupId')],
        )
    )

    for suffix in ['A', 'B']:
        template.add_resource(
            resource=DBInstance(
                title='SampleDBInstance' + suffix,
                DBClusterIdentifier=Ref(cluster),
                DBInstanceClass=Ref(instance_class),
                Engine='aurora-mysql',
            )
        )

    with open('./aurora.yml', mode='w') as file:
        file.write(template.to_yaml())


if __name__ == '__main__':
    create_aurora_template()
