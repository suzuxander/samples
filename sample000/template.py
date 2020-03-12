from troposphere import Template, GetAtt
from troposphere.cloudformation import Stack

from sample000.bucket import create_bucket_template
from sample000.common import camel_to_snake
from sample000.role import create_service_role
from sample000.securitygroup import create_security_group_template
from sample000.vpc import create_vpc_template


def __create_common_resource() -> dict:
    export_dict = {}
    template = Template()

    bucket_template = create_bucket_template()
    template.add_resource(
        __create_stack('Bucket', bucket_template, export_dict)
    )

    role_template = create_service_role()
    template.add_resource(
        __create_stack('Role', role_template, export_dict)
    )

    vpc_template = create_vpc_template()
    vpc_stack = template.add_resource(
        __create_stack('Vpc', vpc_template, export_dict)
    )

    # security_group_template = create_security_group_template()
    # template.add_resource(
    #     __create_stack(
    #         'SecurityGroup', security_group_template, export_dict,
    #         {
    #             'VpcId': GetAtt(vpc_stack, 'Outputs.' + OutputIdEnum.VPC_ID.value)
    #         }
    #     )
    # )

    __output_template(template, './template/template.yml')
    return export_dict


def __create_stack(title: str, template: Template, export_dict: dict, parameters: dict = None) -> Stack:
    __add_export_dict(export_dict, template)

    template_path = './' + title.lower() + '.yml'
    stack = Stack(
        title=title,
        TemplateURL=template_path
    )
    if parameters:
        stack.Parameters = parameters

    __output_template(template, 'template/' + template_path)
    return stack


def __add_export_dict(export_dict: dict, template: Template) -> None:
    for key, value in template.outputs.items():
        export_dict[key] = value.properties['Export'].data['Name']


def __output_template(template: Template, template_path: str) -> None:
    with open('./' + template_path, mode='w') as file:
        file.write(template.to_yaml())


def __import_export_resource_enum(export_dict: dict):
    text = 'from enum import Enum\n\n\n'
    text = text + 'class CommonResource():\n'

    text = text + '    class OutputName(Enum):\n'
    for key, _ in export_dict.items():
        text = text + "        {} = '{}'\n".format(camel_to_snake(key.replace('Sample', '')).upper(), key)

    text = text + '\n'

    text = text + '    class ExportName(Enum):\n'
    for key, value in export_dict.items():
        text = text + "        {} = '{}'\n".format(camel_to_snake(key.replace('Sample', '')).upper(), value)

    with open('./export.py', mode='w') as file:
        file.write(text)


if __name__ == '__main__':
    export_dict = __create_common_resource()
    __import_export_resource_enum(export_dict)
