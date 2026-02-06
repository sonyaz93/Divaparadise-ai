#!/usr/bin/env python3
"""
Setup script for AI System API Server
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and handle errors"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed: {e.stderr}")
        return None

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def setup_virtual_environment():
    """Setup virtual environment"""
    venv_path = Path(".venv")
    
    if not venv_path.exists():
        print("🔄 Creating virtual environment...")
        if platform.system() == "Windows":
            run_command("python -m venv .venv", "Creating virtual environment")
            activate_cmd = ".venv\\Scripts\\activate"
        else:
            run_command("python3 -m venv .venv", "Creating virtual environment")
            activate_cmd = "source .venv/bin/activate"
        
        print(f"📝 To activate: {activate_cmd}")
    else:
        print("✅ Virtual environment already exists")

def install_dependencies():
    """Install Python dependencies"""
    if platform.system() == "Windows":
        pip_cmd = ".venv\\Scripts\\pip"
    else:
        pip_cmd = ".venv/bin/pip"
    
    # Upgrade pip first
    run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip")
    
    # Install requirements
    run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# AI System API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# File Storage
UPLOAD_DIR=./uploads
OUTPUT_DIR=./outputs

# Database (if needed)
DATABASE_URL=sqlite:///./ai_system.db
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file - Please update with your API keys")
    else:
        print("✅ .env file already exists")

def create_directories():
    """Create necessary directories"""
    dirs = ["uploads", "outputs", "logs", "temp"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    print("✅ Created necessary directories")

def test_server():
    """Test if server can start"""
    print("🔄 Testing server startup...")
    
    if platform.system() == "Windows":
        python_cmd = ".venv\\Scripts\\python"
    else:
        python_cmd = ".venv/bin/python"
    
    # Quick import test
    test_cmd = f"{python_cmd} -c \"import fastapi; import uvicorn; print('✅ Server dependencies OK')\""
    result = run_command(test_cmd, "Testing server dependencies")
    
    if result:
        print("🚀 Server is ready to start!")
        print("📍 Run: python api_server.py")
        print("🌐 API Docs: http://localhost:8000/docs")
    else:
        print("❌ Server test failed")

def main():
    """Main setup function"""
    print("🚀 Setting up Divaparadises AI System API Server")
    print("=" * 50)
    
    # Check Python version
    if not check_python():
        sys.exit(1)
    
    # Setup steps
    setup_virtual_environment()
    install_dependencies()
    create_env_file()
    create_directories()
    test_server()
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your API keys")
    print("2. Activate virtual environment:")
    if platform.system() == "Windows":
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("3. Start the server:")
    print("   python api_server.py")
    print("4. Visit http://localhost:8000/docs for API documentation")

if __name__ == "__main__":
    main()