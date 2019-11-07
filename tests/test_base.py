import os
from functions.wishlist_handler import claim_gift, list_gifts


class TestBase(object):
    
    def setup(self):

        os.environ["dbname"] = 'wishlist'
        os.environ["user"] = 'postgres'
        os.environ["password"] = 'postgres'
        os.environ["host"] = 'localhost'
        os.environ["port"] = '5432'

    def test_base(self):
    
        event = {'pathParameters':{"id":1}}
        # event = {'pathParameters':{"id":1},'requestContext':{'stage':'local'}}

        claim_gift(event,None)

    def test_list(self):
    
        result = list_gifts({},None)

        print(result)