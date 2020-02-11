from utils.db_credentials import DBCredentials
from lib.data_models.db_connector import DatabaseConnFactory

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

class Database(object):

    def __call__(self, f):
        
        def run(**kwargs):
            
            credentials = DBCredentials()
            session = DatabaseConnFactory.get_session(**credentials.credentials)
            result = None

            try:
                result = f(session=session,**kwargs)
                session.commit()
            except Exception as e:
                log.exception(str(e))
                raise
            finally:
                session.close()
                return result
                
        return run