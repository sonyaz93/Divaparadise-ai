# Google Cloud Console Setup Guide

## 🌐 ขั้นตอนการ Setup Google Cloud Console

### 1. เข้าสู่ Google Cloud Console
1. ไปที่: https://console.cloud.google.com/
2. Login ด้วย Google Account ของคุณ
3. สร้าง Project ใหม่ (ถ้ายังไม่มี)
   - คลิกที่โปรเจกต์ dropdown บนหัวข้อ
   - เลือก "NEW PROJECT"
   - ตั้งชื่อ: `Diva AI System`
   - คลิก "CREATE"

### 2. เปิด Google Drive API
1. ในเมนูด้านซ้าย → APIs & Services → Library
2. ค้นหา: "Google Drive API"
3. คลิกที่ "Google Drive API"
4. คลิก "ENABLE"

### 3. สร้าง OAuth 2.0 Credentials
1. ไปที่ APIs & Services → Credentials
2. คลิก "+ CREATE CREDENTIALS"
3. เลือก "OAuth client ID"
4. ถ้ายังไม่ได้ configure OAuth consent screen:
   - คลิก "CONFIGURE CONSENT SCREEN"
   - เลือก "External"
   - คลิก "CREATE"

### 4. ตั้งค่า OAuth Consent Screen
**App information:**
- App name: `Diva AI System`
- User support email: เลือก email ของคุณ
- Developer contact information: email ของคุณ

**Scopes:**
- คลิก "ADD OR REMOVE SCOPES"
- ค้นหา: `https://www.googleapis.com/auth/drive`
- คลิก "ADD" → "UPDATE"

**Test users:**
- คลิก "ADD USERS"
- เพิ่ม email ของคุณเป็น test user
- คลิก "SAVE AND CONTINUE"

### 5. สร้าง OAuth Client ID
1. กลับไปที่ Credentials page
2. คลิก "+ CREATE CREDENTIALS" → "OAuth client ID"
3. Application type: เลือก "Desktop app"
4. Name: `Diva AI Drive Client`
5. คลิก "CREATE"

### 6. ดาวน์โหลด Credentials
1. หลังจากสร้างเสร็จ จะมีหน้าต่าง popup ขึ้นมา
2. คลิก "DOWNLOAD JSON"
3. ตั้งชื่อไฟล์: `credentials.json`
4. **สำคัญ:** วางไฟล์นี้ในโฟลเดอร์:
   ```
   c:\Divaparadises\Divaparadises\AI-System\Google_Drive_Integration\config\
   ```

## 🔧 การติดตั้ง Dependencies

เปิด terminal และรัน:
```bash
cd "c:\Divaparadises\Divaparadises\AI-System\Google_Drive_Integration"
pip install -r config/requirements.txt
```

## 🧪 การทดสอบ Connection

สร้างไฟล์ทดสอบ `test_drive.py`:
```python
from api.drive_manager import GoogleDriveManager

try:
    drive = GoogleDriveManager()
    print("✅ Connection successful!")
    
    # Test list files
    files = drive.list_files()
    print(f"Found {len(files)} files in Drive")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

รันทดสอบ:
```bash
cd "c:\Divaparadises\Divaparadises\AI-System\Google_Drive_Integration"
python test_drive.py
```

## 🚨 ข้อควรระวัง

- **ครั้งแรกรัน:** จะเปิด browser ให้ login และ authorize
- **credentials.json:** อย่าเผยแพร่หรืออัปโหลดที่อื่น
- **token.json:** จะสร้างอัตโนมัติหลังจาก login ครั้งแรก
- **Quota:** ตรวจสอบขีดจำกัดการใช้งานบน Google Cloud Console

## 🆘 การแก้ไขปัญหา

### "redirect_uri_mismatch"
- ตรวจสอบว่าสร้าง OAuth client แบบ "Desktop app"
- หรือแก้ไข redirect URI ใน credentials

### "access_denied"
- ตรวจสอบว่าเพิ่ม email ของคุณใน Test users
- ตรวจสอบ scopes ที่เลือก

### "invalid_client"
- ตรวจสอบว่า credentials.json ถูกต้อง
- ลองสร้าง OAuth client ใหม่

## 📱 หลังจาก Setup เสร็จ

คุณสามารถ:
1. ใช้งาน Google Drive API ผ่าน `drive_manager.py`
2. Sync ไฟล์อัตโนมัติด้วย `auto_backup_workflow.py`
3. Backup ข้อมูล AI System ไปยัง Google Drive

---

🎭 **พร้อมใช้งานแล้ว!**
