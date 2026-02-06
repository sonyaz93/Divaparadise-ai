import os
import shutil
from datetime import datetime
from pathlib import Path

class FileSyncManager:
    def __init__(self, local_base_path, drive_manager):
        """
        Initialize file synchronization between local and Google Drive
        Args:
            local_base_path: Base path for local files
            drive_manager: GoogleDriveManager instance
        """
        self.local_base = Path(local_base_path)
        self.drive = drive_manager
        self.sync_log = []
        
    def sync_folder_to_drive(self, local_folder_path, drive_parent_id=None):
        """
        Sync entire local folder to Google Drive
        Args:
            local_folder_path: Path to local folder
            drive_parent_id: Parent folder ID in Drive (optional)
        """
        local_path = Path(local_folder_path)
        if not local_path.exists():
            print(f"[ERROR] Local folder not found: {local_path}")
            return
        
        # Create Drive folder with same name
        drive_folder = self.drive.create_folder(
            local_path.name, 
            drive_parent_id
        )
        
        if not drive_folder:
            return
            
        drive_folder_id = drive_folder['id']
        
        # Sync all files and subfolders
        for item in local_path.rglob('*'):
            if item.is_file():
                # Create subfolder structure if needed
                relative_path = item.relative_to(local_path)
                parent_id = self._ensure_folder_structure(relative_path.parent, drive_folder_id)
                
                # Upload file
                result = self.drive.upload_file(
                    str(item),
                    parent_id,
                    f"Synced from {relative_path} at {datetime.now()}"
                )
                
                if result:
                    self.sync_log.append({
                        'action': 'upload',
                        'file': str(relative_path),
                        'drive_id': result['id'],
                        'timestamp': datetime.now()
                    })
        
        print(f"[SYNC] Completed sync of {local_folder_path}")
        return drive_folder_id

    def sync_from_drive(self, drive_folder_id, local_destination_path):
        """
        Sync files from Google Drive to local folder
        Args:
            drive_folder_id: Drive folder ID
            local_destination_path: Local destination path
        """
        local_dest = Path(local_destination_path)
        local_dest.mkdir(parents=True, exist_ok=True)
        
        # Get all files in Drive folder
        files = self.drive.list_files(drive_folder_id)
        
        for file_info in files:
            if file_info['mimeType'] != 'application/vnd.google-apps.folder':
                # Download file
                file_name = file_info['name']
                local_file_path = local_dest / file_name
                
                self.drive.download_file(file_info['id'], str(local_file_path))
                
                self.sync_log.append({
                    'action': 'download',
                    'file': file_name,
                    'drive_id': file_info['id'],
                    'local_path': str(local_file_path),
                    'timestamp': datetime.now()
                })
        
        print(f"[SYNC] Downloaded {len(files)} files to {local_destination_path}")

    def _ensure_folder_structure(self, folder_path, parent_id):
        """
        Ensure folder structure exists in Drive
        Args:
            folder_path: Relative path from root
            parent_id: Starting parent folder ID
        Returns:
            Final folder ID
        """
        current_id = parent_id
        
        for folder_name in folder_path.parts:
            # Check if folder exists
            existing = self.drive.list_files(current_id, folder_name)
            
            if existing and existing[0]['mimeType'] == 'application/vnd.google-apps.folder':
                current_id = existing[0]['id']
            else:
                # Create new folder
                new_folder = self.drive.create_folder(folder_name, current_id)
                if new_folder:
                    current_id = new_folder['id']
                else:
                    return None
        
        return current_id

    def backup_generated_content(self, content_folder, backup_name=None):
        """
        Backup AI generated content to Google Drive
        Args:
            content_folder: Path to generated content
            backup_name: Custom backup folder name
        """
        content_path = Path(content_folder)
        if not content_path.exists():
            print(f"[ERROR] Content folder not found: {content_folder}")
            return
        
        # Generate backup name
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"AI_Content_Backup_{timestamp}"
        
        print(f"[BACKUP] Starting backup: {backup_name}")
        
        # Sync to Drive
        drive_folder_id = self.sync_folder_to_drive(content_folder)
        
        if drive_folder_id:
            # Rename the folder to backup name
            # Note: This would require additional API calls to update metadata
            print(f"[BACKUP] Completed: {backup_name}")
            return drive_folder_id
        
        return None

    def get_sync_log(self):
        """Get synchronization log"""
        return self.sync_log

    def clear_sync_log(self):
        """Clear synchronization log"""
        self.sync_log = []
