import sys
import os
import logging
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QComboBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime
from singleton_recorder import AudioRecorder
from singleton_user import UserSingleton

# Configure logging to file for debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('recorder.log'),
        logging.StreamHandler()
    ]
)

class RecorderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AIMScribe")
        self.setGeometry(200, 100, 400, 600)
        try:
            self.recorder = AudioRecorder.getInstance()
            os.makedirs('input_wav_files', exist_ok=True)
            os.makedirs('temp_wav_files', exist_ok=True)
            self.recorder.recover_temp_files()
        except Exception as e:
            logging.error(f"Failed to initialize recorder: {e}")
            QMessageBox.critical(self, "Initialization Error", f"Cannot initialize recorder: {str(e)}")
            sys.exit(1)
        self.recording = False
        self.timer_count = 600  # 10 minutes in seconds
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Apply stylish stylesheet
        central_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f5f5f5, stop:1 #ffffff);
                border-radius: 10px;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit, QSpinBox, QComboBox {
                border: 2px solid #26a69a;
                border-radius: 8px;
                padding: 6px;
                font-size: 14px;
                background-color: #ffffff;
                min-width: 200px;
                max-width: 200px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                border-color: #ff7043;
                background-color: #e0f2f1;
            }
            QLineEdit:hover, QSpinBox:hover, QComboBox:hover {
                border-color: #ff8a65;
            }
            QLabel {
                font-size: 16px;
                color: #00695c;
                font-weight: bold;
                padding: 4px;
                qproperty-alignment: AlignCenter;
            }
            QPushButton#startButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #26a69a, stop:1 #43a047);
                color: white;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton#startButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1e7d71, stop:1 #2e7d32);
            }
            QPushButton#startButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #155a4e, stop:1 #1b5e20);
            }
            QPushButton#stopButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ff7043, stop:1 #ef5350);
                color: white;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton#stopButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f4511e, stop:1 #e53935);
            }
            QPushButton#stopButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #bf360c, stop:1 #c62828);
            }
            QPushButton:disabled {
                background: #b0bec5;
                color: #78909c;
            }
            #timerLabel {
                font-size: 16px;
                color: #ff7043;
                font-weight: bold;
                border: 2px solid #ff8a65;
                border-radius: 8px;
                padding: 6px;
                background-color: #fff3e0;
                min-width: 150px;
                qproperty-alignment: AlignCenter;
            }
            #statusLabel {
                font-size: 14px;
                color: #00695c;
                padding: 4px;
                background-color: #e0f7fa;
                border-radius: 5px;
                min-width: 200px;
                qproperty-alignment: AlignCenter;
            }
            #headerLabel {
                font-size: 24px;
                color: #004d40;
                font-weight: bold;
                font-family: 'Arial Black', sans-serif;
                padding: 10px;
                background-color: #b2dfdb;
                border-radius: 8px;
                qproperty-alignment: AlignCenter;
            }
        """)

        # Header with AIMScribe branding
        header = QLabel("AIMScribe")
        header.setObjectName("headerLabel")
        main_layout.addWidget(header)
        
        
        # Patient ID
        patient_id_layout = QHBoxLayout()
        patient_id_layout.setAlignment(Qt.AlignCenter)
        patient_id_label = QLabel("Patient_ID")
        self.patient_id_input = QLineEdit()
        patient_id_layout.addWidget(patient_id_label)
        patient_id_layout.addWidget(self.patient_id_input)
        main_layout.addLayout(patient_id_layout)

        # Patient Name
        name_layout = QHBoxLayout()
        name_layout.setAlignment(Qt.AlignCenter)
        name_label = QLabel("Patient_Name")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        main_layout.addLayout(name_layout)

        # Doctor ID
        doctor_layout = QHBoxLayout()
        doctor_layout.setAlignment(Qt.AlignCenter)
        doctor_label = QLabel("Doctor_ID")
        self.doctor_input = QLineEdit()
        doctor_layout.addWidget(doctor_label)
        doctor_layout.addWidget(self.doctor_input)
        main_layout.addLayout(doctor_layout)
        # Hospital
        hospital_layout = QHBoxLayout()
        hospital_layout.setAlignment(Qt.AlignCenter)    
        hospital_label = QLabel("Hospital")
        self.hospital_input = QLineEdit()
        hospital_layout.addWidget(hospital_label)
        hospital_layout.addWidget(self.hospital_input)
        main_layout.addLayout(hospital_layout)

        # Patient Age
        age_layout = QHBoxLayout()
        age_layout.setAlignment(Qt.AlignCenter)
        age_label = QLabel("Age")
        self.age_input = QSpinBox()
        self.age_input.setRange(0, 150)
        age_layout.addWidget(age_label)
        age_layout.addWidget(self.age_input)
        main_layout.addLayout(age_layout)

        # Patient Sex
        gender_layout = QHBoxLayout()
        gender_layout.setAlignment(Qt.AlignCenter)
        gender_label = QLabel("Gender")
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(self.gender_input)
        main_layout.addLayout(gender_layout)
        
        # Start Time
        time_layout = QHBoxLayout()
        time_layout.setAlignment(Qt.AlignCenter)
        time_label = QLabel("Start Time (HH:MM):")
        self.time_input = QLineEdit(datetime.now().strftime("%H:%M"))
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_input)
        main_layout.addLayout(time_layout)

        # Date
        date_layout = QHBoxLayout()
        date_layout.setAlignment(Qt.AlignCenter)
        date_label = QLabel("Date (YYYY-MM-DD):")
        self.date_input = QLineEdit(datetime.now().strftime("%Y-%m-%d"))
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input)
        main_layout.addLayout(date_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        self.start_button = QPushButton("Start Recording")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        main_layout.addLayout(button_layout)

        # Timer Display
        self.timer_label = QLabel("Recording Time: Not Recording")
        self.timer_label.setObjectName("timerLabel")
        main_layout.addWidget(self.timer_label)

        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")
        main_layout.addWidget(self.status_label)

        # Timer for countdown
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        central_widget.setLayout(main_layout)

    def start_recording(self):
        patient_id = self.patient_id_input.text().strip()
        patient_name = self.name_input.text().strip()
        doctor_id = self.doctor_input.text().strip()
        hospital = self.hospital_input.text().strip()
        age = self.age_input.value()
        gender = self.gender_input.currentText()
        start_time = self.time_input.text().strip()
        date = self.date_input.text().strip()

        if not all([patient_id, patient_name, doctor_id, hospital, start_time, date]):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        try:
            datetime.strptime(start_time, "%H:%M")
            start_time = start_time.replace(":", "_")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Start Time must be in HH:MM format.")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
            date = date.replace("-", "_")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Date must be in YYYY-MM-DD format.")
            return

        try:
            # Use a dummy hospital or prompt for it if needed
              # Replace with actual input if required
            user = UserSingleton.getInstance(patient_id, hospital, doctor_id)

            if self.recorder.is_recording:
                self.recorder.stop_audio(start_time)
                self.recording = False
                self.timer.stop()
                self.timer_label.setText("Recording Time: Not Recording")
                self.stop_button.setEnabled(False)
                self.start_button.setEnabled(True)

            self.recording = True
            self.timer_count = 600
            self.timer.start(1000)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.status_label.setText(f"Recording started for patient {patient_id} at {start_time} on {date}")
            self.update_timer()

            recording_thread = threading.Thread(target=self.recorder.start_audio, args=(user, start_time, date))
            recording_thread.daemon = True
            recording_thread.start()

            self.patient_id_input.clear()
            self.hospital_input.clear()
            self.name_input.clear()
            self.doctor_input.clear()
            self.age_input.setValue(0)
            self.gender_input.setCurrentIndex(0)
            self.time_input.clear()
            self.date_input.clear()
            
        except Exception as e:
            logging.error(f"Failed to start recording: {e}")
            QMessageBox.critical(self, "Recording Error", f"Failed to start recording: {str(e)}")
            self.status_label.setText("Recording failed")
            self.recording = False
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def stop_recording(self):
        try:
            if self.recorder.is_recording:
                self.recorder.stop_audio()
                self.recording = False
                self.timer.stop()
                self.timer_label.setText("Recording Time: Stopped")
                self.status_label.setText("Recording stopped and saved")
                self.start_button.setEnabled(True)
                self.stop_button.setEnabled(False)
            else:
                self.status_label.setText("No recording in progress")
        except Exception as e:
            logging.error(f"Failed to stop recording: {e}")
            QMessageBox.critical(self, "Recording Error", f"Failed to stop recording: {str(e)}")
            self.status_label.setText("Stop failed")

    def update_timer(self):
        if self.recording:
            self.timer_count -= 1
            minutes = self.timer_count // 60
            seconds = self.timer_count % 60
            self.timer_label.setText(f"Recording Time: {minutes:02d}:{seconds:02d}")
            if self.timer_count <= 0:
                self.stop_recording()
        else:
            self.timer.stop()
            self.timer_label.setText("Recording Time: Not Recording")

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = RecorderWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Application failed to start: {e}")
        print(f"Error: {e}")