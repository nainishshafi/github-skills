# sync-forks.ps1 — Clone or pull all GitHub forks for a user
# Requires: gh CLI (authenticated), git

foreach ($cmd in @('gh', 'git')) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Error "Error: '$cmd' is required but not found on PATH. Install it and retry."
        exit 1
    }
}

$GITHUB_USERNAME = (gh api user | ConvertFrom-Json).login
$BASE_DIR = if ($env:BASE_DIR) { $env:BASE_DIR } else { Join-Path $env:USERPROFILE 'git-repos' }
New-Item -ItemType Directory -Path $BASE_DIR -Force | Out-Null

$cloned = 0
$pulled = 0
$failed = 0
$page   = 1

Write-Host "Fetching forks for $GITHUB_USERNAME ..."

while ($true) {
    $repos = gh api "user/repos?type=forks&per_page=100&page=$page" | ConvertFrom-Json
    if (-not $repos -or $repos.Count -eq 0) { break }

    foreach ($repo in $repos) {
        $name      = $repo.name
        $ssh_url   = $repo.ssh_url
        $local_dir = Join-Path $BASE_DIR $name

        if (Test-Path (Join-Path $local_dir '.git')) {
            $branch = try { git -C $local_dir rev-parse --abbrev-ref HEAD 2>$null } catch { 'main' }
            if (-not $branch) { $branch = 'main' }
            Write-Host "  [pull]   $name (branch: $branch)"
            git -C $local_dir pull origin $branch --ff-only 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) { $pulled++ } else {
                Write-Warning "  [failed] $name (pull error)"
                $failed++
            }
        } else {
            Write-Host "  [clone]  $name -> $local_dir"
            git clone $ssh_url $local_dir 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) { $cloned++ } else {
                Write-Warning "  [failed] $name (clone error)"
                $failed++
            }
        }
    }

    $page++
}

Write-Host ""
Write-Host "Done — cloned $cloned, pulled $pulled, failed $failed"
