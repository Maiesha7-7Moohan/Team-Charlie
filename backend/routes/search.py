# routes/search.py

import os
import json

from flask import Blueprint, jsonify, request, current_app

search_bp = Blueprint("search", __name__, url_prefix="/api/search")


@search_bp.route("/", methods=["GET"])
def search_articles():

    search_term = request.args.get("q")

    if not search_term:
        return jsonify({
        "error": "Please provide a search term."
    }), 400

    data_file = os.path.join(current_app.root_path, "data", "articles.json")

    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)

    results = []

    for article in articles:
        if search_term.lower() in article["title"].lower():
            results.append(article)

    return jsonify(results), 200