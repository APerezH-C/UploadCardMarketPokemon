@echo off
echo ============================================================
echo CARDMARKET BOT - STEALTH MODE (ANTI-CLOUDFLARE)
echo ============================================================
echo 21 anti-detection techniques active
echo Webdriver hidden + Fingerprints spoofed
echo Persistent profile (cookies saved between sessions)
echo ============================================================
echo First time: Solve captcha if it appears (only once)
echo Following times: NO MORE CAPTCHA
echo ============================================================
echo.

if "%1"=="" (
    echo Usage: run_bot_chrome.bat cards_file.csv
    echo Example: run_bot_chrome.bat example_cards.csv
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\python.exe" (
    echo [INFO] Using virtual environment
    venv\Scripts\python.exe cardmarket_bot_chrome.py %*
) else (
    echo [INFO] Using system Python
    "C:\Users\byjan\AppData\Local\Programs\Python\Python312\python.exe" cardmarket_bot_chrome.py %*
)

pause
