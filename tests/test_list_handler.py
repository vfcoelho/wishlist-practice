import os
from functions.list_handler import put_list, list_lists, add_guest, delete_guest
from tests.test_base import TestBase

class TestListHandler(TestBase):
    
    # def setup(self):
    #     super().setup()

    def test_list_host(self):
        event = {
            'pathParameters':{
                "user_id":2
            },
            'queryStringParameters':{
                "is_host": True
            }
        }

        result = list_lists(event,None)

        assert result == {'body': '[{"id": 1, "name": "Segunda lista"}]', 'statusCode': 200}

    def test_list_guest(self):
        event = {
            'pathParameters':{
                "user_id":1
            },
            'queryStringParameters':{
                "is_host": False
            }
        }

        result = list_lists(event,None)

        assert result == {'body': '[{"id": 1, "name": "Segunda lista", "guest_id": 1}]', 'statusCode': 200}

    def test_add(self):
    
        list_name = "Primeira Lista xD"
        
        event = {
            'pathParameters':{
                "user_id":1
            },
            "body":'{"list_name":"'+list_name+'"}'
        }
        
        put_list(event,None)

        self.cur.execute('select list_name from "list" l join "user" u on u.id = l.user_id where u.email=%s',('test@test.com',))
        list_rows = self.cur.fetchall()
        assert len(list_rows) == 1
        assert list_rows[0][0] == list_name

    def test_update(self):
    
        list_name = "Primeira Lista xD"
        
        event = {
            'pathParameters':{
                "user_id":2,
                "list_id":1
            },
            "body":'{"list_name":"'+list_name+'"}'
        }
        
        put_list(event,None)

        self.cur.execute('select list_name from "list"')
        list_rows = self.cur.fetchall()
        assert len(list_rows) == 1
        assert list_rows[0][0] == list_name

    def test_add_guest(self):
    
        event = {
            'pathParameters':{
                "user_id":2,
                "list_id":1
            },
            "body":'{"user_id":3}'
        }
        
        add_guest(event,None)

        self.cur.execute('select * from guest_list')
        list_rows = self.cur.fetchall()
        assert len(list_rows) == 2
    
    def test_delete_guest(self):
    
        event = {
            'pathParameters':{
                "user_id":2,
                "list_id":1,
                "guest_id":1
            }
        }
        
        delete_guest(event,None)

        self.cur.execute('select * from guest_list')
        list_rows = self.cur.fetchall()
        assert len(list_rows) == 0