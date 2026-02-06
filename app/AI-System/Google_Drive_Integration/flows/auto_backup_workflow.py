import os
import time
from datetime import datetime, timedelta
from pathlib import Path
import schedule

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api.drive_manager import GoogleDriveManager
from utils.file_sync import FileSyncManager

class AutoBackupWorkflow:
    def __init__(self, ai_system_base_path):
        """
        Initialize automatic backup workflow for AI System
        Args:
            ai_system_base_path: Base path of AI System
        """
        self.base_path = Path(ai_system_base_path)
        self.drive_manager = None
        self.sync_manager = None
        self.backup_schedule = []
        
        # Define folders to backup
        self.backup_folders = {
            '01_Image_Generation': {
                'subdirs': ['data', 'outputs'],
                'description': 'AI Generated Images'
            },
            '02_Video_Generation': {
                'subdirs': ['data', 'outputs'], 
                'description': 'AI Generated Videos'
            },
            '03_Audio_Generation': {
                'subdirs': ['data', 'outputs'],
                'description': 'AI Generated Audio'
            },
            '05_Text_Generation': {
                'subdirs': ['data', 'outputs'],
                'description': 'AI Generated Text'
            }
        }

    def initialize_drive_connection(self, credentials_path=None):
        """Initialize Google Drive connection"""
        try:
            self.drive_manager = GoogleDriveManager(credentials_path)
            self.sync_manager = FileSyncManager(str(self.base_path), self.drive_manager)
            print("[WORKFLOW] Drive connection initialized")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to initialize Drive: {e}")
            return False

    def create_backup_structure(self):
        """Create organized backup structure in Google Drive"""
        if not self.drive_manager:
            return False
        
        # Create main backup folder
        main_backup = self.drive_manager.create_folder("Diva AI System Backups")
        if not main_backup:
            return False
        
        main_id = main_backup['id']
        
        # Create subfolders for each module
        for module_name, config in self.backup_folders.items():
            module_folder = self.drive_manager.create_folder(
                f"{module_name} - {config['description']}", 
                main_id
            )
            
            if module_folder:
                # Create date-based subfolders
                today = datetime.now().strftime("%Y-%m")
                date_folder = self.drive_manager.create_folder(today, module_folder['id'])
                print(f"[STRUCTURE] Created: {module_name}/{today}")
        
        return main_id

    def backup_module(self, module_name, create_date_folder=True):
        """
        Backup specific module
        Args:
            module_name: Name of module to backup
            create_date_folder: Whether to create date-based subfolder
        """
        if module_name not in self.backup_folders:
            print(f"[ERROR] Unknown module: {module_name}")
            return
        
        if not self.sync_manager:
            print("[ERROR] Sync manager not initialized")
            return
        
        module_path = self.base_path / module_name
        if not module_path.exists():
            print(f"[ERROR] Module path not found: {module_path}")
            return
        
        config = self.backup_folders[module_name]
        
        # Backup each subdirectory
        for subdir in config['subdirs']:
            subdir_path = module_path / subdir
            if subdir_path.exists():
                print(f"[BACKUP] Starting: {module_name}/{subdir}")
                
                # Create Drive folder structure
                drive_folder = self.drive_manager.create_folder(
                    f"{module_name} - {config['description']}"
                )
                
                if drive_folder:
                    parent_id = drive_folder['id']
                    
                    if create_date_folder:
                        today = datetime.now().strftime("%Y-%m-%d")
                        date_folder = self.drive_manager.create_folder(today, parent_id)
                        if date_folder:
                            parent_id = date_folder['id']
                    
                    # Sync the subdirectory
                    self.sync_manager.sync_folder_to_drive(str(subdir_path), parent_id)

    def backup_all_modules(self):
        """Backup all configured modules"""
        print(f"[BACKUP] Starting full backup at {datetime.now()}")
        
        for module_name in self.backup_folders.keys():
            try:
                self.backup_module(module_name)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"[ERROR] Failed to backup {module_name}: {e}")
        
        print(f"[BACKUP] Full backup completed at {datetime.now()}")

    def schedule_daily_backup(self, time_str="02:00"):
        """
        Schedule daily backup
        Args:
            time_str: Time in HH:MM format (default 2:00 AM)
        """
        schedule.every().day.at(time_str).do(self.backup_all_modules)
        print(f"[SCHEDULE] Daily backup scheduled at {time_str}")

    def schedule_weekly_backup(self, day="sunday", time_str="01:00"):
        """
        Schedule weekly backup
        Args:
            day: Day of week
            time_str: Time in HH:MM format
        """
        getattr(schedule.every(), day.lower()).at(time_str).do(self.backup_all_modules)
        print(f"[SCHEDULE] Weekly backup scheduled for {day} at {time_str}")

    def run_scheduler(self):
        """Run the backup scheduler continuously"""
        print("[SCHEDULER] Starting backup scheduler...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def manual_backup(self, module_name=None):
        """
        Perform manual backup
        Args:
            module_name: Specific module to backup (optional, backups all if None)
        """
        if module_name:
            self.backup_module(module_name)
        else:
            self.backup_all_modules()

    def get_backup_status(self):
        """Get backup status and logs"""
        if self.sync_manager:
            return {
                'sync_log': self.sync_manager.get_sync_log(),
                'last_backup': datetime.now(),
                'scheduled_jobs': len(schedule.jobs)
            }
        return None

if __name__ == "__main__":
    # Example usage
    ai_system_path = r"c:\Divaparadises\Divaparadises\AI-System"
    
    workflow = AutoBackupWorkflow(ai_system_path)
    
    if workflow.initialize_drive_connection():
        # Create backup structure
        workflow.create_backup_structure()
        
        # Manual backup
        workflow.manual_backup()
        
        # Schedule daily backup at 2 AM
        workflow.schedule_daily_backup("02:00")
        
        # Uncomment to run scheduler continuously
        # workflow.run_scheduler()
    else:
        print("Failed to initialize backup workflow")
