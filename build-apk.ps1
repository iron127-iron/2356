#Requires -Version 5.1
<#
.SYNOPSIS
    Build MHDDoS APK on Windows 11 using WSL2 + Docker
.DESCRIPTION
    This script will:
    1. Check/Install WSL2 if needed
    2. Check/Install Docker Desktop if needed
    3. Build the APK using Docker + Buildozer in WSL2
#>

$ErrorActionPreference = "Stop"

function Write-Step($msg) {
    Write-Host "`n>>> $msg" -ForegroundColor Cyan
}

function Test-WSL {
    try {
        $wsl = wsl --status 2>$null
        return $LASTEXITCODE -eq 0
    } catch { return $false }
}

function Test-Docker {
    try {
        $v = docker --version 2>$null
        return $v -match "Docker"
    } catch { return $false }
}

# --- Check WSL2 ---
Write-Step "Checking WSL2..."
if (-not (Test-WSL)) {
    Write-Host "[!] WSL2 not found. Installing..." -ForegroundColor Yellow
    wsl --install -d Ubuntu
    Write-Host "[!] WSL2 installed. Please REBOOT and run this script again." -ForegroundColor Red
    exit 1
} else {
    Write-Host "[+] WSL2 is installed" -ForegroundColor Green
}

# --- Check Docker ---
Write-Step "Checking Docker Desktop..."
if (-not (Test-Docker)) {
    Write-Host "[!] Docker Desktop not found." -ForegroundColor Yellow
    Write-Host "    Download from: https://www.docker.com/products/docker-desktop/"
    Write-Host "    Install Docker Desktop, enable WSL2 backend, then run this script again."
    exit 1
} else {
    Write-Host "[+] Docker Desktop is installed" -ForegroundColor Green
}

# --- Build in WSL2 ---
Write-Step "Building APK in WSL2..."
$wslCmd = @"
cd /mnt/$(pwd -W | sed 's/://' | tr '\\' '/')
bash docker-build-apk.sh
"@

wsl -d Ubuntu -e bash -c $wslCmd

Write-Step "APK build complete!"
Write-Host "Check the 'bin/' folder for the APK file." -ForegroundColor Green
