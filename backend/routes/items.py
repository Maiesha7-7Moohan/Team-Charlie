# routes/items.py

import os
import json

from flask import Blueprint, jsonify, request, current_app

items_bp = Blueprint("items", __name__, url_prefix="/api/items")

import csv
import io
from flask import Blueprint, jsonify, request, current_app, Response


@items_bp.route("/export", methods=["GET"])
def export_items():
    data_file = os.path.join(
        current_app.root_path,
        "data",
        "cleaned",
        "articles_cleaned.json"
    )

    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)

    for index, article in enumerate(articles, start=1):
        article.setdefault("id", index)

    if not articles:
        return jsonify({"error": "No items to export"}), 404

    export_format = request.args.get("format", default="csv")

    if export_format == "json":
        response = Response(
            json.dumps(articles, indent=2, ensure_ascii=False),
            mimetype="application/json"
        )
        response.headers["Content-Disposition"] = "attachment; filename=articles.json"
        return response

    # default: csv
    output = io.StringIO()
    fieldnames = list(articles[0].keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for article in articles:
        writer.writerow(article)

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=articles.csv"
    return response


@items_bp.route("", methods=["GET"])
def get_items():
    data_file = os.path.join(
        current_app.root_path,
        "data",
        "cleaned",
        "articles_cleaned.json"
    )

    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)
    
    for index, article in enumerate(articles, start=1):
        article.setdefault("id", index)
        

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
        
    for index, article in enumerate(articles, start=1):
        article.setdefault("id", index)

    for article in articles:
        if article.get("id") == item_id:
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

    required_fields = [
        "title",
        "description",
        "author",
        "published",
        "source"
    ]

    missing_fields = [
        field for field in required_fields
        if not payload.get(field)
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "missing_fields": missing_fields
        }), 400

    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)
        
    for index, article in enumerate(articles, start=1):
        article.setdefault("id", index)

    highest_id = 0

    for article in articles:
        highest_id = max(highest_id, article.get("id", 0))

    new_article = {
        "id": highest_id + 1,
        "title": payload["title"],
        "description": payload["description"],
        "author": payload["author"],
        "published": payload["published"],
        "source": payload["source"],
        "category": payload.get("category", ""),
        "image_url": payload.get("image_url", ""),
        "article": payload.get("article", ""),
        "link": payload.get("link", "")
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

    required_fields = [
        "title",
        "description",
        "author",
        "published",
        "source"
    ]

    missing_fields = [
        field for field in required_fields
        if not payload.get(field)
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "missing_fields": missing_fields
        }), 400

    with open(data_file, "r", encoding="utf-8") as file:
        articles = json.load(file)
        
    for index, article in enumerate(articles, start=1):
        article.setdefault("id", index)

    for article in articles:
        if article.get("id") == item_id:

            article["title"] = payload["title"]
            article["description"] = payload["description"]
            article["author"] = payload["author"]
            article["published"] = payload["published"]
            article["source"] = payload["source"]

            article["category"] = payload.get(
                "category",
                article.get("category", "")
            )

            article["image_url"] = payload.get(
                "image_url",
                article.get("image_url", "")
            )

            article["article"] = payload.get(
                "article",
                article.get("article", "")
            )

            article["link"] = payload.get(
                "link",
                article.get("link", "")
            )

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

    for index, article in enumerate(articles, start=1):
        article.setdefault("id", index)

    for article in articles:
        if article.get("id") == item_id:

            articles.remove(article)

            with open(data_file, "w", encoding="utf-8") as file:
                json.dump(articles, file, indent=2, ensure_ascii=False)
                file.write("\n")

            return jsonify({
                "message": "Article deleted successfully."
            }), 200

    return jsonify({
        "error": "Article not found."
    }), 404