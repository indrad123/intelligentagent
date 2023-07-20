from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import shutil

app = Flask(__name__)

suspicious_file_types = ['.exe', '.com', '.bat', '.cmd', '.scr', '.msi', '.pif', '.gadget',
                         '.js', '.jse', '.vb', '.vbe', '.ws', '.wsf', '.wsc', '.wsh', '.ps1', '.ps1xml', '.ps2', '.ps2xml', '.psc1', '.psc2', '.msh', '.msh1', '.msh2', '.mshxml', '.msh1xml', '.msh2xml', '.scf', '.lnk', '.inf', '.reg',
                         '.docm', '.xlsm', '.pptm', '.dotm', '.xltm', '.potm', '.sldm', '.ppam', '.ppsm', '.sldm', '.accde', '.ade', '.adp', '.accdc', '.adn', '.accdr', '.accdu', '.ashx', '.aspx', '.asp', '.cer', '.crt', '.crl', '.der', '.asx', '.wax', '.m3u', '.wvx', '.wmx',
                         '.website', '.mcf', '.library-ms', '.lnk', '.settings', '.pif', '.ins', '.isp', '.url',
                         '.gadget', '.msp', '.cpl', '.msc', '.jar', '.cmd', '.bat', '.vbs', '.vbe', '.jse', '.ws', '.wsf', '.wsc', '.wsh', '.ps1', '.ps1xml', '.ps2', '.ps2xml', '.psc1', '.psc2', '.msh', '.msh1', '.msh2', '.mshxml', '.msh1xml', '.msh2xml']

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods = ['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        for file in files:
            UploadAgent(file)
        return redirect(url_for('view_files'))
    else:
        return 'No file uploaded!'

@app.route('/view', methods = ['GET'])
def view_files():
    safe_files = os.listdir('safe') if os.path.exists('safe') else []
    suspicious_files = os.listdir('suspicious') if os.path.exists('suspicious') else []
    return render_template('view.html', safe_files=safe_files, suspicious_files=suspicious_files)

def UploadAgent(file):
    filename = secure_filename(file.filename)
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    file.save(os.path.join('uploads', filename))
    ClassifierAgent(filename)

def ClassifierAgent(filename):
    # Checking if file extension is in the list of suspicious file types
    if any(filename.endswith(ft) for ft in suspicious_file_types):
        MoveFileAgent(filename, 'suspicious')
    else:
        MoveFileAgent(filename, 'safe')
    
def MoveFileAgent(filename, classification):
    if not os.path.exists(classification):
        os.makedirs(classification)
    shutil.move(os.path.join('uploads', filename), os.path.join(classification, filename))

if __name__ == '__main__':
    app.run(debug = True)

