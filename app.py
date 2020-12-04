from flask import Flask, request, make_response
from sp import *
import pymysql

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hello world"

@app.route('/login')
def wow():
    return "login page"

@app.route('/monitoring', methods=['POST'])
def get_monitoring_data():
    monitoring_data = request.get_json()
    print(monitoring_data)
    return monitoring_data

@app.route('/auth', methods=['POST'])
def auth():
    auth_data = request.get_json()
    api_key = auth_data['api_key']
    is_validate = sp_auth_server(api_key=api_key)
    if is_validate:
        resp = make_response('', 200)
        return resp
    else:
        resp = make_response('', 404)
        return resp

@app.route('/dbtest')
def db_test():
    result = sp_db_test()

    return str(result)
    
if __name__ == '__main__':
    app.run(debug=True)
