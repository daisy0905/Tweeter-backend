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

@app.route('/api/users', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def users():
    if request.method == 'GET':
        conn = None
        cursor = None
        user_id = request.args.get("id")
        # print(user_id)
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
                # print(users)
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
            # print(rows)
            if rows == 1:
                user_id = cursor.lastrowid
                print(user_id)
                loginToken = create_token()
                # print(loginToken)
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
            # print(user)
            if user != None and user != []:
                user_id = user[2]
                # print(user_id)
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

#################### Users ######################## Users ############################# Users #################

@app.route('/api/login', methods=['POST', 'DELETE'])
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
                # print(user_id)
                loginToken = create_token()
                # print(loginToken)
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

#################### Login ######################## Login ############################# Login #################

####Added "search" feature: changed SQL statement using LIKE for GET api requests
####Added "Tweet using an uploaded photo" feature: changed SQL statement for GET, POST and PATCH api requests
@app.route('/api/tweets', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def tweets():
    if request.method == 'GET':
        conn = None
        cursor = None
        tweets = None
        content = request.args.get("content")
        user_id = request.args.get("id")
        print(user_id)
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if user_id != None and user_id != "":
                cursor.execute("SELECT tweet.id, tweet.content, tweet.image, tweet.created_at, tweet.user_id, users.username FROM tweet INNER JOIN users ON tweet.user_id = users.id WHERE user_id=? ORDER BY tweet.created_at DESC", [user_id,])
                rows = cursor.fetchall()
                tweets = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    tweet = dict(zip(headers, row))
                    cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id=?", [tweet['id']])
                    like_amount = cursor.fetchone()[0]
                    print(like_amount)
                    tweet["like_amount"] = like_amount
                    tweets.append(tweet)
                print(tweets)
            elif content != None and content != "":
                cursor.execute("SELECT tweet.id, tweet.content, tweet.image, tweet.created_at, tweet.user_id, users.username FROM tweet INNER JOIN users ON tweet.user_id = users.id WHERE username LIKE ? OR email LIKE ? OR content LIKE ? ORDER BY tweet.created_at DESC", [user_id, "%{}%".format(content), "%{}%".format(content), "%{}%".format(content)])
                rows = cursor.fetchall()
                tweets = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    tweet = dict(zip(headers, row))
                    cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id=?", [tweet['id']])
                    like_amount = cursor.fetchone()[0]
                    print(like_amount)
                    tweet["like_amount"] = like_amount
                    tweets.append(tweet)
                # print(tweets)
            elif user_id == None or user_id == "" and content == None or content == "":
                cursor.execute("SELECT tweet.id, tweet.content, tweet.image, tweet.created_at, tweet.user_id, users.username FROM tweet INNER JOIN users ON tweet.user_id = users.id ORDER BY tweet.created_at DESC")
                rows = cursor.fetchall()
                tweets = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    tweet = dict(zip(headers, row))
                    cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id=?", [tweet['id']])
                    like_amount = cursor.fetchone()[0]
                    print(like_amount)
                    tweet["like_amount"] = like_amount
                    tweets.append(tweet)
                # print(tweets)
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
        tweet_image = request.json.get("image")
        token = request.json.get("token")
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
                cursor.execute("INSERT INTO tweet(content, image, user_id) VALUES(?, ?, ?)", [tweet_content, tweet_image, user_id])
                conn.commit()
                rows = cursor.rowcount
                if rows == 1:
                    tweet_id = cursor.lastrowid
                    print(tweet_id)
                    cursor.execute("SELECT * FROM tweet INNER JOIN users ON tweet.user_id = users.id WHERE tweet.id=?", [tweet_id])
                    row = cursor.fetchone()
                    print(row)
                    tweet = {
                        "id": row[0],
                        "content": row[1],
                        "image": row[4],
                        "created_at": row[2],
                        "user_id": row[3],
                        "username": row[6]
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
        tweet_image = request.json.get("image")
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
                if tweet_image != "" and tweet_image != None:
                    cursor.execute("UPDATE tweet SET image=? WHERE id=? AND user_id=?", [tweet_image, tweet_id, user_id])
                conn.commit()
                rows = cursor.rowcount
                print(rows)
                cursor.execute("SELECT * FROM tweet WHERE id=? AND user_id=?", [tweet_id, user_id])
                tweet_row = cursor.fetchone()
                print(tweet_row)
                tweet={
                    "id": tweet_row[0],
                    "content": tweet_row[1],
                    "image": tweet_row[4]
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
            # print(user)
            if user != None and user != []:
                user_id = user[2]
                # print(user_id) 
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

#################### Tweets ######################## Tweets ############################# Tweets #################

####Added "Comment using an uploaded photo" feature: changed SQL statement for GET, POST and PATCH api requests
@app.route('/api/comments', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def comments():
    if request.method == 'GET':
        conn = None
        cursor = None
        comments = None
        tweet_id = request.args.get("tweet_id")
        # print(tweet_id)
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if tweet_id != None and tweet_id != "":
                cursor.execute("SELECT comment.id, comment.content, comment.image, comment.created_at, comment.user_id, comment.tweet_id, users.username FROM comment INNER JOIN tweet ON comment.tweet_id = tweet.id INNER JOIN users ON comment.user_id = users.id WHERE tweet_id=? ORDER BY comment.created_at DESC", [tweet_id])
                rows = cursor.fetchall()
                # print(rows)
                comments = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    comment = dict(zip(headers, row))
                    print(comment)
                    # print(comment)
                    cursor.execute("SELECT COUNT(*) FROM comment_like WHERE comment_id=?", [comment['id']])
                    like_amount = cursor.fetchone()[0]
                    # print(like_amount)
                    comment["like_amount"] = like_amount
                    comments.append(comment)
                    print(comments)
            else:
                cursor.execute("SELECT comment.id, comment.content, comment.image, comment.created_at, comment.user_id, comment.tweet_id, users.username FROM comment INNER JOIN users ON comment.user_id = users.id ORDER BY comment.created_at DESC")
                rows = cursor.fetchall()
                comments = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    comment = dict(zip(headers, row))
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
        comment_image = request.json.get("image")
        user = None
        rows = None
        comment = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_session WHERE loginToken=?", [token,])
            user = cursor.fetchone()
            # print(user)
            if user != None and user != []:
                user_id = user[2]
                # print(user_id)
                cursor.execute("INSERT INTO comment(content, image, user_id, tweet_id) VALUES(?, ?, ?, ?)", [comment_content, comment_image, user_id, tweet_id])
                conn.commit()
                rows = cursor.rowcount
                if rows == 1:
                    comment_id = cursor.lastrowid
                    print(comment_id)
                    cursor.execute("SELECT comment.id, comment.content, comment.image, comment.created_at, comment.user_id, comment.tweet_id, users.username FROM comment INNER JOIN users ON comment.user_id = users.id WHERE comment.id=?", [comment_id])
                    row = cursor.fetchone()
                    print(row)
                    comment = {}
                    headers = [i[0] for i in cursor.description]
                    comment = dict(zip(headers, row))
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
        comment_image = request.json.get("image")
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
                if comment_image != "" and comment_image != None:
                    cursor.execute("UPDATE comment SET image=? WHERE id=? AND user_id=?", [comment_image, comment_id, user_id])
                conn.commit()
                rows = cursor.rowcount
                print(rows)
                cursor.execute("SELECT comment.id, comment.content, comment.image, comment.created_at, comment.user_id, comment.tweet_id, users.username FROM comment INNER JOIN users ON comment.user_id = users.id WHERE comment.id=?", [comment_id])
                comment_row = cursor.fetchone()
                print(comment_row)
                comment = {}
                headers = [i[0] for i in cursor.description]
                comment = dict(zip(headers, comment_row))
                print(comment)
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

#################### Comments ######################## Comments ############################# Comments #################

@app.route('/api/tweet-likes', methods=['GET', 'POST', 'DELETE'])
def tweet_likes():
    if request.method == 'GET':
        conn = None
        cursor = None
        tweet_likes = None
        tweet_id = request.args.get("tweet_id")
        # print(tweet_id)
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
            # print(user)
            if user != None and user != []:
                user_id = user[2]
                # print(user_id)
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
                # print(user_id)
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

#################### Tweet-likes ######################## Tweet-likes ############################# Tweet-likes #################

@app.route('/api/comment-likes', methods=['GET', 'POST', 'DELETE'])
def comment_likes():
    if request.method == 'GET':
        conn = None
        cursor = None
        comment_likes = None
        comment_id = request.args.get("comment_id")
        # print(comment_id)
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if comment_id != None and comment_id != "":
                cursor.execute("SELECT * FROM comment_like WHERE comment_id=?", [comment_id])
                rows = cursor.fetchall()
                comment_likes = []
                for row in rows:
                    user_id = row[2]
                    # print(user_id)
                    cursor.execute("SELECT * FROM users WHERE id=?", [user_id])
                    user_row = cursor.fetchone()
                    username = user_row[1]
                    comment_like = {
                        "comment_id": comment_id,
                        "user_id": user_id,
                        "username": username
                    }
                    # print(comment_like)
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
            # print(user)
            if user != None and user != []:
                user_id = user[2]
                # print(user_id)
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

#################### Comment-likes ######################## Comment-likes ############################# Comment-likes #################

@app.route('/api/follows', methods=['GET', 'POST', 'DELETE'])
def follows():
    if request.method == 'GET':
        conn = None
        cursor = None
        user_id = request.args.get("user_id")
        # print(user_id)
        follows = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if user_id != None and user_id != "":
                cursor.execute("SELECT * FROM follow INNER JOIN users ON follow.follow_id = users.id WHERE user_id=?", [user_id])
                rows = cursor.fetchall()
                # print(rows)
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
            # print(user)
            if user != None and user != []:
                user_id = user[2]
                # print(user_id)
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
            # print(user)
            if user != None and user != []:
                user_id = user[2]
                # print(user_id)
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

#################### Follow ######################## Follow ############################# Follow #################

@app.route('/api/followers', methods=['GET'])
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

#################### Follower ######################## Follower ############################# Follower #################

@app.route('/api/nested-comments', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def nested_comments():
    if request.method == 'GET':
        conn = None
        cursor = None
        nested_comments = None
        comment_id = request.args.get("comment_id")
        # print(comment_id)
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if comment_id != None and comment_id != "":
                cursor.execute("SELECT nested_comment.id, nested_comment.content, nested_comment.created_at, nested_comment.comment_id, nested_comment.user_id, users.username FROM nested_comment INNER JOIN users ON nested_comment.user_id = users.id WHERE comment_id=? ORDER BY nested_comment.created_at DESC", [comment_id])
                rows = cursor.fetchall()
                print(rows)
                nested_comments = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    nested_comment = dict(zip(headers, row))
                    # print(nested_comment)
                    nested_comments.append(nested_comment)
                print(nested_comments)
            else:
                cursor.execute("SELECT nested_comment.id, nested_comment.content, nested_comment.created_at, nested_comment.comment_id, nested_comment.user_id, users.username FROM nested_comment INNER JOIN users ON nested_comment.user_id = users.id ORDER BY nested_comment.created_at DESC")
                rows = cursor.fetchall()
                nested_comments = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    nested_comment = dict(zip(headers, row))
                    # print(nested_comment)
                    nested_comments.append(nested_comment)
                print(nested_comments)
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
            if(nested_comments != None):
                return Response(json.dumps(nested_comments, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)

    elif request.method == 'POST':
        conn = None
        cursor = None
        token = request.json.get("token")
        comment_id = request.json.get("comment_id")
        nested_comment_content = request.json.get("content")
        nested_comment = None
        user = None
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_session WHERE loginToken=?", [token,])
            user = cursor.fetchone()
            # print(user)
            if user != None and user != []:
                user_id = user[2]
                # print(user_id)
                cursor.execute("INSERT INTO nested_comment(content, comment_id, user_id) VALUES(?, ?, ?)", [nested_comment_content, comment_id, user_id])
                conn.commit()
                rows = cursor.rowcount
                # print(rows)
                if rows == 1:
                    nested_comment_id = cursor.lastrowid
                    print(nested_comment_id)
                    cursor.execute("SELECT * FROM nested_comment INNER JOIN users ON nested_comment.user_id = users.id WHERE nested_comment.id=?", [nested_comment_id,])
                    row = cursor.fetchone()
                    # print(row)
                    nested_comment = {}
                    nested_comment = {
                        "id": row[0],
                        "content": row[1],
                        "created_at": row[2],
                        "comment_id": row[3],
                        "user_id": row[4],
                        "username": row[6]
                    }
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
                return Response(json.dumps(nested_comment, default=str), mimetype="application/json", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'PATCH':
        conn = None
        cursor = None
        token = request.json.get("token")
        nested_comment_id = request.json.get("id")
        nested_comment_content = request.json.get("content")
        nested_comment = None
        user = None
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor() 
            cursor.execute("SELECT * FROM user_session WHERE loginToken=?", [token,])
            user = cursor.fetchone()
            # print(user)
            if user != None and user != []:
                user_id = user[2]
                # print(user_id)
                if nested_comment_content != "" and nested_comment_content != None:
                    cursor.execute("UPDATE nested_comment SET content=? WHERE id=? AND user_id=?", [nested_comment_content, nested_comment_id, user_id])
                    conn.commit()
                    rows = cursor.rowcount
                # print(rows)
                cursor.execute("SELECT * FROM nested_comment INNER JOIN users ON nested_comment.user_id = users.id WHERE nested_comment.id=?", [nested_comment_id])
                row = cursor.fetchone()
                # print(row)
                nested_comment = {}
                nested_comment = {
                    "id": row[0],
                    "content": row[1],
                    "created_at": row[2],
                    "comment_id": row[3],
                    "user_id": row[4],
                    "username": row[6]
                }
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
                return Response(json.dumps(nested_comment, default=str), mimetype="application/json", status=200)
            else:
                return Response("Updated failed", mimetype="text/html", status=500)
    
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        token = request.json.get("token")
        nested_comment_id = request.json.get("id")
        rows = None
        user = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_session WHERE loginToken=?", [token,])
            user = cursor.fetchone()
            # print(user)
            if user != None and user != []:
                user_id = user[2]
                # print(user_id) 
                cursor.execute("DELETE FROM nested_comment WHERE id=? AND user_id=?", [nested_comment_id, user_id])
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

#################### Nested-comments ######################## Nested-comments ############################# Nested-comments #################

@app.route('/api/retweets', methods=['GET', 'POST', 'DELETE'])
def retweets():
    if request.method == 'GET':
        conn = None
        cursor = None
        retweets = None
        user_id = request.args.get("user_id")
        print(user_id)
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if user_id != None and user_id != "":
                cursor.execute("SELECT retweet.id, retweet.tweet_id, retweet.user_id, retweet.createdAt, tweet.content, tweet.image, tweet.created_at, users.id, users.username FROM retweet INNER JOIN tweet ON retweet.tweet_id = tweet.id INNER JOIN users ON tweet.user_id = users.id WHERE retweet.user_id=? ORDER BY retweet.createdAt DESC", [user_id])
                rows = cursor.fetchall()
                retweets = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    retweet = dict(zip(headers, row))
                    cursor.execute("SELECT username FROM users WHERE id=?", [user_id,])
                    user_row = cursor.fetchone()
                    name = user_row[0]
                    retweet["name"] = name
                    cursor.execute("SELECT COUNT(*) FROM retweet WHERE tweet_id=?", [retweet['tweet_id']])
                    retweet_amount = cursor.fetchone()[0]
                    retweet["retweet_amount"] = retweet_amount
                    retweets.append(retweet)
                print(retweets)
            else:
                cursor.execute("SELECT retweet.id, retweet.tweet_id, retweet.user_id, retweet.createdAt, tweet.content, tweet.image, tweet.created_at, users.id, users.username FROM retweet INNER JOIN tweet ON retweet.tweet_id = tweet.id INNER JOIN users ON tweet.user_id = users.id ORDER BY retweet.createdAt DESC")
                rows = cursor.fetchall()
                retweets = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    retweet = dict(zip(headers, row))
                    cursor.execute("SELECT username FROM users WHERE id=?", [retweet['user_id']])
                    user_row = cursor.fetchone()
                    name = user_row[0]
                    retweet["name"] = name
                    cursor.execute("SELECT COUNT(*) FROM retweet WHERE tweet_id=?", [retweet['tweet_id']])
                    retweet_amount = cursor.fetchone()[0]
                    retweet["retweet_amount"] = retweet_amount
                    retweets.append(retweet)
                print(retweets)
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
            if(retweets != None):
                return Response(json.dumps(retweets, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'POST':
        conn = None
        cursor = None
        tweet_id = request.json.get("tweet_id")
        token = request.json.get("token")
        user = None
        rows = None
        retweet = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_session WHERE loginToken=?", [token,])
            user = cursor.fetchone()
            # print(user)
            if user != None and user != []:
                user_id = user[2]
                # print(user_id)
                cursor.execute("INSERT INTO retweet(tweet_id, user_id) VALUES(?, ?)", [tweet_id, user_id])
                conn.commit()
                rows = cursor.rowcount
                # print(rows)
                cursor.execute("SELECT retweet.id, retweet.tweet_id, retweet.user_id, retweet.createdAt, tweet.content, tweet.image, tweet.created_at, tweet.user_id, users.username FROM retweet INNER JOIN tweet ON retweet.tweet_id = tweet.id INNER JOIN users ON tweet.user_id = users.id WHERE retweet.tweet_id=? AND retweet.user_id=?", [tweet_id, user_id])
                row = cursor.fetchone()
                # print(row)
                retweet = {}
                headers = [i[0] for i in cursor.description]
                retweet = dict(zip(headers, row))
                cursor.execute("SELECT username FROM users WHERE id=?", [retweet['user_id']])
                user_row = cursor.fetchone()
                name = user_row[0]
                retweet["name"] = name
                print(retweet)
                cursor.execute("SELECT COUNT(*) FROM retweet WHERE tweet_id=?", [retweet['tweet_id']])
                retweet_amount = cursor.fetchone()[0]
                retweet["retweet_amount"] = retweet_amount
                print(retweet)
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
                return Response(json.dumps(retweet, default=str), mimetype="application/json", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
       
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        token = request.json.get("token")
        tweet_id = request.json.get("tweet_id")
        # print(tweet_id)
        rows = None
        user = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_session WHERE loginToken=?", [token,])
            user = cursor.fetchone()
            # print(user)
            if user != None and user != []:
                user_id = user[2]
                # print(user_id) 
                cursor.execute("DELETE FROM retweet WHERE tweet_id=? AND user_id=?", [tweet_id, user_id])
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

#################### Retweets ######################## Retweets ############################# Retweets #################

    

        
        


