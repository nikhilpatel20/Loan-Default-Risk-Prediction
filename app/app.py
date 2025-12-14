from flask import Flask, request, jsonify, send_from_directory
from app.inference import predict_risk
import os

app = Flask(__name__)

# ---------------- HEALTH ----------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Loan Default Risk API running"})


# ---------------- INDEX (optional UI) ----------------
@app.route("/", methods=["GET"])
def index():
    # UI optional hai; agar file nahi hai to clean message do
    if os.path.exists("index.html"):
        return send_from_directory(".", "index.html")
    return jsonify({"message": "UI not available. Use /predict endpoint."})


# ---------------- PREDICT ----------------
@app.route("/predict", methods=["POST"])
def predict():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object expected"}), 400

    # debug log
    app.logger.info(f"Incoming payload: {data}")

    try:
        result = predict_risk(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 400
