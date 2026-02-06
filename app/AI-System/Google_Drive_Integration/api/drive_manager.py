import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

class GoogleDriveManager:
    def __init__(self, credentials_path=None, token_path=None):
        """
        Initialize Google Drive API connection
        Args:
            credentials_path: Path to credentials.json file
            token_path: Path to token.json file for persistent auth
        """
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.creds = None
        
        # Default paths
        if not credentials_path:
            config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
            # หาไฟล์ credentials ที่ขึ้นต้นด้วย client_secret_
            credentials_files = [
                f for f in os.listdir(config_dir) 
                if f.startswith('client_secret_') and f.endswith('.json')
            ]
            if credentials_files:
                credentials_path = os.path.join(config_dir, credentials_files[0])
            else:
                credentials_path = os.path.join(config_dir, 'credentials.json')
        if not token_path:
            token_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'token.json')
        
        # Load existing token
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(credentials_path):
                    raise FileNotFoundError(f"Credentials file not found at {credentials_path}")
                
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())
        
        # Build Drive service
        self.service = build('drive', 'v3', credentials=self.creds)
        print("[CONNECTED] Google Drive API")

    def upload_file(self, file_path, folder_id=None, description=""):
        """
        Upload a file to Google Drive
        Args:
            file_path: Local path to file
            folder_id: Google Drive folder ID (optional)
            description: File description
        Returns:
            File information dictionary
        """
        file_name = os.path.basename(file_path)
        
        file_metadata = {
            'name': file_name,
            'description': description
        }
        
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        media = MediaFileUpload(file_path, resumable=True)
        
        try:
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,size,mimeType,webViewLink'
            ).execute()
            
            print(f"[UPLOAD] {file_name} -> {file.get('webViewLink')}")
            return file
            
        except Exception as e:
            print(f"[ERROR] Upload failed: {e}")
            return None

    def list_files(self, folder_id=None, query=""):
        """
        List files in Google Drive
        Args:
            folder_id: Folder ID to list contents (optional)
            query: Search query string
        Returns:
            List of file information
        """
        try:
            # Build query
            q = "trashed=false"
            if folder_id:
                q += f" and '{folder_id}' in parents"
            if query:
                q += f" and name contains '{query}'"
            
            results = self.service.files().list(
                q=q,
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, size, webViewLink, createdTime)"
            ).execute()
            
            items = results.get('files', [])
            print(f"[FOUND] {len(items)} files")
            return items
            
        except Exception as e:
            print(f"[ERROR] List failed: {e}")
            return []

    def download_file(self, file_id, output_path):
        """
        Download a file from Google Drive
        Args:
            file_id: Google Drive file ID
            output_path: Local path to save file
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            
            with open(output_path, 'wb') as file:
                downloader = MediaIoBaseDownload(file, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print(f"[DOWNLOAD] {int(status.progress() * 100)}%")
            
            print(f"[SUCCESS] Downloaded to {output_path}")
            
        except Exception as e:
            print(f"[ERROR] Download failed: {e}")

    def create_folder(self, folder_name, parent_folder_id=None):
        """
        Create a folder in Google Drive
        Args:
            folder_name: Name of the folder
            parent_folder_id: Parent folder ID (optional)
        Returns:
            Folder information
        """
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_folder_id:
            folder_metadata['parents'] = [parent_folder_id]
        
        try:
            folder = self.service.files().create(
                body=folder_metadata,
                fields='id,name,mimeType,webViewLink'
            ).execute()
            
            print(f"[FOLDER] Created {folder_name} -> {folder.get('webViewLink')}")
            return folder
            
        except Exception as e:
            print(f"[ERROR] Folder creation failed: {e}")
            return None

    def delete_file(self, file_id):
        """
        Delete a file from Google Drive
        Args:
            file_id: Google Drive file ID
        """
        try:
            self.service.files().delete(fileId=file_id).execute()
            print(f"[DELETED] File {file_id}")
            
        except Exception as e:
            print(f"[ERROR] Delete failed: {e}")

    def search_files(self, query):
        """
        Search for files in Google Drive
        Args:
            query: Search query
        Returns:
            List of matching files
        """
        return self.list_files(query=query)

if __name__ == "__main__":
    # Example usage
    try:
        drive = GoogleDriveManager()
        
        # Create a test folder
        folder = drive.create_folder("Diva AI Generated Content")
        if folder:
            folder_id = folder['id']
            
            # List files
            files = drive.list_files()
            print(f"Found {len(files)} files")
            
    except Exception as e:
        print(f"Error: {e}")
