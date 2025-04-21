import os
import time
import logging
import requests
from Audio_File_Reducer import OUTPUT_FOLDER
from flask import Flask, request, jsonify
import os
import logging
from werkzeug.utils import secure_filename
from pathlib import Path
# from kaggle.api.kaggle_api_extended import KaggleApi

TEXT_UPLOAD_FOLDER = 'C:/uploaded_text_files'
os.makedirs(TEXT_UPLOAD_FOLDER, exist_ok=True)

OUTPUT_FOLDER = 'compressed_audio_files'
# DOWNLOAD_FOLDER = 'transcription_files'
UPLOAD_URL_BASE = 'https://7150-103-187-94-62.ngrok-free.app/upload-audio/v1'
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/upload-text/v1/<fileName>', methods=['POST'])
def upload_text(fileName):
    logging.info(f"New text file found to save = {fileName}")

    if 'textFile' not in request.files:
        return "No text file part in the request", 400

    text_file = request.files['textFile']
    if text_file.filename == '':
        return "No selected file", 400

    try:
        if not fileName.lower().endswith('.txt'):
            fileName += '.txt'
        filename = secure_filename(fileName)
        file_path = Path(TEXT_UPLOAD_FOLDER) / filename
        text_file.save(file_path)

        logging.info(f"Text file saved to {file_path}")
        logging.info(f"Text file successfully saved. Responding to client.")
        return "Text file uploaded successfully!", 200

    except Exception as e:
        logging.error(f"Failed to upload text file: {e}")
        return "Failed to upload text file!", 500
    
    
    
    
# class Uploader:
#     def __init__(self, output_folder,upload_url_base):
#         self.output_folder = output_folder
#         self.upload_url_base = upload_url_base

#     def upload_file(self, file_path):
#         # Extract the filename from the full file path
#         sound_file_name = os.path.basename(file_path)
#         # Construct the full URL for uploading the file
#         url = f"{self.upload_url_base}/{sound_file_name}"

#         try:
#             with open(file_path, 'rb') as file:
#                 files = {'audioFile': file}
#                 response = requests.post(url, files=files)
            
#             if response.status_code == 200:
#                 if response.status_code == 200:
#                  if response.text.strip() == "Audio file uploaded successfully!":
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
        
#         for sound_file_name in os.listdir(self.output_folder):
            
#             if sound_file_name.endswith('.wav'):
                
#                 file_path = os.path.join(self.output_folder, sound_file_name)
               
#                 self.upload_file(file_path)


#     def scheduler(self, interval=200):
#         while True:
#             try:
#                 logging.info("Checking for files to upload...")
                
#                 self.process_files()
#             except Exception as e:
#                 logging.error(f"Error during scheduled operation: {e}")
            
#             time.sleep(interval)
            

if __name__ == '__main__':
    # try:
        
    #     uploader = Uploader(OUTPUT_FOLDER, UPLOAD_URL_BASE)
    #     uploader.scheduler()
    # except Exception as e:
    #     logging.error(f"Failed to start the uploader: {e}")           
    app.run(debug=True, host='0.0.0.0', port=9998)
    
    
