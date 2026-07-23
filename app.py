import os
from flask import Flask, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure a folder where uploaded files will be saved
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads folder automatically if it doesn't exist yet
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check if the post request actually has the file part
        if 'file_input' not in request.files:
            return "No file selected", 400
            
        file = request.files['file_input']
        
        # If the user submits without selecting a file
        if file.filename == '':
            return "No file selected", 400
            
        if file:
            # secure_filename cleans up the file name (e.g., converts "../../hacked.exe" to "hacked.exe")
            filename = secure_filename(file.filename)
            
            # Combine the upload folder path with the safe filename
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save the file to your hard drive
            file.save(save_path)
            
            return f"<h1>File successfully uploaded!</h1><p>Saved to: {save_path}</p><a href='/upload'>Upload another</a>"

    # If it's a GET request, display the upload form
    return """
        <!doctype html>
        <title>Upload a File</title>
        <h1>Upload New File</h1>
        <form method="POST" enctype="multipart/form-data">
          <input type="file" name="file_input" required>
          <button type="submit">Upload</button>
        </form>
    """

@app.route("/")
def home():
    return "<h1>Team Charlie's Flask Server is Live!</h1> <a href='/upload'>Go to File Uploader</a>"