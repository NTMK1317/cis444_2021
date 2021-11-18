from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

import bcrypt
from db_con import get_db_instance, get_db
global_db_con = get_db()

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user

    password_from_user_form = request.form['password']
    firstname_from_user_form = request.form['firstname']

    print(password_from_user_form)

    cur = global_db_con.cursor()
    cur.execute(f"select password from users where username = '{firstname_from_user_form}';")
    db_pass = cur.fetchone()

    if db_pass is None:
        return json_response( message = 'Invalid credentials', authenticated =  False )

    db_pass_encode = db_pass[0].encode('utf-8')

    if( bcrypt.checkpw(  bytes(password_from_user_form,  'utf-8' )  , db_pass_encode ) ):
        user = {
            "sub" : request.form['firstname'] #sub is used by pyJwt as the owner of the token
            }
        print(user)
        if not user:
            return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )

        return json_response( token = create_token(user) , authenticated = True)
    else:
        return json_response( message = 'Invalid credentials', authenticated =  False )

