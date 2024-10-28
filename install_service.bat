@echo off
REM install_service.bat
setlocal enabledelayedexpansion

echo Checking for administrator privileges...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrator privileges.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
echo Script directory: %SCRIPT_DIR%

REM Create service directories
set "SERVICE_DIR=C:\ProgramData\YTTranscriber"
echo Creating service directory: %SERVICE_DIR%
mkdir "%SERVICE_DIR%" 2>nul
mkdir "%SERVICE_DIR%\logs" 2>nul

REM Check if source files exist
if not exist "%SCRIPT_DIR%service.py" (
    echo Error: service.py not found in %SCRIPT_DIR%
    echo Please make sure service.py is in the same directory as this script.
    pause
    exit /b 1
)

if not exist "%SCRIPT_DIR%server.py" (
    echo Error: server.py not found in %SCRIPT_DIR%
    echo Please make sure server.py is in the same directory as this script.
    pause
    exit /b 1
)

REM Copy service files to Program Data with full paths
echo Copying service files...
echo From: %SCRIPT_DIR%service.py
echo To: %SERVICE_DIR%\service.py
copy /Y "%SCRIPT_DIR%service.py" "%SERVICE_DIR%\" || (
    echo Failed to copy service.py
    pause
    exit /b 1
)

echo From: %SCRIPT_DIR%server.py
echo To: %SERVICE_DIR%\server.py
copy /Y "%SCRIPT_DIR%server.py" "%SERVICE_DIR%\" || (
    echo Failed to copy server.py
    pause
    exit /b 1
)

REM Remove existing service if it exists
echo Removing existing service if present...
sc query YTTranscriberService >nul 2>&1
if %errorLevel% equ 0 (
    echo Stopping existing service...
    net stop YTTranscriberService
    echo Removing existing service...
    sc delete YTTranscriberService
)

REM Install and start service
echo Installing service...
cd /d "%SERVICE_DIR%"
python "%SERVICE_DIR%\service.py" --startup auto install

if %errorLevel% equ 0 (
    echo Service installed successfully.
    echo Starting service...
    python "%SERVICE_DIR%\service.py" start
    if %errorLevel% equ 0 (
        echo Service started successfully!
    ) else (
        echo Failed to start service. Check the logs at %SERVICE_DIR%\logs\service.log
    )
) else (
    echo Failed to install service. Check the logs at %SERVICE_DIR%\logs\service.log
)

echo.
echo Installation complete!
echo Service files location: %SERVICE_DIR%
echo Log file location: %SERVICE_DIR%\logs\service.log
echo.

pause
endlocal