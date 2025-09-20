#!/usr/bin/env python3
"""
Setup Verification Script for Multi-Agent AI System
Checks if all required dependencies and components are properly installed
"""

import sys
import importlib
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.9+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ required. Current version:", f"{version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_required_packages():
    """Check if all required packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'streamlit', 'pandas', 'numpy',
        'matplotlib', 'plotly', 'seaborn', 'requests', 'pydantic',
        'sentence_transformers', 'faiss', 'nltk', 'fitz'  # PyMuPDF
    ]
    
    missing_packages = []
    installed_packages = []
    
    for package in required_packages:
        try:
            # Special handling for PyMuPDF
            if package == 'fitz':
                importlib.import_module('fitz')
                installed_packages.append('PyMuPDF (fitz)')
            else:
                importlib.import_module(package)
                installed_packages.append(package)
        except ImportError:
            missing_packages.append(package)
    
    print(f"✅ Installed packages ({len(installed_packages)}):")
    for package in installed_packages:
        print(f"   • {package}")
    
    if missing_packages:
        print(f"\n❌ Missing packages ({len(missing_packages)}):")
        for package in missing_packages:
            print(f"   • {package}")
        return False
    
    return True

def check_project_structure():
    """Check if project structure is correct"""
    required_files = [
        'requirements.txt',
        'README.md',
        'docker-compose.yml',
        'backend/main.py',
        'backend/agents/__init__.py',
        'backend/agents/data_intelligence_agent.py',
        'backend/agents/research_assistant_agent.py',
        'backend/agents/orchestrator_agent.py',
        'frontend/app.py',
        'sample_data/sales_data.csv',
        'sample_data/customer_data.csv',
        'docker/Dockerfile.backend',
        'docker/Dockerfile.frontend'
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            existing_files.append(file_path)
        else:
            missing_files.append(file_path)
    
    print(f"✅ Project structure ({len(existing_files)}/{len(required_files)} files):")
    for file_path in existing_files:
        print(f"   • {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing files ({len(missing_files)}):")
        for file_path in missing_files:
            print(f"   • {file_path}")
        return False
    
    return True

def check_docker():
    """Check if Docker and Docker Compose are available"""
    try:
        # Check Docker
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, check=True)
        docker_version = result.stdout.strip()
        print(f"✅ {docker_version}")
        
        # Check Docker Compose
        result = subprocess.run(['docker-compose', '--version'], 
                              capture_output=True, text=True, check=True)
        compose_version = result.stdout.strip()
        print(f"✅ {compose_version}")
        
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker or Docker Compose not found")
        print("   Install Docker Desktop to use containerized deployment")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    try:
        import nltk
        print("📥 Downloading NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ NLTK data downloaded successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to download NLTK data: {e}")
        return False

def main():
    """Main setup check function"""
    print("🤖 Multi-Agent AI System - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("Project Structure", check_project_structure),
        ("Docker (Optional)", check_docker),
        ("NLTK Data", download_nltk_data)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        print(f"\n🔍 Checking {check_name}...")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Error during {check_name}: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Setup Verification Summary:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {check_name}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Your system is ready to go.")
        print("\n🚀 Next steps:")
        print("   1. Run locally: python run.py")
        print("   2. Run with Docker: docker-compose up --build")
        print("   3. Access frontend: http://localhost:8501")
    else:
        print("\n⚠️  Some checks failed. Please address the issues above.")
        print("\n💡 Common solutions:")
        print("   • Install missing packages: pip install -r requirements.txt")
        print("   • Install Docker Desktop for containerized deployment")
        print("   • Check file paths and project structure")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
