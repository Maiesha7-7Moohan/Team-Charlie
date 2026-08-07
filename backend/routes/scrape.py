import os
import json
from datetime import datetime
from flask import Blueprint, jsonify, request, current_app

from scrapers.bbc_scraper import bbc_scraper
from scrapers.cnn_scraper import run as run_cnn
from scrapers.techcrunch_scraper import run as run_techcrunch
from scrapers.coindesk_scraper import run as run_coindesk
from scrapers.generic_scraper import scrape_site
from utils.cleaning.clean_articles import clean_all

scrape_bp = Blueprint("scrape", __name__, url_prefix="/api/scrape")

# Sites that have a dedicated, hand-tuned scraper
CUSTOM_SCRAPERS = {
    "BBC": bbc_scraper,
    "CNN": run_cnn,
    "TechCrunch": run_techcrunch,
    "CoinDesk": run_coindesk,
}


def _load_websites():
    data_file = os.path.join(current_app.root_path, "data", "cleaned", "websites.json")
    try:
        with open(data_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


@scrape_bp.route("", methods=["GET"])
def scrape_status():
    websites = _load_websites()
    all_targets = sorted({*CUSTOM_SCRAPERS.keys(), *(w["name"] for w in websites)})
    return jsonify({"message": "Scraper is ready.", "available_targets": all_targets}), 200


@scrape_bp.route("", methods=["POST"])
def run_scraper():
    payload = request.get_json(silent=True) or {}
    websites = _load_websites()
    website_lookup = {w["name"]: w for w in websites}

    # By default, scrape every hand-tuned source AND every site currently
    # sitting in the Website Manager. This is what makes "Scrape Now" and
    # the Website Manager actually connected to each other.
    default_targets = sorted({*CUSTOM_SCRAPERS.keys(), *website_lookup.keys()})
    targets = payload.get("targets", default_targets)

    results = []
    for name in targets:
        try:
            if name in CUSTOM_SCRAPERS:
                result = CUSTOM_SCRAPERS[name]()
            elif name in website_lookup:
                result = scrape_site(website_lookup[name])
            else:
                results.append({"source": name, "success": False, "message": "Unknown target"})
                continue
            results.append({"source": name, **result})
        except Exception as e:
            results.append({"source": name, "success": False, "message": str(e)})

    # Merge newly scraped raw data into the cleaned dataset
    total_cleaned = clean_all(current_app.root_path)

    # Log this run to history.json
    history_file = os.path.join(current_app.root_path, "data", "cleaned", "history.json")
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