@echo off
echo ============================================================
echo Activating Virtual Environment
echo ============================================================
echo.
call venv\Scripts\activate.bat
echo.
echo [OK] Virtual environment activated!
echo [INFO] Python: venv\Scripts\python.exe
echo.
echo To run the bot:
echo   python cardmarket_bot_chrome.py example_cards.csv
echo.
echo To deactivate:
echo   deactivate
echo.
