from flask import Flask, render_template, request
from flask_cors import CORS
import os
from datetime import datetime

# Create Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Directory to save uploaded audio files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Home route – renders index.html
@app.route('/')
def index():
    return render_template("index.html")

# Upload route – handles audio blob + username
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    username = request.form.get('username', 'anonymous').replace(" ", "_")

    if file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{username}_{timestamp}.wav"
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        # Optional logging
        with open("log.csv", "a") as log:
            log.write(f"{username},{filename},{datetime.now()}\n")

        return f"Uploaded as {filename}"
    return "No file received", 400

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
