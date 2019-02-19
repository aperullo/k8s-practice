from flask import Flask
import os, signal
from random import randint
app = Flask(__name__)

num = 0;

@app.route('/')
def hello():
    return 'Hello world!'

# Kills the flask server
@app.route('/killme')
def killme():
    os.kill(os.getpid(), signal.SIGKILL)
    return "didn't die. PID: " + str(os.getpid())
    
# to help us test out config maps in kubernetes  
@app.route('/id')
def listfiles():
    global num
    if num == 0:
        num = randint(1,1000)
    
    return "this is podv3 " + str(num)
    
   
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
