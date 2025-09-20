#!/usr/bin/env python3
"""
Multi-Agent AI System Launcher
Convenient script to run the system locally without Docker
"""

import subprocess
import sys
import time
import threading
import os
from pathlib import Path

def run_backend():
    """Run the FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    os.chdir(Path(__file__).parent / "backend")
    subprocess.run([
        sys.executable, "-m", "uvicorn", "main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])

def run_frontend():
    """Run the Streamlit frontend"""
    print("🌐 Starting Streamlit frontend...")
    os.chdir(Path(__file__).parent / "frontend")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])

def main():
    """Main launcher function"""
    print("🤖 Multi-Agent AI System Launcher")
    print("=" * 50)
    
    # Check if required packages are installed
    required_packages = ["fastapi", "streamlit", "pandas", "plotly"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install requirements: pip install -r requirements.txt")
        return
    
    print("✅ All required packages found")
    print("\n📊 Services will be available at:")
    print("   - Backend API: http://localhost:8000")
    print("   - API Docs: http://localhost:8000/docs")
    print("   - Frontend: http://localhost:8501")
    print("\n🔄 Starting services...\n")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a bit for backend to start
    time.sleep(3)
    
    # Start frontend (this will block)
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down services...")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
