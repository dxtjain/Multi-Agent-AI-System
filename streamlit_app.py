"""
Streamlit Cloud Entry Point for Multi-Agent AI System
This file serves as the main entry point for Streamlit Cloud deployment
"""

import sys
import os
from pathlib import Path

# Add the frontend directory to the Python path
current_dir = Path(__file__).parent
frontend_dir = current_dir / "frontend"
sys.path.insert(0, str(frontend_dir))

# Import and run the clean, production-ready app for cloud deployment
from app_clean import main

if __name__ == "__main__":
    main()
