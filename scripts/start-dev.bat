@echo off
echo Starting UniFi SMS Gateway in development mode...

REM Start backend API with correct virtual environment path
echo Starting Flask API server...
start "Flask API" cmd /k "cd /d F:\Git\unifi_sms_gateway\backend && venv\Scripts\activate && set FLASK_ENV=development && set FLASK_DEBUG=1 && python app.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend development server
echo Starting Vue.js frontend...
start "Vue Frontend" cmd /k "cd /d F:\Git\unifi_sms_gateway\frontend && npm run dev"

echo Both services are starting...
echo API will be available at: http://localhost:8585
echo Frontend will be available at: http://localhost:3000
echo.
echo Press any key to stop all services...
pause >nul

REM Kill both processes
taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul
echo Services stopped.
