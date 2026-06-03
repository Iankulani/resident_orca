@echo off
title Resident Orca Installer
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║     🐋 RESIDENT ORCA - INSTALLATION SCRIPT v1.0              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check Python
echo [*] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [✗] Python not found. Please install Python 3.7+ from python.org
    pause
    exit /b 1
)
echo [✓] Python found

REM Create virtual environment
echo.
echo [*] Creating virtual environment...
python -m venv orca_env
if errorlevel 1 (
    echo [✗] Failed to create virtual environment
    pause
    exit /b 1
)
echo [✓] Virtual environment created

REM Activate and install packages
echo.
echo [*] Installing Python packages...
call orca_env\Scripts\activate.bat

pip install --upgrade pip
pip install requests paramiko psutil Flask matplotlib seaborn numpy reportlab scapy whois qrcode pyshorteners discord.py telethon slack-sdk colorama

if errorlevel 1 (
    echo [✗] Package installation failed
    pause
    exit /b 1
)
echo [✓] Packages installed

REM Create directories
echo.
echo [*] Creating directories...
mkdir .resident_orca\ssh_keys 2>nul
mkdir .resident_orca\phishing_pages 2>nul
mkdir orca_reports\graphics 2>nul
mkdir temp 2>nul
echo [✓] Directories created

REM Create config file
echo.
echo [*] Creating configuration...
(
echo {
echo     "version": "1.0.0",
echo     "database": ".resident_orca/orca_data.db",
echo     "log_file": ".resident_orca/orca.log",
echo     "web_port": 5000,
echo     "phishing_port": 8080,
echo     "auto_start_web": true
echo }
) > .resident_orca\config.json
echo [✓] Configuration created

REM Create run script
echo.
echo [*] Creating launcher...
(
echo @echo off
echo call orca_env\Scripts\activate.bat
echo python resident_orca.py %%*
) > run_orca.bat
echo [✓] Launcher created: run_orca.bat

echo.
echo ════════════════════════════════════════════════════════════════
echo ✅ RESIDENT ORCA INSTALLATION COMPLETE!
echo ════════════════════════════════════════════════════════════════
echo.
echo To start Resident Orca:
echo   run_orca.bat
echo.
echo To run tests:
echo   orca_env\Scripts\activate.bat ^&^& python test_commands.py
echo.
echo Web Dashboard:
echo   http://localhost:5000
echo.
echo ════════════════════════════════════════════════════════════════
pause