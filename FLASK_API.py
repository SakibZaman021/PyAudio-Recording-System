from flask import Flask, request, jsonify
from singleton_recorder import AudioRecorder
from singleton_user import UserSingleton
import atexit
import logging

# Initialize Flask app and logging
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


recorder = AudioRecorder.getInstance()
recorder.recover_temp_files()
@atexit.register
def server_shutdown():
    if recorder.is_recording:
        recorder.stop_audio()  # Ensure recording is stopped and saved on shutdown
    logging.info("Server Closing")

import threading
from datetime import datetime



@app.route('/api/record/start', methods=['POST'])
def start_recording():
    try:
        data = request.get_json()

        # Validate that all required fields are present
        required_fields = ["id", "hospital", "doc_id", "start_time", "date"]
        if not all(key in data for key in required_fields):
            logging.error("Missing required data fields")
            return jsonify({'message': 'Missing required data fields'}), 400

        # Extract relevant data
        user_id = data["id"]
        hospital = data["hospital"]
        doctor_id = data["doc_id"]
        start_time = data["start_time"]
        date = data["date"]

        logging.info(f"Received data: {data}")

        # Initialize AudioRecorder instance
        recorder = AudioRecorder.getInstance()

        # If a recording is already in progress, stop it and adjust the new start time
        if recorder.is_recording:
            logging.info("Stopping current recording before starting a new one.")
            previous_end_time = datetime.now().strftime("%H_%M")  # End time of the current recording
            recorder.stop_audio(previous_end_time)

            # Use the end time of the previous recording as the start time for the new recording
            start_time = previous_end_time
            logging.info(f"New recording will start at {start_time}.")

        # Initialize user and start the new recording in a separate thread
        user = UserSingleton.getInstance(user_id, hospital, doctor_id)
        
        # Start recording in a new thread
        recording_thread = threading.Thread(target=recorder.start_audio, args=(user, start_time, date))
        recording_thread.daemon = True  # Ensures thread closes when the main program exits
        recording_thread.start()

        return jsonify({'message': f'Recording started successfully for patient {user_id}', 'patient_id': user_id}), 200

    except Exception as e:
        logging.error(f"Error in start_recording function: {e}")
        return jsonify({'message': 'An error occurred while starting the recording.'}), 500



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
