from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from models.text_disease_model import predict_disease_text
from models.image_disease_model import predict_disease_image
from models.voice_to_text import voice_to_text

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/predict/text", methods=["POST"])
def predict_text():
    data = request.json
    symptoms = data.get("symptoms", "")
    result = predict_disease_text(symptoms)
    return jsonify(result)

@app.route("/predict/image", methods=["POST"])
def predict_image():
    image = request.files["image"]
    path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(path)

    result = predict_disease_image(path)
    return jsonify(result)

@app.route("/predict/voice", methods=["POST"])
def predict_voice():
    audio = request.files["audio"]
    path = os.path.join(UPLOAD_FOLDER, audio.filename)
    audio.save(path)

    recognized_text = voice_to_text(path)
    result = predict_disease_text(recognized_text)

    return jsonify({
        "recognized_text": recognized_text,
        "prediction": result
    })

if __name__ == "__main__":
    app.run(debug=True)
