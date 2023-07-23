from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import shutil

app = Flask(__name__)

# The list of file extensions is chosen based on common malicious file types.
# This list can be modified to fit the specific security needs of the application.
suspicious_file_types = ['.exe', '.com', '.bat', '.cmd', '.scr', '.msi', '.pif', '.gadget',
                         '.js', '.jse', '.vb', '.vbe', '.ws', '.wsf', '.wsc', '.wsh', '.ps1', '.ps1xml', '.ps2', '.ps2xml', 
                         '.psc1', '.psc2', '.msh', '.msh1', '.msh2', '.mshxml', '.msh1xml', '.msh2xml', '.scf', '.lnk', '.inf', '.reg',
                         '.docm', '.xlsm', '.pptm', '.dotm', '.xltm', '.potm', '.sldm', '.ppam', '.ppsm', '.sldm', 
                         '.accde', '.ade', '.adp', '.accdc', '.adn', '.accdr', '.accdu', '.ashx', '.aspx', '.asp', 
                         '.cer', '.crt', '.crl', '.der', '.asx', '.wax', '.m3u', '.wvx', '.wmx',
                         '.website', '.mcf', '.library-ms', '.lnk', '.settings', '.pif', '.ins', '.isp', '.url',
                         '.gadget', '.msp', '.cpl', '.msc', '.jar', '.cmd', '.bat', '.vbs', '.vbe', '.jse', '.ws', 
                         '.wsf', '.wsc', '.wsh', '.ps1', '.ps1xml', '.ps2', '.ps2xml', '.psc1', '.psc2', 
                         '.msh', '.msh1', '.msh2', '.mshxml', '.msh1xml', '.msh2xml']

@app.route('/')
def upload_file():
    # The upload form is rendered as the main page for simplicity.
    return render_template('upload.html')

@app.route('/upload', methods = ['GET', 'POST'])
def upload_files():
    # File upload is handled in a separate route to separate concerns and improve code readability.
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        for file in files:
            # Each file is processed individually to allow for more granular error handling.
            UploadAgent(file)
        # After all files are processed, the user is redirected to the view page.
        return redirect(url_for('view_files'))
    else:
        return 'No file uploaded!'

@app.route('/view', methods = ['GET'])
def view_files():
    # The view route is separate from the upload route to adhere to the Single Responsibility Principle.
    safe_files = os.listdir('safe') if os.path.exists('safe') else []
    suspicious_files = os.listdir('suspicious') if os.path.exists('suspicious') else []
    return render_template('view.html', safe_files=safe_files, suspicious_files=suspicious_files)

def UploadAgent(file):
    # Files are saved in a separate 'uploads' directory to keep the application directory clean.
    filename = secure_filename(file.filename)
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    file.save(os.path.join('uploads', filename))
    # After saving, each file is immediately classified to provide quick feedback to the user.
    ClassifierAgent(filename)

def ClassifierAgent(filename):
    # Classification is based on file extension, which is a simple but effective method for this use case.
    # If the file extension is in the list of suspicious file types, it is classified as suspicious.
    # Otherwise, it is classified as safe.
    if any(filename.endswith(ft) for ft in suspicious_file_types):
        MoveFileAgent(filename, 'suspicious')
    else:
        MoveFileAgent(filename, 'safe')
    
def MoveFileAgent(filename, classification):
    # Files are moved to their respective directories immediately after classification to avoid reclassification.
    # This also helps in organizing the files based on their classification.
    if not os.path.exists(classification):
        os.makedirs(classification)
    shutil.move(os.path.join('uploads', filename), os.path.join(classification, filename))

if __name__ == '__main__':
    # The application is run in debug mode by default for easier development.
    # Debug mode provides more detailed error messages and enables the reloader for easier debugging.
    app.run(debug = True)
