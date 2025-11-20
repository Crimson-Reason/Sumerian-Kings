<#
push_to_fork.ps1

Helper script to push the current branch to a fork/remote and display next steps for creating a Pull Request.

Usage:
  .\push_to_fork.ps1                        # push current branch to 'fork' remote if present, otherwise 'origin'
  .\push_to_fork.ps1 -ForkUrl <url>         # add/update remote named 'fork' to <url> and push
  .\push_to_fork.ps1 -Branch feature-xyz    # push specific branch

Notes:
- This script does not create the PR on GitHub automatically. It prints the exact commands/URLs
  to create a PR using your browser or gh/other tools.
- Use HTTPS+Git Credential Manager or an SSH key configured with GitHub to authenticate pushes.
#>

param(
    [string]$ForkUrl = '',
    [string]$Branch = ''
)

function Exec-Git {
    param([string[]]$Args)
    $proc = Start-Process -FilePath git -ArgumentList $Args -NoNewWindow -RedirectStandardOutput -RedirectStandardError -PassThru -Wait
    return $proc.ExitCode
}

if (-not (Test-Path -Path .git)) {
    Write-Error "This folder is not a git repository (no .git). Run this from the repo root."
    exit 1
}

if (-not $Branch) {
    $Branch = (& git rev-parse --abbrev-ref HEAD).Trim()
}

if ($ForkUrl) {
    Write-Host "Adding/updating remote 'fork' -> $ForkUrl" -ForegroundColor Cyan
    & git remote remove fork 2>$null
    & git remote add fork $ForkUrl
}

$remotes = & git remote -v
Write-Host "Current remotes:" -ForegroundColor Gray
Write-Host $remotes

# Choose remote preference: fork then origin
$targetRemote = 'fork'
$remList = (& git remote).Trim().Split("`n").Trim()
if (-not ($remList -contains $targetRemote)) { $targetRemote = 'origin' }
if (-not ($remList -contains $targetRemote)) {
    Write-Error "No 'fork' or 'origin' remote found. Add a remote or supply -ForkUrl."; exit 1
}

Write-Host "Pushing branch '$Branch' to remote '$targetRemote'..." -ForegroundColor Cyan
& git push $targetRemote $Branch

if ($LASTEXITCODE -ne 0) {
    Write-Error "git push failed. Check credentials or remote url."; exit 1
}

Write-Host "Push succeeded. Next steps to create a Pull Request:" -ForegroundColor Green
Write-Host "1) Open the compare page in your browser:" -ForegroundColor Gray
try {
    $repoUrlLine = (& git remote get-url $targetRemote).Trim()
    # convert git@ form to https if necessary
    if ($repoUrlLine -match '^git@github.com:(.+)\.git$') { $https = "https://github.com/$($Matches[1])" } elseif ($repoUrlLine -match '^https?://') { $https = $repoUrlLine -replace '\.git$','' } else { $https = $repoUrlLine }
    $prUrl = "$https/compare/$Branch?expand=1"
    Write-Host "   $prUrl" -ForegroundColor Cyan
    Write-Host "2) Or use the GitHub CLI (if installed): `gh pr create --base main --head $Branch`" -ForegroundColor Gray
} catch {
    Write-Host "Could not determine remote URL; open GitHub and create a PR from your fork's branch to the upstream repo." -ForegroundColor Yellow
}
