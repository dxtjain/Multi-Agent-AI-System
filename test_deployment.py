#!/usr/bin/env python3
"""
Pre-deployment Testing Script
Tests all components before submission and deployment
"""

import sys
import subprocess
import requests
import time
from pathlib import Path

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    
    required_modules = [
        'streamlit', 'fastapi', 'uvicorn', 'pandas', 'numpy', 
        'plotly', 'sentence_transformers', 'faiss', 'fitz', 'nltk'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            if module == 'fitz':
                __import__('fitz')
            else:
                __import__(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_file_structure():
    """Test project file structure"""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        'README.md',
        'requirements.txt',
        'streamlit_requirements.txt',
        'streamlit_app.py',
        'backend/main.py',
        'backend/agents/orchestrator_agent.py',
        'backend/agents/data_intelligence_agent.py',
        'backend/agents/research_assistant_agent.py',
        'frontend/app.py',
        'frontend/app_standalone.py',
        'sample_data/sales_data.csv',
        'sample_data/customer_data.csv',
        'docker-compose.yml',
        '.streamlit/config.toml'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_streamlit_app():
    """Test if Streamlit app can be imported"""
    print("\n🔍 Testing Streamlit app...")
    
    try:
        # Test standalone app import
        sys.path.append('frontend')
        from app_standalone import main
        print("  ✅ Standalone app imports successfully")
        
        # Test streamlit app entry point
        from streamlit_app import main as streamlit_main
        print("  ✅ Streamlit entry point imports successfully")
        
        return True
    except Exception as e:
        print(f"  ❌ Streamlit app test failed: {e}")
        return False

def test_sample_data():
    """Test sample data loading"""
    print("\n🔍 Testing sample data...")
    
    try:
        import pandas as pd
        
        # Test CSV files
        sales_df = pd.read_csv('sample_data/sales_data.csv')
        customer_df = pd.read_csv('sample_data/customer_data.csv')
        
        print(f"  ✅ Sales data: {sales_df.shape[0]} rows, {sales_df.shape[1]} columns")
        print(f"  ✅ Customer data: {customer_df.shape[0]} rows, {customer_df.shape[1]} columns")
        
        # Test text file
        with open('sample_data/sample_research_paper.txt', 'r') as f:
            content = f.read()
        print(f"  ✅ Research paper: {len(content)} characters")
        
        return True
    except Exception as e:
        print(f"  ❌ Sample data test failed: {e}")
        return False

def test_docker_config():
    """Test Docker configuration"""
    print("\n🔍 Testing Docker configuration...")
    
    docker_files = [
        'docker-compose.yml',
        'docker/Dockerfile.backend',
        'docker/Dockerfile.frontend'
    ]
    
    all_exist = True
    for file_path in docker_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            all_exist = False
    
    return all_exist

def generate_deployment_checklist():
    """Generate final deployment checklist"""
    print("\n📋 DEPLOYMENT CHECKLIST:")
    print("=" * 50)
    
    checklist = [
        ("✅", "All required files present"),
        ("✅", "Dependencies properly specified"),
        ("✅", "Streamlit app configured for cloud"),
        ("✅", "Sample data ready for testing"),
        ("✅", "Docker configuration complete"),
        ("⏳", "Create GitHub repository"),
        ("⏳", "Push code to GitHub"),
        ("⏳", "Deploy to Streamlit Cloud"),
        ("⏳", "Test live deployment"),
        ("⏳", "Create demo video"),
    ]
    
    for status, item in checklist:
        print(f"  {status} {item}")
    
    print("\n🚀 READY FOR DEPLOYMENT!")
    print("\nNext steps:")
    print("1. Create GitHub repository")
    print("2. Push code: git push origin main")
    print("3. Deploy to Streamlit Cloud")
    print("4. Test live deployment")

def main():
    """Run all tests"""
    print("🤖 Multi-Agent AI System - Pre-Deployment Testing")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("File Structure Test", test_file_structure),
        ("Streamlit App Test", test_streamlit_app),
        ("Sample Data Test", test_sample_data),
        ("Docker Config Test", test_docker_config),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        generate_deployment_checklist()
        return True
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
