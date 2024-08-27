
import os
import shutil
import librosa
import soundfile as sf
import noisereduce as nr
import numpy as np
import logging
from noisereduce.generate_noise import band_limited_noise
from pydub import AudioSegment
import time
from Audio_Receiver import UPLOAD_FOLDER




# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NoiseReductionPipeline:
    def __init__(self, upload_folder, output_folder):
        self.upload_folder = upload_folder
        self.output_folder = output_folder
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
    
    
    def enhance_voice(self, data, rate):
    #     # Apply a high-pass filter to remove low-frequency noise (below human voice range)
    #     data = librosa.effects.preemphasis(data, coef=0.97)
        
    #     # Boost frequencies in the range of 85Hz to 255Hz to enhance human voice
        boosted = librosa.effects.equalizer(data, center_freq=160, gain_db=5, bandwidth=0.7)
        
        return boosted

    def noise_reduction(self, file_path, noise_reduce=True):
        try:
            data, rate = self.read_audio(file_path)
            if noise_reduce:
                noise_len = 2  
                noise = band_limited_noise(min_freq=50, max_freq=16000, samples=len(data), samplerate=rate) * 1.5  
                noise_clip = noise[:rate * noise_len]
                audio_clip_band_limited = data + noise
                reduced_noise = nr.reduce_noise(y=audio_clip_band_limited, sr=rate,n_std_thresh_stationary=0.5, stationary=True, use_torch=False)
                reduced_noise = nr.reduce_noise(y=reduced_noise, sr=rate, thresh_n_mult_nonstationary=0.5, stationary=False, use_torch=False)
                                            
            else:
                reduced_noise = librosa.effects.preemphasis(data)

            return reduced_noise, rate
        except Exception as e:
            logging.error(f"Failed to denoise {file_path}: {e}")
        return None, None

        
    def process_files(self):
        for sound_file_name in os.listdir(self.upload_folder):
            if sound_file_name.endswith('.wav'):
                input_file_path = os.path.join(self.upload_folder, sound_file_name)
                y_denoised, sr = self.noise_reduction(input_file_path)
                if y_denoised is not None:
                    output_file_path = os.path.join(self.output_folder, sound_file_name)
                    sf.write(output_file_path, y_denoised, sr)
                    os.remove(input_file_path)
                    logging.info(f"Processed and removed original file: {sound_file_name}")

                else:
                    failed_file_path = os.path.join(self.input_folder, f"failed_{sound_file_name}")
                    shutil.move(input_file_path, failed_file_path)
                    logging.warning(f"Moved failed file to retry: {sound_file_name}")
 
    def retry_failed_files(self):
        for sound_file_name in os.listdir(self.upload_folder):
            if sound_file_name.startswith('failed_') and sound_file_name.endswith('.wav'):
                failed_file_path = os.path.join(self.upload_folder, sound_file_name)
                y_denoised, sr = self.noise_reduction(failed_file_path)
                if y_denoised is not None:
                    output_file_path = os.path.join(self.output_folder, sound_file_name.replace('failed_', ''))
                    sf.write(output_file_path, y_denoised, sr)
                    os.remove(failed_file_path)
                    logging.info(f"Retried and removed failed file: {sound_file_name}")  # Upload the file after processing     

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
          # Ensure this module and variable exist
        OUTPUT_FOLDER = 'd:/output_denoised_files'
        
        pipeline = NoiseReductionPipeline(UPLOAD_FOLDER, OUTPUT_FOLDER)
        pipeline.scheduler()
    except Exception as e:
        logging.error(f"Failed to start the pipeline: {e}")
