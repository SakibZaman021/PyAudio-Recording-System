from flask import Flask, request, jsonify
import os
import logging
from werkzeug.utils import secure_filename
from pathlib import Path

app = Flask(__name__)

UPLOAD_FOLDER = 'C:/uploaded_audio_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/upload-audio/v1/<fileName>', methods=['POST'])
def upload_audio(fileName):
    logging.info(f"New file found to save = {fileName}")

    if 'audioFile' not in request.files:
        return "No audio file part in the request", 400

    audio_file = request.files['audioFile']
    if audio_file.filename == '':
        return "No selected file", 400

    try:
        # Ensure the filename ends with .mp3
        if not fileName.lower().endswith('.mp3'):
            fileName += '.mp3'

        filename = secure_filename(fileName)
        file_path = Path(UPLOAD_FOLDER) / filename

        audio_file.save(file_path)

        logging.info(f"File saved to {file_path}")
        logging.info(f"File successfully saved. Responding to client.")
        return "Audio file uploaded successfully!", 200

    except Exception as e:
        logging.error(f"Failed to upload audio file: {e}")
        return "Failed to upload audio file!", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9999)
