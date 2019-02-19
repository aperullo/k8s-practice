from flask import Flask, request
import os, signal, json
from random import randint, choice
app = Flask(__name__)

class Shared:

    dictionary = {}
    num = 0  # an id field

    # ENV vars
    dict_loc = os.getenv('DICT_LOC', 'dict_data/dictionary.json')
    secret_dir = os.getenv('SECRET_DIR', 'secret_dir')

# get definition of word
@app.route('/get-def')
def get_def(word='example', user='wrong', passw='wrong'):

    # internal versions of the vars since we don't want to override the arguments
    _word = word if request.args.get('word') is None else request.args.get('word')
    _user = user if request.args.get('user') is None else request.args.get('user')
    _passw = passw if request.args.get('passw') is None else request.args.get('passw')
    
    # Authenticate 
    try:
        if not authenticate(_user, _passw):
            return 'Provided Credentials are invalid. Forbidden.', 403    
    except FileNotFoundError as error:
        print(error)
        return 'Internal server error: no auth files', 500     
   
    # Is the dictionary loaded?
    if not any(Shared.dictionary):
        load_dict()
    
    definition = Shared.dictionary.get(_word.upper(), 'is not in the dictionary, or is spelled incorrectly')
    
    # randomly have a chance to die in the middle of the operation
    if randint(0,5) == 1:
            killme() 
    
    return '{id} {word}: {definition}'.format(**{'id': id(),'word': _word.title(), 'definition': definition}) 
    
    
# Random definition
@app.route('/rand-def')
def rand_def():

    # Is the dictionary loaded?
    if not any(Shared.dictionary):
        load_dict()
    
    # choose a random word from the keys.
    word = choice(list(Shared.dictionary.keys()))
    return get_def(word=word, user=request.args.get('user'), passw=request.args.get('passw'))
    

def authenticate(user, passw):

    real_user, real_passw = '',''
    
    # May throw FileNotFoundError
    try:
        # try to find secret directory, then corresponding files
        os.path.exists(Shared.secret_dir)
              
        with open(Shared.secret_dir + '/username', 'r') as user_file:
            real_user = user_file.read()
    
        with open(Shared.secret_dir + '/password', 'r') as passw_file:
            real_passw = passw_file.read()
    
    except FileNotFoundError as error:
        # Chain the exception to add our message to the stacktrace
        raise FileNotFoundError('DB: Authentication files not found') from error 
            
    #print(user.__repr__(), real_user.__repr__(), user == real_user)
    #print(passw.__repr__(), real_passw.__repr__(), passw == real_passw)
    
    # do the user names and passwords match?   
    return ((user == real_user) and (passw == real_passw))
   
 
# Kills the flask server 
def killme():
    os.kill(os.getpid(), signal.SIGKILL)
    return 'did not die. PID: ' + str(os.getpid())
    

@app.route('/id')
def id():
    #todo: remove global
    if Shared.num == 0:
        Shared.num = randint(1,1000)
    
    return 'DB pod: ' + str(Shared.num)  + ' '
    

def load_dict():
    #global dictionary
    #global dict_loc
    with open(Shared.dict_loc) as dict_file:
        Shared.dictionary = json.load(dict_file)
   

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') #port=4999
    
    
