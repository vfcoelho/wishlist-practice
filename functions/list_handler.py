import json

import psycopg2

from utils.db_credentials import DBCredentials

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

def list_list(event,context):
    log.info(json.dumps(event))
    user_id = event['pathParameters']['user_id']
    is_host = event['queryStringParameters']['is_host']

    credentials = DBCredentials()

    conn = psycopg2.connect(**credentials.credentials)
    cur = conn.cursor()

    if is_host:
        cur.execute("select id,list_name from list where user_id = %s",(user_id,))
    else:
        cur.execute("insert into list (list_name,user_id) values (%s,%s)",(list_name,user_id,))

    cur.close()
    conn.commit()
    conn.close()

    response = {
        "statusCode": 200
    }
    return response

def put_list(event,context):
    log.info(json.dumps(event))
    user_id = event['pathParameters']['user_id']
    list_id = event['pathParameters'].get('id')
    body = json.loads(event['body'])
    list_name = body['list_name']

    credentials = DBCredentials()

    conn = psycopg2.connect(**credentials.credentials)
    cur = conn.cursor()

    if list_id:
        cur.execute("update list set list_name = %s where id = %s",(list_name,list_id,))
    else:
        cur.execute("insert into list (list_name,user_id) values (%s,%s)",(list_name,user_id,))

    cur.close()
    conn.commit()
    conn.close()

    response = {
        "statusCode": 200
    }
    return response