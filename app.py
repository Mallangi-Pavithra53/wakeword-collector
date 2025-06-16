from flask import Flask, render_template, request
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Ensure the uploads folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if 'audio_data' not in request.files:
        return "No audio data part", 400

    file = request.files['audio_data']
    if file.filename == '':
        return "No selected file", 400

    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"wakeword_{timestamp}.webm"
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    return "Upload successful", 200

if __name__ == "__main__":
    # Render requires host=0.0.0.0 and PORT from env
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
