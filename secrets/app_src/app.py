from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello world!'

# to help us test out config maps in kubernetes  
@app.route('/listenv')
def listenv():
    return os.getenv('USERNAME', 'no py subjec')
    
# to help us test out config maps in kubernetes  
@app.route('/listfiles')
def listfiles():
    try:
        return str(os.listdir("/etc/secret_dir"))
    except FileNotFoundError:
        return "no file at that loc" 
   
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
