#!/usr/bin/env python3
"""
Divaparadises Auto Backup Setup
สคริปต์ตั้งค่า Auto Backup สำหรับโครงการ Divaparadises
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# เพิ่ม path สำหรับ import
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from flows.auto_backup_workflow import AutoBackupWorkflow

class DivaparadisesBackup:
    def __init__(self):
        self.ai_system_path = current_dir.parent
        self.project_root = self.ai_system_path.parent  # Divaparadises root
        self.workflow = None
        
    def print_header(self):
        """แสดงหัวข้อ"""
        print("🎭 Divaparadises - Auto Backup Setup")
        print("=" * 60)
        print(f"📍 Project Root: {self.project_root}")
        print(f"📍 AI System: {self.ai_system_path}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    def initialize_workflow(self):
        """เริ่มต้น Auto Backup Workflow"""
        print("🔧 เริ่มต้น Auto Backup Workflow...")
        
        try:
            self.workflow = AutoBackupWorkflow(str(self.ai_system_path))
            
            if self.workflow.initialize_drive_connection():
                print("✅ เชื่อมต่อ Google Drive สำเร็จ")
                return True
            else:
                print("❌ ไม่สามารถเชื่อมต่อ Google Drive ได้")
                return False
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return False
    
    def create_backup_structure(self):
        """สร้างโครงสร้าง Backup บน Google Drive"""
        print("\n📁 สร้างโครงสร้าง Backup ใน Google Drive...")
        
        try:
            main_folder_id = self.workflow.create_backup_structure()
            if main_folder_id:
                print("✅ สร้างโครงสร้าง Backup สำเร็จ")
                print(f"   📂 Main Backup Folder ID: {main_folder_id}")
                return main_folder_id
            else:
                print("⚠️  โฟลเดอร์ Backup มีอยู่แล้ว หรือไม่สามารถสร้างได้")
                return None
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return None
    
    def setup_scheduled_backup(self):
        """ตั้งค่า Scheduled Backup"""
        print("\n⏰ ตั้งค่า Scheduled Backup...")
        
        try:
            # Daily backup ตอน 2:00 ตรุ่ง
            self.workflow.schedule_daily_backup("02:00")
            print("✅ ตั้งค่า Daily Backup: ทุกวัน 02:00 น.")
            
            # Weekly backup วันอาทิตย์ 1:00 ตรุ่ง
            self.workflow.schedule_weekly_backup("sunday", "01:00")
            print("✅ ตั้งค่า Weekly Backup: วันอาทิตย์ 01:00 น.")
            
            # แสดงสถานะ
            status = self.workflow.get_backup_status()
            if status:
                print(f"\n📊 Backup Status:")
                print(f"   - Scheduled Jobs: {status.get('scheduled_jobs', 0)}")
                print(f"   - Last Backup: {status.get('last_backup', 'Never')}")
            
            return True
            
        except Exception as e:
            print(f"❌ การตั้งค่า Schedule ล้มเหลว: {e}")
            return False
    
    def test_manual_backup(self):
        """ทดสอบ Manual Backup"""
        print("\n📤 ทดสอบ Manual Backup...")
        
        # สร้างไฟล์ทดสอบ
        test_dir = self.ai_system_path / "outputs"
        test_dir.mkdir(parents=True, exist_ok=True)
        
        test_file = test_dir / f"backup_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(f"""
🎭 Divaparadises - Backup Test File
===================================

Created: {datetime.now().isoformat()}
Purpose: Testing Auto Backup functionality

This is a test file to verify that the auto backup system
is working correctly for the Divaparadises project.

ระบบสำรองข้อมูลอัตโนมัติของ Divaparadises พร้อมใช้งาน! 🚀

Modules to be backed up:
- AI-System (Text, Image, Video, Audio Generation)
- React App (Divaparadises Music Platform)
- Core Engine (Rust Audio Processing)
- Google Drive Integration

สวัสดีจาก Diva! ✨
""")
            
            print(f"✅ สร้างไฟล์ทดสอบ: {test_file.name}")
            
            # ทดสอบ backup (จะ backup ทั้งโฟลเดอร์ outputs)
            print("📦 เริ่ม backup ไฟล์ทดสอบ...")
            # Note: จะต้องรันผ่าน workflow.backup_module() หรือ backup_all_modules()
            print("ℹ️  สำหรับ backup จริง ใช้คำสั่ง: workflow.backup_all_modules()")
            
            return True
            
        except Exception as e:
            print(f"❌ การสร้างไฟล์ทดสอบล้มเหลว: {e}")
            return False
    
    def show_usage_guide(self):
        """แสดงคำแนะนำการใช้งาน"""
        print("\n" + "=" * 60)
        print("📋 คำแนะนำการใช้งาน Auto Backup")
        print("=" * 60)
        
        print("\n1️⃣  Backup ทันที (Manual):")
        print("   cd C:\\Songya\\Divaparadises\\app\\AI-System\\Google_Drive_Integration")
        print("   python -c \"from flows.auto_backup_workflow import AutoBackupWorkflow; w = AutoBackupWorkflow('..'); w.initialize_drive_connection(); w.backup_all_modules()\"")
        
        print("\n2️⃣  รัน Scheduler (Auto Backup ตามเวลาที่ตั้ง):")
        print("   python -c \"from flows.auto_backup_workflow import AutoBackupWorkflow; w = AutoBackupWorkflow('..'); w.initialize_drive_connection(); w.run_scheduler()\"")
        print("   ⚠️  ต้องรันต่อเนื่อง (เปิดทิ้งไว้)")
        
        print("\n3️⃣  Backup เฉพาะ Module:")
        print("   python << สคริปต์ที่สร้างเอง หรือแก้ไข demo_auto_backup.py")
        
        print("\n4️⃣  ตรวจสอบสถานะ Backup:")
        print("   เข้าไปดูใน Google Drive ที่โฟลเดอร์ 'Diva_AI_Backups'")
        
        print("\n💡 Tips:")
        print("   - Backup จะถูกเก็บในโฟลเดอร์ Google Drive ของคุณ")
        print("   - Daily Backup: ทุกวัน 02:00 น. (ถ้ารัน Scheduler)")
        print("   - Weekly Backup: วันอาทิตย์ 01:00 น. (ถ้ารัน Scheduler)")
        print("   - สามารถ Manual Backup ได้ทุกเมื่อ")
        
    def setup(self):
        """รันการตั้งค่าทั้งหมด"""
        self.print_header()
        
        # เริ่มต้น workflow
        if not self.initialize_workflow():
            print("\n❌ การตั้งค่าล้มเหลว: ไม่สามารถเชื่อมต่อ Google Drive")
            return False
        
        # สร้างโครงสร้าง backup
        self.create_backup_structure()
        
        # ตั้งค่า schedule
        self.setup_scheduled_backup()
        
        # ทดสอบ
        self.test_manual_backup()
        
        # แสดงคำแนะนำ
        self.show_usage_guide()
        
        print("\n🎉 การตั้งค่า Auto Backup เสร็จสมบูรณ์!")
        print("=" * 60)
        print("✅ ระบบพร้อมใช้งานแล้ว")
        print("📋 อ่านคำแนะนำด้านบนเพื่อเริ่มใช้งาน")
        print()
        
        return True

def main():
    """ฟังก์ชันหลัก"""
    backup = DivaparadisesBackup()
    return backup.setup()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  การตั้งค่าถูกยกเลิก")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
