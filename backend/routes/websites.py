# routes/websites.py

import os
import json

  
from flask import Blueprint, jsonify, request, current_app 

websites_bp = Blueprint("websites", __name__, url_prefix="/api/websites")

@websites_bp.route("", methods=["GET"])
def get_websites():
    
    data_file = os.path.join(
        current_app.root_path,
        "data",
        "cleaned",
        "websites.json"
    )

    with open(data_file, "r", encoding="utf-8") as file:
        websites = json.load(file)

    return jsonify(websites), 200

@websites_bp.route("", methods=["POST"])
def add_website():

    data_file = os.path.join(
        current_app.root_path,
        "data",
        "cleaned",
        "websites.json")
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