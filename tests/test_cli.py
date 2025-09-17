#!/usr/bin/env python3
"""
Test script for RngKit CLI.

This script provides basic functionality tests for the CLI application.
"""

import sys
import os
import subprocess
from pathlib import Path

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from src.rngkit_cli.utils import ensure_data_dir, print_banner, print_device_status
        from src.rngkit_cli.collector import DataCollector
        from src.rngkit_cli.analyzer import DataAnalyzer
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_directory():
    """Test data directory creation."""
    print("Testing data directory...")
    try:
        from src.rngkit_cli.utils import ensure_data_dir
        data_dir = ensure_data_dir()
        if os.path.exists(data_dir):
            print(f"✅ Data directory created: {data_dir}")
            return True
        else:
            print(f"❌ Data directory not created: {data_dir}")
            return False
    except Exception as e:
        print(f"❌ Data directory error: {e}")
        return False

def test_device_status():
    """Test device status checking."""
    print("Testing device status...")
    try:
        from src.rngkit_cli.utils import print_device_status
        print_device_status(verbose=True)
        print("✅ Device status check completed")
        return True
    except Exception as e:
        print(f"❌ Device status error: {e}")
        return False

def test_cli_help():
    """Test CLI help command."""
    print("Testing CLI help...")
    try:
        result = subprocess.run([sys.executable, "main.py", "--help"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and "RngKit CLI" in result.stdout:
            print("✅ CLI help command works")
            return True
        else:
            print(f"❌ CLI help failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ CLI help error: {e}")
        return False

def test_status_command():
    """Test status command."""
    print("Testing status command...")
    try:
        result = subprocess.run([sys.executable, "main.py", "status"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Status command works")
            return True
        else:
            print(f"❌ Status command failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Status command error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Running RngKit CLI Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_data_directory,
        test_device_status,
        test_cli_help,
        test_status_command
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())

