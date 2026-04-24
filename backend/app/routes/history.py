import json
import os
from datetime import datetime
from flask import Blueprint, request, jsonify

history_bp = Blueprint("history", __name__)

HISTORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data", "history.json"
)


def _load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


def _save_history(records):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(records, f, indent=2)


@history_bp.route("/history", methods=["GET"])
def get_history():
    records = _load_history()
    return jsonify(records)


@history_bp.route("/history", methods=["POST"])
def save_history():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    record = {
        "id": len(_load_history()) + 1,
        "timestamp": datetime.now().isoformat(),
        "input": data.get("input", {}),
        "result": data.get("result", {})
    }

    records = _load_history()
    records.insert(0, record)
    _save_history(records)

    return jsonify(record), 201
