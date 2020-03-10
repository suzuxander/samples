import json


def lambda_handler(event, context):
    print(json.dumps(event))
    request = event['Records'][0]['cf']['request']
    print(json.dumps(request))
    return request
