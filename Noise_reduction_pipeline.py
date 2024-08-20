# # import os
# # import shutil
# # import librosa
# # import soundfile as sf
# # import numpy as np
# # import scipy.signal
# # # import malaya_speech
# # import logging
# # # from malaya_speech import Pipeline
# # # from malaya_speech.utils import load_wav
# # from singleton_recorder import INPUT_FOLDER

# # OUTPUT_FOLDER = 'output_denoised_files'
# # os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# # # model = malaya_speech.noise_reduction.deep_model(model='resnet-unet', quantized=False)


# # def noise_reduction(file_path, noise_reduce=True):
# #     # try:
# #     #     y, sr = load_wav(file_path, sr=44100)

# #     #     if noise_reduce:
# #     #         # Apply Malaya-Speech noise reduction
# #     #         y_denoised = model(y)
# #     #         y_denoised = y_denoised['voice']
# #     #     else:
# #     #         # Apply pre-emphasis
# #     #         y_denoised = librosa.effects.preemphasis(y)
        
# #     #     return y_denoised, sr
# #     # except Exception as e:
# #     #     logging.error(f"Failed to denoise {file_path}: {e}")
# #     #     return None, None


# #     try:
# #         y, sr = librosa.load(file_path, sr=None)

# #         if noise_reduce:
# #             # Apply spectral gating noise reduction
# #             y_denoised = spectral_gating(y, sr)
# #         else:
# #             # Apply pre-emphasis
# #             y_denoised = librosa.effects.preemphasis(y)
        
# #         return y_denoised, sr
# #     except Exception as e:
# #         print(f"Failed to denoise {file_path}: {e}")
# #         return None, None

# # def spectral_gating(y, sr):
# #     # Parameters for spectral gating
# #     noise_clip = y[:sr]  # Use the first second as noise clip
# #     n_fft = 2048
# #     hop_length = 512
# #     win_length = 2048
# #     noise_reduction_factor = 0.5

# #     # Compute STFT of the audio
# #     stft = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
# #     stft_db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

# #     # Compute STFT of the noise clip
# #     noise_stft = librosa.stft(noise_clip, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
# #     noise_stft_db = librosa.amplitude_to_db(np.abs(noise_stft), ref=np.max)

# #     # Calculate the mean noise profile
# #     mean_noise_stft_db = np.mean(noise_stft_db, axis=1, keepdims=True)

# #     # Subtract the mean noise profile from the original audio
# #     stft_db_denoised = stft_db - noise_reduction_factor * mean_noise_stft_db
# #     stft_db_denoised = np.maximum(stft_db_denoised, -80)  # Clamp to minimum of -80 dB

# #     # Convert back to amplitude and inverse STFT
# #     stft_amplitude_denoised = librosa.db_to_amplitude(stft_db_denoised, ref=np.max)
# #     y_denoised = librosa.istft(stft_amplitude_denoised, hop_length=hop_length, win_length=win_length)
    
# #     return y_denoised
# import os
# import shutil
# import librosa
# import soundfile as sf
# import numpy as np
# import noisereduce as nr
# import logging
# from singleton_recorder import INPUT_FOLDER
# from noisereduce.generate_noise import band_limited_noise
# import matplotlib.pyplot as plt
# from pydub import AudioSegment
# import time

# # Path to input and output folders
# # OUTPUT_FOLDER = 'output_denoised_files'
# # os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# # def read_audio(file_name):
# #     try:
# #         # Try reading as a .wav file
# #         data, rate = sf.read(file_name)
# #     except:
# #         # If it fails, try reading with pydub to detect the actual format
# #         audio = AudioSegment.from_file(file_name)
# #         file_path = 'converted_file.wav'
# #         audio.export(file_path, format='wav')
# #         data, rate = sf.read(file_path)
# #     return data, rate

# # def noise_reduction(file_path, noise_reduce=True):
# #     try:
# #         data, rate = read_audio(file_path)

# #         if noise_reduce:
# #             # Add noise for testing purposes
# #             noise_len = 2  # seconds
# #             noise = band_limited_noise(min_freq=2000, max_freq=12000, samples=len(data), samplerate=rate) * 10
# #             noise_clip = noise[:rate * noise_len]
# #             audio_clip_band_limited = data + noise

# #             # Reduce noise
# #             reduced_noise = nr.reduce_noise(y=audio_clip_band_limited, sr=rate, n_std_thresh_stationary=1.5, stationary=True, use_torch=False)
# #             reduced_noise = nr.reduce_noise(y=reduced_noise, sr=rate, thresh_n_mult_nonstationary=2, stationary=False, use_torch=False)
# #         else:
# #             # Apply pre-emphasis
# #             reduced_noise = librosa.effects.preemphasis(data)
        
# #         return reduced_noise, rate
# #     except Exception as e:
# #         logging.error(f"Failed to denoise {file_path}: {e}")
# #         return None, None

# # def process_files():
# #     for sound_file_name in os.listdir(INPUT_FOLDER):
# #         if sound_file_name.endswith('.wav'):
# #             input_file_path = os.path.join(INPUT_FOLDER, sound_file_name)
# #             y_denoised, sr = noise_reduction(input_file_path)

# #             if y_denoised is not None:
# #                 output_file_path = os.path.join(OUTPUT_FOLDER, sound_file_name)
# #                 sf.write(output_file_path, y_denoised, sr)
# #                 os.remove(input_file_path)
# #                 logging.info(f"Processed and removed original file: {sound_file_name}")
# #             else:
# #                 failed_file_path = os.path.join(INPUT_FOLDER, sound_file_name)
# #                 shutil.move(input_file_path, failed_file_path)
# #                 logging.warning(f"Moved failed file to retry: {sound_file_name}")
              

# # def retry_failed_files():
# #     for sound_file_name in os.listdir(INPUT_FOLDER):
# #         if sound_file_name.endswith('.wav'):
# #             failed_file_path = os.path.join(INPUT_FOLDER, sound_file_name)
# #             y_denoised, sr = noise_reduction(failed_file_path)

# #             if y_denoised is not None:
# #                 output_file_path = os.path.join("OUTPUT_FOLDER", sound_file_name)
# #                 sf.write(output_file_path, y_denoised, sr)
# #                 os.remove(failed_file_path)
# #                 logging.info(f"Retried and removed failed file: {sound_file_name}")

# class NoiseReductionPipeline:
#     def __init__(self, input_folder, output_folder):
#         self.input_folder = input_folder
#         self.output_folder = output_folder
#         os.makedirs(self.output_folder, exist_ok=True)

#     def read_audio(self, file_name):
#         try:
#             # Try reading as a .wav file
#             data, rate = sf.read(file_name)
#         except:
#             # If it fails, try reading with pydub to detect the actual format
#             audio = AudioSegment.from_file(file_name)
#             file_path = 'converted_file.wav'
#             audio.export(file_path, format='wav')
#             data, rate = sf.read(file_path)
#         return data, rate

#     def noise_reduction(self, file_path, noise_reduce=True):
#         try:
#             data, rate = self.read_audio(file_path)

#             if noise_reduce:
#                 # Add noise for testing purposes
#                 noise_len = 2  # seconds
#                 noise = band_limited_noise(min_freq=2000, max_freq=12000, samples=len(data), samplerate=rate) * 10
#                 noise_clip = noise[:rate * noise_len]
#                 audio_clip_band_limited = data + noise

#                 # Reduce noise
#                 reduced_noise = nr.reduce_noise(y=audio_clip_band_limited, sr=rate, n_std_thresh_stationary=1.5, stationary=True, use_torch=False)
#                 reduced_noise = nr.reduce_noise(y=reduced_noise, sr=rate, thresh_n_mult_nonstationary=2, stationary=False, use_torch=False)
#             else:
#                 # Apply pre-emphasis
#                 reduced_noise = librosa.effects.preemphasis(data)
            
#             return reduced_noise, rate
#         except Exception as e:
#             logging.error(f"Failed to denoise {file_path}: {e}")
#             return None, None

#     def process_files(self):
#         for sound_file_name in os.listdir(self.input_folder):
#             if sound_file_name.endswith('.wav'):
#                 input_file_path = os.path.join(self.input_folder, sound_file_name)
#                 y_denoised, sr = self.noise_reduction(input_file_path)

#                 if y_denoised is not None:
#                     output_file_path = os.path.join(self.output_folder, sound_file_name)
#                     sf.write(output_file_path, y_denoised, sr)
#                     os.remove(input_file_path)
#                     logging.info(f"Processed and removed original file: {sound_file_name}")
#                 else:
#                     failed_file_path = os.path.join(self.input_folder, f"failed_{sound_file_name}")
#                     shutil.move(input_file_path, failed_file_path)
#                     logging.warning(f"Moved failed file to retry: {sound_file_name}")

#     def retry_failed_files(self):
#         for sound_file_name in os.listdir(self.input_folder):
#             if sound_file_name.startswith('failed_') and sound_file_name.endswith('.wav'):
#                 failed_file_path = os.path.join(self.input_folder, sound_file_name)
#                 y_denoised, sr = self.noise_reduction(failed_file_path)

#                 if y_denoised is not None:
#                     output_file_path = os.path.join(self.output_folder, sound_file_name.replace('failed_', ''))
#                     sf.write(output_file_path, y_denoised, sr)
#                     os.remove(failed_file_path)
#                     logging.info(f"Retried and removed failed file: {sound_file_name}")








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
from Recorder_API import INPUT_FOLDER




# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NoiseReductionPipeline:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
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

    # def noise_reduction(self, file_path, noise_reduce=True):
    #     try:
    #         data, rate = self.read_audio(file_path)
    #         if noise_reduce:
    #             noise_len = 2  # seconds
    #             noise = band_limited_noise(min_freq=2000, max_freq=12000, samples=len(data), samplerate=rate) * 10
    #             noise_clip = noise[:rate * noise_len]
    #             audio_clip_band_limited = data + noise
    #             reduced_noise = nr.reduce_noise(y=audio_clip_band_limited, sr=rate, n_std_thresh_stationary=1.5, stationary=True, use_torch=False)
    #             reduced_noise = nr.reduce_noise(y=reduced_noise, sr=rate, thresh_n_mult_nonstationary=2, stationary=False, use_torch=False)
    #         else:
    #             reduced_noise = librosa.effects.preemphasis(data)
    #         return reduced_noise, rate
    #     except Exception as e:
    #         logging.error(f"Failed to denoise {file_path}: {e}")
    #         return None, None
        
    def noise_reduction(self, file_path, noise_reduce=True):
        try:
            data, rate = self.read_audio(file_path)
            if noise_reduce:
                noise_len = 2  
                noise = band_limited_noise(min_freq=2000, max_freq=12000, samples=len(data), samplerate=rate) * 5  
                noise_clip = noise[:rate * noise_len]
                audio_clip_band_limited = data + noise
                reduced_noise = nr.reduce_noise(y=audio_clip_band_limited, sr=rate,n_std_thresh_stationary=1.0, stationary=True, use_torch=False)
                reduced_noise = nr.reduce_noise(y=reduced_noise, sr=rate, thresh_n_mult_nonstationary=1.5, stationary=False, use_torch=False)
                                            
            else:
                reduced_noise = librosa.effects.preemphasis(data)

            return reduced_noise, rate
        except Exception as e:
            logging.error(f"Failed to denoise {file_path}: {e}")
        return None, None

        
    def process_files(self):
        for sound_file_name in os.listdir(self.input_folder):
            if sound_file_name.endswith('.wav'):
                input_file_path = os.path.join(self.input_folder, sound_file_name)
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
        for sound_file_name in os.listdir(self.input_folder):
            if sound_file_name.startswith('failed_') and sound_file_name.endswith('.wav'):
                failed_file_path = os.path.join(self.input_folder, sound_file_name)
                y_denoised, sr = self.noise_reduction(failed_file_path)
                if y_denoised is not None:
                    output_file_path = os.path.join(self.output_folder, sound_file_name.replace('failed_', ''))
                    sf.write(output_file_path, y_denoised, sr)
                    os.remove(failed_file_path)
                    logging.info(f"Retried and removed failed file: {sound_file_name}")  # Upload the file after processing     

    def scheduler(self, interval=60):
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
        OUTPUT_FOLDER = 'output_denoised_files'
        
        pipeline = NoiseReductionPipeline(INPUT_FOLDER, OUTPUT_FOLDER)
        pipeline.scheduler()
    except Exception as e:
        logging.error(f"Failed to start the pipeline: {e}")
