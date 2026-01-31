# Script to run Realtek, Intel installers and network tuning script with proper waiting

# Function to start a process and wait until it and any child processes exit
function Run-And-Wait {
    param(
        [string]$FilePath,
        [string[]]$Arguments
    )

    Write-Host "Starting installer: $FilePath $($Arguments -join ' ')"
    # Start process and get its PID
    $proc = Start-Process -FilePath $FilePath -ArgumentList $Arguments -PassThru
    # Wait for the initial process to exit
    Wait-Process -Id $proc.Id -ErrorAction SilentlyContinue

    # Determine base process name (no extension)
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($FilePath)

    # Wait until no processes with that base name are running
    do {
        $children = Get-Process -Name $baseName -ErrorAction SilentlyContinue
        if ($children) {
            Start-Sleep -Seconds 3
        }
    } while ($children)

    Write-Host "Installer completed: $baseName"
}

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Installer paths
$realtekInstaller = Join-Path $scriptDir 'Realtek.exe'
$intelInstaller   = Join-Path $scriptDir 'INTEL\Wired_driver_28.2.1_x64.exe'
$networkTuningBat = Join-Path $scriptDir 'networktuning.bat'

# Run Realtek installer
Run-And-Wait -FilePath $realtekInstaller -Arguments @('/silent','/S')

# Run Intel installer
Run-And-Wait -FilePath $intelInstaller -Arguments @('/silent','/S')

# Run network tuning batch file (will wait automatically)
Write-Host "Starting network tuning script: $networkTuningBat"
& "$networkTuningBat"
Write-Host "Network tuning completed."

Write-Host "All operations finished successfully."
