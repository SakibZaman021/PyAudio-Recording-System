import os
import shutil
import soundfile as sf
import numpy as np
import logging
import torch
import torchaudio
from pydub import AudioSegment
import time
from Audio_Receiver import UPLOAD_FOLDER
from dns_challenge_model import DNSModel  # Hypothetical import for DNS model

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NoiseReductionPipeline:
    def __init__(self, upload_folder, output_folder, original_audio_folder, model):
        self.upload_folder = upload_folder
        self.output_folder = output_folder
        self.original_audio_folder = original_audio_folder
        self.model = model
        os.makedirs(self.output_folder, exist_ok=True)
        
    def read_audio(self, file_name):
        try:
            data, rate = sf.read(file_name)
        except:
            audio = AudioSegment.from_file(file_name)
            file_path = 'converted_file.wav'
            audio.export(file_path, format='wav')
            data, rate = sf.read(file_path)
        return data, rate

    def noise_reduction(self, file_path):
        try:
            data, rate = self.read_audio(file_path)
            if data is not None and rate is not None:
                # Resample if necessary
                if rate != 16000:
                    data = torchaudio.transforms.Resample(orig_freq=rate, new_freq=16000)(torch.tensor(data))
                    rate = 16000
                
                # Convert numpy array to torch tensor
                data_tensor = torch.tensor(data).float()
                
                # Pass the data through the DNS model
                with torch.no_grad():
                    denoised_data = self.model(data_tensor.unsqueeze(0)).squeeze(0).numpy()
                    
                return denoised_data, rate
        except Exception as e:
            logging.error(f"Failed to reduce noise for {file_path}: {e}")
        return None, None

    def process_files(self):
        for sound_file_name in os.listdir(self.upload_folder):
            if sound_file_name.endswith('.mp3'):
                input_file_path = os.path.join(self.upload_folder, sound_file_name)
                y_denoised, sr = self.noise_reduction(input_file_path)
                if y_denoised is not None:
                    output_file_path = os.path.join(self.output_folder, sound_file_name.replace('.mp3', '.wav'))
                    sf.write(output_file_path, y_denoised, sr)

                    original_file_path = os.path.join(self.original_audio_folder, sound_file_name)
                    shutil.move(input_file_path, original_file_path)
                    logging.info(f"Processed and moved original file to {original_file_path}")
                else:
                    failed_file_path = os.path.join(self.upload_folder, f"failed_{sound_file_name}")
                    shutil.move(input_file_path, failed_file_path)
                    logging.warning(f"Moved failed file to retry: {sound_file_name}")

    def retry_failed_files(self):
        for sound_file_name in os.listdir(self.upload_folder):
            if sound_file_name.startswith('failed_') and sound_file_name.endswith('.mp3'):
                failed_file_path = os.path.join(self.upload_folder, sound_file_name)
                y_denoised, sr = self.noise_reduction(failed_file_path)
                if y_denoised is not None:
                    output_file_path = os.path.join(self.output_folder, sound_file_name.replace('failed_', '').replace('.mp3', '.wav'))
                    sf.write(output_file_path, y_denoised, sr)

                    original_file_path = os.path.join(self.original_audio_folder, sound_file_name.replace('failed_', ''))
                    shutil.move(failed_file_path, original_file_path)
                    logging.info(f"Retried and moved original failed file to {original_file_path}")

    def scheduler(self, interval=10):
        while True:
            try:
                logging.info("Checking for new files...")
                self.process_files()
                self.retry_failed_files()
            except Exception as e:
                logging.error(f"Error during scheduled operation: {e}")
            time.sleep(interval)

if __name__ == "__main__":
    try:
        OUTPUT_FOLDER = 'd:/output_denoised_files'
        ORIGINAL_AUDIO_FOLDER = 'd:/original_audio_files'
        dns_model = DNSModel()  # Initialize the DNS model

        pipeline = NoiseReductionPipeline(UPLOAD_FOLDER, OUTPUT_FOLDER, ORIGINAL_AUDIO_FOLDER, dns_model)
        pipeline.scheduler()
    except Exception as e:
        logging.error(f"Failed to start the pipeline: {e}")
