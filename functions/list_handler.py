
from utils.decorators.lambda_decorator import Lambda
from utils.decorators.network_decorator import Network
from utils.decorators.database_decorator import Database
from lib.data_models.db_model import List, GuestList

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

@Lambda()
@Network()
@Database()
def list_lists(user_id,is_host,session,**kwargs):
    list_list = []
    if is_host:
        list_list = session.query(List).filter(List.user_id == user_id).all()
    else:
        list_list = session.query(List).join(GuestList, GuestList.list_id == List.id).filter(GuestList.user_id == user_id).all()

    results = []
    for list_row in list_list:

        result = {
            "id":list_row.id,
            "name":list_row.list_name
        }
        if not is_host:
            result['guest_id'] = [x.id for x in list_row.guest_list_list if x.user_id == user_id][0]

        results.append(result)

    return results

@Lambda()
@Network()
@Database()
def put_list(user_id,body,session,list_id=None,**kwargs):
    
    list_name = body['list_name']

    wish_list = None
    if list_id:
        wish_list = session.query(List).filter(List.id == list_id).one_or_none()
        wish_list.list_name = list_name
    else:
        wish_list = List()
        wish_list.user_id = user_id
        wish_list.list_name = list_name

    session.add(wish_list)


@Lambda()
@Network()
@Database()
def add_guest(list_id,body,session,**kwargs):
    
    user_id = body['user_id']
    
    guest = GuestList()
    guest.list_id = list_id
    guest.user_id = user_id
    session.add(guest)

@Lambda()
@Network()
@Database()
def delete_guest(guest_id,session,**kwargs):

    session.query(GuestList).filter(GuestList.id == guest_id).delete()