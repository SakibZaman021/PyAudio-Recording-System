from pydub import AudioSegment
import os
import time
import logging

INPUT_FOLDER = 'input_wav_files'
OUTPUT_FOLDER = 'compressed_audio_files'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Set up logging
logging.basicConfig(level=logging.INFO)

class AudioCompressor:
    def __init__(self, input_folder, output_folder, target_format='mp3', bitrate='192k', sample_rate=16000):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.target_format = target_format
        self.bitrate = bitrate
        self.sample_rate = sample_rate

    def compress_audio(self, file_name):
        try:
            audio_path = os.path.join(self.input_folder, file_name)
            audio = AudioSegment.from_wav(audio_path)
            
            # Set the frame rate
            audio = audio.set_frame_rate(self.sample_rate)
            
            # Normalize the audio to ensure consistent volume
            audio = audio.normalize()
            
            output_file_name = os.path.splitext(file_name)[0] + f".{self.target_format}"
            output_path = os.path.join(self.output_folder, output_file_name)

            # Export with a high bitrate
            audio.export(output_path, format=self.target_format, bitrate=self.bitrate)
            
            logging.info(f"Compressed and saved file to {output_path}")

            # Delete the original WAV file after successful conversion
            os.remove(audio_path)
            logging.info(f"Deleted original file {audio_path}")

            return output_path

        except Exception as e:
            logging.error(f"Failed to compress audio file {file_name}: {e}")
            return None

    def process_files(self):
        logging.info("Checking for files in input folder...")
        files = os.listdir(self.input_folder)
        if not files:
            logging.info("No files found in the input folder.")
        else:
            for file_name in files:
                if file_name.endswith('.wav'):
                    logging.info(f"Processing file: {file_name}")
                    self.compress_audio(file_name)

    def scheduler(self, interval=6):  # Default interval set to 600 seconds (10 minutes)
        while True:
            try:
                logging.info("Checking for files to process...")
                self.process_files()
            except Exception as e:
                logging.error(f"Error during scheduled operation: {e}")
            time.sleep(interval)

if __name__ == "__main__":
    try:
        compressor = AudioCompressor(INPUT_FOLDER, OUTPUT_FOLDER)
        compressor.scheduler()  # Start the scheduler
    except Exception as e:
        logging.error(f"Failed to start the compressor: {e}")
