@echo off
REM uninstall_service.bat

echo Checking for administrator privileges...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrator privileges.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

set SERVICE_DIR=C:\ProgramData\YTTranscriber

echo Stopping service...
python "%SERVICE_DIR%\service.py" stop

echo Removing service...
python "%SERVICE_DIR%\service.py" remove

echo Cleaning up files...
rd /s /q "%SERVICE_DIR%"

echo Service uninstalled!
pause