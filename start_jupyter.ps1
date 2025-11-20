<#
start_jupyter.ps1

Simple helper to start a Jupyter Notebook server from this project folder.

Usage (PowerShell):
  .\start_jupyter.ps1              # runs 'python -m notebook' in this folder (foreground)
  .\start_jupyter.ps1 -Port 8889   # run on a different port
  .\start_jupyter.ps1 -NoBrowser   # run with --no-browser

This script uses the first available `python` or `python3` on PATH. If python is not on PATH,
specify the full path to python by setting the `PYTHON_EXE` environment variable before running,
or add Python to your PATH (see `add_python_scripts_to_path.ps1`).
#>

param(
    [switch]$NoBrowser,
    [int]$Port = 8888
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

# Locate python
$pythonCmd = $null
try {
    $cmd = Get-Command python -ErrorAction Stop
    $pythonCmd = $cmd.Source
} catch {
    try {
        $cmd2 = Get-Command python3 -ErrorAction Stop
        $pythonCmd = $cmd2.Source
    } catch {
        if ($env:PYTHON_EXE) { $pythonCmd = $env:PYTHON_EXE }
    }
}

if (-not $pythonCmd) {
    Write-Error "Python executable not found on PATH. Either add Python to PATH or set the PYTHON_EXE environment variable to the full path to python.exe."
    exit 1
}

$args = @('-m','notebook','--notebook-dir', $scriptDir, '--port', $Port.ToString())
if ($NoBrowser) { $args += '--no-browser' }

Write-Host "Starting Jupyter Notebook server in: $scriptDir" -ForegroundColor Cyan
Write-Host "Using Python: $pythonCmd" -ForegroundColor Cyan
Write-Host "Command: $pythonCmd $($args -join ' ')" -ForegroundColor DarkGray

# Run in the current window so user can see the server token and logs
& $pythonCmd @args

Write-Host "Jupyter process ended (if you see this, the server stopped)." -ForegroundColor Yellow
