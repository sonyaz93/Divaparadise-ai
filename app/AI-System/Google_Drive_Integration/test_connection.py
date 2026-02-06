#!/usr/bin/env python3
"""
Google Drive Connection Test Script
สคริปต์ทดสอบการเชื่อมต่อ Google Drive สำหรับ Diva AI System

Usage: python test_connection.py
"""

import os
import sys
import json
import tempfile
from datetime import datetime

# เพิ่ม path สำหรับ import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.drive_manager import GoogleDriveManager

class GoogleDriveConnectionTest:
    def __init__(self):
        self.drive = None
        self.test_folder_id = None
        self.test_results = []
        
    def log_test(self, test_name, success, message="", details=None):
        """บันทึกผลการทดสอบ"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details:
            print(f"    Details: {details}")
    
    def check_credentials(self):
        """ตรวจสอบไฟล์ credentials"""
        print("\n🔍 ตรวจสอบไฟล์ Credentials...")
        
        config_dir = os.path.join(os.path.dirname(__file__), 'config')
        credentials_files = [
            f for f in os.listdir(config_dir) 
            if f.startswith('client_secret_') and f.endswith('.json')
        ]
        
        if not credentials_files:
            self.log_test(
                "Credentials Check", 
                False, 
                "ไม่พบไฟล์ credentials ใน config/",
                "กรุณาดาวน์โหลดไฟล์ credentials จาก Google Cloud Console"
            )
            return False
        
        credentials_file = credentials_files[0]
        credentials_path = os.path.join(config_dir, credentials_file)
        
        try:
            with open(credentials_path, 'r') as f:
                creds_data = json.load(f)
                client_id = creds_data.get('installed', {}).get('client_id', 'Unknown')
                
            self.log_test(
                "Credentials Check", 
                True, 
                f"พบไฟล์ credentials: {credentials_file}",
                f"Client ID: {client_id[:20]}..."
            )
            return True
            
        except Exception as e:
            self.log_test(
                "Credentials Check", 
                False, 
                f"ไฟล์ credentials ผิดพลาด: {str(e)}"
            )
            return False
    
    def test_authentication(self):
        """ทดสอบการ authenticate"""
        print("\n🔐 ทดสอบการ Authentication...")
        
        try:
            # หาไฟล์ credentials
            config_dir = os.path.join(os.path.dirname(__file__), 'config')
            credentials_files = [
                f for f in os.listdir(config_dir) 
                if f.startswith('client_secret_') and f.endswith('.json')
            ]
            
            if credentials_files:
                credentials_path = os.path.join(config_dir, credentials_files[0])
                token_path = os.path.join(config_dir, 'token.json')
                
                self.drive = GoogleDriveManager(credentials_path, token_path)
                
                self.log_test(
                    "Authentication", 
                    True, 
                    "เชื่อมต่อ Google Drive สำเร็จ"
                )
                return True
            else:
                self.log_test(
                    "Authentication", 
                    False, 
                    "ไม่พบไฟล์ credentials"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Authentication", 
                False, 
                f"การ authenticate ล้มเหลว: {str(e)}"
            )
            return False
    
    def test_list_files(self):
        """ทดสอบการแสดงรายการไฟล์"""
        print("\n📁 ทดสอบการแสดงรายการไฟล์...")
        
        try:
            files = self.drive.list_files()
            
            self.log_test(
                "List Files", 
                True, 
                f"พบไฟล์ทั้งหมด {len(files)} ไฟล์",
                f"ไฟล์ล่าสุด: {files[0]['name'] if files else 'ไม่มีไฟล์'}"
            )
            
            # แสดงรายการไฟล์ 5 ไฟล์แรก
            if files:
                print("    📋 รายการไฟล์ (5 ไฟล์แรก):")
                for i, file in enumerate(files[:5]):
                    size = file.get('size', 'N/A')
                    if size != 'N/A' and size.isdigit():
                        size = f"{int(size):,} bytes"
                    print(f"    {i+1}. {file['name']} ({size})")
            
            return True
            
        except Exception as e:
            self.log_test(
                "List Files", 
                False, 
                f"ไม่สามารถแสดงรายการไฟล์ได้: {str(e)}"
            )
            return False
    
    def test_create_folder(self):
        """ทดสอบการสร้างโฟลเดอร์"""
        print("\n📂 ทดสอบการสร้างโฟลเดอร์...")
        
        try:
            folder_name = f"Diva_AI_Test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            folder = self.drive.create_folder(folder_name)
            
            if folder:
                self.test_folder_id = folder['id']
                self.log_test(
                    "Create Folder", 
                    True, 
                    f"สร้างโฟลเดอร์ '{folder_name}' สำเร็จ",
                    f"Folder ID: {self.test_folder_id}"
                )
                return True
            else:
                self.log_test(
                    "Create Folder", 
                    False, 
                    "ไม่สามารถสร้างโฟลเดอร์ได้"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Create Folder", 
                False, 
                f"การสร้างโฟลเดอร์ล้มเหลว: {str(e)}"
            )
            return False
    
    def test_upload_file(self):
        """ทดสอบการอัปโหลดไฟล์"""
        print("\n📤 ทดสอบการอัปโหลดไฟล์...")
        
        try:
            # สร้างไฟล์ทดสอบ
            test_content = f"""
🎭 Diva AI System - Google Drive Integration Test
==============================================

Test File Created: {datetime.now().isoformat()}
System: Diva Paradises AI
Module: Google Drive Integration
Location: C:\\Divaparadises\\Divaparadises\\AI-System\\Google_Drive_Integration

This is a test file to verify Google Drive upload functionality.

Test Results:
- Authentication: ✅
- File Creation: ✅
- Upload Process: In Progress...

สวัสดีจาก Diva AI System! 🚀
การทดสอบการอัปโหลดไฟล์สำเร็จ
"""
            
            # สร้างไฟล์ชั่วคราว
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(test_content)
                temp_file_path = temp_file.name
            
            # อัปโหลดไฟล์
            file_name = f"diva_ai_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            # เปลี่ยนชื่อไฟล์ชั่วคราว
            final_path = os.path.join(os.path.dirname(temp_file_path), file_name)
            os.rename(temp_file_path, final_path)
            
            uploaded_file = self.drive.upload_file(
                final_path, 
                folder_id=self.test_folder_id,
                description="Test file from Diva AI System - Google Drive Integration"
            )
            
            # ลบไฟล์ชั่วคราว
            os.unlink(final_path)
            
            if uploaded_file:
                self.log_test(
                    "Upload File", 
                    True, 
                    f"อัปโหลดไฟล์ '{file_name}' สำเร็จ",
                    f"File ID: {uploaded_file['id']}, Size: {uploaded_file.get('size', 'N/A')} bytes"
                )
                return uploaded_file
            else:
                self.log_test(
                    "Upload File", 
                    False, 
                    "ไม่สามารถอัปโหลดไฟล์ได้"
                )
                return None
                
        except Exception as e:
            self.log_test(
                "Upload File", 
                False, 
                f"การอัปโหลดไฟล์ล้มเหลว: {str(e)}"
            )
            return None
    
    def test_download_file(self, file_info):
        """ทดสอบการดาวน์โหลดไฟล์"""
        print("\n📥 ทดสอบการดาวน์โหลดไฟล์...")
        
        try:
            if not file_info:
                self.log_test(
                    "Download File", 
                    False, 
                    "ไม่มีไฟล์สำหรับทดสอบดาวน์โหลด"
                )
                return False
            
            # สร้าง path สำหรับดาวน์โหลด
            download_path = os.path.join(
                tempfile.gettempdir(), 
                f"downloaded_{file_info['name']}"
            )
            
            self.drive.download_file(file_info['id'], download_path)
            
            if os.path.exists(download_path):
                file_size = os.path.getsize(download_path)
                
                # อ่านเนื้อหาไฟล์เพื่อตรวจสอบ
                with open(download_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    is_valid = "Diva AI System" in content
                
                # ลบไฟล์ที่ดาวน์โหลด
                os.unlink(download_path)
                
                self.log_test(
                    "Download File", 
                    True, 
                    f"ดาวน์โหลดไฟล์สำเร็จ",
                    f"Size: {file_size} bytes, Content Valid: {is_valid}"
                )
                return True
            else:
                self.log_test(
                    "Download File", 
                    False, 
                    "ไฟล์ไม่ถูกดาวน์โหลด"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Download File", 
                False, 
                f"การดาวน์โหลดไฟล์ล้มเหลว: {str(e)}"
            )
            return False
    
    def test_search_files(self):
        """ทดสอบการค้นหาไฟล์"""
        print("\n🔍 ทดสอบการค้นหาไฟล์...")
        
        try:
            search_results = self.drive.search_files("diva_ai_test")
            
            self.log_test(
                "Search Files", 
                True, 
                f"พบไฟล์ที่ตรงกับคำค้นหา {len(search_results)} ไฟล์",
                f"คำค้นหา: 'diva_ai_test'"
            )
            return True
            
        except Exception as e:
            self.log_test(
                "Search Files", 
                False, 
                f"การค้นหาไฟล์ล้มเหลว: {str(e)}"
            )
            return False
    
    def cleanup_test_files(self):
        """ทำความสะอาดไฟล์ทดสอบ"""
        print("\n🧹 ทำความสะอาดไฟล์ทดสอบ...")
        
        try:
            if self.test_folder_id:
                # ลบไฟล์ในโฟลเดอร์ทดสอบ
                files_in_folder = self.drive.list_files(folder_id=self.test_folder_id)
                for file in files_in_folder:
                    self.drive.delete_file(file['id'])
                
                # ลบโฟลเดอร์ทดสอบ
                self.drive.delete_file(self.test_folder_id)
                
                self.log_test(
                    "Cleanup", 
                    True, 
                    f"ลบไฟล์ทดสอบ {len(files_in_folder)} ไฟล์ และโฟลเดอร์ทดสอบแล้ว"
                )
            else:
                self.log_test(
                    "Cleanup", 
                    True, 
                    "ไม่มีไฟล์ทดสอบที่ต้องลบ"
                )
                
        except Exception as e:
            self.log_test(
                "Cleanup", 
                False, 
                f"การทำความสะอาดล้มเหลว: {str(e)}"
            )
    
    def generate_report(self):
        """สร้างรายงานผลการทดสอบ"""
        print("\n📊 สรุปผลการทดสอบ")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"📈 ทดสอบทั้งหมด: {total_tests}")
        print(f"✅ ผ่าน: {passed_tests}")
        print(f"❌ ไม่ผ่าน: {failed_tests}")
        print(f"📊 อัตราความสำเร็จ: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ การทดสอบที่ล้มเหลว:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   - {result['test']}: {result['message']}")
        
        # บันทึกรายงานเป็นไฟล์
        report_file = os.path.join(
            os.path.dirname(__file__), 
            f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': (passed_tests/total_tests)*100
                },
                'test_results': self.test_results,
                'timestamp': datetime.now().isoformat(),
                'system_info': {
                    'location': 'C:\\Divaparadises\\Divaparadises\\AI-System\\Google_Drive_Integration',
                    'python_version': sys.version,
                    'platform': sys.platform
                }
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 รายงานถูกบันทึกที่: {report_file}")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """รันการทดสอบทั้งหมด"""
        print("🎭 Diva AI System - Google Drive Integration Test")
        print("=" * 60)
        print(f"📍 Location: C:\\Divaparadises\\Divaparadises\\AI-System\\Google_Drive_Integration")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # ตรวจสอบ credentials
        if not self.check_credentials():
            print("\n❌ การทดสอบหยุดเนื่องจากไม่พบไฟล์ credentials")
            return False
        
        # ทดสอบ authentication
        if not self.test_authentication():
            print("\n❌ การทดสอบหยุดเนื่องจาก authentication ล้มเหลว")
            return False
        
        # รันการทดสอบต่างๆ
        self.test_list_files()
        self.test_create_folder()
        uploaded_file = self.test_upload_file()
        self.test_download_file(uploaded_file)
        self.test_search_files()
        
        # ทำความสะอาด
        self.cleanup_test_files()
        
        # สร้างรายงาน
        success = self.generate_report()
        
        print(f"\n⏰ Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if success:
            print("\n🎉 การทดสอบเสร็จสิ้นสำเร็จ! Google Drive Integration พร้อมใช้งาน")
        else:
            print("\n⚠️ การทดสอบมีปัญหา กรุณาตรวจสอบและแก้ไข")
        
        return success

def main():
    """ฟังก์ชันหลัก"""
    test = GoogleDriveConnectionTest()
    return test.run_all_tests()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ การทดสอบถูกยกเลิกโดยผู้ใช้")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
        sys.exit(1)