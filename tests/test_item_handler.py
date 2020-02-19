import os
from functions.item_handler import add_item,delete_item,release_item,claim_item
from tests.test_base import TestBase
from lib.data_models.db_model import Item

class TestItemHandler(TestBase):
    
    # def setup(self):
    #     super().setup()

    def test_add_item(self):
        event = {
            'pathParameters':{
                "user_id":1,
                "list_id":1
            },
            'body':'{"item_name": "Panelas"}'
        }

        result = add_item(event,None)

        rows = self.db_connection.session.query(Item).all()
        assert len(rows) == 2
        assert rows[1].item_name == 'Panelas'

    def test_delete_item(self):
        event = {
            'pathParameters':{
                "user_id":1,
                "list_id":1,
                "item_id":1
            }
        }

        result = delete_item(event,None)

        self.cur.execute('select item_name from item')
        rows = self.cur.fetchall()
        assert len(rows) == 0

    def test_claim_item(self):
    
        list_name = "Primeira Lista xD"
        
        event = {
            'pathParameters':{
                "user_id":1,
                "list_id":1,
                "item_id":1
            },
            'body':'{"guest_id": 1}'
        }
        
        claim_item(event,None)

        self.cur.execute('select guest_id from item')
        list_rows = self.cur.fetchall()
        assert len(list_rows) == 1
        assert list_rows[0][0] == 1
    
    def test_release_item(self):
    
        list_name = "Primeira Lista xD"
        
        event = {
            'pathParameters':{
                "user_id":1,
                "list_id":1,
                "item_id":1,
                "guest_id":1
            }
        }
        
        release_item(event,None)

        self.cur.execute('select guest_id from item')
        list_rows = self.cur.fetchall()
        assert len(list_rows) == 1
        assert list_rows[0][0] == None
