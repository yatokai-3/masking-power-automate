from flask import Flask, request, jsonify
from masking import mask_text

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "Masking API is running, new code with small lib of spacy."})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})

@app.route("/mask", methods=["POST"])
def mask():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Send JSON like {'text':'your text here'}"}), 400

    try:
        return jsonify({"masked_text": mask_text(text)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
