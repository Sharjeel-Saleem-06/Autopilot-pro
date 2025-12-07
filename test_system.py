#!/usr/bin/env python3
"""
Test script to verify all model files and paths are correct.
Run this before launching the full system to catch any issues.
"""

import os
import sys
from pathlib import Path

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

def print_colored(message, color):
    print(f"{color}{message}{END}")

def check_file(filepath, description):
    """Check if a file exists and print result"""
    if filepath.exists():
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print_colored(f"  ✅ {description}: Found ({size_mb:.1f} MB)", GREEN)
        return True
    else:
        print_colored(f"  ❌ {description}: NOT FOUND", RED)
        print_colored(f"     Expected at: {filepath}", YELLOW)
        return False

def main():
    print_colored("\n" + "="*60, BLUE)
    print_colored("🔍 Autopilot Pro - System Verification", BLUE)
    print_colored("="*60 + "\n", BLUE)
    
    base_dir = Path(__file__).parent
    all_good = True
    
    # Check Python version
    print_colored("🐍 Python Version Check:", BLUE)
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_colored(f"  ✅ Python {version.major}.{version.minor}.{version.micro} (OK)", GREEN)
    else:
        print_colored(f"  ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)", RED)
        all_good = False
    print()
    
    # Check dependencies
    print_colored("📦 Dependency Check:", BLUE)
    deps = {
        'gradio': 'Gradio (Web UI)',
        'ultralytics': 'Ultralytics YOLO',
        'cv2': 'OpenCV',
        'PIL': 'Pillow (Image Processing)',
        'numpy': 'NumPy',
        'requests': 'Requests'
    }
    
    for module, name in deps.items():
        try:
            __import__(module)
            print_colored(f"  ✅ {name}", GREEN)
        except ImportError:
            print_colored(f"  ❌ {name} - NOT INSTALLED", RED)
            all_good = False
    print()
    
    # Check launcher files
    print_colored("📄 Launcher Files:", BLUE)
    launcher_files = [
        ('launch_all.py', 'Main Launcher'),
        ('config.py', 'Configuration'),
        ('requirements.txt', 'Requirements'),
        ('README.md', 'Documentation')
    ]
    
    for filename, desc in launcher_files:
        all_good &= check_file(base_dir / filename, desc)
    print()
    
    # Check model scripts
    print_colored("🤖 Model Scripts:", BLUE)
    model_scripts = [
        ('LTV_HTV_Model/LTV_HTV_Model.py', 'LTV/HTV Model Script'),
        ('Pedestrian_Model/Pedestrian_Model.py', 'Pedestrian Model Script'),
        ('Traffic_Light_Model/TRAFFIC_LIGHT_MODEL.py', 'Traffic Light Model Script'),
        ('TRAFFIC_SIGN_MODEL/TRAFFIC_SIGN_MODEL.py', 'Traffic Sign Model Script'),
        ('AUTOPILOT PRO/Autopilotpro.py', 'Autopilot Pro Script')
    ]
    
    for filepath, desc in model_scripts:
        all_good &= check_file(base_dir / filepath, desc)
    print()
    
    # Check model weights
    print_colored("⚖️  Model Weight Files:", BLUE)
    model_weights = [
        ('LTV_HTV_Model/LTV_HTV.pt', 'LTV/HTV Weights'),
        ('Pedestrian_Model/last.pt', 'Pedestrian Weights'),
        ('Traffic_Light_Model/epoch70.pt', 'Traffic Light Weights'),
        ('TRAFFIC_SIGN_MODEL/trafic.pt', 'Traffic Sign Weights')
    ]
    
    for filepath, desc in model_weights:
        all_good &= check_file(base_dir / filepath, desc)
    print()
    
    # Check UI files
    print_colored("🎨 UI Files:", BLUE)
    ui_files = [
        ('UI/home.html', 'Main UI HTML'),
        ('UI/home.css', 'UI Styles'),
        ('UI/table1.html', 'Performance Table 1'),
        ('UI/table2.html', 'Performance Table 2'),
        ('UI/table3.html', 'Performance Table 3')
    ]
    
    for filepath, desc in ui_files:
        all_good &= check_file(base_dir / filepath, desc)
    print()
    
    # Check test images
    print_colored("🖼️  Test Images:", BLUE)
    test_dirs = [
        'Testing_images/LTV_HTV_Images',
        'Testing_images/Pedestrian_Images',
        'Testing_images/Traffic_light_images',
        'Testing_images/Traffic_Sign_Images'
    ]
    
    for dir_path in test_dirs:
        full_path = base_dir / dir_path
        if full_path.exists() and full_path.is_dir():
            count = len(list(full_path.glob('*.*')))
            print_colored(f"  ✅ {dir_path}: {count} images", GREEN)
        else:
            print_colored(f"  ⚠️  {dir_path}: Directory not found", YELLOW)
    print()
    
    # Port availability check
    print_colored("🔌 Port Availability Check:", BLUE)
    import socket
    ports = [7860, 7861, 7862, 7868, 7869]
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result != 0:
            print_colored(f"  ✅ Port {port}: Available", GREEN)
        else:
            print_colored(f"  ⚠️  Port {port}: Already in use", YELLOW)
    print()
    
    # Final verdict
    print_colored("="*60, BLUE)
    if all_good:
        print_colored("✅ All checks passed! System is ready to launch.", GREEN)
        print_colored("\nRun: python launch_all.py", GREEN)
    else:
        print_colored("❌ Some checks failed. Please fix the issues above.", RED)
        print_colored("\nTry: pip install -r requirements.txt", YELLOW)
    print_colored("="*60 + "\n", BLUE)
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())

