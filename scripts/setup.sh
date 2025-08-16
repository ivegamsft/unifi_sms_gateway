#!/bin/bash

echo "Setting up UniFi SMS Gateway development environment..."

# Create Python virtual environment for backend
echo "Creating Python virtual environment..."
cd backend
python -m venv venv

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

pip install -r requirements.txt

# Initialize database
echo "Setting up database..."
flask db init || true
flask db migrate -m "Initial migration" || true
flask db upgrade || true

cd ..

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "Setup complete!"
echo ""
echo "To start the application:"
echo "1. Start PostgreSQL database"
echo "2. Run './scripts/start-dev.sh' or use Docker: 'docker-compose -f docker/docker-compose.yml up'"
