from flask import Flask, request, jsonify, send_from_directory
import os
from app.inference import predict_risk

app = Flask(__name__)

# ---------------- HEALTH ----------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Loan Default Risk API running"})


# ---------------- INDEX ----------------
@app.route("/", methods=["GET"])
def index():
    if os.path.exists("templates/index.html"):
        return send_from_directory(".", "templates/index.html")
    return jsonify({"message": "UI not available. Use /predict endpoint."})


# ---------------- PREDICT ----------------
@app.route("/predict", methods=["POST"])
def predict():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object expected"}), 400

    try:
        result = predict_risk(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 400

# ---------------- LOCAL RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
