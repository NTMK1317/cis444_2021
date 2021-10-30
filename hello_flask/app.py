from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt
import bcrypt

import datetime

from db_con2 import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"
JWT_SECRET = "gkhgfkhgjfhjd,jhfhj"

global_db_con = get_db()


#with open("secret", "r") as f:
        #JWT_SECRET = f.read()

@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    print(request.form)
    return render_template('backatu.html',input_from_browser= str(request.form) )

@app.route('/getTime', methods=['GET']) #endpoint
def get_time():
    return json_response(data={"password" : request.args.get('password'),
                                "class" : "cis44",
                                "serverTime":str(datetime.datetime.now())
                            }
                )

#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )

#Assigment 3
@app.route('/auth',  methods=['POST']) #endpoint
def auth():
    print(request.form)
    return json_response(data=request.form)

@app.route('/auth3',  methods=['POST']) #endpoint
def auth3():
    print(request.form)
    usern = request.form['username']
    passw = request.form['password']

    cur = global_db_con.cursor()
    cur.execute(f"select password from users where username = '{usern}';")
    db_pass = cur.fetchone()[0]
    #print( db_pass )
    db_pass_encode = db_pass.encode('utf-8')
    #print( bcrypt.checkpw(  bytes(passw,  'utf-8' )  , db_pass_encode ) )

    return json_response(data=request.form)


@app.route('/auth4',  methods=['POST']) #endpoint
def auth4():
    print(request.form)
    usern = request.form['username']
    passw = request.form['password']

    cur = global_db_con.cursor()
    cur.execute(f"select password from users where username = '{usern}';")

    db_pass = cur.fetchone()

    if db_pass is None:
        return json_response(data={"jwt" : "false"})

    db_pass_encode = db_pass[0].encode('utf-8')
    
    if( bcrypt.checkpw(  bytes(passw,  'utf-8' )  , db_pass_encode ) ):
        jwt_str = jwt.encode({"UN" : usern,
                    "PW" : passw} 
                    , JWT_SECRET, algorithm="HS256")
        print(jwt_str)
        #jwt = jwt_str
        return json_response(data={"jwt" : jwt_str})
    else:
        return json_response(data={"jwt" : "false"})

@app.route('/getBook', methods=['GET']) #endpoint
def get_book():
    cur = global_db_con.cursor()
    cur.execute("select * from books;")
    db_books = cur.fetchall()
    return json_response(books = db_books)

@app.route('/addUser',  methods=['POST']) #endpoint
def add_user():
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

@app.route('/purchase', methods=['POST']) #endpoint
def pur_bk():
    jwt_token = request.form['jwt']
    output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"])
    u_name = output['UN'];
    b_id = request.form['bkid'];

    print(jwt_token)
    print(output)

    cur = global_db_con.cursor()
    cur.execute(f"select id from users where username = '{u_name}';")
    u_id = cur.fetchone()[0]
    date_t = str(datetime.datetime.now())

    cur.execute(f"insert into purchases (book_id, buyer_id, date_time) values ('{b_id}', '{u_id}', '{date_t}');")
    global_db_con.commit()
    return json_response(data={"status" : "good"})

@app.route('/exposejwt', methods=['POST']) #endpoint
def exposejwt():
    jwt_token = request.form['jwt']
    print(jwt_token)
    output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"])
    print(output)
    print(output['UN'])

    return json_response(data={"status" : "good"})

app.run(host='0.0.0.0', port=80)

