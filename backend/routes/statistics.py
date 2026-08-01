# routes/statistics.py

import os
import json

from flask import Blueprint, jsonify, request, current_app

statistics_bp = Blueprint("statistics", __name__, url_prefix="/api/statistics")

@statistics_bp.route("", methods=["GET"])
def get_statistics():

    data_file = os.path.join(current_app.root_path, "data", "articles.json")

    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)

    sources = set()

    for article in articles:
        sources.add(article["source"])

    return jsonify({
        "total_articles": len(articles),
        "total_sources": len(sources)
    }), 200