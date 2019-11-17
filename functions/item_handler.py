import json

import psycopg2

from utils.db_credentials import DBCredentials

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

def add_item(event,context):
    log.info(json.dumps(event))
    user_id = event['pathParameters']['user_id']
    list_id = event['pathParameters']['list_id']
    body = json.loads(event['body'])
    item_name = body['item_name']
    
    credentials = DBCredentials()

    conn = psycopg2.connect(**credentials.credentials)
    cur = conn.cursor()

    cur.execute('insert into item (list_id,item_name) values (%s,%s)',(list_id,item_name,))

    cur.close()
    conn.commit()
    conn.close()

    response = {
        "statusCode": 200
    }
    return response

def delete_item(event,context):
    log.info(json.dumps(event))
    user_id = event['pathParameters']['user_id']
    list_id = event['pathParameters']['list_id']
    item_id = event['pathParameters']['item_id']
    
    credentials = DBCredentials()

    conn = psycopg2.connect(**credentials.credentials)
    cur = conn.cursor()

    cur.execute('delete from item where id = %s',(item_id,))

    cur.close()
    conn.commit()
    conn.close()

    response = {
        "statusCode": 200
    }
    return response

def claim_item(event,context):
    log.info(json.dumps(event))
    user_id = event['pathParameters']['user_id']
    list_id = event['pathParameters']['list_id']
    item_id = event['pathParameters']['item_id']
    body = json.loads(event['body'])
    guest_id = body['guest_id']

    credentials = DBCredentials()

    conn = psycopg2.connect(**credentials.credentials)
    cur = conn.cursor()

    cur.execute('update item set guest_id = %s where id = %s',(guest_id,item_id,))

    cur.close()
    conn.commit()
    conn.close()

    response = {
        "statusCode": 200
    }
    return response

def release_item(event,context):
    log.info(json.dumps(event))
    user_id = event['pathParameters']['user_id']
    list_id = event['pathParameters']['list_id']
    item_id = event['pathParameters']['item_id']
    item_id = event['pathParameters']['guest_id']
    
    credentials = DBCredentials()

    conn = psycopg2.connect(**credentials.credentials)
    cur = conn.cursor()

    cur.execute('update item set guest_id = null where id = %s',(item_id,))

    cur.close()
    conn.commit()
    conn.close()

    response = {
        "statusCode": 200
    }
    return response