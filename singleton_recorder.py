# # import pyaudio
# # import wave
# # from threading import Timer, Lock
# # from datetime import datetime
# # import os
# # import logging
# # from singleton_user import UserSingleton

# # INPUT_FOLDER = 'input_wav_files'
# # os.makedirs(INPUT_FOLDER, exist_ok=True)

# # class AudioRecorder:
# #     _instance = None
# #     _lock = Lock()

# #     def __init__(self):
# #         if AudioRecorder._instance is not None:
# #             raise Exception("Singleton class exists already")
# #         else:
# #             self.user = None
# #             self.audio = None
# #             self.stream = None
# #             self.frames = []
# #             self.is_recording = False
# #             self.start_time = None
# #             self.end_time = None
# #             self.date = None
# #             self.timer = None  # Timer for auto-stop

# #     @staticmethod
# #     def getInstance():
# #         with AudioRecorder._lock:
# #             if AudioRecorder._instance is None:
# #                 AudioRecorder._instance = AudioRecorder()
# #         return AudioRecorder._instance

# #     def start_audio(self, user, start_time, date):
# #         try:
# #             # Stop the previous recording if one is ongoing
# #             if self.is_recording:
# #                 self.stop_audio(start_time)

# #             # Start a new recording session
# #             self.user = user
# #             self.is_recording = True
# #             self.frames = []
# #             self.start_time = start_time
# #             self.date = date
            
# #             self.audio = pyaudio.PyAudio()
# #             self.stream = self.audio.open(
# #                 format=pyaudio.paInt16,
# #                 channels=2,
# #                 rate=48000,
# #                 input=True,
# #                 frames_per_buffer=1024
# #             )

# #             logging.info(f"Start recording for {user.userId} at {start_time} on {date}")

# #             # Start the auto-stop timer (20 minutes)
# #             if self.timer:
# #                 self.timer.cancel()
# #             self.timer = Timer(20 * 60, self.stop_audio)  # 20-minute timer
# #             self.timer.start()

# #             # Capture audio in a loop
# #             while self.is_recording:
# #                 try:
# #                     audio_data = self.stream.read(1024)
# #                     self.frames.append(audio_data)
# #                 except Exception as e:
# #                     logging.error(f"Error during recording: {e}")
# #                     self.is_recording = False

# #         except Exception as e:
# #             logging.error(f"Failed to start audio recording: {e}")
# #             raise

# #     def stop_audio(self, end_time=None):
# #         if not self.is_recording:
# #             logging.warning("No recording to stop.")
# #             return

# #         try:
# #             # Stop the recording session
# #             self.is_recording = False
# #             self.end_time = end_time or datetime.now().strftime("%H_%M")

# #             self.stream.stop_stream()
# #             self.stream.close()
# #             self.audio.terminate()

# #             # Save the recorded audio to a file
# #             sound_file_name = f"{self.user.userId}_{self.user.doctorId}_{self.user.hospital}_{self.start_time}_{self.end_time}_{self.date}.wav"
# #             raw_file_path = os.path.join(INPUT_FOLDER, sound_file_name)
# #             with wave.open(raw_file_path, "wb") as wf:
# #                 wf.setnchannels(2)
# #                 wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
# #                 wf.setframerate(48000)
# #                 wf.writeframes(b''.join(self.frames))

# #             logging.info(f"Stopped recording for {self.user.userId}. File saved to {raw_file_path}")

# #             # Reset the state
# #             self.user = None
# #             self.start_time = None
# #             self.end_time = None
# #             self.date = None
# #             self.frames = []

# #             # Cancel the auto-stop timer if it exists
# #             if self.timer:
# #                 self.timer.cancel()
# #                 self.timer = None

# #         except Exception as e:
# #             logging.error(f"Failed to stop audio recording: {e}")
# #             raise

# #     def handle_requests(self):
# #         while True:
# #             patient_id = input("Enter Patient ID: ")
# #             hospital_name = input("Enter Hospital Name: ")
# #             doctor_id = input("Enter Doctor ID: ")
# #             start_time = datetime.now().strftime("%H_%M")
# #             date = datetime.now().strftime("%Y_%m_%d")
            
# #             user = UserSingleton.getInstance(patient_id, hospital_name, doctor_id)
# #             self.start_audio(user, start_time, date)


# # if __name__ == '__main__':
# #     recorder = AudioRecorder.getInstance()
# #     recorder.handle_requests()


# import pyaudio
# import wave
# from threading import Timer, Lock
# from datetime import datetime
# import os
# import logging
# from singleton_user import UserSingleton

# INPUT_FOLDER = 'input_wav_files'
# os.makedirs(INPUT_FOLDER, exist_ok=True)

# class AudioRecorder:
#     _instance = None
#     _lock = Lock()

#     def __init__(self):
#         if AudioRecorder._instance is not None:
#             raise Exception("Singleton class exists already")
#         self.user = None
#         self.audio = None
#         self.stream = None
#         self.frames = []
#         self.is_recording = False
#         self.start_time = None
#         self.end_time = None
#         self.date = None
#         self.timer = None

#     @staticmethod
#     def getInstance():
#         with AudioRecorder._lock:
#             if AudioRecorder._instance is None:
#                 AudioRecorder._instance = AudioRecorder()
#         return AudioRecorder._instance

#     def start_audio(self, user, start_time, date):
#         try:
#             if self.is_recording:
#                 self.stop_audio(start_time)

#             self.user = user
#             self.is_recording = True
#             self.frames = []
#             self.start_time = start_time
#             self.date = date
            
#             self.audio = pyaudio.PyAudio()
            
#             # Log available audio devices for debugging
#             for i in range(self.audio.get_device_count()):
#                 dev = self.audio.get_device_info_by_index(i)
#                 logging.info(f"Device {i}: {dev['name']}, "
#                            f"Input Channels: {dev['maxInputChannels']}")

#             # Explicitly specify the input device that supports stereo
#             device_index = None
#             for i in range(self.audio.get_device_count()):
#                 dev = self.audio.get_device_info_by_index(i)
#                 if dev['maxInputChannels'] >= 2:
#                     device_index = i
#                     break
                    
#             if device_index is None:
#                 logging.warning("No stereo input device found!")
            
#             self.stream = self.audio.open(
#                 format=pyaudio.paInt16,
#                 channels=2,
#                 rate=48000,
#                 input=True,
#                 frames_per_buffer=1024,
#                 input_device_index=device_index  # Add device index
#             )

#             # Verify stream configuration
#             logging.info(f"Stream opened with: "
#                         f"Channels: {self.stream._channels}, "
#                         f"Rate: {self.stream._rate}, "
#                         f"Format: {self.stream._format}")

#             logging.info(f"Start recording for {user.userId} at {start_time} on {date}")

#             self.timer = Timer(20 * 60, self.stop_audio)
#             self.timer.start()

#             while self.is_recording:
#                 try:
#                     audio_data = self.stream.read(1024, exception_on_overflow=False)
#                     self.frames.append(audio_data)
#                 except Exception as e:
#                     logging.error(f"Error during recording: {e}")
#                     self.is_recording = False

#         except Exception as e:
#             logging.error(f"Failed to start audio recording: {e}")
#             raise

#     def stop_audio(self, end_time=None):
#         if not self.is_recording:
#             logging.warning("No recording to stop.")
#             return

#         try:
#             self.is_recording = False
#             self.end_time = end_time or datetime.now().strftime("%H_%M")

#             self.stream.stop_stream()
#             self.stream.close()
#             self.audio.terminate()

#             sound_file_name = f"{self.user.userId}_{self.user.doctorId}_{self.user.hospital}_{self.start_time}_{self.end_time}_{self.date}.wav"
#             raw_file_path = os.path.join(INPUT_FOLDER, sound_file_name)
            
#             with wave.open(raw_file_path, "wb") as wf:
#                 wf.setnchannels(2)
#                 wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
#                 wf.setframerate(48000)
#                 wf.writeframes(b''.join(self.frames))

#             logging.info(f"Stopped recording for {self.user.userId}. File saved to {raw_file_path}")

#             # Verify file properties
#             with wave.open(raw_file_path, "rb") as wf:
#                 logging.info(f"Output file properties - "
#                            f"Channels: {wf.getnchannels()}, "
#                            f"Sample width: {wf.getsampwidth()}, "
#                            f"Frame rate: {wf.getframerate()}")

#             self.user = None
#             self.start_time = None
#             self.end_time = None
#             self.date = None
#             self.frames = []

#             if self.timer:
#                 self.timer.cancel()
#                 self.timer = None

#         except Exception as e:
#             logging.error(f"Failed to stop audio recording: {e}")
#             raise

#     def handle_requests(self):
#         while True:
#             patient_id = input("Enter Patient ID: ")
#             hospital_name = input("Enter Hospital Name: ")
#             doctor_id = input("Enter Doctor ID: ")
#             start_time = datetime.now().strftime("%H_%M")
#             date = datetime.now().strftime("%Y_%m_%d")
            
#             user = UserSingleton.getInstance(patient_id, hospital_name, doctor_id)
#             self.start_audio(user, start_time, date)

# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     recorder = AudioRecorder.getInstance()
#     recorder.handle_requests()


import pyaudio
import wave
from threading import Timer, Lock, Thread
from datetime import datetime
import os
import logging
import time
from singleton_user import UserSingleton

INPUT_FOLDER = 'input_wav_files'
TEMP_FOLDER = 'temp_wav_files'  # Temporary folder for periodic saves
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

class AudioRecorder:
    _instance = None
    _lock = Lock()

    def __init__(self):
        if AudioRecorder._instance is not None:
            raise Exception("Singleton class exists already")
        self.user = None
        self.audio = None
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.start_time = None
        self.end_time = None
        self.date = None
        self.timer = None
        self.temp_file = None
        self.save_interval = 30  # Save every 30 seconds
        self.save_thread = None

    @staticmethod
    def getInstance():
        with AudioRecorder._lock:
            if AudioRecorder._instance is None:
                AudioRecorder._instance = AudioRecorder()
        return AudioRecorder._instance

    def _save_temp_audio(self):
        """Periodically save the current frames to a temporary file."""
        while self.is_recording:
            if self.frames:
                try:
                    temp_file_name = f"temp_{self.user.userId}_{self.start_time}_{self.date}.wav"
                    temp_file_path = os.path.join(TEMP_FOLDER, temp_file_name)
                    with wave.open(temp_file_path, "wb") as wf:
                        wf.setnchannels(2)
                        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                        wf.setframerate(48000)
                        wf.writeframes(b''.join(self.frames))
                    logging.info(f"Temporary audio saved to {temp_file_path}")
                except Exception as e:
                    logging.error(f"Error saving temporary audio: {e}")
            # Sleep for the save interval
            for _ in range(self.save_interval * 10):  # Check every 0.1s to allow quick stop
                if not self.is_recording:
                    return
                time.sleep(0.1)

    def start_audio(self, user, start_time, date):
        try:
            if self.is_recording:
                self.stop_audio(start_time)

            self.user = user
            self.is_recording = True
            self.frames = []
            self.start_time = start_time
            self.date = date
            
            self.audio = pyaudio.PyAudio()
            
            # Log available audio devices for debugging
            for i in range(self.audio.get_device_count()):
                dev = self.audio.get_device_info_by_index(i)
                logging.info(f"Device {i}: {dev['name']}, "
                           f"Input Channels: {dev['maxInputChannels']}")

            # Explicitly specify the input device that supports stereo
            device_index = None
            for i in range(self.audio.get_device_count()):
                dev = self.audio.get_device_info_by_index(i)
                if dev['maxInputChannels'] >= 2:
                    device_index = i
                    break
                    
            if device_index is None:
                logging.warning("No stereo input device found!")
            
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=2,
                rate=48000,
                input=True,
                frames_per_buffer=1024,
                input_device_index=device_index
            )

            logging.info(f"Start recording for {user.userId} at {start_time} on {date}")

            # Start the auto-stop timer (20 minutes)
            self.timer = Timer(20 * 60, self.stop_audio)
            self.timer.start()

            # Start the periodic save thread
            self.save_thread = Thread(target=self._save_temp_audio)
            self.save_thread.daemon = True
            self.save_thread.start()

            # Capture audio in a loop
            while self.is_recording:
                try:
                    audio_data = self.stream.read(1024, exception_on_overflow=False)
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
            self.is_recording = False
            self.end_time = end_time or datetime.now().strftime("%H_%M")

            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            # Save the final audio file
            sound_file_name = f"{self.user.userId}_{self.user.doctorId}_{self.user.hospital}_{self.start_time}_{self.end_time}_{self.date}.wav"
            raw_file_path = os.path.join(INPUT_FOLDER, sound_file_name)
            
            with wave.open(raw_file_path, "wb") as wf:
                wf.setnchannels(2)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(48000)
                wf.writeframes(b''.join(self.frames))

            logging.info(f"Stopped recording for {self.user.userId}. File saved to {raw_file_path}")

            # Verify file properties
            with wave.open(raw_file_path, "rb") as wf:
                logging.info(f"Output file properties - "
                           f"Channels: {wf.getnchannels()}, "
                           f"Sample width: {wf.getsampwidth()}, "
                           f"Frame rate: {wf.getframerate()}")

            # Clean up temporary file
            temp_file_name = f"temp_{self.user.userId}_{self.start_time}_{self.date}.wav"
            temp_file_path = os.path.join(TEMP_FOLDER, temp_file_name)
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                logging.info(f"Cleaned up temporary file: {temp_file_path}")

            # Reset state
            self.user = None
            self.start_time = None
            self.end_time = None
            self.date = None
            self.frames = []

            if self.timer:
                self.timer.cancel()
                self.timer = None

            if self.save_thread:
                self.save_thread.join()  # Wait for the save thread to finish
                self.save_thread = None

        except Exception as e:
            logging.error(f"Failed to stop audio recording: {e}")
            raise

    def recover_temp_files(self):

        for temp_file in os.listdir(TEMP_FOLDER):
            if temp_file.startswith("temp_") and temp_file.endswith(".wav"):
                temp_file_path = os.path.join(TEMP_FOLDER, temp_file)
                logging.info(f"Found temporary file: {temp_file_path}")
                # You can decide how to handle recovery (e.g., rename or process further)
                # For now, just log it
                # Example: Rename to a final file with an "incomplete" suffix
                parts = temp_file.split('_')
                user_id = parts[1]
                start_time = parts[2]
                date = parts[3].replace('.wav', '')
                end_time = datetime.now().strftime("%H_%M")
                recovered_file_name = f"{user_id}_unknown_unknown_{start_time}_{end_time}_{date}_incomplete.wav"
                recovered_file_path = os.path.join(INPUT_FOLDER, recovered_file_name)
                os.rename(temp_file_path, recovered_file_path)
                logging.info(f"Recovered temporary file to: {recovered_file_path}")

    def handle_requests(self):
        # Check for temporary files on startup
        self.recover_temp_files()
        while True:
            patient_id = input("Enter Patient ID: ")
            hospital_name = input("Enter Hospital Name: ")
            doctor_id = input("Enter Doctor ID: ")
            start_time = datetime.now().strftime("%H_%M")
            date = datetime.now().strftime("%Y_%m_%d")
            
            user = UserSingleton.getInstance(patient_id, hospital_name, doctor_id)
            self.start_audio(user, start_time, date)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    recorder = AudioRecorder.getInstance()
    recorder.handle_requests()