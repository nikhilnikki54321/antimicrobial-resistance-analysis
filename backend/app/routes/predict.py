import os
import json
from flask import Blueprint, request, jsonify
from app.ml.predict import predict_all_drugs, predict_with_model
from app.utils.validators import validate_predict_input
import config

predict_bp = Blueprint("predict", __name__)

MICROBE_LIST = [
    "Escherichia coli",
    "Klebsiella pneumoniae",
    "Proteus mirabilis",
    "Pseudomonas aeruginosa",
    "Acinetobacter baumannii",
    "Enterobacteria spp.",
    "Citrobacter spp.",
    "Morganella morganii",
    "Serratia marcescens",
]


@predict_bp.route("/microbes", methods=["GET"])
def get_microbes():
    return jsonify(MICROBE_LIST)


@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    errors = validate_predict_input(data)
    if errors:
        return jsonify({"errors": errors}), 422

    model_key = data.get("model", None)
    microbe_name = data.get("microbe_name", "")

    if model_key:
        result = predict_with_model(
            model_key=model_key,
            age=data["age"],
            gender=max(data["gender"], 0),
            diabetes=data.get("diabetes", 0),
            hypertension=data.get("hypertension", 0),
            hospital_before=data.get("hospital_before", 0),
            infection_freq=data.get("infection_freq", 0.0),
            microbe_name=microbe_name,
        )
    else:
        result = predict_all_drugs(
            age=data["age"],
            gender=max(data["gender"], 0),
            diabetes=data.get("diabetes", 0),
            hypertension=data.get("hypertension", 0),
            hospital_before=data.get("hospital_before", 0),
            infection_freq=data.get("infection_freq", 0.0),
            microbe_name=microbe_name,
        )

    return jsonify(result)


@predict_bp.route("/models/comparison", methods=["GET"])
def get_model_comparison():
    report_path = os.path.join(config.DATA_MODELS, "model_comparison.json")
    if not os.path.exists(report_path):
        return jsonify({"error": "No comparison data. Run train_all_models.py first."}), 404
    with open(report_path, "r") as f:
        return jsonify(json.load(f))
