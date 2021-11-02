import json
from pymongo import MongoClient
import boto3
import bcrypt
from datetime import datetime, timedelta
import jwt


def get_secret():
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="ap-northeast-2"
    )
    get_secret_value_response = client.get_secret_value(
        SecretId='pymongo'
    )
    token = get_secret_value_response['SecretString']
    return eval(token)


def db_ops():
    secrets = get_secret()
    client = MongoClient("mongodb://{0}:{1}@{2}".format(secrets['user'], secrets['password'], secrets['host']))
    return client


def lambda_handler(event, context):
    type = event['queryStringParameters']['type']
    if type == 'article':
        if event['httpMethod'] == 'OPTIONS':
            body = json.dumps({
                "message": "success",
            })
        else:
            client = db_ops()
            db = client.bestmealever
            secret = "secrete"

            body = json.loads(event['body'])
            title = body['title']
            content = body['content']

            post = {
                'idx': max_value,
                'title': title,
                'content': content,
                'reg_date': datetime.now()
            }
            db.article.insert_one(post)

            return {
                "statusCode": 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                "body": json.dumps({
                    "result": "success",
                }),
            }