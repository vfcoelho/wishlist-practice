import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseConnFactory():
    
    conn_string=None
    session=None
    engine=None

    def set_conn_string(self,user,password,host,port,database):

        if not self.conn_string:

            database_type = os.environ.get('database_type','postgresql')

            driver = 'psycopg2'
            if database_type == 'mysql':
                driver='pymysql'

            self.conn_string = '{database_type}+{driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'.format(
                database_type=database_type,
                driver=driver,
                db_user=user,
                db_password=password,
                db_host=host,
                db_port=port,
                db_name=database
                )

        return self


    def set_engine(self):
        
        if not self.engine:

            conn_string = f'{self.conn_string}'
            self.engine = create_engine(conn_string)

        return self
        

    def set_session(self):
        
        if not self.session:

            Session = sessionmaker()
            Session.configure(bind=self.engine)
            self.session = Session()

        return self

