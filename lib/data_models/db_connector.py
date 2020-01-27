from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseConnFactory():
    
    @classmethod
    def get_session(self, user,password,host,port,database):
                
        conn_string = '{database_type}+{driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'.format(
            database_type='postgresql',
            driver='psycopg2',
            db_user=user,
            db_password=password,
            db_host=host,
            db_port=port,
            db_name=database
            )

        engine = create_engine(conn_string)
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()

        return session