

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()

gauth.LocalWebserverAuth()


drive = GoogleDrive(gauth)



from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import os


SCOPES = ['https://www.googleapis.com/auth/drive.file']
DRIVE_FOLDER_ID = "1_Be4w3kORi4vkcyeJn7tu7PIiEDQDLzq"  
MONITORED_FOLDER = r"d:\input_wav_files" 


def authenticate_google_drive():
   
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If credentials are not valid, initiate OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save new credentials for future use
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def upload_file_to_drive(file_path, drive_folder_id):

    \
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return

    try:
        with open(file_path, 'rb') as f: 
            pass
    except Exception as e:
        print(f"Error accessing file {file_path}: {e}")
        return
    
      
    service = authenticate_google_drive()

    file_name = os.path.basename(file_path)
    print(f"Uploading {file_name} to Google Drive folder {drive_folder_id}...")

    file_metadata = {
        'name': file_name,
        'parents': [drive_folder_id]  # Specify the folder ID
    }
    media = MediaFileUpload(file_path, resumable=True)

    try:
        uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"File uploaded successfully. File ID: {uploaded_file['id']}")
    except Exception as e:
        print(f"An error occurred during upload: {e}")
        
        
        
class FileEventHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.mp3', '.wav', '.flac')):
            print(f"New file detected: {event.src_path}")
            time.sleep(2)  
            upload_file_to_drive(event.src_path, DRIVE_FOLDER_ID)

def monitor_folder():
    if not os.path.exists(MONITORED_FOLDER):
        os.makedirs(MONITORED_FOLDER)

    print(f"Monitoring folder: {MONITORED_FOLDER} for new audio files...")
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, MONITORED_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_folder()
    # # Replace 'audio.mp3' with the path of the file you want to upload
    # file_to_upload = input("Enter the full path of the audio file to upload: ").strip()

    # if os.path.exists(file_to_upload):
    #     upload_file_to_drive(file_to_upload, DRIVE_FOLDER_ID)
    # else:
    #     print("File not found. Please check the path and try again.")
    







# import os
# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from google.oauth2.credentials import Credentials

# # Folder to monitor for new audio files
# MONITORED_FOLDER = "C:/uploaded_audio_files"
# CREDENTIALS_FILE = "client_secrets.json"
# TOKEN_FILE = "token.json"

# class GoogleDriveUploader:
#     def __init__(self):
#         self.service = self.authenticate_drive_api()

#     def authenticate_drive_api(self):
#         """Authenticate and build the Google Drive service."""
#         creds = None
#         if os.path.exists(TOKEN_FILE):
#             creds = Credentials.from_authorized_user_file(TOKEN_FILE, scopes=["https://www.googleapis.com/auth/drive"])
#         if not creds or not creds.valid:
#             raise ValueError("Missing or invalid credentials. Please authenticate.")
#         return build('drive', 'v3', credentials=creds)

#     def upload_file(self, file_path):
#         """Uploads a file to Google Drive."""
#         file_name = os.path.basename(file_path)
#         print(f"Uploading {file_name} to Google Drive...")
#         media = MediaFileUpload(file_path, resumable=True)
#         file_metadata = {'name': file_name}
#         try:
#             uploaded_file = self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()
#             print(f"Uploaded {file_name}, File ID: {uploaded_file['id']}")
#         except Exception as e:
#             print(f"Failed to upload {file_name}. Error: {e}")

# class NewFileHandler(FileSystemEventHandler):
#     def __init__(self, uploader):
#         self.uploader = uploader

#     def on_created(self, event):
#         if not event.is_directory and event.src_path.endswith(('.mp3', '.wav', '.flac')):
#             print(f"New file detected: {event.src_path}")
#             self.uploader.upload_file(event.src_path)

# def monitor_folder(folder_path, uploader):
#     """Monitors a folder for new files and uploads them to Google Drive."""
#     event_handler = NewFileHandler(uploader)
#     observer = Observer()
#     observer.schedule(event_handler, folder_path, recursive=False)
#     observer.start()
#     print(f"Monitoring folder: {folder_path} for new audio files...")
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()

# if __name__ == "__main__":
#     if not os.path.exists(MONITORED_FOLDER):
#         os.makedirs(MONITORED_FOLDER)

#     uploader = GoogleDriveUploader()
#     monitor_folder(MONITORED_FOLDER, uploader)
