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
        except mariadb.dataError:
            print("There seems to be something wrong with your data.")
        except mariadb.databaseError:
            print("There seems to be something wrong with your database.")
        except mariadb.ProgrammingError:
            print("There seems to be something wrong with SQL written.")
        except mariadb.OperationalError:
            print("There seems to be something wrong with the connection.")
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
        user_image = request.json.get("image")
        rows = None
        user = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users(username, password, birthdate, bio, email, image) VALUES(?, ?, ?, ?, ?, ?)", [user_username, user_password, user_birthdate, user_bio, user_email, user_image])
            conn.commit()
            rows = cursor.rowcount
            print(rows)
            cursor.execute("SELECT * FROM users WHERE username=?", [user_username])
            user_row = cursor.fetchone()
            user_id = user_row[0]
            print(user_id)
            user = {}
            headers = [i[0] for i in cursor.description]
            user = dict(zip(headers, user_row))
            token = random.randint(0, 10000000)
            cursor.execute("INSERT INTO user_session(loginToken, user_id) VALUES(?, ?)", [token, user_id])
            conn.commit()
            rows = cursor.rowcount
            if rows == 1:
                user["loginToken"] = token
                print(token)
                print(user)
        except mariadb.dataError:
            print("There seems to be something wrong with your data.")
        except mariadb.databaseError:
            print("There seems to be something wrong with your database.")
        except mariadb.ProgrammingError:
            print("There seems to be something wrong with SQL written.")
        except mariadb.OperationalError:
            print("There seems to be something wrong with the connection.")
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
        token = request.json.get("token")
        user_username = request.json.get("username")
        user_password = request.json.get("password")
        user_birthdate = request.json.get("birthdate")
        user_bio = request.json.get("bio")
        user_email = request.json.get("email")
        user_image = request.json.get("image")
        rows = None
        user = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor() 
            cursor.execute("SELECT * FROM user_session WHERE loginToken=?", [token,])
            user = cursor.fetchone()
            print(user)
            if user != None and user != []:
                user_id = user[2]
                print(user_id)
                if user_username != "" and user_username != None:
                    cursor.execute("UPDATE users SET username=? WHERE id=?", [user_username, user_id])
                if user_password != "" and user_password != None:
                    cursor.execute("UPDATE users SET password=? WHERE id=?", [user_password, user_id])
                if user_birthdate != "" and user_birthdate != None:
                    cursor.execute("UPDATE users SET birthdate=? WHERE id=?", [user_birthdate, user_id])
                if user_bio != "" and user_bio != None:
                    cursor.execute("UPDATE users SET bio=? WHERE id=?", [user_bio, user_id])
                if user_email != "" and user_email != None:
                    cursor.execute("UPDATE users SET email=? WHERE id=?", [user_email, user_id])
                if user_image != "" and user_image != None:
                    cursor.execute("UPDATE users SET image=? WHERE id=?", [user_image, user_id])
                conn.commit()
                rows = cursor.rowcount
                cursor.execute("SELECT * FROM users WHERE id=?", [user_id])
                user_row = cursor.fetchone()
                users = {}
                headers = [i[0] for i in cursor.description]
                users = dict(zip(headers, user_row))
        except mariadb.dataError:
            print("There seems to be something wrong with your data.")
        except mariadb.databaseError:
            print("There seems to be something wrong with your database.")
        except mariadb.ProgrammingError:
            print("There seems to be something wrong with SQL written.")
        except mariadb.OperationalError:
            print("There seems to be something wrong with the connection.")
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response(json.dumps(users, default=str), mimetype="application/json", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)

    # elif request.method == 'DELETE'

@app.route('/login', methods=['POST', 'DELETE'])
def login():
    if request.method == 'POST':
        conn = None
        cursor = None
        user_username = request.json.get("username")
        user_password = request.json.get("password")
        rows = None
        user = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", [user_username, user_password])
            user_row = cursor.fetchone()
            print(user_row)
            user = {}
            headers = [i[0] for i in cursor.description]
            user = dict(zip(headers, user_row))
            if user_row != None and user_row != []:
                user_id = user_row[0]
                print(user_id)
                token = random.randint(0, 10000000)
                cursor.execute("INSERT INTO user_session(loginToken, user_id) VALUES(?, ?)", [token, user_id])
                conn.commit()
                rows = cursor.rowcount
                print(rows)
                user["loginToken"] = token
                print(token)
                print(user)      
        except mariadb.dataError:
            print("There seems to be something wrong with your data.")
        except mariadb.databaseError:
            print("There seems to be something wrong with your database.")
        except mariadb.ProgrammingError:
            print("There seems to be something wrong with SQL written.")
        except mariadb.OperationalError:
            print("There seems to be something wrong with the connection.")
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
        except mariadb.dataError:
            print("There seems to be something wrong with your data.")
        except mariadb.databaseError:
            print("There seems to be something wrong with your database.")
        except mariadb.ProgrammingError:
            print("There seems to be something wrong with SQL written.")
        except mariadb.OperationalError:
            print("There seems to be something wrong with the connection.")
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


