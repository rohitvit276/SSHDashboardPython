#!/usr/bin/env python3
"""
SSH Connectivity Dashboard Setup Script
Automates the installation and setup process for deployment
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major != 3 or version.minor < 11:
        print("❌ Python 3.11+ required. Current version:", sys.version)
        return False
    print("✅ Python version compatible:", sys.version.split()[0])
    return True

def install_dependencies():
    """Install required Python packages"""
    dependencies = [
        "streamlit>=1.28.0",
        "pandas>=2.0.0", 
        "paramiko>=3.3.0"
    ]
    
    print("📦 Installing dependencies...")
    try:
        for dep in dependencies:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_required_files():
    """Check if all required application files exist"""
    required_files = [
        "app.py",
        "ssh_checker.py",
        ".streamlit/config.toml"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files present")
    return True

def setup_streamlit_config():
    """Create .streamlit directory and config if needed"""
    os.makedirs(".streamlit", exist_ok=True)
    
    config_content = """[server]
headless = true
address = "0.0.0.0"
port = 5000

[browser]
gatherUsageStats = false
"""
    
    config_path = ".streamlit/config.toml"
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            f.write(config_content)
        print("✅ Created Streamlit configuration")
    else:
        print("✅ Streamlit configuration exists")

def main():
    """Main setup function"""
    print("🚀 SSH Connectivity Dashboard Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check required files
    if not check_required_files():
        print("Please ensure all application files are in the current directory")
        sys.exit(1)
    
    # Setup Streamlit config
    setup_streamlit_config()
    
    print("\n✅ Setup completed successfully!")
    print("\n🎯 To start the dashboard:")
    print("   streamlit run app.py --server.port 5000")
    print("\n🌐 Then open your browser to:")
    print("   http://localhost:5000")
    print("   or http://your-server-ip:5000 for network access")

if __name__ == "__main__":
    main()