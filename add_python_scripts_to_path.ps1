<#
add_python_scripts_to_path.ps1

Detect common Python "Scripts" locations and optionally add one to the User PATH permanently.

Usage (PowerShell):
  .\add_python_scripts_to_path.ps1         # lists detected candidate paths
  .\add_python_scripts_to_path.ps1 -Add 1  # add candidate #1 to user PATH (persisted)

Be careful: modifying PATH is permanent for the current user. This script only touches the
User PATH (not System PATH). You may need to open a new terminal or sign out/in for
the change to be visible to other programs.
#>

param(
    [int]$Add = 0
)

function Get-Candidate-ScriptDirs {
    $candidates = [System.Collections.Generic.List[string]]::new()

    # If python on PATH, infer Scripts path
    try {
        $pythonCmd = (Get-Command python -ErrorAction Stop).Source
    } catch {
        try { $pythonCmd = (Get-Command python3 -ErrorAction Stop).Source } catch { $pythonCmd = $null }
    }
    if ($pythonCmd) {
        $pyDir = Split-Path -Parent $pythonCmd
        # If python executable is inside 'Scripts', try parent
        if ((Split-Path -Leaf $pyDir) -ieq 'Scripts') { $candidates.Add((Split-Path -Parent $pyDir)) }
        $candidates.Add((Join-Path $pyDir 'Scripts'))
    }

    # Common per-user locations
    $user = $env:USERPROFILE
    if ($user) {
        $candidates.Add((Join-Path $env:LocalAppData 'Programs\Python\Python*\Scripts'))
        $candidates.Add((Join-Path $env:APPDATA 'Python\Python*\Scripts'))
        $candidates.Add((Join-Path $env:USERPROFILE 'AppData\Roaming\Python\Python*\Scripts'))
    }

    # Resolve glob candidates to existing directories
    $resolved = [System.Collections.Generic.List[string]]::new()
    foreach ($c in $candidates) {
        try {
            Get-ChildItem -Path $c -Directory -ErrorAction SilentlyContinue | ForEach-Object { $resolved.Add($_.FullName) }
        } catch { }
    }

    # Remove duplicates and return
    return $resolved | Sort-Object -Unique
}

$cands = Get-Candidate-ScriptDirs
if (-not $cands -or $cands.Count -eq 0) {
    Write-Host "No candidate Python Scripts directories detected on this system." -ForegroundColor Yellow
    Write-Host "If you know the path to your Python Scripts folder, run: [Environment]::SetEnvironmentVariable('PATH', [Environment]::GetEnvironmentVariable('PATH','User') + ';C:\path\to\Scripts','User')" -ForegroundColor Gray
    exit 0
}

Write-Host "Detected candidate Python Scripts directories:" -ForegroundColor Cyan
$i = 0
foreach ($p in $cands) { $i++; Write-Host "[$i] $p" }

if ($Add -gt 0) {
    if ($Add -le $cands.Count) {
        $chosen = $cands[$Add - 1]
        $current = [Environment]::GetEnvironmentVariable('PATH','User')
        if ($current -and $current.ToLower().Contains($chosen.ToLower())) {
            Write-Host "Chosen path is already in User PATH." -ForegroundColor Yellow
        } else {
            $new = if ($current) { "$current;$chosen" } else { $chosen }
            [Environment]::SetEnvironmentVariable('PATH', $new, 'User')
            Write-Host "Added to User PATH: $chosen" -ForegroundColor Green
            Write-Host "You may need to open a new PowerShell window for changes to take effect." -ForegroundColor Gray
        }
    } else {
        Write-Error "Invalid selection index for -Add. Choose a number between 1 and $($cands.Count)."
    }
} else {
    Write-Host "To add one of the above to your User PATH, re-run this script with -Add <n> (e.g. -Add 1)." -ForegroundColor Gray
}
