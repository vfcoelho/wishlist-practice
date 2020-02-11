
from utils.decorators.lambda_decorator import Lambda
from utils.decorators.network_decorator import Network
from utils.decorators.database_decorator import Database

from lib.data_models.db_model import Item

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

@Lambda()
@Network()
@Database()
def add_item(list_id,body,session,**kwargs):
    item_name = body['item_name']
    
    item = Item()
    item.list_id = list_id
    item.item_name = item_name

    session.add(item)

@Lambda()
@Network()
@Database()
def delete_item(item_id,session,**kwargs):
    
    session.query(Item).filter(Item.id == item_id).delete()

@Lambda()
@Network()
@Database()
def claim_item(item_id,body,session,**kwargs):
    guest_id = body['guest_id']

    item = session.query(Item).filter(Item.id == item_id).one_or_none()
    item.guest_id = guest_id
    session.add(item)

@Lambda()
@Network()
@Database()
def release_item(item_id,session,**kwargs):
    
    item = session.query(Item).filter(Item.id == item_id).one_or_none()
    item.guest_id = None
    session.add(item)

