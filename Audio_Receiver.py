from flask import Flask, request, jsonify
import os
import logging
from werkzeug.utils import secure_filename
from pathlib import Path
import requests
import os
import time
import logging
import requests
from flask import Flask
import os
import logging
from pathlib import Path

app = Flask(__name__)

Audio_UPLOAD_FOLDER = 'C:/uploaded_audio_files'
os.makedirs(Audio_UPLOAD_FOLDER, exist_ok=True)
# Text_OUTPUT_FOLDER = 'C:/transcripted_files'
# os.makedirs(Text_OUTPUT_FOLDER, exist_ok=True)
# # DOWNLOAD_FOLDER = 'transcription_files'
# UPLOAD_URL_BASE = 'https://49f8-203-190-10-105.ngrok-free.app/upload-text/v1'
app = Flask(__name__)

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
        if not fileName.lower().endswith('.wav'):
            fileName += '.'

        filename = secure_filename(fileName)
        file_path = Path(Audio_UPLOAD_FOLDER) / filename

        audio_file.save(file_path)

        logging.info(f"File saved to {file_path}")
        logging.info(f"File successfully saved. Responding to client.")
        return "Audio file uploaded successfully!", 200

    except Exception as e:
        logging.error(f"Failed to upload audio file: {e}")
        return "Failed to upload audio file!", 500


# class Uploader:
#     def __init__(self, output_folder,upload_url_base):
#         self.output_folder = Text_OUTPUT_FOLDER
#         self.upload_url_base = upload_url_base

#     def upload_file(self, file_path):
#         # Extract the filename from the full file path
#         text_file_name = os.path.basename(file_path)
#         # Construct the full URL for uploading the file
#         url = f"{self.upload_url_base}/{text_file_name}"

#         try:
#             with open(file_path, 'rb') as file:
#                 files = {'textfile': file}
#                 response = requests.post(url, files=files)
            
#             if response.status_code == 200:
#                 if response.status_code == 200:
#                  if response.text.strip() == "Text file uploaded successfully!":
#                     logging.info(f"Successfully uploaded {file_path}")
#                     # Attempt to delete the file with retries
#                     for attempt in range(5):
#                         try:
#                             os.remove(file_path)  # Delete the file after successful upload
#                             logging.info(f"File {file_path} deleted successfully")
#                             break
#                         except Exception as delete_error:
#                             logging.error(f"Attempt {attempt + 1} failed to delete {file_path}: {delete_error}")
#                             time.sleep(1)  # Wait before retrying
#                 else:
#                     logging.error(f"Unexpected response from server: {response.text}")
#             else:
#                 logging.error(f"Failed to upload {file_path} with status code: {response.status_code}")
#         except Exception as e:
#             logging.error(f"An error occurred while uploading {file_path}: {e}")
       

#     def process_files(self):
        
#         for text_file_name in os.listdir(self.output_folder):
            
#             if text_file_name.endswith('.txt'):
                
#                 file_path = os.path.join(self.output_folder, text_file_name)
               
#                 self.upload_file(file_path)


#     def scheduler(self, interval=20):
#         while True:
#             try:
#                 logging.info("Checking for files to upload...")
                
#                 self.process_files()
#             except Exception as e:
#                 logging.error(f"Error during scheduled operation: {e}")
            
#             time.sleep(interval)
            
if __name__ == '__main__':
    # try:
        
    #     uploader = Uploader(Text_OUTPUT_FOLDER, UPLOAD_URL_BASE)
    #     uploader.scheduler()
    # except Exception as e:
    #     logging.error(f"Failed to start the uploader: {e}")           
    app.run(debug=True, host='0.0.0.0', port=9999)           