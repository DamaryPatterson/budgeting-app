$python = Get-Command python -ErrorAction SilentlyContinue

if (-not $python) {
    $bundledPython = "C:\Users\damar\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
    if (Test-Path $bundledPython) {
        $python = $bundledPython
    } else {
        Write-Error "Python was not found. Install Python 3.12+ or update this script with your Python path."
        exit 1
    }
}

& $python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
