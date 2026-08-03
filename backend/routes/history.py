# routes/history.py

import os
import json

  
from flask import Blueprint, jsonify, request, current_app 

history_bp = Blueprint("history", __name__, url_prefix="/api/history")

@history_bp.route("", methods=["GET"])
def get_history():
    
    data_file = os.path.join(
        current_app.root_path,
        "data",
        "cleaned",
        "history.json"
    )

    with open(data_file, "r", encoding="utf-8") as file:
        history = json.load(file)

    return jsonify(history), 200
