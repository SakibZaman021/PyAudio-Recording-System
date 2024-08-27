from pydub import AudioSegment
import os

INPUT_FOLDER = 'd:\output_denoised_files'
OUTPUT_FOLDER = 'd:\converted_wav_files'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

class AudioReconverted:
    def __init__(self, input_folder, output_folder, target_format='wav', sample_rate=16100):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.target_format = target_format
        self.sample_rate = sample_rate

    def enhance_audio(self, audio):
        """
        Enhances the audio by applying normalization and any other desired effects.
        """
        # Normalize the audio to ensure consistent volume
        audio = audio.normalize()

        # Further enhancements can be added here, such as equalization
        # Example: Increase bass (This requires additional libraries like pydub's effects or numpy)
        audio = audio.low_pass_filter(900).apply_gain(5)  # Simple bass boost

        return audio

    def reconvert_audio(self, file_name):
        try:
            audio_path = os.path.join(self.input_folder, file_name)
            audio = AudioSegment.from_file(audio_path, format="wav")
            
            # Enhance the audio
            audio = self.enhance_audio(audio)

            # Set the frame rate back to the original sample rate
            audio = audio.set_frame_rate(self.sample_rate)
            
            output_file_name = os.path.splitext(file_name)[0] + f".{self.target_format}"
            output_path = os.path.join(self.output_folder, output_file_name)

            # Export as WAV
            audio.export(output_path, format=self.target_format)
            
            print(f"Reconverted and saved file to {output_path}")
            return output_path

        except Exception as e:
            print(f"Failed to reconvert audio file {file_name}: {e}")
            return None

    def process_files(self):
        for file_name in os.listdir(self.input_folder):
            if file_name.endswith('.wav'):
                self.reconvert_audio(file_name)

if __name__ == "__main__":
    reconverted = AudioReconverted(INPUT_FOLDER, OUTPUT_FOLDER)
    reconverted.process_files()
