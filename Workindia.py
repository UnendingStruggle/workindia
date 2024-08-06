from flask_api_key import api_key_required
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from databaseManagement import DB, DBparam
import hashlib
from flask_api_key import APIKeyManager
from datetime import datetime
import json
from constants import PASSWORD_SALT, FLASK_SECRET_KEY
import secrets
app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
SECRET_KEY = b'rvJKxe6D7ozSPIOLpYH-aIlD13-9Vi-yqMmiVO0TzCc='
cipher = Fernet(SECRET_KEY)
my_key_manager = APIKeyManager(app)
app.config['API_KEY_SECRET'] = 'your_secret_key'


def generate_api_key():
    return secrets.token_hex(32)


@app.route('/api/signup', methods=['GET', 'POST'])
def register():
    db = DB()
    if request.method == 'GET':
        if len(db.query(r"select * from Users ")) > 0:
            return jsonify(db.query(r"select * from Users")), 200
        else:
            return jsonify('Nothing Found'), 404
    if request.method == 'POST':
        new_username = request.json.get('username')
        new_password = request.json.get('password') + PASSWORD_SALT
        new_email = request.json.get('email')
        user = {
            'username': new_username,
            'password': hashlib.md5(new_password.encode()).hexdigest(),
            'email': new_email
        }
        db.query(r"Insert into Users(Username,password,email) values('%s','%s','%s')" %
                 (user['username'], user['password'], user['email']))
        user_data = db.query(
            r"Select * from Users where Username='%s'" % (user['username']))
        response = {
            'status': 'Account successfully created',
            'status_code': 200,
            'user_id': user_data[0][0]
        }
        return jsonify(response), 200


@ app.route('/api/login', methods=['GET', 'POST'])
def login():
    db = DB()
    if request.method == 'GET':
        if len(db.query(r"select * from Users ")) > 0:
            return jsonify(db.query(r"select * from Users")), 200
        else:
            'Nothing Found', 404
    if request.method == 'POST':
        new_username = request.json.get('username')
        new_password = request.json.get('password')+PASSWORD_SALT
        user = {
            'username': new_username,
            'password': hashlib.md5(new_password.encode()).hexdigest()
        }
        users = db.query(r"select * from Users")
        for acc in users:
            if user['username'] == acc[1] and user['password'] == acc[2]:
                api_key = generate_api_key()
                app.config['API_KEY_SECRET'] = api_key
                return jsonify({'status': 'Login Successful', 'status_code': 200, 'user_id': acc[0], 'access_token': api_key})
        response = {
            'status': 'Incorrect Username/password provided. Please retry',
            'status_code': 401
        }
        return jsonify(response), 401


@ app.route('/api/shorts/create', methods=['GET', 'POST'])
def shorts():
    db = DB()
    if request.method == 'POST':
        category = request.json.get('category')
        title = request.json.get('title')
        author = request.json.get('author')
        publish_date_str = request.json.get('publish_date')
        publish_date = datetime.strptime(
            publish_date_str, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')
        content = request.json.get('content')
        actual_content_link = request.json.get('actual_content_link')
        print(actual_content_link)
        image = request.json.get('image')
        votes = request.json.get('votes')
        db.query(r"insert into Shorts(category, title, author, publish_date, content, actual_content_link, image, upvote, downvote) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %
                 (category, title, author, publish_date, content, actual_content_link, image, votes['upvote'], votes['downvote']))
        short = db.query(
            r"Select * from Shorts where actual_content_link='%s'" % (actual_content_link))
        response = {
            'status': 'Short added Successfully',
            'short_id': short[0][0],
            'status_code': 200
        }
        return jsonify(response), 200


@app.route('/api/shorts/feed', methods=['GET', 'POST'])
def feed():
    db = DB()
    if request.method == 'GET':
        shorts = db.query(
            r"select * from Shorts ORDER BY publish_date DESC, upvote DESC;")
        short_list = []
        for short in shorts:
            short_dict = {
                "short_id": short[0],
                "category": short[1],
                "title": short[2],
                "author": short[3],
                "publish_date": short[4].strftime('%Y-%m-%dT%H:%M:%SZ'),
                "content": short[5],
                "actual_content_link": short[6],
                "image": short[7],
                "votes": {
                    "upvote": short[8],
                    "downvote": short[9]
                }
            }
            short_list.append(short_dict)
        return jsonify(short_list), 200


@app.route('/api/shorts/filter', methods=['GET', 'POST'])
def filter_shorts():
    db = DBparam()
    if request.method == 'GET':
        api_key = request.headers.get('Authorization')
        if api_key != app.config['API_KEY_SECRET']:
            return jsonify({"error": "Unauthorized"}), 401
        filters = request.args.get('filter', {})
        searches = request.args.get('search', {})
        filters = json.loads(filters)
        searches = json.loads(searches)
        query = "SELECT * FROM Shorts WHERE 1=1"
        if 'category' in filters:
            query += " AND category = %s"
        if 'publish_date' in filters:
            query += " AND publish_date >= %s"
        if 'upvote' in filters:
            query += " AND upvote >= %s"
        if 'title' in searches:
            query += " AND title LIKE %s"
        if 'keyword' in searches:
            query += " AND (title LIKE %s OR content LIKE %s)"
        if 'author' in searches:
            query += " AND author LIKE %s"
        params = []
        if 'category' in filters:
            params.append(filters['category'])
        if 'publish_date' in filters:
            publish_date = datetime.strptime(
                filters['publish_date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')
            params.append(publish_date)
        if 'upvote' in filters:
            params.append(filters['upvote'])
        if 'title' in searches:
            params.append(f"%{searches['title']}%")
        if 'keyword' in searches:
            keyword = f"%{searches['keyword']}%"
            params.append(keyword)
            params.append(keyword)
        if 'author' in searches:
            params.append(f"%{searches['author']}%")
        shorts = db.query(query, params)
        result = []
        for short in shorts:
            contains_title = 'title' in searches and searches['title'].lower(
            ) in short['title'].lower()
            contains_content = 'keyword' in searches and searches['keyword'].lower(
            ) in short['content'].lower()
            contains_author = 'author' in searches and searches['author'].lower(
            ) in short['author'].lower()
            short.update({
                "contains_title": contains_title,
                "contains_content": contains_content,
                "contains_author": contains_author
            })
            result.append(short)
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"status": "No short matches your search criteria", "status_code": 400}), 400


if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
