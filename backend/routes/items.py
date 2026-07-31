# routes/items.py
from flask import Blueprint, jsonify, request

items_bp = Blueprint("items", __name__, url_prefix="/api/items")

