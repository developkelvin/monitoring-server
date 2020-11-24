from flask import Flask, request
from env import get_connection
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
    return 'success msg'

@app.route('/dbtest')
def db_test():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = 'insert into `test_table` (`col_str`, `col_timestamp`, `col_datetime`) values (%s, now(), now())'
            cursor.execute(sql, ('flask_test'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a whole records
            sql = "SELECT * FROM `test_table`"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    finally:
        connection.close()

    return str(result)
    

# @app.route("/me")
# def me_api():
#     user = get_current_user()
#     return {
#         "username": user.username,
#         "theme": user.theme,
#         "image": url_for("user_image", filename=user.image),
#     }





# PyMySQL Test Codes




# API Test Code

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('profile', username='John Doe'))
