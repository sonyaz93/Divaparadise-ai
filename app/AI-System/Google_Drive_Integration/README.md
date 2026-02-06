# Google Drive Integration for Diva AI System

ระบบเชื่อมต่อและสำรองข้อมูลอัตโนมัติสำหรับ Diva AI System กับ Google Drive

## 📁 โครงสร้างโฟลเดอร์

```
Google_Drive_Integration/
├── api/                    # API สำหรับเชื่อมต่อ Google Drive
│   └── drive_manager.py   # คลาสหลักสำหรับจัดการ Drive API
├── utils/                  # เครื่องมือช่วยเหลือ
│   └── file_sync.py        # ฟังก์ชัน sync ไฟล์
├── flows/                  # Workflow อัตโนมัติ
│   └── auto_backup_workflow.py  # ระบบ backup อัตโนมัติ
├── config/                 # การตั้งค่า
│   ├── requirements.txt    # Dependencies ที่ต้องการ
│   └── client_secret_*.json  # Google OAuth credentials (ต้องเพิ่มเอง)
├── docs/                   # เอกสาร
├── test_connection.py      # สคริปต์ทดสอบการเชื่อมต่อแบบเต็ม
├── quick_test.py          # สคริปต์ทดสอบแบบเร็ว
├── setup_drive.py         # สคริปต์ตั้งค่าระบบ
├── setup.bat              # Windows batch script สำหรับตั้งค่า
└── run_test.bat           # Windows batch script สำหรับทดสอบ
```

## 🚀 การติดตั้งและใช้งาน

### วิธีที่ 1: ใช้ Setup Script (แนะนำ)
```bash
# Windows
setup.bat

# หรือ
python setup_drive.py
```

### วิธีที่ 2: ติดตั้งแบบ Manual

#### 1. Install Dependencies
```bash
pip install -r config/requirements.txt
```

#### 2. Google Cloud Console Setup
1. ไปที่ [Google Cloud Console](https://console.cloud.google.com/)
2. สร้าง Project ใหม่หรือเลือกโปรเจคที่มีอยู่
3. เปิดใช้งาน Google Drive API:
   - ไปที่ "APIs & Services" > "Library"
   - ค้นหา "Google Drive API" และคลิก "Enable"
4. สร้าง OAuth 2.0 Credentials:
   - ไปที่ "APIs & Services" > "Credentials"
   - คลิก "Create Credentials" > "OAuth client ID"
   - เลือก "Desktop application"
   - ตั้งชื่อ (เช่น "Diva AI Drive Client")
5. ดาวน์โหลดไฟล์ JSON (จะมีชื่อขึ้นต้นด้วย `client_secret_`)
6. วางไฟล์ในโฟลเดอร์ `config/`

#### 3. ทดสอบการเชื่อมต่อ
```bash
# ทดสอบแบบเร็ว
python quick_test.py

# ทดสอบแบบเต็ม
python test_connection.py

# Windows batch
run_test.bat
```

#### 4. การใช้งานครั้งแรก
```python
from api.drive_manager import GoogleDriveManager

# สร้าง connection (จะมีหน้าต่างให้ login ครั้งแรก)
drive = GoogleDriveManager()

# ทดสอบอัปโหลดไฟล์
drive.upload_file("test.jpg")
```

## 📋 ฟังก์ชันหลัก

### GoogleDriveManager
- `upload_file()` - อัปโหลดไฟล์
- `list_files()` - ดูรายการไฟล์
- `download_file()` - ดาวน์โหลดไฟล์
- `create_folder()` - สร้างโฟลเดอร์
- `delete_file()` - ลบไฟล์
- `search_files()` - ค้นหาไฟล์

### FileSyncManager
- `sync_folder_to_drive()` - Sync โฟลเดอร์ขึ้น Drive
- `sync_from_drive()` - Sync จาก Drive ลงเครื่อง
- `backup_generated_content()` - Backup เนื้อหาที่สร้าง

### AutoBackupWorkflow
- `backup_all_modules()` - Backup ทุก module
- `schedule_daily_backup()` - ตั้งเวลา backup รายวัน
- `manual_backup()` - Backup แบบ manual

## 💡 ตัวอย่างการใช้งาน

### อัปโหลดไฟล์เดี่ยว
```python
from api.drive_manager import GoogleDriveManager

drive = GoogleDriveManager()
result = drive.upload_file("image.png", description="AI Generated Image")
print(f"Uploaded: {result['webViewLink']}")
```

### Backup ทั้งระบบ
```python
from flows.auto_backup_workflow import AutoBackupWorkflow

workflow = AutoBackupWorkflow("c:/Divaparadises/Divaparadises/AI-System")
workflow.initialize_drive_connection()
workflow.backup_all_modules()
```

### ตั้งเวลา Backup อัตโนมัติ
```python
# Backup ทุกวันตอน 2 ตรุ่ง
workflow.schedule_daily_backup("02:00")

# Backup ทุกวันอาทิตย์ตอน 1 ตรุ่ง
workflow.schedule_weekly_backup("sunday", "01:00")

# Run scheduler (ต้องรันตลอดเวลา)
workflow.run_scheduler()
```

### Sync โฟลเดอร์
```python
from utils.file_sync import FileSyncManager

sync = FileSyncManager("local/path", drive_manager)
sync.sync_folder_to_drive("local/folder/to/sync")
```

## 🔧 การตั้งค่า

### Environment Variables
```bash
# ไม่จำเป็นต้องตั้งค่า ใช้ OAuth 2.0 แทน
```

### Config Files
- `config/credentials.json` - OAuth credentials
- `config/token.json` - Authentication token (สร้างอัตโนมัติ)

## 📝 ข้อมูลสำคัญ

- **การ Auth**: ใช้ OAuth 2.0 ครั้งแรกจะมีหน้าต่าง browser ให้ login
- **Rate Limit**: Google Drive มีขีดจำกัดการใช้งาน
- **File Size**: จำกัดที่ 100GB ต่อไฟล์
- **Storage**: ใช้พื้นที่จาก Google Account ของคุณ

## 🚨 ข้อควรระวัง

- อย่าเผยแพร่ `credentials.json` และ `token.json`
- ตรวจสอบ quota การใช้งานบน Google Cloud Console
- Backup ข้อมูลสำคัญก่อนใช้งานจริง
- ใช้สำหรับการทดสอบและพัฒนาเท่านั้น

## 🆘 การแก้ไขปัญหา

### Authentication Error
```bash
# ลบ token.json แล้วรันใหม่
rm config/token.json
python api/drive_manager.py
```

### Quota Exceeded
- ตรวจสอบ Google Cloud Console
- รอจนกว่า quota จะรีเซ็ต
- ใช้บัญชีอื่นหรืออัปเกรดแพ็กเกจ

### File Not Found
- ตรวจสอบ path ของไฟล์
- ตรวจสอบสิทธิ์การเข้าถึงไฟล์
- ตรวจสอบว่าไฟล์มีอยู่จริง

---

🎭 **Diva Paradises AI System** - Google Drive Integration Module
