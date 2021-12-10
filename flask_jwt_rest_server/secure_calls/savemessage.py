from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

from db_con import get_db_instance, get_db
global_db_con = get_db()

def handle_request():
    logger.debug("Save Message Handle Request")
    print(g.jwt_data)
    print(request.args.get('user_msg_sent'))
    u_name = g.jwt_data['sub'];
    u_msg = request.args.get('user_msg_sent')

    cur = global_db_con.cursor()
    cur.execute(f"insert into messages (name, message) values ('{u_name}', '{u_msg}');")
    global_db_con.commit()

    return json_response( token = create_token(  g.jwt_data ))

