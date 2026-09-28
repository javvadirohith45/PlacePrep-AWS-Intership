@echo off
setlocal EnableExtensions
title PlacePrep Startup

cd /d "%~dp0"

echo ======================================
echo          PLACEPREP STARTUP
echo ======================================
echo.

if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found.
    echo Please make sure this BAT file is inside the main PlacePrep folder.
    pause
    exit /b 1
)

echo [1/3] Checking PlacePrep application...
"venv\Scripts\python.exe" -c "import app; print('PlacePrep application loaded successfully.')"
if errorlevel 1 (
    echo.
    echo ERROR: PlacePrep could not start.
    echo Check the error above.
    pause
    exit /b 1
)

echo.
echo [2/3] Starting PlacePrep server...
start "PlacePrep Server" cmd /k ""%~dp0venv\Scripts\python.exe" "%~dp0app.py""

echo.
echo [3/3] Waiting for PlacePrep server...
echo Please wait. The browser will open automatically when the server responds.
echo.

set "READY="
for /L %%N in (1,1,60) do (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:5000/' -UseBasicParsing -TimeoutSec 1; if ($r.StatusCode -ge 200 -and $r.StatusCode -lt 600) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
    if not errorlevel 1 (
        set "READY=1"
        goto :server_ready
    )
    timeout /t 1 /nobreak >nul
)

echo.
echo ERROR: PlacePrep did not respond on http://127.0.0.1:5000
echo.
echo Check the "PlacePrep Server" window for the actual Flask error.
pause
exit /b 1

:server_ready
echo.
echo ======================================
echo       PLACEPREP SERVER IS READY
echo ======================================
echo Opening Microsoft Edge...
start "" msedge.exe "http://127.0.0.1:5000/"
if errorlevel 1 start "" "http://127.0.0.1:5000/"
echo.
echo PlacePrep is running.
echo Keep the "PlacePrep Server" window open.
echo.
timeout /t 3 /nobreak >nul
exit /b 0
