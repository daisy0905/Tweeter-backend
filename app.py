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
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if rows == 1:
                return Response(json.dumps(user, default=str), mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        rows = None
        token = request.json.get("token")
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_session WHERE loginToken=?", [token,])
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

@app.route('/tweets', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def tweets():
    if request.method == 'GET':
        conn = None
        cursor = None
        tweets = None
        user_id = request.args.get("id")
        print(user_id)
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if user_id != None and user_id != "":
                cursor.execute("SELECT * FROM tweet WHERE user_id=?", [user_id])
                rows = cursor.fetchall()
                tweets = []
                headers = [i[0] for i in cursor.description]
                cursor.execute("SELECT * FROM users WHERE id=?", [user_id])
                user_row = cursor.fetchone()
                username = user_row[1]
                print(username)
                for row in rows:
                    tweets.append(dict(zip(headers, row)))
                for tweet in tweets:
                    tweet["username"] = username
                print(tweets)
            else:
                cursor.execute("SELECT * FROM tweet INNER JOIN users ON tweet.user_id = users.id")
                rows = cursor.fetchall()
                tweets = []
                for i in range(len(rows)):
                    tweet={
                        "id": rows[i][0],
                        "content": rows[i][1],
                        "created_at": rows[i][2],
                        "user_id": rows[i][3],
                        "username": rows[i][5]
                    }
                    print(tweet)
                    tweets.append(tweet)
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
            if(tweets != None):
                return Response(json.dumps(tweets, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'POST':
        conn = None
        cursor = None
        tweet_content = request.json.get("content")
        token = request.json.get("token")
        user = None
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_session WHERE loginToken=?", [token,])
            user = cursor.fetchone()
            print(user)
            if user != None and user != []:
                user_id = user[2]
                print(user_id)
                cursor.execute("INSERT INTO tweet(content, user_id) VALUES(?, ?)", [tweet_content, user_id])
                conn.commit()
                rows = cursor.rowcount
                cursor.execute("SELECT * FROM tweet WHERE content=? AND user_id=?", [tweet_content, user_id])
                tweet_row = cursor.fetchone()
                print(tweet_row)
                tweet = {}
                headers = [i[0] for i in cursor.description]
                tweet = dict(zip(headers, tweet_row))
                print(tweet)
                cursor.execute("SELECT * FROM users WHERE id=?", [user_id])
                user_row = cursor.fetchone()
                username = user_row[1]
                print(username)
                tweet["username"] = username
                print(tweet)
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
                return Response(json.dumps(tweet, default=str), mimetype="application/json", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'PATCH':
        conn = None
        cursor = None
        token = request.json.get("token")
        tweet_content = request.json.get("content")
        tweet_id = request.json.get("id")
        user = None
        rows = None
        tweet = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor() 
            cursor.execute("SELECT * FROM user_session WHERE loginToken=?", [token,])
            user = cursor.fetchone()
            print(user)
            if user != None and user != []:
                user_id = user[2]
                print(user_id)
                if tweet_content != "" and tweet_content != None:
                    cursor.execute("UPDATE tweet SET content=? WHERE id=? AND user_id=?", [tweet_content, tweet_id, user_id])
                conn.commit()
                rows = cursor.rowcount
                cursor.execute("SELECT * FROM tweet WHERE id=? AND user_id=?", [tweet_id, user_id])
                tweet_row = cursor.fetchone()
                print(tweet_row)
                tweet={
                    "id": tweet_row[0],
                    "content": tweet_row[1]
                }
                print(tweet)
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
                return Response(json.dumps(tweet, default=str), mimetype="application/json", status=201)
            else:
                return Response("Updated failed", mimetype="text/html", status=500)
    
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        token = request.json.get("token")
        tweet_id = request.json.get("id")
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
                cursor.execute("DELETE FROM tweet WHERE id=? AND user_id=?", [tweet_id, user_id])
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
                return Response("Delete Success", mimetype="text/html", status=204)
            else:
                return Response("Delete failed", mimetype="text/html", status=500)

@app.route('/comments', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def comments():
    if request.method == 'GET':
        conn = None
        cursor = None
        comments = None
        tweet_id = request.args.get("tweet_id")
        print(tweet_id)
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if tweet_id != None and tweet_id != "":
                cursor.execute("SELECT * FROM tweet WHERE id=?", [tweet_id])
                row = cursor.fetchone()
                user_id = row[3]
                print(user_id)
                cursor.execute("SELECT * FROM comment WHERE user_id=? AND tweet_id=?", [user_id, tweet_id])
                rows = cursor.fetchall()
                print(rows)
                comments = []
                headers = [i[0] for i in cursor.description]
                cursor.execute("SELECT * FROM users WHERE id=?", [user_id])
                user_row = cursor.fetchone()
                username = user_row[1]
                print(username)
                for row in rows:
                    comments.append(dict(zip(headers, row)))
                for comment in comments:
                    comment["username"] = username
                print(comments)
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
            if(comments != None):
                return Response(json.dumps(comments, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)

    elif request.method == 'POST':
        conn = None
        cursor = None
        token = request.json.get("token")
        tweet_id = request.json.get("tweet_id")
        comment_content = request.json.get("content")
        user = None
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_session WHERE loginToken=?", [token,])
            user = cursor.fetchone()
            print(user)
            if user != None and user != []:
                user_id = user[2]
                print(user_id)
                cursor.execute("INSERT INTO comment(content, user_id, tweet_id) VALUES(?, ?, ?)", [comment_content, user_id, tweet_id])
                conn.commit()
                rows = cursor.rowcount
                cursor.execute("SELECT * FROM comment WHERE content=? AND user_id=? AND tweet_id=?", [comment_content, user_id, tweet_id])
                comment_row = cursor.fetchone()
                print(comment_row)
                comment = {}
                headers = [i[0] for i in cursor.description]
                comment = dict(zip(headers, comment_row))
                cursor.execute("SELECT * FROM users WHERE id=?", [user_id])
                user_row = cursor.fetchone()
                username = user_row[1]
                print(username)
                comment["username"] = username
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
                return Response(json.dumps(comment, default=str), mimetype="application/json", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'PATCH':
        conn = None
        cursor = None
        token = request.json.get("token")
        comment_content = request.json.get("content")
        comment_id = request.json.get("id")
        user = None
        rows = None
        comment = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor() 
            cursor.execute("SELECT * FROM user_session WHERE loginToken=?", [token,])
            user = cursor.fetchone()
            print(user)
            if user != None and user != []:
                user_id = user[2]
                print(user_id)
                if comment_content != "" and comment_content != None:
                    cursor.execute("UPDATE comment SET content=? WHERE id=? AND user_id=?", [comment_content, comment_id, user_id])
                conn.commit()
                rows = cursor.rowcount
                cursor.execute("SELECT * FROM comment WHERE id=? AND user_id=?", [comment_id, user_id])
                comment_row = cursor.fetchone()
                print(comment_row)
                comment = {}
                headers = [i[0] for i in cursor.description]
                comment = dict(zip(headers, comment_row))
                cursor.execute("SELECT * FROM users WHERE id=?", [user_id])
                user_row = cursor.fetchone()
                username = user_row[1]
                print(username)
                comment["username"] = username
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
                return Response(json.dumps(comment, default=str), mimetype="application/json", status=200)
            else:
                return Response("Updated failed", mimetype="text/html", status=500)
    
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        token = request.json.get("token")
        comment_id = request.json.get("id")
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
                cursor.execute("DELETE FROM comment WHERE id=? AND user_id=?", [comment_id, user_id])
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
                return Response("Delete Success", mimetype="text/html", status=204)
            else:
                return Response("Delete failed", mimetype="text/html", status=500)

@app.route('/tweet_likes', methods=['GET', 'POST', 'DELETE'])
def tweet_likes():
    if request.method == 'GET':
        conn = None
        cursor = None
        tweet_id = request.args.get("tweet_id")
        print(tweet_id)
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if tweet_id != None and tweet_id != "":
                cursor.execute("SELECT * FROM tweet_like WHERE tweet_id=?", [tweet_id])
                rows = cursor.fetchall()
                tweet_likes = []
                for row in rows:
                    user_id = row[2]
                    print(user_id)
                    cursor.execute("SELECT * FROM users WHERE id=?", [user_id])
                    user_row = cursor.fetchone()
                    username = user_row[1]
                    tweet_like = {
                        "tweet_id": tweet_id,
                        "user_id": user_id,
                        "username": username
                    }
                    print(tweet_like)
                    tweet_likes.append(tweet_like)
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
            if(tweet_likes != None):
                return Response(json.dumps(tweet_likes, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'POST':
        conn = None
        cursor = None
        token = request.json.get("token")
        tweet_id = request.json.get("tweet_id")
        user = None
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_session WHERE loginToken=?", [token,])
            user = cursor.fetchone()
            print(user)
            if user != None and user != []:
                user_id = user[2]
                print(user_id)
                cursor.execute("INSERT INTO tweet_like(tweet_id, user_id) VALUES(?, ?)", [tweet_id, user_id])
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
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("like success!", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)

    elif request.method == 'DELETE':
        conn = None
        cursor = None
        token = request.json.get("token")
        tweet_id = request.json.get("tweet_id")
        user = None
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_session WHERE loginToken=?", [token,])
            user = cursor.fetchone()
            print(user)
            if user != None and user != []:
                user_id = user[2]
                print(user_id)
                cursor.execute("DELETE FROM tweet_like WHERE tweet_id=? AND user_id=?", [tweet_id, user_id])
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
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("Deleted success!", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    

    

        
        


