from flask import Flask, request, make_response, render_template, session
from flask.helpers import url_for
from werkzeug.utils import redirect
from sp import *
import pymysql

app = Flask(__name__)

app.secret_key = b'_kelvinkelvin_'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/workspace')
def workspace():
    if 'user_id' in session:
        workspaces = sp_get_user_workspace(session['user_id'])
        return render_template('workspace.html',workspaces=workspaces)
    else:
        return redirect(url_for('login'))

@app.route('/addworkspace', methods=['GET', 'POST'])
def add_workspace():
    if 'user_id' in session:
        if request.method == 'GET':
            return render_template('add_workspace.html')
        elif request.method == 'POST':
            name = request.form['name']
            desc = request.form['desc']
            is_success = sp_add_workspace(session['user_id'], name, desc)
            if is_success:
                return redirect(url_for('workspace'))
            else:
                return render_template('add_workspace.html')
    else:
        return redirect(url_for('login'))

@app.route('/registserver', methods=['GET', 'POST'])
def regist_server():
    if 'user_id' in session:
        if request.method == 'GET':
            return render_template('regist_server.html')
        elif request.method == 'POST':
            # do_something
            raise NotImplementedError()
            return redirect(url_for('workspace'))
    else:
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'GET':
        # render login page
        return render_template('signup.html')
    else: 
        id = request.form['id'] 
        pwd = request.form['pwd']
        name = request.form['name']
        email = request.form['email']
        desc = request.form['desc']

        is_signup_success = sp_signup(id, pwd, name, email, desc)

        if is_signup_success:
            return redirect(url_for('login'))
        else:
            return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'GET':
        # render login page
        return render_template('login.html')
    else: 
        id = request.form['id'] 
        pwd = request.form['pwd']

        is_login_success = sp_login(id, pwd)
        if is_login_success:
            session['user_id'] = id
            session['sp'] = StoredProcedures(id)
            return redirect('/workspace')
        else:
            return redirect('/login')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/monitoring', methods=['POST'])
def get_monitoring_data():
    # aws lambda에서 처리해도 될듯?
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
