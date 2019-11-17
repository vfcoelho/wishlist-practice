import os,sys
import psycopg2
# from functions.wishlist_handler import claim_gift, list_gifts
from utils.db_credentials import DBCredentials

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "."))
sys.path.append(os.path.join(here, ".."))

class TestBase(object):
    
    def drop_all_tables(self):
        self.cur.execute('SELECT tablename FROM pg_tables WHERE schemaname = current_schema()')

        for row in self.cur.fetchall():
            self.cur.execute(f'DROP TABLE IF EXISTS "{row[0]}" CASCADE;')

        self.conn.commit()

    def setup(self):

        os.environ["dbname"] = 'wishlist'
        os.environ["user"] = 'postgres'
        os.environ["password"] = 'postgres'
        os.environ["host"] = 'localhost'
        os.environ["port"] = '5432'

        credentials = DBCredentials()
        self.conn = psycopg2.connect(**credentials.credentials)
        self.cur = self.conn.cursor()

        self.drop_all_tables()

        with open(f'{here}/../database_scripts.sql','r') as db_scripts_file:
            db_scripts = db_scripts_file.read().replace('\n',' ').replace('\t','')
            db_scripts_list = db_scripts.split(';')

            allowed_commands = ['create','insert']

            for script in db_scripts_list:
                first_word = script.strip().split(' ',1)[0]
                if first_word not in allowed_commands:
                    continue
                self.cur.execute(script)
                self.conn.commit()
    
    def teardown(self):

        self.cur.close()
        self.conn.commit()
        self.conn.close()

    # def test_base(self):
    
    #     event = {'pathParameters':{"id":1}}
    #     # event = {'pathParameters':{"id":1},'requestContext':{'stage':'local'}}

    #     claim_gift(event,None)

    # def test_list(self):
    
    #     result = list_gifts({},None)

    #     print(result)