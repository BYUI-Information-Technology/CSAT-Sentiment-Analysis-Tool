#!/usr/bin/env python3
"""
Build script to create executables for the Sentiment Analysis Flask App
Supports Windows (.exe) and macOS (.app) platforms
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


def install_requirements():
    """Install all required packages"""
    print("📦 Installing requirements...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    )
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])


def create_spec_file():
    """Create PyInstaller spec file for the application"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'flask',
        'transformers',
        'torch',
        'pandas',
        'matplotlib',
        'seaborn',
        'numpy',
        'openpyxl',
        'werkzeug',
        'PIL',
        'transformers.pipelines',
        'transformers.models.roberta',
        'sklearn.metrics.pairwise',
        'sklearn.feature_extraction.text',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SentimentAnalyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SentimentAnalyzer',
)

# For macOS, create an app bundle
import platform
if platform.system() == 'Darwin':
    app = BUNDLE(
        coll,
        name='SentimentAnalyzer.app',
        icon=None,
        bundle_identifier='com.sentimentanalyzer.app',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
        },
    )
"""

    with open("sentiment_analyzer.spec", "w") as f:
        f.write(spec_content)


def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable...")

    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")

    # Create spec file
    create_spec_file()

    # Build with PyInstaller
    cmd = ["pyinstaller", "--clean", "--noconfirm", "sentiment_analyzer.spec"]

    subprocess.check_call(cmd)


def create_launcher_script():
    """Create a launcher script for the executable"""
    system = platform.system()

    if system == "Windows":
        launcher_content = """@echo off
echo Starting Sentiment Analysis Application...
echo Please wait while the application loads...
echo.
echo Once started, open your web browser and go to:
echo http://localhost:5001
echo.
echo Press Ctrl+C to stop the application
echo.
cd /d "%~dp0"
SentimentAnalyzer.exe
pause
"""
        with open("dist/SentimentAnalyzer/start_app.bat", "w") as f:
            f.write(launcher_content)

    elif system == "Darwin":  # macOS
        launcher_content = """#!/bin/bash
echo "Starting Sentiment Analysis Application..."
echo "Please wait while the application loads..."
echo ""
echo "Once started, open your web browser and go to:"
echo "http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

# Start the application
./SentimentAnalyzer

echo "Application stopped. Press any key to close this window."
read -n 1
"""
        launcher_path = "dist/SentimentAnalyzer/start_app.sh"
        with open(launcher_path, "w") as f:
            f.write(launcher_content)
        os.chmod(launcher_path, 0o755)


def create_readme():
    """Create a README file for the executable"""
    readme_content = """# Sentiment Analysis Application

## Quick Start

1. **Windows**: Double-click `start_app.bat`
2. **macOS**: Double-click `start_app.sh`

## Manual Start

1. Run the executable: `SentimentAnalyzer` (or `SentimentAnalyzer.exe` on Windows)
2. Open your web browser
3. Go to: http://localhost:5001

## Usage

1. Upload an Excel file (.xlsx or .xls) with a column named "Response"
2. Click "Analyze Sentiment" 
3. View results and download the analyzed file

## Requirements

- Your Excel file must have a column named "Why satisfied text area" containing text to analyze
- Supported file formats: .xlsx, .xls
- Maximum file size: 16MB

## Features

- AI-powered sentiment analysis using RoBERTa model
- Beautiful web interface
- Downloadable results with sentiment labels and confidence scores
- Comprehensive data visualizations

## Troubleshooting

- **Port in use**: App uses port 5001 by default (5000 conflicts with macOS AirPlay)
- **Model download**: First run may take longer as it downloads the AI model
- **File upload errors**: Ensure your Excel file has a "Why satisfied text area" column

## Technical Details

- Model: cardiffnlp/twitter-roberta-base-sentiment-latest
- Framework: Flask web application
- Sentiment categories: POSITIVE, NEGATIVE, NEUTRAL
- Confidence scores: 0.0 to 1.0 (higher = more confident)

## Support

For technical support or issues, check the application logs in the console window.
"""

    with open("dist/SentimentAnalyzer/README.txt", "w") as f:
        f.write(readme_content)


def main():
    """Main build process"""
    print("🚀 Building Sentiment Analysis Executable")
    print(f"Platform: {platform.system()} {platform.machine()}")
    print("-" * 50)

    try:
        # Step 1: Install requirements
        install_requirements()

        # Step 2: Build executable
        build_executable()

        # Step 3: Create launcher script
        create_launcher_script()

        # Step 4: Create README
        create_readme()

        print("\n✅ Build completed successfully!")
        print(f"📁 Executable location: dist/SentimentAnalyzer/")

        system = platform.system()
        if system == "Windows":
            print(
                "🚀 To run: Double-click 'start_app.bat' or run 'SentimentAnalyzer.exe'"
            )
        elif system == "Darwin":
            print("🚀 To run: Double-click 'start_app.sh' or run './SentimentAnalyzer'")
        else:
            print("🚀 To run: Execute './SentimentAnalyzer'")

        print("🌐 Then open browser to: http://localhost:5001")

    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
