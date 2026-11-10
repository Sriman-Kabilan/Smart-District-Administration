#!/bin/bash

echo "Setting up District Administration Dashboard for local development..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Install frontend dependencies
echo "Installing frontend dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env file with your database credentials"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-jose passlib python-multipart pandas numpy scikit-learn plotly altair

echo "Setup complete!"
echo ""
echo "To run the application:"
echo "1. Start backend: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"
echo "2. Start frontend: npm start"
echo ""
echo "Make sure to:"
echo "- Set up your PostgreSQL database"
echo "- Update the DATABASE_URL in .env file"
echo "- Create the database: createdb district_admin"