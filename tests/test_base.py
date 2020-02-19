import os,sys
import psycopg2
# from functions.wishlist_handler import claim_gift, list_gifts
from utils.db_credentials import DBCredentials
from lib.data_models.db_connector import DatabaseConnFactory
from lib.data_models.db_model import build_model, drop_model
from alembic import op
from sqlalchemy import Table, MetaData
from alembic.migration import MigrationContext
from alembic.operations import Operations

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "."))
sys.path.append(os.path.join(here, ".."))

class TestBase(object):

    @classmethod
    def set_env_vars(self):
        os.environ["dbname"] = 'wishlist'
        os.environ["user"] = 'postgres'
        os.environ["password"] = 'postgres'
        os.environ["host"] = 'localhost'
        os.environ["port"] = '5432'

    def _build_db(self):
        build_model()

    def _drop_db(self):
        drop_model()

    def seed(self,db_connection):

        conn = db_connection.engine.connect()
        ctx = MigrationContext.configure(conn)
        op = Operations(ctx)

        meta = MetaData(bind=op.get_bind())
        meta.reflect(only=('user','list','guest_list','item'))
        user = Table('user', meta)
        op.bulk_insert(user,
            [
                {'name':'Coelho dos Testes',
                        'email':'test@test.com'},
                {'name':'Tartaruga dos Testes',
                        'email':'test2@test.com'},
                {'name':'Cavalo dos Testes',
                        'email':'cavalo@test.com'}
            ]
        )
        
        list = Table('list', meta)
        op.bulk_insert(list,
            [
                {'list_name':'Segunda lista',
                        'user_id':2}
            ]
        )

        guest_list = Table('guest_list', meta)
        op.bulk_insert(guest_list,
            [
                {'list_id':1,
                        'user_id':1}
            ]
        )

        item = Table('item', meta)
        op.bulk_insert(item,
            [
                {'list_id':1,
                        'item_name':'Jogo de Copos'}
            ]
        )

    def setup(self):

        TestBase.set_env_vars()

        credentials = DBCredentials()
        db_connection = DatabaseConnFactory()
        self.db_connection = db_connection.set_conn_string(**credentials.credentials)\
                .set_engine()\
                .set_session()

        self._build_db()

        self.seed(db_connection)
    
    def teardown(self):


        self.db_connection.session.close()
        self._drop_db()
