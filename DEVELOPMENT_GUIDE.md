# Development Instructions

## Directory Structure
```
F:\Git\unifi_sms_gateway\
├── backend/                  # Flask API server
│   ├── venv/                # Python virtual environment (backend specific)
│   ├── requirements.txt      # Python dependencies
│   ├── app.py               # Main Flask app (3-tier architecture)
│   ├── sms.py               # Simple SMS gateway API
│   ├── models.py            # Database models
│   ├── routes/              # API routes
│   └── .env                 # Backend environment variables
├── frontend/                # Vue.js frontend
│   ├── package.json         # Node.js dependencies
│   ├── src/                 # Vue source files
│   └── node_modules/        # Node dependencies
└── scripts/                 # Startup scripts
```

## Backend Development Instructions

### Prerequisites
- Python virtual environment is in backend directory: `backend/venv/`
- Backend files are in `backend/` directory
- Environment file is at `backend/.env`

### Correct Workflow for Backend Tasks:
1. **Navigate to backend directory**: `cd F:\Git\unifi_sms_gateway\backend`
2. **Activate virtual environment**: `& .\venv\Scripts\Activate.ps1`
3. **Install/update dependencies**: `pip install -r requirements.txt`
4. **Run backend server**: `python app.py` (for 3-tier) or `python sms.py` (for simple API)

### Backend Authentication System:
- **User Auth**: Email + Phone + Shared Key (hardcoded in `DEFAULT_SHARED_KEY` env var)
- **API Auth**: JWT tokens for frontend-backend communication
- **Gateway Auth**: SSH credentials for UniFi device access

## Frontend Development Instructions

### Prerequisites
- Node.js and npm installed
- Frontend files are in `frontend/` directory
- Vue.js with Vite build system

### Correct Workflow for Frontend Tasks:
1. **Navigate to frontend directory**: `cd F:\Git\unifi_sms_gateway\frontend`
2. **Install/update dependencies**: `npm install`
3. **Run development server**: `npm run dev`
4. **Build for production**: `npm run build`

### Frontend Configuration:
- **Development URL**: http://localhost:3000 (Vite default)
- **API Base URL**: http://localhost:8585 (Flask backend)
- **Authentication**: JWT tokens stored in localStorage

## Common Mistakes to Avoid:
1. ❌ Don't activate venv from wrong directory
2. ❌ Don't install Python packages globally
3. ❌ Don't run backend commands from frontend directory
4. ❌ Don't run frontend commands from backend directory
5. ❌ Don't forget to activate venv before Python work

## Startup Commands:

### For Backend (from root):
```powershell
cd F:\Git\unifi_sms_gateway
& .\.venv\Scripts\Activate.ps1
cd backend
python app.py
```

### For Frontend (from root):
```powershell
cd F:\Git\unifi_sms_gateway\frontend
npm run dev
```

### For Both (using scripts):
```powershell
cd F:\Git\unifi_sms_gateway
.\scripts\start-dev.bat
```

## Environment Variables:
- Backend: `backend/.env`
- Frontend: Environment-specific configs in `frontend/`

## Port Configuration:
- Backend API: 8585
- Frontend Dev: 3000 (Vite)
- Frontend Build: 5173 (Vite preview)
