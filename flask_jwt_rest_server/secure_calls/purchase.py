from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

from db_con import get_db_instance, get_db
global_db_con = get_db()
import datetime

def handle_request():
    logger.debug("Purchase Book Handle Request")
    print(g.jwt_data)
    print(request.args.get('book_id'))
    u_name = g.jwt_data['sub'];
    b_id = request.args.get('book_id')

    cur = global_db_con.cursor()
    cur.execute(f"select id from users where username = '{u_name}';")
    u_id = cur.fetchone()[0]
    date_t = str(datetime.datetime.now())

    cur.execute(f"insert into purchases (book_id, buyer_id, date_time) values ('{b_id}', '{u_id}', '{date_t}');")
    global_db_con.commit()

    return json_response( token = create_token(  g.jwt_data ))

