@echo off
REM restart_service.bat

echo Checking for administrator privileges...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrator privileges.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

set "SERVICE_DIR=C:\ProgramData\YTTranscriber"
set "SERVICE_NAME=YTTranscriberService"

echo.
echo Checking service status...
sc query %SERVICE_NAME% | findstr "STATE" > nul
if %errorLevel% neq 0 (
    echo Service %SERVICE_NAME% is not installed!
    echo Please run the installation script first.
    pause
    exit /b 1
)

echo.
echo Stopping %SERVICE_NAME%...
net stop %SERVICE_NAME%
if %errorLevel% neq 0 (
    echo Failed to stop service. It might already be stopped.
)

echo.
echo Waiting for service to fully stop...
timeout /t 5 /nobreak

echo.
echo Starting %SERVICE_NAME%...
net start %SERVICE_NAME%
if %errorLevel% equ 0 (
    echo.
    echo Service restarted successfully!
    echo Logs can be found at: %SERVICE_DIR%\logs\service.log
) else (
    echo.
    echo Failed to start service. 
    echo Please check the logs at: %SERVICE_DIR%\logs\service.log
)

echo.
echo Current service status:
sc query %SERVICE_NAME% | findstr "STATE"

pause