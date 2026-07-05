
from flask import Flask, render_template, request, send_from_directory, redirect
from pathlib import Path
import random,string

app = Flask(__name__)
UPLOADS = Path('uploads')
UPLOADS.mkdir(exist_ok=True)
links = {}

def code():
    return ''.join(random.choices(string.ascii_uppercase+string.digits,k=6))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    f=request.files['file']
    c=code()
    name=f'{c}_{f.filename}'
    f.save(UPLOADS/name)
    links[c]=name
    return f'Share code: <b>{c}</b><br><a href="/download/{c}">Download link</a>'

@app.route('/download/<c>')
def download(c):
    if c not in links:
      return 'Code not found',404
    return send_from_directory(UPLOADS, links[c], as_attachment=True)
