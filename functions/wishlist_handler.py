import json

import psycopg2

from utils.db_credentials import DBCredentials

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

def list_gifts(event, context):
    log.info(json.dumps(event))

    credentials = DBCredentials()

    connection = psycopg2.connect(**credentials.credentials)

    cursor = connection.cursor()
    cursor.execute("select * from items")

    columns = (
        'id', 'name', 'reserved'
    )

    gifts = []

    for row in cursor.fetchall():
        gift = {
            'id': row[0], 
            'name': row[1], 
            'reserved': row[2]
        }

        gifts.append(gift)

    giftsJson = json.dumps(gifts)

    cursor.close()
    connection.commit()
    connection.close()

    response = {"statusCode": 200, "body": giftsJson}

    return response

def claim_gift(event,context):
    log.info(json.dumps(event))
    item_id = event['pathParameters']['id']
    
    log.info(f"item_id: {item_id}")
    
    credentials = DBCredentials()

    conn = psycopg2.connect(**credentials.credentials)
    cur = conn.cursor()

    cur.execute("update items set reserved = true where id = %s",(item_id,))

    cur.close()
    conn.commit()
    conn.close()

    response = {
        "statusCode": 200
    }
    return response

    