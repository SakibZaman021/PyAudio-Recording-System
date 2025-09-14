import os
import logging
import time
import base64
from pydub import AudioSegment
from singleton_recorder import INPUT_FOLDER

INPUT_FOLDER = 'd:/input_wav_files'
OUTPUT_FOLDER = 'd:/converted_base64_files'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

class AudioReconverter:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def enhance_audio(self, audio):
        # Normalize the audio to ensure consistent volume
        audio = audio.normalize()
        # Optionally, apply other effects like a simple bass boost
        audio = audio.low_pass_filter(900).apply_gain(5)
        return audio

    def convert_audio_to_base64(self, file_name):
        try:
            audio_path = os.path.join(self.input_folder, file_name)
            audio = AudioSegment.from_file(audio_path, format="wav")
            
            # Enhance the audio (if needed)
            audio = self.enhance_audio(audio)

            # Export the enhanced audio to bytes
            audio_bytes = audio.export(format="wav").read()

            # Encode the bytes to Base64
            base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
            
            # Save the Base64 string to a .txt file
            output_file_name = os.path.splitext(file_name)[0] + ".txt"
            output_path = os.path.join(self.output_folder, output_file_name)

            with open(output_path, 'w') as f:
                f.write(base64_audio)

            print(f"Converted and saved Base64 audio to {output_path}")
            return output_path

        except Exception as e:
            print(f"Failed to convert audio file {file_name} to Base64: {e}")
            return None

    def process_files(self):
        for file_name in os.listdir(self.input_folder):
            if file_name.endswith('.wav'):
                output_path = self.convert_audio_to_base64(file_name)
                if output_path:
                    os.remove(os.path.join(self.input_folder, file_name))
                    logging.info(f"Deleted original MP3 file: {file_name}")
                
    def scheduler(self, interval=10):
        while True:
            try:
                logging.info("Checking for files to process...")
                self.process_files()
            except Exception as e:
                logging.error(f"Error during scheduled operation: {e}")
            
            time.sleep(interval)

if __name__ == "__main__":
    reconverter = AudioReconverter(INPUT_FOLDER, OUTPUT_FOLDER)
    reconverter.scheduler()
