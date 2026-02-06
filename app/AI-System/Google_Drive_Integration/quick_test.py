#!/usr/bin/env python3
"""
Quick Google Drive Connection Test
การทดสอบการเชื่อมต่อ Google Drive แบบเร็ว

Usage: python quick_test.py
"""

import os
import sys
from datetime import datetime

# เพิ่ม path สำหรับ import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_requirements():
    """ตรวจสอบ requirements อย่างเร็ว"""
    print("🔍 ตรวจสอบ requirements...")
    
    required_modules = [
        'googleapiclient',
        'google.auth',
        'google_auth_oauthlib'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"❌ ขาด modules: {', '.join(missing)}")
        print("📦 รันคำสั่ง: pip install -r config/requirements.txt")
        return False
    
    print("✅ Requirements ครบถ้วน")
    return True

def check_credentials():
    """ตรวจสอบไฟล์ credentials อย่างเร็ว"""
    print("🔑 ตรวจสอบ credentials...")
    
    config_dir = os.path.join(os.path.dirname(__file__), 'config')
    
    # หาไฟล์ credentials
    credentials_files = [
        f for f in os.listdir(config_dir) 
        if f.startswith('client_secret_') and f.endswith('.json')
    ]
    
    if not credentials_files:
        print("❌ ไม่พบไฟล์ credentials")
        print("📝 วางไฟล์ client_secret_*.json ในโฟลเดอร์ config/")
        return False
    
    print(f"✅ พบ credentials: {credentials_files[0]}")
    return True

def quick_connection_test():
    """ทดสอบการเชื่อมต่อแบบเร็ว"""
    print("🚀 ทดสอบการเชื่อมต่อ Google Drive...")
    
    try:
        from api.drive_manager import GoogleDriveManager
        
        # สร้าง connection
        drive = GoogleDriveManager()
        
        # ทดสอบ list files
        files = drive.list_files()
        print(f"✅ เชื่อมต่อสำเร็จ! พบไฟล์ {len(files)} ไฟล์")
        
        # แสดงไฟล์ 3 ไฟล์แรก
        if files:
            print("📁 ไฟล์ล่าสุด:")
            for i, file in enumerate(files[:3]):
                print(f"   {i+1}. {file['name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ การเชื่อมต่อล้มเหลว: {e}")
        return False

def main():
    """ฟังก์ชันหลัก"""
    print("⚡ Google Drive Quick Test")
    print("=" * 40)
    print(f"📍 {os.path.dirname(os.path.abspath(__file__))}")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # ตรวจสอบ requirements
    if not check_requirements():
        return False
    
    # ตรวจสอบ credentials
    if not check_credentials():
        return False
    
    # ทดสอบการเชื่อมต่อ
    success = quick_connection_test()
    
    print()
    if success:
        print("🎉 การทดสอบเร็วสำเร็จ!")
        print("📋 รันการทดสอบแบบเต็ม: python test_connection.py")
    else:
        print("❌ การทดสอบล้มเหลว")
        print("🔧 รันการตั้งค่า: python setup_drive.py")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ การทดสอบถูกยกเลิก")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
        sys.exit(1)