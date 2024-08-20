from flask import Flask, request, jsonify
from Recorder_API import AudioRecorder
from singleton_user import UserSingleton
import atexit
from werkzeug.utils import secure_filename
import logging
import traceback

# Initialize Flask app and logging
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@atexit.register
def server_shutdown():
    logging.info("Server Closing")

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

        # Initialize UserSingleton and AudioRecorder instances
        try:
            user = UserSingleton.getInstance(user_id, hospital, doctor_id)
            recorder = AudioRecorder.getInstance()
        except Exception as e:
            logging.error(f"Error initializing instances: {e}")
            return jsonify({'message': 'Error initializing recording components'}), 500

        # Stop the previous recording and start a new one
        try:
            if recorder.is_recording:
                logging.info(f"Stopping previous recording.")
                previous_end_time = start_time  # Use the start time of the new patient as the end time of the previous recording
                recorder.stop_audio(previous_end_time)
                logging.info(f"Previous recording stopped at {previous_end_time}.")

            logging.info(f"Starting new recording for patient {user_id}.")
            recorder.start_audio(user, start_time, date)
            return jsonify({'message': f'Recording started successfully for patient {user_id}', 'patient_id': user_id}), 200

        except Exception as e:
            logging.error(f"Error during recording operations: {e}")
            return jsonify({'message': 'Error during recording operations'}), 500

    except Exception as e:
        logging.error(f"Error in handle_recording function: {e}")
        return jsonify({'message': 'An error occurred while starting the recording.'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)