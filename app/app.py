from flask import Flask, request, jsonify, render_template
from app.inference import predict_risk

app = Flask(__name__, template_folder="templates")

# ---------------- INDEX (HTML UI) ----------------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# ---------------- HEALTH ----------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Loan Default Risk API running"})


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
        }), 500


# ---------------- LOCAL RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
