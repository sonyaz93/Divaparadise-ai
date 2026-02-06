#!/usr/bin/env python3
"""
Demo Auto Backup Script for Diva AI System
สคริปตสำหรับทดสอบและตั้งค่า Auto Backup

Usage: python demo_auto_backup.py
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# เพิ่ม path สำหรับ import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.drive_manager import GoogleDriveManager
from utils.file_sync import FileSyncManager
from flows.auto_backup_workflow import AutoBackupWorkflow

class AutoBackupDemo:
    def __init__(self):
        self.ai_system_path = Path(__file__).parent.parent
        self.workflow = None
        
    def print_header(self):
        """แสดงหัวข้อ"""
        print("🎭 Diva AI System - Auto Backup Demo")
        print("=" * 50)
        print(f"📍 AI System Path: {self.ai_system_path}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    def initialize_workflow(self):
        """เริ่มต้น Auto Backup Workflow"""
        print("🔧 เริ่มต้น Auto Backup Workflow...")
        
        try:
            self.workflow = AutoBackupWorkflow(str(self.ai_system_path))
            
            if self.workflow.initialize_drive_connection():
                print("✅ เชื่อมต่อ Google Drive สำเรจ")
                return True
            else:
                print("❌ ไม่สามารถเชื่อมต่อ Google Drive ได้")
                return False
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return False
    
    def demo_backup_structure(self):
        """สาิตการสร้างครงสร้าง Backup"""
        print("\n📁 สร้างครงสร้าง Backup ใน Google Drive...")
        
        try:
            main_folder_id = self.workflow.create_backup_structure()
            if main_folder_id:
                print("✅ สร้างครงสร้าง Backup สำเรจ")
                print(f"   📂 Main Backup Folder ID: {main_folder_id}")
                return main_folder_id
            else:
                print("❌ ไม่สามารถสร้างครงสร้าง Backup ได้")
                return None
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return None
    
    def demo_manual_backup(self):
        """สาิตการ Backup แบบ Manual"""
        print("\n📤 ทดสอบ Manual Backup...")
        
        # สร้างไฟลทดสอบ
        test_dir = self.ai_system_path / "01_Image_Generation" / "data"
        test_dir.mkdir(parents=True, exist_ok=True)
        
        test_file = test_dir / "demo_backup_test.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(f"""
🎭 Diva AI System - Demo Backup Test File
==========================================

Created: {datetime.now().isoformat()}
Purpose: Testing Auto Backup functionality
Module: 01_Image_Generation
Type: Demo file for backup testing

This file demonstrates the auto backup functionality
of the Diva AI System Google Drive Integration.

Content will be automatically backed up to Google Drive
when the backup workflow is executed.

สวัสดีจาก Diva AI System! 🚀
""")
        
        print(f"✅ สร้างไฟลทดสอบ: {test_file}")
        
        try:
            # ทดสอบ backup module เดียว
            print("📦 เริ่ม backup module: 01_Image_Generation...")
            self.workflow.backup_module("01_Image_Generation")
            print("✅ Manual backup เสรจสิ้น")
            
            # ลบไฟลทดสอบ
            test_file.unlink()
            print("🧹 ลบไฟลทดสอบแล้ว")
            
        except Exception as e:
            print(f"❌ Manual backup ล้มเหลว: {e}")
    
    def demo_schedule_setup(self):
        """สาิตการตั้งค่า Schedule"""
        print("\n⏰ ตั้งค่า Backup Schedule...")
        
        try:
            # ตั้งค่า daily backup
            self.workflow.schedule_daily_backup("02:00")
            print("✅ ตั้งค่า Daily Backup ที่ 02:00 น.")
            
            # ตั้งค่า weekly backup
            self.workflow.schedule_weekly_backup("sunday", "01:00")
            print("✅ ตั้งค่า Weekly Backup วันอาทิตย 01:00 น.")
            
            # แสดงสถานะ
            status = self.workflow.get_backup_status()
            if status:
                print(f"📊 Scheduled Jobs: {status['scheduled_jobs']}")
            
        except Exception as e:
            print(f"❌ การตั้งค่า Schedule ล้มเหลว: {e}")
    
    def demo_file_sync(self):
        """สาิตการใช้งาน File Sync"""
        print("\n🔄 ทดสอบ File Sync...")
        
        try:
            # สร้าง sync manager
            sync_manager = FileSyncManager(str(self.ai_system_path), self.workflow.drive_manager)
            
            # สร้างฟลเดอรทดสอบ
            test_sync_dir = self.ai_system_path / "test_sync_demo"
            test_sync_dir.mkdir(exist_ok=True)
            
            # สร้างไฟลทดสอบ
            for i in range(3):
                test_file = test_sync_dir / f"sync_test_{i+1}.txt"
                with open(test_file, 'w', encoding='utf-8') as f:
                    f.write(f"Sync test file {i+1} - {datetime.now()}")
            
            print(f"✅ สร้างไฟลทดสอบ 3 ไฟลใน {test_sync_dir}")
            
            # ทดสอบ sync
            print("📤 เริ่ม sync ไฟลไป Google Drive...")
            drive_folder_id = sync_manager.sync_folder_to_drive(str(test_sync_dir))
            
            if drive_folder_id:
                print("✅ File Sync สำเรจ")
                
                # แสดง sync log
                sync_log = sync_manager.get_sync_log()
                print(f"📋 Sync Log: {len(sync_log)} รายการ")
                for log_entry in sync_log[-3:]:  # แสดง 3 รายการล่าสุด
                    print(f"   - {log_entry['action']}: {log_entry['file']}")
            
            # ลบฟลเดอรทดสอบ
            import shutil
            shutil.rmtree(test_sync_dir)
            print("🧹 ลบฟลเดอรทดสอบแล้ว")
            
        except Exception as e:
            print(f"❌ File Sync ล้มเหลว: {e}")
    
    def show_usage_examples(self):
        """แสดงตัวอย่างการใช้งาน"""
        print("\n📋 ตัวอย่างการใช้งาน:")
        print("=" * 30)
        
        print("\n1. Manual Backup ทั้งระบบ:")
        print("   from flows.auto_backup_workflow import AutoBackupWorkflow")
        print("   workflow = AutoBackupWorkflow('path/to/ai-system')")
        print("   workflow.initialize_drive_connection()")
        print("   workflow.backup_all_modules()")
        
        print("\n2. Backup module เดียว:")
        print("   workflow.backup_module('01_Image_Generation')")
        
        print("\n3. ตั้งค่า Auto Backup:")
        print("   workflow.schedule_daily_backup('02:00')")
        print("   workflow.run_scheduler()  # รันต่อเนื่อง")
        
        print("\n4. File Sync:")
        print("   from utils.file_sync import FileSyncManager")
        print("   sync = FileSyncManager('local/path', drive_manager)")
        print("   sync.sync_folder_to_drive('folder/to/sync')")
        
        print("\n5. รันจาก Command Line:")
        print("   python demo_auto_backup.py")
        print("   python flows/auto_backup_workflow.py")
    
    def run_demo(self):
        """รันการสาิตทั้งหมด"""
        self.print_header()
        
        # เริ่มต้น workflow
        if not self.initialize_workflow():
            return False
        
        # สาิตฟังกชันต่างๆ
        self.demo_backup_structure()
        self.demo_manual_backup()
        self.demo_schedule_setup()
        self.demo_file_sync()
        self.show_usage_examples()
        
        print("\n🎉 การสาิต Auto Backup เสรจสิ้น!")
        print("📋 ระบบพร้อมใช้งานสำหรับ:")
        print("   - Auto Backup ทุกวันเวลา 02:00 น.")
        print("   - Weekly Backup วันอาทิตย 01:00 น.")
        print("   - Manual Backup เมื่อต้องการ")
        print("   - File Sync แบบ Real-time")
        
        return True

def main():
    """ฟังกชันหลัก"""
    demo = AutoBackupDemo()
    return demo.run_demo()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ การสาิตถกยกเลิกดยผ้ใช้")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
        sys.exit(1)
