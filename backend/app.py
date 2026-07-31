import os
import json
import requests



from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS
from scrapers.bbc_scrapper import bbc_scraper
from scrapers.cnn_scraper import scrape_cnn
from scrapers.techcrunch_scraper import techcrunch_scraper
from scrapers.coindesk_scraper import coindesk_scraper


app = Flask(__name__)
CORS(app)

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

# ------------------------------------------------------------------------
# API ENDPOINTS
# ------------------------------------------------------------------------

# Checks that the server is running.
@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "message": "Team Charlie API is running!"  
    }), 200

# Loops through all available articles and returns
# only the article whose ID matches the one in the URL.
@app.route("/api/items/<int:item_id>", methods=["GET"])
def get_item(item_id):

    data_file = os.path.join(app.root_path, "data", "articles.json")

    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)
        for article in articles:
            if article["id"] == item_id:
                return jsonify(article), 200

        return jsonify({
            "error": "Article not found"
            }), 404

# Checks articles that match a search term provided by a user.
@app.route("/api/search", methods=["GET"])
def search_articles():

    search_term = request.args.get("q")

    # Checks that the user actually searched for something.
    if not search_term:
        return jsonify({
        "error": "Please provide a search term."
    }), 400

    data_file = os.path.join(app.root_path, "data", "articles.json")

    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)

    results = []

    for article in articles:
        if search_term.lower() in article["title"].lower():
            results.append(article)

    return jsonify(results), 200

@app.route("/api/items", methods=["GET"])
def get_items():
    data_file = os.path.join(app.root_path, "data", "articles.json")

    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)

    return jsonify(articles), 200

# Used to create a new article.
@app.route("/api/items", methods=["POST"])
def create_item():

    data_file = os.path.join(app.root_path, "data", "articles.json")
    payload = request.get_json(silent=True)

    # Checks that correct fields are filled before creating a new article.
    if payload is None:
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

    required_fields = ["title", "author", "source", "date", "summary"]
    missing_fields = [field for field in required_fields if not payload.get(field)]


    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "missing_fields": missing_fields
        }), 400

    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)

    # Ensures that all articles are numbered correctly. 
    highest_id = 0

    for article in articles:
        if article.get("id", 0) > highest_id:
            highest_id = article["id"]

    new_id = highest_id + 1
    new_article = {
        "id": new_id,
        "title": payload["title"],
        "author": payload["author"],
        "source": payload["source"],
        "summary": payload["summary"],
        "date": payload["date"]
    }

    articles.append(new_article)

    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(articles, file, indent=2, ensure_ascii=False)
        file.write("\n")

    return jsonify(new_article), 201

# Updates an existing article.
@app.route("/api/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):

    data_file = os.path.join(app.root_path, "data", "articles.json")
    payload = request.get_json(silent=True)

    if payload is None:
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

    required_fields = ["title", "author", "source", "date", "summary"]
    missing_fields = [field for field in required_fields if not payload.get(field)]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "missing_fields": missing_fields
        }), 400

    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)

    for article in articles:
        if article["id"] == item_id:

            article["title"] = payload["title"]
            article["author"] = payload["author"]
            article["source"] = payload["source"]
            article["date"] = payload["date"]
            article["summary"] = payload["summary"]

            with open(data_file, "w", encoding="utf-8") as file:
                json.dump(articles, file, indent=2, ensure_ascii=False)
                file.write("\n")

            return jsonify(article), 200

    return jsonify({
        "error": "Article not found."
    }), 404

# Deletes an article.
@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):

    data_file = os.path.join(app.root_path, "data", "articles.json")

    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)

    for article in articles:
        if article["id"] == item_id:

            articles.remove(article)

            with open(data_file, "w", encoding="utf-8") as file:
                json.dump(articles, file, indent=2, ensure_ascii=False)

            return jsonify({
                "message": "Article deleted successfully."
            }), 200

    return jsonify({
        "error": "Article not found."
    }), 404

# Our little star, the scraper.
@app.route("/api/scrape", methods=["POST"])
def scrape_articles():
    target = request.json.get("target") if request.is_json else None
    scraper_map = {
        "bbc": bbc_scraper,
        "cnn": scrape_cnn,
        "techcrunch": techcrunch_scraper,
        "coindesk": coindesk_scraper,
    }
    # run one, or all if no target specified, then save results to articles.json

    return jsonify({
        "message": "Scraper endpoint is ready. Waiting for website details."
    }), 200
    
@app.route("/api/statistics", methods=["GET"])
def get_statistics():

    data_file = os.path.join(app.root_path, "data", "articles.json")

    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)

    sources = set()

    for article in articles:
        sources.add(article["source"])

    return jsonify({
        "total_articles": len(articles),
        "total_sources": len(sources)
    }), 200
    
@app.route("/api/websites", methods=["GET"])
def get_websites():

    data_file = os.path.join(app.root_path, "data", "websites.json")

    with open(data_file, "r", encoding="utf-8") as file:
        websites = json.load(file)

    return jsonify(websites), 200
    
# Adds a new website to the list of websites to scrape.
@app.route("/api/websites", methods=["POST"])
def add_website():

    data_file = os.path.join(app.root_path, "data", "websites.json")
    payload = request.get_json(silent=True)

    if payload is None:
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

    required_fields = ["name", "url"]
    missing_fields = [field for field in required_fields if not payload.get(field)]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "missing_fields": missing_fields
        }), 400

    with open(data_file, "r", encoding="utf-8") as file:
        websites = json.load(file)

    new_website = {
        "name": payload["name"],
        "url": payload["url"]
    }

    websites.append(new_website)

    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(websites, file, indent=2, ensure_ascii=False)

    return jsonify(new_website), 201

# Returns the scraping history.
@app.route("/api/history", methods=["GET"])
def get_history():

    data_file = os.path.join(app.root_path, "data", "history.json")

    with open(data_file, "r", encoding="utf-8") as file:
        history = json.load(file)

    return jsonify(history), 200

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