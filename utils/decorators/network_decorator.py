import json
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

class Network(object):

    def __call__(self, f):
        
        def run(event, **kwargs):
            log.info(json.dumps(event))
            response = {
                "statusCode": 500
            }

            try:
                path_patameters = event['pathParameters']
                qs_patameters = event['queryStringParameters']
                body = json.loads(event.get('body','{}'))

                results = f(**path_patameters,**qs_patameters,body=body,**kwargs)

                response = {
                    "statusCode": 200,
                    "body": json.dumps(results)
                }

            except Exception as e:
                log.exception(str(e))
            finally:
                return response

        return run
