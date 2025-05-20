
$ErrorActionPreference = "Stop"

Write-Host "🧪 Running test coverage for all Django apps..."


$env:DJANGO_SETTINGS_MODULE = "sahabi.settings"  





$appDirs = Get-ChildItem -Directory | Where-Object {
    $_.Name -notin @('venv', 'env', 'static', 'media', '__pycache__','tests') -and
    (Test-Path "$($_.FullName)\migrations")
} | ForEach-Object { $_.Name }


$sourceApps = $appDirs -join ','


coverage run --source=$sourceApps manage.py test


coverage report -m


coverage html

Write-Host "✅ Coverage HTML report available at: htmlcov\index.html"
