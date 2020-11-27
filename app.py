import mariadb
from flask import Flask, request, Response
import json
import dbcreds
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)
def create_token():
    letters = string.ascii_letters
    loginToken = ''.join(random.choice(letters) for i in range(30))
    return loginToken

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
                rows = cursor.fetchall()
                users = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    user = dict(zip(headers, row))
                    user.pop("password")
                    users.append(user)
                print(users)
            else:
                cursor.execute("SELECT * FROM users")
                rows = cursor.fetchall()
                users = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    user = dict(zip(headers, row))
                    user.pop("password")
                    users.append(user)
                print(users)
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
                return Response(json.dumps(users, default=str), mimetype="application/json", status=200)
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
            if rows == 1:
                user_id = cursor.lastrowid
                print(user_id)
                loginToken = create_token()
                print(loginToken)
                cursor.execute("INSERT INTO user_session(loginToken, user_id) VALUES(?, ?)", [loginToken, user_id])
                conn.commit()
                rows = cursor.rowcount

                cursor.execute("SELECT * FROM users WHERE id=?", [user_id])
                user_row = cursor.fetchone()
                user = {}
                headers = [i[0] for i in cursor.description]
                user = dict(zip(headers, user_row))
                user["loginToken"] = loginToken
                user.pop("password")
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
                user = {}
                headers = [i[0] for i in cursor.description]
                user = dict(zip(headers, user_row))
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
                return Response(json.dumps(user, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)

    elif request.method == 'DELETE':
        conn = None
        cursor = None
        rows = None
        token = request.json.get("token")
        password = request.json.get("password")
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_session INNER JOIN users ON user_session.user_id = users.id WHERE loginToken=? and password=?", [token, password])
            row= cursor.fetchone()
            user_id = row[2]
            cursor.execute("DELETE FROM users WHERE id=?", [user_id,])
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
                return Response("Delete account success!", mimetype="text/html", status=204)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)

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
            if user_row != None and user_row != []:
                user = {}
                headers = [i[0] for i in cursor.description]
                user = dict(zip(headers, user_row))
                user_id = user_row[0]
                print(user_id)
                loginToken = create_token()
                print(loginToken)
                cursor.execute("INSERT INTO user_session(loginToken, user_id) VALUES(?, ?)", [loginToken, user_id])
                conn.commit()
                rows = cursor.rowcount
                user["loginToken"] = loginToken
                user.pop("password")
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
                return Response("logout success!", mimetype="text/html", status=204)
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
                cursor.execute("SELECT * FROM tweet WHERE user_id=? ORDER BY created_at DESC", [user_id])
                rows = cursor.fetchall()
                tweets = []
                headers = [i[0] for i in cursor.description]
                cursor.execute("SELECT * FROM users WHERE id=?", [user_id])
                user_row = cursor.fetchone()
                username = user_row[1]
                print(username)
                for row in rows:
                    tweet = dict(zip(headers, row))
                    tweet["username"] = username
                    cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id=?", [tweet['id']])
                    like_amount = cursor.fetchone()[0]
                    print(like_amount)
                    tweet["like_amount"] = like_amount
                    tweets.append(tweet)
                print(tweets)
            else:
                cursor.execute("SELECT * FROM tweet INNER JOIN users ON tweet.user_id = users.id ORDER BY tweet.created_at DESC")
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
                    cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id=?", [tweet['id']])
                    like_amount = cursor.fetchone()[0]
                    print(like_amount)
                    tweet["like_amount"] = like_amount
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
                return Response(json.dumps(tweet, default=str), mimetype="application/json", status=200)
            else:
                return Response("Updated failed", mimetype="text/html", status=500)
    
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        token = request.json.get("token")
        tweet_id = request.json.get("id")
        print(tweet_id)
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
                cursor.execute("SELECT * FROM comment INNER JOIN tweet ON comment.tweet_id = tweet.id WHERE tweet_id=?", [tweet_id])
                rows = cursor.fetchall()
                print(rows)
                comments = []
                for i in range(len(rows)):
                    comment={
                        "id": rows[i][0],
                        "content": rows[i][1],
                        "created_at": rows[i][2],
                        "user_id": rows[i][3],
                        "tweet_id": rows[i][4]
                    }
                    user_id = rows[i][3]
                    cursor.execute("SELECT * FROM users WHERE id=?", [user_id])
                    user_row = cursor.fetchone()
                    username = user_row[1]
                    comment["username"] = username
                    print(comment)
                    cursor.execute("SELECT COUNT(*) FROM comment_like WHERE comment_id=?", [comment['id']])
                    like_amount = cursor.fetchone()[0]
                    print(like_amount)
                    comment["like_amount"] = like_amount
                    comments.append(comment)
                print(comments)
            else:
                cursor.execute("SELECT * FROM comment INNER JOIN users ON comment.user_id = users.id")
                rows = cursor.fetchall()
                comments = []
                for i in range(len(rows)):
                    comment={
                        "id": rows[i][0],
                        "content": rows[i][1],
                        "created_at": rows[i][2],
                        "user_id": rows[i][3],
                        "tweet_id": rows[i][4],
                        "username": rows[i][6]
                    }
                    print(comment)
                    comments.append(comment)
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

@app.route('/tweet-likes', methods=['GET', 'POST', 'DELETE'])
def tweet_likes():
    if request.method == 'GET':
        conn = None
        cursor = None
        tweet_likes = None
        tweet_id = request.args.get("tweet_id")
        print(tweet_id)
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if tweet_id != None and tweet_id != "":
                cursor.execute("SELECT * FROM tweet_like INNER JOIN users ON tweet_like.user_id = users.id WHERE tweet_id=?", [tweet_id])
                rows = cursor.fetchall()
                tweet_likes = []
                for row in rows:
                    tweet_like = {
                        "tweet_id": row[1],
                        "user_id": row[2],
                        "username": row[4]
                    }
                    print(tweet_like)
                    tweet_likes.append(tweet_like)

            else:
                cursor.execute("SELECT * FROM tweet_like INNER JOIN users ON tweet_like.user_id = users.id")
                rows = cursor.fetchall()
                tweet_likes = []
                for i in range(len(rows)):
                    tweet_like={
                        "tweet_id": rows[i][1],
                        "user_id": rows[i][2],
                        "username": rows[i][4]
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
        print(tweet_id)
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
                return Response("Deleted success!", mimetype="text/html", status=204)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)

@app.route('/comment-likes', methods=['GET', 'POST', 'DELETE'])
def comment_likes():
    if request.method == 'GET':
        conn = None
        cursor = None
        comment_likes = None
        comment_id = request.args.get("comment_id")
        print(comment_id)
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if comment_id != None and comment_id != "":
                cursor.execute("SELECT * FROM comment_like WHERE comment_id=?", [comment_id])
                rows = cursor.fetchall()
                comment_likes = []
                for row in rows:
                    user_id = row[2]
                    print(user_id)
                    cursor.execute("SELECT * FROM users WHERE id=?", [user_id])
                    user_row = cursor.fetchone()
                    username = user_row[1]
                    comment_like = {
                        "comment_id": comment_id,
                        "user_id": user_id,
                        "username": username
                    }
                    print(comment_like)
                    comment_likes.append(comment_like)
            else:
                cursor.execute("SELECT * FROM comment_like INNER JOIN users ON comment_like.user_id = users.id")
                rows = cursor.fetchall()
                comment_likes = []
                for i in range(len(rows)):
                    comment_like={
                        "comment_id": rows[i][1],
                        "user_id": rows[i][2],
                        "username": rows[i][4]
                    }
                    print(comment_like)
                    comment_likes.append(comment_like)
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
            if(comment_likes != None):
                return Response(json.dumps(comment_likes, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'POST':
        conn = None
        cursor = None
        token = request.json.get("token")
        comment_id = request.json.get("comment_id")
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
                cursor.execute("INSERT INTO comment_like(comment_id, user_id) VALUES(?, ?)", [comment_id, user_id])
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
        comment_id = request.json.get("comment_id")
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
                cursor.execute("DELETE FROM comment_like WHERE comment_id=? AND user_id=?", [comment_id, user_id])
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
                return Response("Deleted success!", mimetype="text/html", status=204)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)

@app.route('/follows', methods=['GET', 'POST', 'DELETE'])
def follows():
    if request.method == 'GET':
        conn = None
        cursor = None
        user_id = request.args.get("user_id")
        print(user_id)
        follows = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if user_id != None and user_id != "":
                cursor.execute("SELECT * FROM follow INNER JOIN users ON follow.follow_id = users.id WHERE user_id=?", [user_id])
                rows = cursor.fetchall()
                print(rows)
                follows = []
                for i in range(len(rows)):
                    follow={
                        "follow_id": rows[i][2],
                        "username": rows[i][4],
                        "birthdate": rows[i][6],
                        "bio": rows[i][7],
                        "email": rows[i][8],
                        "image": rows[i][9],
                        "created_at": rows[i][10]
                    }
                    print(follow)
                    follows.append(follow)          
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
                return Response(json.dumps(follows, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)

    elif request.method == 'POST':
        conn = None
        cursor = None
        follow_id = request.json.get("follow_id")
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
                cursor.execute("INSERT INTO follow(user_id, follow_id) VALUES(?, ?)", [user_id, follow_id])
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
                return Response("Follow success!", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)

    elif request.method == 'DELETE':
        conn = None
        cursor = None
        token = request.json.get("token")
        follow_id = request.json.get("follow_id")
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
                cursor.execute("DELETE FROM follow WHERE user_id=? AND follow_id=?", [user_id, follow_id])
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
                return Response("Deleted success!", mimetype="text/html", status=204)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)

@app.route('/followers', methods=['GET'])
def followers():
    if request.method == 'GET':
        conn = None
        cursor = None
        follow_id = request.args.get("follow_id")
        print(follow_id)
        followers = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if follow_id != None and follow_id != "":
                cursor.execute("SELECT * FROM follow INNER JOIN users ON follow.user_id = users.id WHERE follow_id=?", [follow_id])
                rows = cursor.fetchall()
                print(rows)
                followers = []
                for i in range(len(rows)):
                    follower={
                        "user_id": rows[i][1],
                        "username": rows[i][4],
                        "birthdate": rows[i][6],
                        "bio": rows[i][7],
                        "email": rows[i][8],
                        "image": rows[i][9],
                        "created_at": rows[i][10]
                    }
                    print(follower)
                    followers.append(follower)
                    
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
                return Response(json.dumps(followers, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
            

    

        
        


