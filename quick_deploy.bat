@echo off
echo 🐋 Deploying Resident Orca...
if not exist "resident_orca.py" (
    echo Error: resident_orca.py not found
    pause
    exit /b 1
)
call install.bat
echo Starting Resident Orca...
call run_orca.bat