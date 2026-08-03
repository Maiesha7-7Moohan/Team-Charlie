import os
import json
from datetime import datetime
from flask import Blueprint, jsonify, request, current_app

from scrapers.bbc_scraper import bbc_scraper
from scrapers.cnn_scraper import run as run_cnn
from scrapers.techcrunch_scraper import run as run_techcrunch
from scrapers.coindesk_scraper import run as run_coindesk
from utils.cleaning.clean_articles import clean_all

scrape_bp = Blueprint("scrape", __name__, url_prefix="/api/scrape")

SCRAPERS = {
    "BBC": bbc_scraper,
    "CNN": run_cnn,
    "TechCrunch": run_techcrunch,
    "CoinDesk": run_coindesk,
}

@scrape_bp.route("", methods=["GET"])
def scrape_status():
    return jsonify({"message": "Scraper is ready.", "available_targets": list(SCRAPERS.keys())}), 200


@scrape_bp.route("", methods=["POST"])
def run_scraper():
    payload = request.get_json(silent=True) or {}
    targets = payload.get("targets", list(SCRAPERS.keys()))

    results = []
    for name in targets:
        fn = SCRAPERS.get(name)
        if not fn:
            results.append({"source": name, "success": False, "message": "Unknown target"})
            continue
        try:
            result = fn()
            results.append({"source": name, **result})
        except Exception as e:
            results.append({"source": name, "success": False, "message": str(e)})

    # Merge newly scraped raw data into the cleaned dataset
    total_cleaned = clean_all(current_app.root_path)

    # Log this run to history.json
    history_file = os.path.join(current_app.root_path, "data", "history.json")
    with open(history_file, "r", encoding="utf-8") as f:
        history = json.load(f)

    history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "targets": targets,
        "results": results,
        "total_cleaned_articles": total_cleaned,
    })

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    return jsonify({"message": "Scrape run complete", "results": results}), 200