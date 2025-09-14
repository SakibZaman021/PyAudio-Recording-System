from flask import Flask, request, jsonify
from singleton_recorder import AudioRecorder
from singleton_user import UserSingleton
import atexit
import logging
import threading
from datetime import datetime
import uuid

# Initialize Flask app and logging
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Thread-safe recorder initialization
_recorder_lock = threading.RLock()
recorder = None

def get_recorder():
    global recorder
    with _recorder_lock:
        if recorder is None:
            recorder = AudioRecorder.getInstance()
            recorder.recover_temp_files()
    return recorder

@atexit.register
def server_shutdown():
    try:
        recorder_instance = get_recorder()
        if recorder_instance.is_recording:
            recorder_instance.stop_audio()
        logging.info("Server Closing - Recording stopped safely")
    except Exception as e:
        logging.error(f"Error during server shutdown: {e}")

def quick_validate(data):
    """Fast validation - only check essentials"""
    if not isinstance(data, dict):
        return False, "Invalid JSON format"
    
    required = ["id", "hospital", "doc_id", "start_time", "date"]
    missing = [f for f in required if f not in data or not str(data[f]).strip()]
    
    if missing:
        return False, f"Missing or empty fields: {', '.join(missing)}"
    
    return True, {
        "id": str(data["id"]).strip(),
        "hospital": str(data["hospital"]).strip(),
        "doc_id": str(data["doc_id"]).strip(),
        "start_time": str(data["start_time"]).strip(),
        "date": str(data["date"]).strip()
    }

@app.route('/api/record/start', methods=['POST'])
def start_recording():
    request_id = str(uuid.uuid4())[:8]
    
    try:
        # Fast JSON parsing
        data = request.get_json(force=True)
        if not data:
            return jsonify({
                'message': 'No JSON data provided',
                'request_id': request_id
            }), 400

        # Quick validation
        is_valid, result = quick_validate(data)
        if not is_valid:
            return jsonify({
                'message': result,
                'request_id': request_id
            }), 400
        
        validated_data = result
        user_id = validated_data["id"]
        hospital = validated_data["hospital"]
        doctor_id = validated_data["doc_id"]
        start_time = validated_data["start_time"]
        date = validated_data["date"]

        # Get recorder instance
        recorder_instance = get_recorder()
        
        # Initialize response
        response_data = {
            'message': f'Recording started successfully for patient {user_id}',
            'patient_id': user_id,
            'request_id': request_id
        }
        
        # Handle existing recording (thread-safe but fast)
        previous_recording_info = None
        
        with _recorder_lock:
            if recorder_instance.is_recording:
                try:
                    previous_end_time = datetime.now().strftime("%H_%M")
                    previous_recording_info = {
                        'status': 'stopped_and_saved',
                        'end_time': previous_end_time,
                        'stopped_at': datetime.now().isoformat()
                    }
                    
                    recorder_instance.stop_audio(previous_end_time)
                    start_time = previous_end_time  # Update start time
                    
                except Exception as e:
                    logging.error(f"[{request_id}] Error stopping previous recording: {e}")
                    previous_recording_info = {
                        'status': 'stop_failed',
                        'error': str(e)
                    }
            else:
                previous_recording_info = {'status': 'no_previous_recording'}
        
        response_data['previous_recording'] = previous_recording_info

        # Initialize user
        user = UserSingleton.getInstance(user_id, hospital, doctor_id)
        
        # Start recording in background (FAST - like your original)
        def recording_task():
            try:
                logging.info(f"[{request_id}] Starting background recording")
                recorder_instance.start_audio(user, start_time, date)
            except Exception as e:
                logging.error(f"[{request_id}] Background recording failed: {e}")
        
        recording_thread = threading.Thread(target=recording_task, name=f"rec-{request_id}")
        recording_thread.daemon = True
        recording_thread.start()
        
        # Add current recording info
        response_data['current_recording'] = {
            'status': 'started_successfully',
            'start_time': start_time,
            'date': date,
            'started_at': datetime.now().isoformat()
        }
        
        logging.info(f"[{request_id}] Fast response sent, recording starting in background")
        return jsonify(response_data), 200

    except Exception as e:
        logging.error(f"[{request_id}] Error: {e}")
        return jsonify({
            'message': 'An error occurred while starting the recording',
            'error': str(e),
            'request_id': request_id
        }), 500

# Simple health check
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        recorder_instance = get_recorder()
        return jsonify({
            'status': 'healthy',
            'recording_active': recorder_instance.is_recording if recorder_instance else False
        }), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)