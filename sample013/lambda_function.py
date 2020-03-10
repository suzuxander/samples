import json


def lambda_handler(event, context):
    print(json.dumps(event))
    return {
        'statusCode': 200,
        'isBase64Encoded': True,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'message': 'OK'})
    }
