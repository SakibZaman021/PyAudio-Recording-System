import os
import time
import logging
import requests


OUTPUT_FOLDER = 'input_wav_files'
UPLOAD_URL_BASE = 'https://5f3e4af486b7.ngrok-free.app/upload-audio/v1'

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Uploader:
    def __init__(self, output_folder, upload_url_base):
        self.output_folder = output_folder
        self.upload_url_base = upload_url_base

    def upload_file(self, file_path):
        # Extract the filename from the full file path
        sound_file_name = os.path.basename(file_path)
        # Construct the full URL for uploading the file
        url = f"{self.upload_url_base}/{sound_file_name}"

        try:
          
        
            with open(file_path, 'rb') as file:
                files = {'audioFile': file}
                response = requests.post(url, files=files)
            
            if response.status_code == 200:
                if response.status_code == 200:
                 if response.text.strip() == "Audio file uploaded successfully!":
                    logging.info(f"Successfully uploaded {file_path}")
                    # Attempt to delete the file with retries
                    for attempt in range(5):
                        try:
                            os.remove(file_path)  # Delete the file after successful upload
                            logging.info(f"File {file_path} deleted successfully")
                            break
                        except Exception as delete_error:
                            logging.error(f"Attempt {attempt + 1} failed to delete {file_path}: {delete_error}")
                            time.sleep(1)  # Wait before retrying
                else:
                    logging.error(f"Unexpected response from server: {response.text}")
            else:
                logging.error(f"Failed to upload {file_path} with status code: {response.status_code}")
        except Exception as e:
            logging.error(f"An error occurred while uploading {file_path}: {e}")
       

    def process_files(self):
        
        for sound_file_name in os.listdir(self.output_folder):
            
            if sound_file_name.endswith('.wav'):
                
                file_path = os.path.join(self.output_folder, sound_file_name)
               
                self.upload_file(file_path)
                

    def scheduler(self, interval=10):
        while True:
            try:
                logging.info("Checking for files to upload...")
                
                self.process_files()
            except Exception as e:
                logging.error(f"Error during scheduled operation: {e}")
            
            time.sleep(interval)

if __name__ == "__main__":
    try:
        
        uploader = Uploader(OUTPUT_FOLDER, UPLOAD_URL_BASE)
        uploader.scheduler()
    except Exception as e:
        logging.error(f"Failed to start the uploader: {e}")