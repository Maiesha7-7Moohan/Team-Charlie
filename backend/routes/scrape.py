# routes/scrape.py

import os
import json

  
from flask import Blueprint, jsonify, request, current_app

scrape_bp = Blueprint("scrape", __name__, url_prefix="/api/scrape")

@scrape_bp.route("", methods=["GET"])
def scrape_status():

  data_file = os.path.join(
      current_app.root_path,
      "data",
      "cleaned",
      "articles_cleaned.json"
  )

  with open(data_file, "r", encoding="utf-8") as file:
      articles = json.load(file)

  return jsonify({
      "message": "Scraper endpoint is ready. Waiting for website details."
  }), 200

@scrape_bp.route("", methods=["POST"])
def run_scraper():

    return jsonify({
        "message": "Scraper endpoint is ready. Waiting for website details."
    }), 200
    
 