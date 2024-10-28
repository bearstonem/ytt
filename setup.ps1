# Check if Chocolatey is installed
if (!(Get-Command choco.exe -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}

# Install system dependencies
Write-Host "Installing FFmpeg and yt-dlp..."
choco install ffmpeg -y
choco install yt-dlp -y

# Install Poetry if not already installed
if (!(Get-Command poetry -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Poetry..."
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
}

# Install project dependencies
Write-Host "Installing project dependencies..."
poetry install

# execute installation script 'install_service.bat', run as administrator
& "$PSScriptRoot\install_service.bat"

Write-Host "Setup complete!"
