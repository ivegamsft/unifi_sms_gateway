# Test Suite Organization

This directory contains tests organized by application tier and scope.

## Directory Structure

```
tests/
├── backend/                 # Backend API unit tests
│   └── test_api.py         # Flask API endpoint tests
├── frontend/               # Frontend unit and component tests
│   └── (Vue.js test files)
├── integration/            # End-to-end integration tests
│   ├── test_device_connection.py    # Full API-to-device integration (urllib-based)
│   └── test_sms_device.py          # SMS device communication tests (requests-based)
└── README.md              # This file
```

## Test Categories

### Backend Tests (`tests/backend/`)
- **Purpose**: Test Flask API endpoints, authentication, and business logic
- **Scope**: Backend API layer only
- **Dependencies**: Requires virtual environment activation
- **Run from**: `F:\Git\unifi_sms_gateway` (root)
- **Command**: 
  ```powershell
  & .\.venv\Scripts\Activate.ps1
  cd tests\backend
  python test_api.py
  ```

### Frontend Tests (`tests/frontend/`)
- **Purpose**: Test Vue.js components, user interactions, and frontend logic
- **Scope**: Frontend application layer
- **Dependencies**: Node.js/npm
- **Run from**: `F:\Git\unifi_sms_gateway\frontend`
- **Command**: 
  ```powershell
  cd frontend
  npm test
  ```

### Integration Tests (`tests/integration/`)
- **Purpose**: Test full application flow from frontend through backend to SMS device
- **Scope**: End-to-end functionality
- **Dependencies**: 
  - Backend server running (port 8585)
  - UniFi SMS device accessible
  - Environment variables configured
- **Run from**: `F:\Git\unifi_sms_gateway` (root)
- **Command**:
  ```powershell
  & .\.venv\Scripts\Activate.ps1
  cd tests\integration
  python test_device_connection.py
  python test_sms_device.py
  ```

## Test Execution Order

1. **Backend Tests**: Ensure API endpoints work correctly
2. **Frontend Tests**: Verify UI components and interactions
3. **Integration Tests**: Validate complete application workflow

## Environment Requirements

### For Backend/Integration Tests:
- Python virtual environment activated
- `backend/.env` file configured with:
  - `SMS_API_KEY`
  - `UNIFI_HOST`, `UNIFI_USERNAME`, `UNIFI_PASSWORD`
  - `DEFAULT_SHARED_KEY`

### For Frontend Tests:
- Node.js environment
- Frontend dependencies installed (`npm install`)

## Test Files Description

### `test_api.py`
- Tests basic SMS API endpoints
- Validates authentication mechanisms
- Checks response formats and status codes

### `test_device_connection.py`
- Uses only built-in Python libraries (urllib)
- Tests API server connectivity
- Validates authentication workflows
- Tests device communication
- Retrieves SMS messages
- Provides detailed device information

### `test_sms_device.py`
- Uses external dependencies (requests)
- Similar functionality to device_connection test
- Alternative implementation for comparison

## Running All Tests

To run the complete test suite:

```powershell
# From project root
cd F:\Git\unifi_sms_gateway

# Backend tests
& .\.venv\Scripts\Activate.ps1
python tests\backend\test_api.py

# Integration tests (requires backend server running)
python tests\integration\test_device_connection.py
python tests\integration\test_sms_device.py

# Frontend tests
cd frontend
npm test
```
