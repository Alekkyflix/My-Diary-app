<<<<<<< HEAD
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)  # Corrected from 'name' to '__name__'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(200))
    user = db.relationship('User', backref='entries')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    entries = DiaryEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', entries=entries)

@app.route('/add_entry', methods=['GET', 'POST'])
@login_required
def add_entry():
    if request.method == 'POST':
        content = request.form['content']
        media_file = request.files.get('media')
        
        media_url = None
        if media_file:
            media_filename = secure_filename(media_file.filename)
            media_file.save(os.path.join(app.config['UPLOAD_FOLDER'], media_filename))
            media_url = f"{request.host_url}{app.config['UPLOAD_FOLDER']}{media_filename}"
        
        # Only create a new entry if content is provided
        if content:
            new_entry = DiaryEntry(user_id=current_user.id, content=content, media_url=media_url)
            db.session.add(new_entry)
            db.session.commit()
            flash('Entry added successfully!', 'success')
            return redirect(url_for('dashboard'))

    return render_template('add_entry.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':  # Corrected from 'name' to '__name__'
    if not os.path.exists('diary.db'):
        db.create_all()
    app.run(debug=True)
=======
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
import calendar


app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store diary entries in memory (this could be replaced with a database)
diary_entries = []
start_date = None  # To track when the user started using the app

@app.route('/')
def index():
    global start_date
    # Set start date only if it's None
    if start_date is None and diary_entries:
        start_date = diary_entries[0]['date']  # Set start date to the date of the first entry
    return render_template('index.html', entries=diary_entries, start_date=start_date)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    global start_date
    text = request.form.get('diaryEntry')
    files = request.files.getlist('mediaInput')

    # Create a new entry
    entry_date = datetime.now().date()
    entry = {'text': text, 'media': [], 'date': entry_date}

    # Save uploaded files
    for file in files:
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            entry['media'].append(file.filename)

    diary_entries.append(entry)

    # Set start date if it's the first entry
    if start_date is None:
        start_date = entry_date  # Corrected line 25: Set to current date when adding the first entry

    return redirect(url_for('index'))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit file size to 16 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

@app.route('/delete_entry/<int:index>', methods=['POST'])
def delete_entry(index):
    if 0 <= index < len(diary_entries):
        entry = diary_entries[index]
        # Delete media files
        for media_file in entry['media']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], media_file)
            if os.path.exists(file_path):
                os.remove(file_path)
        del diary_entries[index]
        
        # Reset start date if all entries are deleted
        if not diary_entries:
            global start_date
            start_date = None
    return redirect(url_for('index'))
def get_marked_dates():
    """ Returns a list of dates that have diary entries. """
    return [entry['date'] for entry in diary_entries]

@app.context_processor
def inject_calendar():
    today = datetime.now().date()
    marked_dates = get_marked_dates()
    return dict(today=today, marked_dates=marked_dates)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
import calendar


app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


diary_entries = []
start_date = None  # To track when the user started using the app

@app.route('/')
def index():
    global start_date
    # Set start date only if it's None
    if start_date is None and diary_entries:
        start_date = diary_entries[0]['date']  # Set start date to the date of the first entry
    
    return render_template('index.html', entries=diary_entries, start_date=start_date)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    global start_date
     # Set start date if it's the first entry
    if start_date is None:
        start_date = entry_date  # Corrected line 25: Set to current date when adding the first entry
    text = request.form.get('diaryEntry')
    files = request.files.getlist('mediaInput')

    # Create a new entry
    entry_date = datetime.now().date()
    entry = {'text': text, 'media': [], 'date': entry_date}

    # Save uploaded files
    for file in files:
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            entry['media'].append(file.filename)

    diary_entries.append(entry)

    return redirect(url_for('index'))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit file size to 16 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

@app.route('/delete_entry/<int:index>', methods=['POST'])
def delete_entry(index):
    if 0 <= index < len(diary_entries):
        entry = diary_entries[index]
        # Delete media files
        for media_file in entry['media']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], media_file)
            if os.path.exists(file_path):
                os.remove(file_path)
        del diary_entries[index]
        
        # Reset start date if all entries are deleted
        if not diary_entries:
            global start_date
            start_date = None
    return redirect(url_for('index'))
def get_marked_dates():
    """ Returns a list of dates that have diary entries. """
    return [entry['date'] for entry in diary_entries]

@app.context_processor
def inject_calendar():
    today = datetime.now().date()
    marked_dates = get_marked_dates()
    return dict(today=today, marked_dates=marked_dates)

if __name__ == '__main__':
    app.run()
>>>>>>> 1655929969d0efccd414235ac451922ac71da4e1
