from flask import Flask, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename

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
    if not request.is_json:
        return jsonify({'status':'error', 'message':'Missing JSON body'}), 400
    data = request.get_json()
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'status':'error', 'message':'Name required'}), 400
    user = next((u for u in users.values() if u['name'].lower() == name.lower()), None)
    if user:
        session['user_id'] = user['id']
        return jsonify({'status':'success', 'user': user})
    if any(u['name'].lower() == name.lower() for u in users.values()):
        return jsonify({'status':'error', 'message':'Username already exists'}), 400
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
@app.route('/books')
def list_books():
    if 'user_id' not in session:
        return jsonify({'status':'error', 'message':'Login required'}), 401
    return jsonify({'books': list(books.values())})


