import os
from functions.wishlist_handler import claim_gift


class TestBase(object):
    
    def test_base(self):
    

        event = {'pathParameters':{"id":1}}
        # event = {'pathParameters':{"id":1},'requestContext':{'stage':'local'}}

        claim_gift(event,None)