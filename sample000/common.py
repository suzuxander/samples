import re

from troposphere import Output, Export


def add_export(template, title, value):
    export_name = __camel_to_kebab(title)
    template.add_output(
        output=Output(
            title=title,
            Export=Export(export_name),
            Value=value
        )
    )


def __camel_to_kebab(target: str) -> str:
    result = re.sub('([A-Z])', lambda x: '-' + x.group(1).lower(), target)
    if result[0] == '-':
        result = result[1:]
    return result


def camel_to_snake(target: str) -> str:
    result = re.sub('([A-Z])', lambda x: '_' + x.group(1).lower(), target)
    if result[0] == '_':
        result = result[1:]
    return result