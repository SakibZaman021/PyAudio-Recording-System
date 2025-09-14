import os
import time
import logging
import requests
from BASE64_Reconverted import OUTPUT_FOLDER
from flask import Flask, request, jsonify
import os
import logging
from werkzeug.utils import secure_filename
from pathlib import Path

OUTPUT_FOLDER = 'converted_base64_files'
NGROK_URL = 'http://5b85-34-31-52-216.ngrok-free.app/upload/v1'  # Replace with ngrok URL from pipeline_testing.py
KAGGLE_API_KEY = os.getenv('3f213bccd7f98dda1198f93ea3d27b74')  # Set in environment variables

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Uploader:
    def __init__(self, output_folder):
        self.output_folder = output_folder
        self.headers = {
            'Authorization': f'Bearer {KAGGLE_API_KEY}',
            'Content-Type': 'application/json'
        }

    def upload_file(self, file_path):
        try:
            sound_file_name = os.path.basename(file_path)
            with open(file_path, 'rb') as file:
                files = {'file': (sound_file_name, file, 'audio/wav')}
                response = requests.post(
                    NGROK_URL,
                    files=files
                )
            
            if response.status_code == 200:
                logging.info(f"Successfully uploaded {file_path} to ngrok endpoint")
                response_json = response.json()
                logging.info(f"Response: {response_json}")
                
                for attempt in range(5):
                    try:
                        os.remove(file_path)
                        logging.info(f"File {file_path} deleted successfully")
                        break
                    except Exception as delete_error:
                        logging.error(f"Attempt {attempt + 1} failed to delete {file_path}: {delete_error}")
                        time.sleep(1)
                
                return True
            else:
                logging.error(f"Failed to upload {file_path} with status code: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"An error occurred while uploading {file_path}: {e}")
            return False

    def process_files(self):
        for sound_file_name in os.listdir(self.output_folder):
            if sound_file_name.endswith('.wav'):
                file_path = os.path.join(self.output_folder, sound_file_name)
                self.upload_file(file_path)
                
                
    
    def scheduler(self, interval=200):
        while True:
            try:
                logging.info("Checking for files to upload to Kaggle notebook...")
                self.process_files()
            except Exception as e:
                logging.error(f"Error during scheduled operation: {e}")
            time.sleep(interval)

if __name__ == '__main__':
    uploader = Uploader(INPUT_FOLDER)
    uploader.scheduler()
    # uploader.process_files()