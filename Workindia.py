from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from databaseManagement import DB
import hashlib
from constants import PASSWORD_SALT, FLASK_SECRET_KEY
app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
SECRET_KEY = b'rvJKxe6D7ozSPIOLpYH-aIlD13-9Vi-yqMmiVO0TzCc='
cipher = Fernet(SECRET_KEY)


@app.route('//app/user', methods=['GET', 'POST'])
def register():
    db = DB()
    if request.method == 'GET':
        if len(db.query(r"select * from Users ")) > 0:
            return jsonify(db.query(r"select * from Users")), 200
        else:
            'Nothing Found', 404
    if request.method == 'POST':
        new_username = request.json.get('username')
        new_password = request.json.get('password') + PASSWORD_SALT
        user = {
            'username': new_username,
            'password': hashlib.md5(new_password.encode()).hexdigest(),
        }
        db.query(r"Insert into Users(Username,password) values('%s','%s')" %
                 (user['username'], user['password']))
        return jsonify({'status': 'account created'}), 201


@ app.route('/app/user/auth', methods=['GET', 'POST'])
def login():
    db = DB()
    if request.method == 'GET':
        if len(db.query(r"select * from Users " != 0) > 0):
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
                return jsonify({'status': 'success', 'id': acc[0]}), 200
        return jsonify({'status': 'unsuccessful'}), 500


@ app.route('/app/sites/list/', methods=['GET', 'POST'])
def notes():
    db = DB()
    if request.method == 'GET':
        userID = request.args.get('user', type=int)
        users = db.query(r"select * from Notes")
        for user in users:
            if user[0] == userID:
                notes = db.query(
                    r"select notes from Notes where note_id='%s'" % (userID))
                l = []
                for note in notes:
                    note = cipher.decrypt(note[0].encode())
                    l.append(note.decode())
                return jsonify(tuple(l)), 200
        return jsonify({'status': 'unsuccessful'}), 500
    if request.method == 'POST':
        userID = request.args.get('user', type=int)
        note = request.json.get('note')
        note = cipher.encrypt(note.encode())
        note = note.decode()
        if not note:
            return jsonify({"error": "No note provided"}), 400
        users = db.query(r"select * from Users")
        for user in users:
            if user[0] == userID:
                db.query(r"insert into Notes values(%d,'%s')" %
                         (userID, note))
                return jsonify({'status': 'success', 'id': user[0]}), 201


if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
