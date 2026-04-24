#!/bin/bash
# ============================================
# AMR Prediction System — Single Command Start
# ============================================
# Starts both Flask backend (port 5000) and
# Next.js frontend (port 3000) simultaneously.
#
# Usage: ./start.sh
# Stop:  Ctrl+C (kills both)
# ============================================

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}==============================${NC}"
echo -e "${GREEN} AMR Prediction System        ${NC}"
echo -e "${GREEN}==============================${NC}"
echo ""

# Check if venv exists
if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "$BACKEND_DIR/venv"
    source "$BACKEND_DIR/venv/bin/activate"
    pip install -r "$BACKEND_DIR/requirements.txt"
else
    source "$BACKEND_DIR/venv/bin/activate"
fi

# Check if model exists
if [ ! -f "$BACKEND_DIR/data/models/multi_rf_model.pkl" ]; then
    echo "Training ML model (first run)..."
    cd "$BACKEND_DIR"
    python -m app.ml.train
fi

# Check if node_modules exists
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd "$FRONTEND_DIR"
    npm install
fi

# Trap Ctrl+C to kill both processes
trap 'echo ""; echo "Shutting down..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT TERM

# Start Flask backend
echo -e "${BLUE}Starting Flask backend on http://localhost:5001${NC}"
cd "$BACKEND_DIR"
source venv/bin/activate
python run.py &
BACKEND_PID=$!

# Start Next.js frontend
echo -e "${BLUE}Starting Next.js frontend on http://localhost:3000${NC}"
cd "$FRONTEND_DIR"
npm run dev &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}==============================${NC}"
echo -e "${GREEN} Both servers running!         ${NC}"
echo -e "${GREEN}                              ${NC}"
echo -e "${GREEN} Frontend: http://localhost:3000${NC}"
echo -e "${GREEN} Backend:  http://localhost:5001${NC}"
echo -e "${GREEN} API:      http://localhost:5001/api/predict${NC}"
echo -e "${GREEN}                              ${NC}"
echo -e "${GREEN} Press Ctrl+C to stop both    ${NC}"
echo -e "${GREEN}==============================${NC}"
echo ""

# Wait for both
wait
