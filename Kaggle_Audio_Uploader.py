import os
import json
import time
import logging
import shutil
import requests
from flask import Flask, request, jsonify
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from Audio_Receiver import UPLOAD_FOLDER
# from singleton_recorder import INPUT_FOLDER

# --- Configuration ---
UPLOAD_FOLDER = 'uploaded_audio_files'
LOCAL_TRANSCRIPT_FOLDER = 'D:\AIMS LAB REVIEW PAPER\pyaudio secondary version\my_recorder_project\dist\downloaded_transcripts' 
AUDIO_WAV_FILES = 'audio_wav_files' 
os.makedirs(AUDIO_WAV_FILES, exist_ok=True)
os.makedirs(LOCAL_TRANSCRIPT_FOLDER, exist_ok=True) 
NGROK_URL = os.environ.get('NGROK_URL', '/upload/v1')

SSL_VERIFY = False

# Load Kaggle API Key securely
try:
    kaggle_path = os.path.expanduser('~/.kaggle/kaggle.json')
    with open(kaggle_path, 'r') as f:
        kaggle_config = json.load(f)
        KAGGLE_API_KEY = kaggle_config['key']
except (FileNotFoundError, KeyError) as e:
    logging.error(f"Could not load Kaggle API key from {kaggle_path}: {e}")
    KAGGLE_API_KEY = None # Handle missing key gracefully

# Set up session with retry logic
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Uploader:
    def __init__(self, output_folder):
        if not KAGGLE_API_KEY:
            raise ValueError("Kaggle API Key could not be loaded.")
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True) # Ensure folder exists
        self.headers = {
            'Authorization': f'Bearer {KAGGLE_API_KEY}',
            # Content-Type is set by requests when using the 'files' parameter
        }

    def upload_file(self, file_path):
        """Uploads a single file and deletes it upon successful upload."""
        file_path = Path(file_path)
        try:
            # The 'files' dict handles Content-Type, so it's not needed in headers
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f, 'audio/wav')}
                upload_url = f"{NGROK_URL}/{file_path.name}"
                logging.info(f"Uploading {file_path} to {upload_url}")
                
                print("--- SSL Verification Check ---")
                print(f"Type of SSL_VERIFY: {type(SSL_VERIFY)}")
                print(f"Value of SSL_VERIFY: {SSL_VERIFY}")
                print("----------------------------")
                
                response = session.post(
                    upload_url,
                    files=files,
                    headers=self.headers,
                    verify=SSL_VERIFY,
                    # timeout=30
                )
            
            response.raise_for_status() # This will raise an HTTPError for 4xx/5xx responses

            # logging.info(f"Successfully uploaded {file_path}. Status: {response.status_code}")
            # logging.info(f"Response: {response.json()}")
            
            response_data = response.json()
            logging.info(f"Successfully uploaded {file_path}. Status: {response.status_code}")
            logging.info(f"Server Response: {response_data}")
            
            # --- TRIGGER THE DOWNLOAD ---
            transcript_to_download = response_data.get('output_file')
        
            if transcript_to_download:
                logging.info(f"Server provided transcript filename: {transcript_to_download}. Starting download.")
                self.download_file(transcript_to_download)
            else:
                logging.warning("Server response did not contain an 'output_file' to download.")
        
            
            
            try:
                destination_path = os.path.join(AUDIO_WAV_FILES, file_path.name)
                shutil.move(str(file_path), destination_path)
                logging.info(f"Successfully moved {file_path} to {destination_path}")
            except OSError as e:
                logging.error(f"Error moving file {file_path} to audio_wav_files: {e}")
            
            return True
                
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error for {file_path}: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error uploading {file_path}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error uploading {file_path}: {e}")
        
        return False
    
    def download_file(self, transcript_filename):
        """Downloads a file from the server's download endpoint."""
      
        base_url = NGROK_URL.replace('/upload/v1', '')
        download_url = f"{base_url}/download/v1/{transcript_filename}"
        
        local_save_path = os.path.join(LOCAL_TRANSCRIPT_FOLDER, transcript_filename)
        os.makedirs(LOCAL_TRANSCRIPT_FOLDER, exist_ok=True) # Ensure the local folder exists

        try:
            logging.info(f"Downloading transcript from: {download_url}")
            # Use stream=True for efficient downloading of files
            with session.get(download_url, stream=True, verify=SSL_VERIFY, timeout=30) as r:
                r.raise_for_status() # Will raise an error for 4xx/5xx responses
                
                # Write the file to the local disk in chunks
                with open(local_save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            logging.info(f"Successfully downloaded and saved transcript to: {local_save_path}")
            return True
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error downloading {transcript_filename}: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error downloading {transcript_filename}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error downloading {transcript_filename}: {e}")
        
        return False

    def process_files(self):
        """Processes all .wav files in the output folder."""
        for file_path in self.output_folder.glob('*.wav'):
            self.upload_file(file_path)
                
    def scheduler(self, interval=200):
        """Periodically checks for files and uploads them."""
        while True:
            try:
                logging.info("Scheduler running: Checking for files to upload...")
                self.process_files()
            except Exception as e:
                logging.error(f"Error in scheduler loop: {e}")
            time.sleep(interval)

if __name__ == '__main__':
    if not KAGGLE_API_KEY:
        logging.error("KAGGLE_API_KEY not found. Please ensure ~/.kaggle/kaggle.json is configured.")
        exit(1)
        
    uploader = Uploader(UPLOAD_FOLDER)
    uploader.scheduler()