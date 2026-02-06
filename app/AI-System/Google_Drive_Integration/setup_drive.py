#!/usr/bin/env python3
"""
Google Drive Integration Setup Script
สคริปต์สำหรับตั้งค่าและเตรียมระบบ Google Drive Integration

Usage: python setup_drive.py
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class GoogleDriveSetup:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.config_dir = self.base_dir / 'config'
        self.requirements_file = self.config_dir / 'requirements.txt'
        
    def print_header(self):
        """แสดงหัวข้อ"""
        print("🎭 Diva AI System - Google Drive Integration Setup")
        print("=" * 60)
        print(f"📍 Location: {self.base_dir}")
        print()
    
    def check_python_version(self):
        """ตรวจสอบเวอร์ชัน Python"""
        print("🐍 ตรวจสอบเวอร์ชัน Python...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            print(f"❌ Python {version.major}.{version.minor} ไม่รองรับ")
            print("📋 ต้องการ Python 3.7 หรือใหม่กว่า")
            return False
        
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} รองรับ")
        return True
    
    def install_requirements(self):
        """ติดตั้ง dependencies"""
        print("\n📦 ติดตั้ง Dependencies...")
        
        if not self.requirements_file.exists():
            print(f"❌ ไม่พบไฟล์ {self.requirements_file}")
            return False
        
        try:
            # อ่านรายการ packages
            with open(self.requirements_file, 'r') as f:
                packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            print(f"📋 จะติดตั้ง {len(packages)} packages:")
            for package in packages:
                print(f"   - {package}")
            
            # ติดตั้ง packages
            cmd = [sys.executable, '-m', 'pip', 'install', '-r', str(self.requirements_file)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ ติดตั้ง dependencies สำเร็จ")
                return True
            else:
                print(f"❌ การติดตั้งล้มเหลว: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return False
    
    def check_credentials(self):
        """ตรวจสอบไฟล์ credentials"""
        print("\n🔑 ตรวจสอบไฟล์ Credentials...")
        
        # หาไฟล์ credentials
        credentials_files = list(self.config_dir.glob('client_secret_*.json'))
        
        if not credentials_files:
            print("❌ ไม่พบไฟล์ credentials")
            print("\n📝 วิธีการตั้งค่า Google Drive API:")
            print("1. ไปที่ https://console.cloud.google.com/")
            print("2. สร้างโปรเจคใหม่หรือเลือกโปรเจคที่มีอยู่")
            print("3. เปิดใช้งาน Google Drive API")
            print("4. ไปที่ 'APIs & Services' > 'Credentials'")
            print("5. คลิก 'Create Credentials' > 'OAuth client ID'")
            print("6. เลือก 'Desktop application'")
            print("7. ดาวน์โหลดไฟล์ JSON")
            print(f"8. วางไฟล์ในโฟลเดอร์: {self.config_dir}")
            print("\n⚠️ ไฟล์ต้องมีชื่อขึ้นต้นด้วย 'client_secret_'")
            return False
        
        credentials_file = credentials_files[0]
        print(f"✅ พบไฟล์ credentials: {credentials_file.name}")
        
        # ตรวจสอบเนื้อหาไฟล์
        try:
            with open(credentials_file, 'r') as f:
                creds_data = json.load(f)
            
            if 'installed' in creds_data:
                client_id = creds_data['installed'].get('client_id', 'Unknown')
                project_id = creds_data['installed'].get('project_id', 'Unknown')
                
                print(f"   📋 Project ID: {project_id}")
                print(f"   🔑 Client ID: {client_id[:20]}...")
                return True
            else:
                print("❌ ไฟล์ credentials ไม่ถูกต้อง")
                print("📝 ต้องเป็นไฟล์สำหรับ Desktop Application")
                return False
                
        except Exception as e:
            print(f"❌ ไม่สามารถอ่านไฟล์ credentials: {e}")
            return False
    
    def create_sample_files(self):
        """สร้างไฟล์ตัวอย่าง"""
        print("\n📄 สร้างไฟล์ตัวอย่าง...")
        
        # สร้างไฟล์ตัวอย่างการใช้งาน
        example_file = self.base_dir / 'example_usage.py'
        
        example_content = '''#!/usr/bin/env python3
"""
ตัวอย่างการใช้งาน Google Drive Integration
"""

import os
import sys
from datetime import datetime

# เพิ่ม path สำหรับ import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.drive_manager import GoogleDriveManager

def main():
    """ตัวอย่างการใช้งานพื้นฐาน"""
    print("🎭 Diva AI System - Google Drive Example")
    print("=" * 50)
    
    try:
        # เชื่อมต่อ Google Drive
        print("🔗 เชื่อมต่อ Google Drive...")
        drive = GoogleDriveManager()
        
        # สร้างโฟลเดอร์สำหรับ Diva AI
        print("📁 สร้างโฟลเดอร์...")
        folder = drive.create_folder("Diva AI Generated Content")
        
        if folder:
            folder_id = folder['id']
            print(f"✅ สร้างโฟลเดอร์สำเร็จ: {folder['webViewLink']}")
            
            # แสดงรายการไฟล์
            print("📋 แสดงรายการไฟล์...")
            files = drive.list_files()
            print(f"พบไฟล์ทั้งหมด: {len(files)} ไฟล์")
            
            # ค้นหาไฟล์
            print("🔍 ค้นหาไฟล์...")
            search_results = drive.search_files("Diva")
            print(f"พบไฟล์ที่เกี่ยวข้องกับ 'Diva': {len(search_results)} ไฟล์")
            
            print("\\n🎉 ตัวอย่างการใช้งานเสร็จสิ้น!")
            
        else:
            print("❌ ไม่สามารถสร้างโฟลเดอร์ได้")
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    main()
'''
        
        with open(example_file, 'w', encoding='utf-8') as f:
            f.write(example_content)
        
        print(f"✅ สร้างไฟล์ตัวอย่าง: {example_file.name}")
        
        # สร้างไฟล์ .gitignore
        gitignore_file = self.base_dir / '.gitignore'
        gitignore_content = '''# Google Drive Integration - Sensitive Files
config/token.json
config/client_secret_*.json
*.pyc
__pycache__/
.env
.venv/
test_report_*.json
*.log

# Temporary files
*.tmp
*.temp
downloaded_*
'''
        
        with open(gitignore_file, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        print(f"✅ สร้างไฟล์ .gitignore")
        
        return True
    
    def run_test_connection(self):
        """รันการทดสอบการเชื่อมต่อ"""
        print("\n🧪 รันการทดสอบการเชื่อมต่อ...")
        
        test_file = self.base_dir / 'test_connection.py'
        if not test_file.exists():
            print("❌ ไม่พบไฟล์ test_connection.py")
            return False
        
        try:
            # รันการทดสอบ
            cmd = [sys.executable, str(test_file)]
            result = subprocess.run(cmd, cwd=str(self.base_dir))
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ ไม่สามารถรันการทดสอบได้: {e}")
            return False
    
    def show_next_steps(self):
        """แสดงขั้นตอนต่อไป"""
        print("\n📋 ขั้นตอนต่อไป:")
        print("1. รันการทดสอบ: python test_connection.py")
        print("2. ดูตัวอย่างการใช้งาน: python example_usage.py")
        print("3. อ่านเอกสาร: README.md")
        print("4. เริ่มใช้งานใน AI modules อื่นๆ")
        print()
        print("📁 ไฟล์สำคัญ:")
        print(f"   - API Manager: {self.base_dir / 'api' / 'drive_manager.py'}")
        print(f"   - Configuration: {self.config_dir}")
        print(f"   - Test Script: {self.base_dir / 'test_connection.py'}")
        print()
        print("🔗 ลิงก์ที่เป็นประโยชน์:")
        print("   - Google Cloud Console: https://console.cloud.google.com/")
        print("   - Google Drive API Docs: https://developers.google.com/drive/api")
        print("   - OAuth 2.0 Setup: https://developers.google.com/identity/protocols/oauth2")
    
    def run_setup(self):
        """รันการตั้งค่าทั้งหมด"""
        self.print_header()
        
        # ตรวจสอบ Python version
        if not self.check_python_version():
            return False
        
        # ติดตั้ง dependencies
        if not self.install_requirements():
            print("⚠️ การติดตั้ง dependencies ล้มเหลว แต่จะดำเนินการต่อ")
        
        # ตรวจสอบ credentials
        has_credentials = self.check_credentials()
        
        # สร้างไฟล์ตัวอย่าง
        self.create_sample_files()
        
        # แสดงขั้นตอนต่อไป
        self.show_next_steps()
        
        if has_credentials:
            print("\n🎉 การตั้งค่าเสร็จสิ้น! ระบบพร้อมใช้งาน")
            
            # ถามว่าต้องการรันการทดสอบหรือไม่
            try:
                response = input("\n❓ ต้องการรันการทดสอบการเชื่อมต่อเลยไหม? (y/n): ").lower()
                if response in ['y', 'yes', 'ใช่']:
                    return self.run_test_connection()
            except KeyboardInterrupt:
                print("\n\n⚠️ การตั้งค่าถูกยกเลิก")
                return False
        else:
            print("\n⚠️ การตั้งค่าเสร็จสิ้น แต่ยังต้องเพิ่มไฟล์ credentials")
            print("📝 กรุณาทำตามขั้นตอนด้านบนเพื่อเพิ่มไฟล์ credentials")
        
        return True

def main():
    """ฟังก์ชันหลัก"""
    setup = GoogleDriveSetup()
    return setup.run_setup()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ การตั้งค่าถูกยกเลิกโดยผู้ใช้")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
        sys.exit(1)