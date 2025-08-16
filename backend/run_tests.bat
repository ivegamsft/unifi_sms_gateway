@echo off
REM Test runner script for the SMS Gateway API
echo Starting SMS Gateway API tests...

REM Start the Flask app in the background
echo Starting Flask app...
start /B python sms.py

REM Wait a moment for the server to start
timeout /t 3 /nobreak >nul

REM Run the test
echo Running API tests...
python test_api.py

REM Check if test passed
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ All tests passed!
) else (
    echo.
    echo ✗ Tests failed!
)

REM Kill the Flask app process
echo Stopping Flask app...
taskkill /f /im python.exe >nul 2>&1

echo Test run complete.
pause
