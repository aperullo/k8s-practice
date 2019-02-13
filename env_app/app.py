from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello world!'
   
# to help us test out config maps in kubernetes  
@app.route('/listenv')
def listenv():
    print(os.getenv('PY_SUBJECT', 'no py subjec'))
    return os.getenv('PY_SUBJECT', 'no py subjec')
   
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
