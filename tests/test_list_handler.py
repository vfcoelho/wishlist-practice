import os
from functions.list_handler import put_list


class TestList(object):
    
    def setup(self):

        os.environ["dbname"] = 'wishlist'
        os.environ["user"] = 'postgres'
        os.environ["password"] = 'postgres'
        os.environ["host"] = 'localhost'
        os.environ["port"] = '5432'

    def test_add(self):
    
        event = {
            'pathParameters':{
                "user_id":1
            },
            "body":'{"list_name":"Primeira Lista xD"}'
        }
        
        put_list(event,None)