# routes/items.py

import os
import json

  
from flask import Blueprint, jsonify, request, current_app 

items_bp = Blueprint("items", __name__, url_prefix="/api/items")

@items_bp.route("", methods=["GET"])
def get_items():
    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)

    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=20, type=int)
    start = (page - 1) * limit
    end = start + limit

    return jsonify({
        "page": page,
        "limit": limit,
        "total": len(articles),
        "items": articles[start:end]
    }), 200

@items_bp.route("/<int:item_id>", methods=["GET"])
def get_item(item_id):  

    data_file = os.path.join(
        current_app.root_path,
        "data",
        "cleaned",
        "articles_cleaned.json"
    )

    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)

    for article in articles:
        if article["id"] == item_id:
            return jsonify(article), 200

    return jsonify({"error": "Article not found"}), 404


@items_bp.route("", methods=["POST"])
def create_item():

    data_file = os.path.join(
        current_app.root_path,
        "data",
        "cleaned",
        "articles_cleaned.json"
    )
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

@items_bp.route("/<int:item_id>", methods=["PUT"])
def update_item(item_id):

    data_file = os.path.join(
        current_app.root_path,
        "data",
        "cleaned",
        "articles_cleaned.json"
    )

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

@items_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):

    data_file = os.path.join(
        current_app.root_path,
        "data",
        "cleaned",
        "articles_cleaned.json"
    )

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