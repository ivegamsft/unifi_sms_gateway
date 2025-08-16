# UniFi SMS Gateway - Development Setup

## Project Overview
A 3-tier application for managing SMS functionality through UniFi devices:
- **Backend**: Flask API with PostgreSQL database
- **Frontend**: Vue.js 3 with Vite
- **Database**: PostgreSQL with user authentication and SMS logging

## Architecture Components

### Backend (Flask API)
- **Location**: `backend/`
- **Main Files**:
  - `app.py` - Main Flask application with CORS and blueprint registration
  - `models/__init__.py` - SQLAlchemy models (User, SMSLog)
  - `services/unifi_service.py` - UniFi device communication via SSH
  - `routes/auth.py` - Authentication endpoints with JWT
  - `routes/sms.py` - SMS sending and history endpoints

### Frontend (Vue.js)
- **Location**: `frontend/`
- **Main Components**:
  - `src/App.vue` - Main application with login/dashboard routing
  - `src/components/LoginForm.vue` - User authentication form
  - `src/components/Dashboard.vue` - SMS management interface

### Database (PostgreSQL)
- **Models**:
  - `User` - email, phone, shared_key (bcrypt hashed), timestamps
  - `SMSLog` - message tracking, status, user relationships

## Quick Start

### Option 1: Using Setup Scripts (Recommended for Windows)
```powershell
# Run the setup script
.\scripts\setup.bat

# Start development servers
.\scripts\start-dev.bat
```

### Option 2: Using Docker
```powershell
# Start all services with Docker
docker-compose -f docker\docker-compose.yml up --build
```

### Option 3: Manual Setup
```powershell
# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
set FLASK_APP=app.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python app.py

# Frontend setup (in new terminal)
cd frontend
npm install
npm run dev
```

## Access Points
- **API**: http://localhost:8585
- **Frontend**: http://localhost:5173 (Vite dev server) or http://localhost:3000 (Docker)
- **Database**: localhost:5432

## Environment Configuration
Ensure your `.env` file in the backend directory contains:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/unifi_sms
SECRET_KEY=your-secret-key-here
UNIFI_HOST=your.unifi.controller.ip
UNIFI_USERNAME=your-unifi-username
UNIFI_PASSWORD=your-unifi-password
```

## API Endpoints

### Authentication
- `POST /auth/login` - User login with email/phone + shared_key
- `POST /auth/users` - Create new user
- `GET /auth/users` - List all users

### SMS Management
- `POST /sms/send` - Send SMS message
- `GET /sms/history` - Get SMS history
- `GET /sms/device-status` - Check UniFi device status
- `GET /sms/received` - Get received messages

## Development Workflow
1. Start PostgreSQL database
2. Run backend Flask API (`python backend/app.py`)
3. Run frontend development server (`npm run dev` in frontend/)
4. Access application at http://localhost:5173
5. Use API at http://localhost:8585

## Testing
Use the test script to validate API functionality:
```powershell
python test_api.py
```

## Production Deployment
Use Docker Compose for production deployment with proper environment variables and security configurations.
