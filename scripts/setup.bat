@echo off
echo Setting up UniFi SMS Gateway development environment...

REM Create Python virtual environment for backend
echo Creating Python virtual environment...
cd backend
python -m venv venv

REM Activate virtual environment and install dependencies
echo Installing Python dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Initialize database (optional - requires PostgreSQL running)
echo Setting up database migrations...
set FLASK_APP=app.py
flask db init 2>nul
flask db migrate -m "Initial migration" 2>nul
flask db upgrade 2>nul

cd ..

REM Install frontend dependencies
echo Installing frontend dependencies...
cd frontend
npm install
cd ..

echo Setup complete!
echo.
echo To start the application:
echo 1. Start PostgreSQL database
echo 2. Run 'scripts\start-dev.bat' or use Docker: 'docker-compose -f docker\docker-compose.yml up'
pause
