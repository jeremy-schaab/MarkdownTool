# Markdown Manager Installer
# PowerShell script to install and run Markdown Manager on any Windows computer

param(
    [switch]$InstallOnly,
    [switch]$RunOnly,
    [string]$InstallPath = "$env:LOCALAPPDATA\MarkdownManager"
)

Write-Host "=== Markdown Manager Installer ===" -ForegroundColor Green
Write-Host ""

# Function to check if Python is installed
function Test-Python {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+\.\d+)") {
            $version = [version]$matches[1]
            if ($version -ge [version]"3.8") {
                Write-Host "✅ Python $($matches[1]) found" -ForegroundColor Green
                return $true
            } else {
                Write-Host "❌ Python $($matches[1]) found but version 3.8+ required" -ForegroundColor Red
                return $false
            }
        }
    } catch {
        Write-Host "❌ Python not found" -ForegroundColor Red
        return $false
    }
    return $false
}

# Function to install Python
function Install-Python {
    Write-Host "📥 Installing Python..." -ForegroundColor Yellow
    
    # Download Python installer
    $pythonUrl = "https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe"
    $pythonInstaller = "$env:TEMP\python-installer.exe"
    
    try {
        Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
        
        # Install Python silently
        Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
        
        # Clean up
        Remove-Item $pythonInstaller -ErrorAction SilentlyContinue
        
        # Refresh PATH
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        Write-Host "✅ Python installed successfully" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Failed to install Python: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to install Markdown Manager
function Install-MarkdownManager {
    Write-Host "📦 Installing Markdown Manager to $InstallPath..." -ForegroundColor Yellow
    
    # Create installation directory
    if (!(Test-Path $InstallPath)) {
        New-Item -Path $InstallPath -ItemType Directory -Force | Out-Null
    }
    
    # Download project files from GitHub (assumes this will be on GitHub)
    $projectFiles = @(
        "markdown_viewer.py",
        "ai_service.py", 
        "requirements.txt",
        "run_app.py",
        ".env.example"
    )
    
    $baseUrl = "https://raw.githubusercontent.com/YOUR_USERNAME/MarkdownTool/main/"
    
    foreach ($file in $projectFiles) {
        try {
            $url = $baseUrl + $file
            $destination = Join-Path $InstallPath $file
            Write-Host "  Downloading $file..."
            Invoke-WebRequest -Uri $url -OutFile $destination
        } catch {
            Write-Host "❌ Failed to download $file. Using local fallback..." -ForegroundColor Red
            
            # Fallback: copy from current directory if available
            $localFile = Join-Path (Get-Location) $file
            if (Test-Path $localFile) {
                Copy-Item $localFile $destination
                Write-Host "  ✅ Copied $file from local directory" -ForegroundColor Green
            }
        }
    }
    
    # Install Python dependencies
    Write-Host "📋 Installing Python dependencies..." -ForegroundColor Yellow
    
    try {
        Set-Location $InstallPath
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt
        
        Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install dependencies: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    
    # Create .env file if it doesn't exist
    $envFile = Join-Path $InstallPath ".env"
    if (!(Test-Path $envFile)) {
        Write-Host "📝 Creating .env configuration file..." -ForegroundColor Yellow
        $envExampleFile = Join-Path $InstallPath ".env.example"
        if (Test-Path $envExampleFile) {
            Copy-Item $envExampleFile $envFile
        }
    }
    
    # Create desktop shortcut
    $shortcutPath = Join-Path $env:USERPROFILE "Desktop\Markdown Manager.lnk"
    $targetPath = "powershell.exe"
    $arguments = "-Command `"cd '$InstallPath'; python run_app.py`""
    
    try {
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($shortcutPath)
        $Shortcut.TargetPath = $targetPath
        $Shortcut.Arguments = $arguments
        $Shortcut.WorkingDirectory = $InstallPath
        $Shortcut.IconLocation = "shell32.dll,13"
        $Shortcut.Description = "Markdown Manager - View and edit markdown files"
        $Shortcut.Save()
        
        Write-Host "✅ Desktop shortcut created" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Could not create desktop shortcut: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    return $true
}

# Function to run Markdown Manager
function Start-MarkdownManager {
    if (Test-Path $InstallPath) {
        Write-Host "🚀 Starting Markdown Manager..." -ForegroundColor Green
        Set-Location $InstallPath
        
        # Check if .env file is configured
        $envFile = Join-Path $InstallPath ".env"
        if (!(Test-Path $envFile) -or (Get-Content $envFile | Select-String "your-api-key-here")) {
            Write-Host ""
            Write-Host "⚠️  IMPORTANT: Configure your Azure OpenAI credentials" -ForegroundColor Yellow
            Write-Host "   Edit the .env file in: $InstallPath" -ForegroundColor Yellow
            Write-Host "   Add your Azure OpenAI endpoint and API key" -ForegroundColor Yellow
            Write-Host ""
        }
        
        python run_app.py
    } else {
        Write-Host "❌ Markdown Manager not found. Run with -InstallOnly first." -ForegroundColor Red
    }
}

# Main execution
try {
    if ($RunOnly) {
        Start-MarkdownManager
        exit
    }
    
    # Check for Python
    if (!(Test-Python)) {
        $response = Read-Host "Would you like to install Python automatically? (y/n)"
        if ($response -eq "y" -or $response -eq "Y") {
            if (!(Install-Python)) {
                Write-Host "❌ Python installation failed. Please install Python 3.8+ manually." -ForegroundColor Red
                exit 1
            }
        } else {
            Write-Host "❌ Python 3.8+ is required. Please install it first." -ForegroundColor Red
            exit 1
        }
    }
    
    # Install Markdown Manager
    if (!(Install-MarkdownManager)) {
        Write-Host "❌ Installation failed" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "🎉 Installation completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Configure Azure OpenAI credentials in: $InstallPath\.env" -ForegroundColor White
    Write-Host "2. Double-click the 'Markdown Manager' desktop shortcut to run" -ForegroundColor White
    Write-Host "3. Or run manually: cd '$InstallPath' && python run_app.py" -ForegroundColor White
    Write-Host ""
    
    if (!$InstallOnly) {
        $response = Read-Host "Would you like to start Markdown Manager now? (y/n)"
        if ($response -eq "y" -or $response -eq "Y") {
            Start-MarkdownManager
        }
    }
    
} catch {
    Write-Host "❌ Installation error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}