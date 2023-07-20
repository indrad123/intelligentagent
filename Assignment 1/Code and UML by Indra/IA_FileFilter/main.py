from flask import Flask, render_template, request
import os
import shutil

app = Flask(__name__)

# Define the folder paths
upload_folder = "uploads"
destination_folder = "destination"

# Define the predefined file extensions to identify
predefined_extensions = [".txt", ".csv", ".xlsx"]


# Function to get a list of files in the upload folder
def get_file_list():
    file_list = os.listdir(upload_folder)
    return file_list


# Function to move files with predefined extensions to the destination folder
def move_files():
    file_list = get_file_list()
    for file in file_list:
        filename, extension = os.path.splitext(file)
        if extension in predefined_extensions:
            source_path = os.path.join(upload_folder, file)
            destination_path = os.path.join(destination_folder, file)
            shutil.move(source_path, destination_path)


# Route to display the list of files
def file_list():
    files = get_file_list()
    return render_template("file_list.html", files=files)


# Route to handle file upload
@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files["file"]
    if uploaded_file:
        file_path = os.path.join(upload_folder, uploaded_file.filename)
        uploaded_file.save(file_path)
        return "File uploaded successfully!"

# Route to move files with predefined extensions
@app.route("/move_files")
def move_files_route():
    move_files()
    return "Files moved successfully!"


if __name__ == "__main__":
    app.run(debug=True)
