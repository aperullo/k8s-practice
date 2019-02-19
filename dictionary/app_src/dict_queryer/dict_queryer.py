from flask import Flask
import os, signal
from random import randint
import requests
app = Flask(__name__)

class Shared:
    db_define_endpoint = 'get-def'
    db_rand_endpoint = 'rand-def'
    #TODO: don't hardcode the user and pass
    user='usernamevalue'
    passw='passwordvalue'
    num=0
    
    # ENV vars
    # In K8S services are exposed by being added as env vars. We're not going to know 
    # the name of that env var, so the yaml file will need to tell us by setting DB_SERVICE_NAME
    # and DB_SERVICE_PORT to the names of the env vars. We'll construct the url by reading those.
    # Or we'll default if thats not available.  
    db_service_envvar_name = os.getenv("DB_SERVICE_NAME", 'APP_DICT_DB_S_SERVICE_HOST')
    db_service_envvar_port = os.getenv("DB_SERVICE_PORT", 'APP_DICT_DB_S_SERVICE_PORT')

    db_service_name = os.getenv(db_service_envvar_name, None)
    db_service_port = os.getenv(db_service_envvar_port, None)
    
    db_url = 'http://127.0.0.1:4999' # default database url
    # if we were able to find the values in the env vars we can assemble the database service url.
    if all([db_service_name, db_service_port]):
        db_url = ':'.join([db_service_name, db_service_port]) 


def make_request(request_url, params):
    # we will retry the query up to five times, since a db may die while querying, we want to try 
    # again as the service will direct us to a new one.
    for retry in range(0,5):
        try: 
            # if it doesn't start with http:// then there probably isn't a protocal attached to the url 
            if not (request_url.startswith('http://') or request_url.startswith('https://')):
                reply = requests.get('http://'+request_url, params=params, timeout=1)
            else: 
                reply = requests.get(request_url, params=Params, timeout=1)

            # if everything worked out
            if reply.status_code == 200:
                return reply.text, 200
            elif reply.status_code == 403:
                return 'The requesting server could not authenticate.', 500
            else: #the return code was probably 500
                print('Error',  reply.status_code, reply.text)
                return 'The database server is misconfigured', 500
        except requests.RequestException:
            continue

    return "DB is unresponsive or keeps dying", 500
    

@app.route('/')
def hello():
    return ('Welcome to Dict service API. \n'
            'GET /define/<word> to get a definition, \n'
            'GET /random to get a random word')


# Defines a given word
@app.route('/define/<word>')
def define(word):
    # assemble back-end query url
    request_url = '/'.join([Shared.db_url, Shared.db_define_endpoint]) 

    # make request params dictionary
    request_params = { 'word': word, 'user': Shared.user, 'passw': Shared.passw }

    # chance to die before sending response
    if randint(0,100) == 1:
        killme()    

    reply = make_request(request_url, request_params)
    return id() + reply[0], reply[1]
   

@app.route('/random')
def rand_word():
    # assemble back-end query url
    request_url = '/'.join([Shared.db_url, Shared.db_rand_endpoint]) 

    # make request params dictionary
    request_params = { 'user': Shared.user, 'passw': Shared.passw }
    
    # chance to die before sending response
    if randint(0,100) == 1:
        killme()    

    reply = make_request(request_url, request_params)
    return id() + reply[0], reply[1]


# Kills the flask server
@app.route('/killme')
def killme():
    os.kill(os.getpid(), signal.SIGKILL)
    return 'did not die. PID: ' + str(os.getpid())

    
@app.route('/id')
def id():
    if Shared.num == 0:
        Shared.num = randint(1,1000)
    
    return 'Qry pod: ' + str(Shared.num) + ' '
    
   
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
