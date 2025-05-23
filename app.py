from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'static/covers'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/covers/<filename>')
def cover_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
    from flask import request, jsonify, session

users = {}
books = {}
transactions = []

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'status':'error', 'message':'Name required'}), 400
    user = next((u for u in users.values() if u['name'].lower() == name.lower()), None)
    if not user:
        user_id = str(len(users) + 1)
        user = {'id': user_id, 'name': name}
        users[user_id] = user
    session['user_id'] = user['id']
    return jsonify({'status':'success', 'user': user})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'status':'success'})

@app.route('/session')
def check_session():
    user_id = session.get('user_id')
    if user_id and user_id in users:
        return jsonify({'logged_in':True, 'user':users[user_id]})
    return jsonify({'logged_in':False})
