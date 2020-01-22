import json

import psycopg2

from utils.db_credentials import DBCredentials
from lib.data_models.db_connector import DatabaseConnFactory
from lib.data_models.db_model import List, GuestList

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

def list_lists(event,context):
    log.info(json.dumps(event))
    user_id = event['pathParameters']['user_id']
    is_host = event['queryStringParameters']['is_host']

    credentials = DBCredentials()
    session = DatabaseConnFactory.get_session(**credentials.credentials)

    list_list = []
    if is_host:
        # cur.execute("select id,list_name from list where user_id = %s",(user_id,))
        list_list = session.query(List).filter(List.user_id == user_id).all()
    else:
        # cur.execute('select l.id,l.list_name,gl.id from list as l join guest_list as gl on l.id = gl.list_id where gl.user_id = %s',(user_id,))
        list_list = session.query(List).join(GuestList, GuestList.list_id == List.id).filter(GuestList.user_id == user_id).all()

    results = []
    for list_row in list_list:

        result = {
            "id":list_row.id,
            "name":list_row.list_name
        }
        # if len(row)==3:
        #     result["guest_id"] = row[2]

        results.append(result)

    session.close()

    response = {
        "statusCode": 200,
        "body": json.dumps(results)
    }
    return response

def put_list(event,context):
    log.info(json.dumps(event))
    user_id = event['pathParameters']['user_id']
    list_id = event['pathParameters'].get('list_id')
    body = json.loads(event['body'])
    list_name = body['list_name']

    credentials = DBCredentials()

    conn = psycopg2.connect(**credentials.credentials)
    cur = conn.cursor()

    try:

        if list_id:
            cur.execute("update list set list_name = %s where id = %s",(list_name,list_id,))
        else:
            cur.execute("insert into list (list_name,user_id) values (%s,%s)",(list_name,user_id,))

        conn.commit()

        response = {
            "statusCode": 200
        }
        return response

    except Exception as e:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def add_guest(event,context):
    log.info(json.dumps(event))
    user_id = event['pathParameters']['user_id']
    list_id = event['pathParameters']['list_id']
    body = json.loads(event['body'])
    user_id = body['user_id']
    
    credentials = DBCredentials()

    conn = psycopg2.connect(**credentials.credentials)
    cur = conn.cursor()

    cur.execute('insert into guest_list (list_id,user_id) values (%s,%s)',(list_id,user_id,))

    cur.close()
    conn.commit()
    conn.close()

    response = {
        "statusCode": 200
    }
    return response

def delete_guest(event,context):
    log.info(json.dumps(event))
    user_id = event['pathParameters']['user_id']
    list_id = event['pathParameters']['list_id']
    guest_id = event['pathParameters']['guest_id']
    
    credentials = DBCredentials()

    conn = psycopg2.connect(**credentials.credentials)
    cur = conn.cursor()

    cur.execute('delete from guest_list where id = %s',(guest_id,))

    cur.close()
    conn.commit()
    conn.close()

    response = {
        "statusCode": 200
    }
    return response