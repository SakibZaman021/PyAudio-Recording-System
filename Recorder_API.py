import pyaudio
import wave
from threading import Timer, Lock
from datetime import datetime
import os
import logging

INPUT_FOLDER = 'input_wav_files'
os.makedirs(INPUT_FOLDER, exist_ok=True)

class AudioRecorder:
    _instance = None
    _lock = Lock()

    def __init__(self):
        if AudioRecorder._instance is not None:
            raise Exception("Singleton class exists already")
        else:
            self.user = None
            self.audio = None
            self.stream = None
            self.frames = []
            self.is_recording = False
            self.start_time = None
            self.end_time = None
            self.date = None
            self.timer = None  # Timer for auto-stop

    @staticmethod
    def getInstance():
        with AudioRecorder._lock:
            if AudioRecorder._instance is None:
                AudioRecorder._instance = AudioRecorder()
        return AudioRecorder._instance

    def start_audio(self, user, start_time, date):
        try:
            # Stop the previous recording if one is ongoing
            if self.is_recording:
                self.stop_audio(start_time)

            # Start a new recording session
            self.user = user
            self.is_recording = True
            self.frames = []
            self.start_time = start_time
            self.date = date
            
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024
            )

            logging.info(f"Start recording for {user.userId} at {start_time} on {date}")

            # Start the auto-stop timer (20 minutes)
            if self.timer:
                self.timer.cancel()
            self.timer = Timer(20 * 60, self.stop_audio)  # 20-minute timer
            self.timer.start()

            # Capture audio in a loop
            while self.is_recording:
                try:
                    audio_data = self.stream.read(1024)
                    self.frames.append(audio_data)
                except Exception as e:
                    logging.error(f"Error during recording: {e}")
                    self.is_recording = False

        except Exception as e:
            logging.error(f"Failed to start audio recording: {e}")
            raise

    def stop_audio(self, end_time=None):
        if not self.is_recording:
            logging.warning("No recording to stop.")
            return

        try:
            # Stop the recording session
            self.is_recording = False
            self.end_time = end_time or datetime.now().strftime("%H_%M")

            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            # Save the recorded audio to a file
            sound_file_name = f"{self.user.userId}_{self.user.doctorId}_{self.user.hospital}_{self.start_time}_{self.end_time}_{self.date}.wav"
            raw_file_path = os.path.join(INPUT_FOLDER, sound_file_name)
            with wave.open(raw_file_path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(44100)
                wf.writeframes(b''.join(self.frames))

            logging.info(f"Stopped recording for {self.user.userId}. File saved to {raw_file_path}")

            # Reset the state
            self.user = None
            self.start_time = None
            self.end_time = None
            self.date = None
            self.frames = []

            # Cancel the auto-stop timer if it exists
            if self.timer:
                self.timer.cancel()
                self.timer = None

        except Exception as e:
            logging.error(f"Failed to stop audio recording: {e}")
            raise

    def handle_requests(self):
        while True:
            patient_id = input("Enter Patient ID: ")
            hospital_name = input("Enter Hospital Name: ")
            doctor_id = input("Enter Doctor ID: ")
            start_time = datetime.now().strftime("%H_%M")
            date = datetime.now().strftime("%Y_%m_%d")
            
            user = UserSingleton.getInstance(patient_id, hospital_name, doctor_id)
            self.start_audio(user, start_time, date)


if __name__ == '__main__':
    recorder = AudioRecorder.getInstance()
    recorder.handle_requests()
