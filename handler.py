import json


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    nome = event['queryStringParameters']['name']

    response = {
        "statusCode": 200,
        "body": nome
    }

    return response

