from flask import Flask, render_template, request, redirect, url_for
import os
app = Flask(__name__)


#folder to store uploaded files
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#ensure uploaded folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#Store diary entries in a memory 
diary_entries = []

@app.route('/')
def index():
    return render_template('index.html', entries = diary_entries)

@app.route('/add_entry', methods = ['POST'])
def add_entry():
    text = request.form.get['diaryEntry']
    files = request.files.getlist('mediaInput')

    #create new entry
    entry = {'text':text, 'media':[]}
    
    #Save uploaded files
    for file in files:
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            entry['Media'].append(file.filename)

    diary_entries.append(entry)
    return redirect(url_for('index'))


@app.route('/delete_entry/<int:index>', methods = ['POST'])
def delete_entry(index):
    if 0<=index<len(diary_entries):
        del diary_entries[index]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)