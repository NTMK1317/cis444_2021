from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

from db_con import get_db_instance, get_db
global_db_con = get_db()

def handle_request():
    logger.debug("Open Call - Get Messages Handle Request")
    #use data here to auth the user

    cur = global_db_con.cursor()
    cur.execute("select * from messages;")
    db_messages = cur.fetchall()

    if db_messages is None:
        return json_response( notify = 'No messages in Database', filled =  False )

    return json_response(filled = db_messages)

