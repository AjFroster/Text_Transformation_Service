from flask import Flask, request, jsonify
from features.chunking import chunk_text
import spacy

app = Flask(__name__)

# Preload the SpaCy model on app startup
nlp = spacy.load("en_core_web_md")
print(f"Loaded SpaCy model: {nlp.meta['name']}")
print(f"Vectors loaded: {len(nlp.vocab.vectors)}")


# Defines Routes and handles input/output
# Calls feature modules (chunking) for text processing
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "Text Transformation Service is running"}), 200


@app.route("/input", methods=["POST"])
def receive_input():
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'ext' in request body"}), 400

    text = data["text"]
    return jsonify({"message": "Text received successfully", "input_text": text}), 200


@app.route("/chunk", methods=["POST"])
def chunk_endpoint():
    data = request.json

    if not data or "text" not in data or "chunk_size" not in data:
        return jsonify({"error": "Missing 'text' or 'chunk_size' in request body"}), 400

    text = data["text"]
    chunk_size = data["chunk_size"]

    try:
        chunk_size = int(chunk_size)
        chunks = chunk_text(text, chunk_size, nlp)
        return jsonify({"chunks": chunks}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
