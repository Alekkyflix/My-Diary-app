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
