from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

import bcrypt
from db_con import get_db_instance, get_db
global_db_con = get_db()

def handle_request():
    logger.debug("Add User Handle Request")
    #use data here to auth the user

    print(request.form['username'])
    newuser = request.form['username']
    password_to_salt = request.form['password']
    salted = bcrypt.hashpw( bytes(password_to_salt,  'utf-8' ) , bcrypt.gensalt(10))
    salt_decode = salted.decode('utf-8')

    print(salt_decode)

    cur = global_db_con.cursor()
    cur.execute(f"insert into users (username, password) values ('{newuser}', '{salt_decode}');")
    global_db_con.commit()
    return json_response(data={"status" : "good"})
