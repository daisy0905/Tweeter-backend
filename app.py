import mariadb
from flask import Flask, request, Response
import json
import dbcreds
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/users', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def users():
    if request.method == 'GET':
        conn = None
        cursor = None
        user_id = request.args.get("id")
        print(user_id)
        users = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if user_id != None and user_id != "":
                cursor.execute("SELECT * FROM users WHERE id=?", [user_id])
                row = cursor.fetchone()
                users = {}
                headers = [i[0] for i in cursor.description]
                users = dict(zip(headers, row))
            else:
                cursor.execute("SELECT * FROM users")
                rows = cursor.fetchall()
                users = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    users.append(dict(zip(headers, row)))
        except Exception as error:
            print("Something went wrong (THIS IS LAZAY): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(users != None):
                return Response(json.dumps(users, default=str), mimetype="application/json", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)

    elif request.method == 'POST':
        conn = None
        cursor = None
        user_username = request.json.get("username")
        user_password = request.json.get("password")
        user_birthdate = request.json.get("birthdate")
        user_bio = request.json.get("bio")
        user_email = request.json.get("email")
        user_url = request.json.get("url")
        rows = None
        user = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users(username, password, birthdate, bio, email, url) VALUES(?, ?, ?, ?, ?, ?)", [user_username, user_password, user_birthdate, user_bio, user_email, user_url])
            conn.commit()
            rows = cursor.rowcount
            print(rows)
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", [user_username, user_password])
            user_row = cursor.fetchone()
            token = random.randint(0, 10000000)
            user = {}
            headers = [i[0] for i in cursor.description]
            user = dict(zip(headers, user_row))
            user["loginToken"] = token
            print(token)
            print(user)
            # cursor.execute("INSERT INTO user_session ")
        except Exception as error:
            print("Something went wrong (THIS IS LAZAY): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response(json.dumps(user, default=str), mimetype="application/json", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'PATCH':
        conn = None
        cursor = None
        loginToken = request.json.get("token")
        user_username = request.json.get("username")
        user_password = request.json.get("password")
        user_birthdate = request.json.get("birthdate")
        user_bio = request.json.get("bio")
        user_email = request.json.get("email")
        user_url = request.json.get("url")
        rows = None


    

@app.route('/api/login', methods=['POST', 'DELETE'])
def login():
    if request.method == 'POST':
        conn = None
        cursor = None
        user_username = request.json.get("username")
        user_password = request.json.get("password")
        users = None
        rows = None
        user = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", [user_username, user_password])
            users = cursor.fetchall()
            print(users)
            if users != None and users != []:
                user_id = users[0][0]
                print(user_id)
                token = random.randint(0, 10000000)
                cursor.execute("INSERT INTO user_login(token, user_id) VALUES(?, ?)", [token, user_id])
                conn.commit()
                rows = cursor.rowcount
                print(rows)
                user = {
                    "id": users[0][0],
                    "username": users[0][1],
                    "token": token
                }
        except Exception as error:
            print("Something went wrong (THIS IS LAZAY): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response(json.dumps(user, default=str), mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        rows = None
        post_token = request.json.get("token")
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_login WHERE token=?", [post_token,])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (THIS IS LAZAY): ")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if rows == 1:
                return Response("logout success!", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)


