import os

from flask import Flask, request, jsonify, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS


from routes.items import items_bp
from routes.search import search_bp
from routes.scrape import scrape_bp
from routes.statistics import statistics_bp
from routes.websites import websites_bp
from routes.history import history_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(items_bp)
app.register_blueprint(search_bp)
app.register_blueprint(scrape_bp)
app.register_blueprint(statistics_bp)
app.register_blueprint(websites_bp)
app.register_blueprint(history_bp)


# Configures a folder where uploaded files will be saved.
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Creates the uploads folder automatically if it doesn't exist yet.
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Checks if the post request actually has the file part.
        if "file_input" not in request.files:
            return "No file selected", 400
            
        file = request.files["file_input"]
        
        # If the user submits without selecting a file.
        if file.filename == "":
            return "No file selected", 400
            
        if file:
            # secure_filename cleans up the file name (e.g., converts "../../hacked.exe" to "hacked.exe").
            filename = secure_filename(file.filename)
            
            # Combines the upload folder path with the safe filename.
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            
            # Saves the file to your hard drive.
            file.save(save_path)
            
            return f"<h1>File successfully uploaded!</h1><p>Saved to: {save_path}</p><a href='/upload'>Upload another</a>"

    # If it's a GET request, display the upload form.
    return """
        <!doctype html>
        <title>Upload a File</title>
        <h1>Upload New File</h1>
        <form method="POST" enctype="multipart/form-data">
          <input type="file" name="file_input" required>
          <button type="submit">Upload</button>
        </form>
    """

# Checks that the server is running.
@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "message": "Team Charlie API is running!"  
    }), 200

# ------------------------------------------------------------------------
# STATUS CODE & ERROR SAMPLES 
# ------------------------------------------------------------------------

@app.route("/dashboard")
def dashboard():
    # Simulating a scenario where a user tries to access the dashboard 
    # but isn't logged in yet. We trigger a '401 Unauthorized' status code.
    user_logged_in = False 
    
    if not user_logged_in:
        abort(401) # This instantly stops execution and sends a 401 status code
        
    return "<h1>Welcome to the Dashboard</h1>"


# ------------------------------------------------------------------------
# CUSTOM ERROR PAGES 
# ------------------------------------------------------------------------

@app.errorhandler(401)
def unauthorized_error(error):
    return "<h1>401: Access Denied</h1><p>Please log in first before viewing the dashboard.</p>", 401


@app.errorhandler(404)
def not_found_error(error):
    # Handles typing mistakes in the URL bar smoothly
    return "<h1>404: Page Not Found</h1><p>Team Charlie hasn't built this page yet!</p>", 404

if __name__ == "__main__":
    app.run(debug=True) 