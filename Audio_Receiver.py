# receiver.py

from flask import Flask, request
import os
import logging
from werkzeug.utils import secure_filename
from pathlib import Path
import traceback
from waitress import serve
# Import traceback for better error logging

# --- Use a relative path for the upload folder ---
# This folder will be created in the same directory as your script.
UPLOAD_FOLDER = 'uploaded_audio_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Configure logging ---
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

@app.route('/upload-audio/v1/<filename>', methods=['POST'])
def upload_audio(filename):
    logging.info(f"Received request to save file: {filename}")

    if 'audioFile' not in request.files:
        logging.error("'audioFile' part not found in the request files.")
        return "No audio file part in the request", 400

    audio_file = request.files['audioFile']
    if audio_file.filename == '':
        logging.error("No file selected in the request.")
        return "No selected file", 400

    try:
        # Use the filename from the URL, but secure it
        safe_filename = secure_filename(filename)
        if not safe_filename:
            logging.error(f"Filename '{filename}' was considered unsafe.")
            return "Invalid filename provided", 400

        # Construct the full path to save the file
        file_path = Path(UPLOAD_FOLDER) / safe_filename
        
        # Save the file
        audio_file.save(file_path)

        logging.info(f"File '{safe_filename}' saved successfully to '{file_path}'")
        return "Audio file uploaded successfully!", 200

    except Exception as e:
        # --- Use logging.exception for detailed error traceback ---
        logging.exception(f"CRITICAL: Failed to save file '{filename}'. Error follows:")
        # The line above will print the full error, like "Permission Denied".
        
        return "Server failed to save the audio file.", 500


if __name__ == '__main__':       
    # Running on port 5000 is standard for Flask, but 9999 is fine too.
    app.run(debug=True, host='0.0.0.0', port=9999)
    # logging.info("Starting production server on http://0.0.0.0:9999")
    # serve(app, host='0.0.0.0', port=9999)