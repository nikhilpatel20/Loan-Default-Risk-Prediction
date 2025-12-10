from flask import Flask, request, jsonify, send_from_directory
from inference import predict_risk
import os

app = Flask(__name__)


# ✅ API root (important for Docker / health check)
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Loan Default Risk API running"})


# ✅ OPTIONAL UI root (sirf tab chalega jab index.html ho)
@app.route("/", methods=["GET"])
def index():
    if os.path.exists("index.html"):
        return send_from_directory(".", "index.html")
    return jsonify({
        "message": "UI not available. Use /predict for API."
    })


@app.route("/predict", methods=["POST"])
def predict():

    if not request.is_json:
        return jsonify({"error": "Request body JSON hona chahiye."}), 400

    data = request.get_json()

    try:
        result = predict_risk(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    # ✅ Dev mode ONLY (Docker me gunicorn use hoga)
    app.run(host="0.0.0.0", port=8000)
