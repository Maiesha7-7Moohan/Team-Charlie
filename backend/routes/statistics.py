# routes/statistics.py

import os
import json

from flask import Blueprint, jsonify, request, current_app

statistics_bp = Blueprint("statistics", __name__, url_prefix="/api/statistics")

@statistics_bp.route("", methods=["GET"])
def get_statistics():
    articles_file = os.path.join(current_app.root_path, "data", "cleaned", "articles_cleaned.json")
    websites_file = os.path.join(current_app.root_path, "data", "cleaned", "websites.json")   # <-- add "cleaned"
    history_file = os.path.join(current_app.root_path, "data", "cleaned", "history.json")     # <-- add "cleaned"

    with open(articles_file, encoding="utf-8") as f:
        articles = json.load(f)
    with open(websites_file, encoding="utf-8") as f:
        websites = json.load(f)
    with open(history_file, encoding="utf-8") as f:
        history = json.load(f)
    

    sources = {a["source"] for a in articles}
    failed = sum(1 for h in history for r in h.get("results", []) if not r.get("success", True))
    total_runs = sum(len(h.get("results", [])) for h in history) or 1
    success_rate = round(100 * (1 - failed / total_runs), 1)

    return jsonify({
        "total_articles": len(articles),
        "total_sources": len(sources),
        "total_websites": len(websites),
        "success_rate": success_rate,
        "last_scrape": history[-1]["timestamp"] if history else None,
    }), 200