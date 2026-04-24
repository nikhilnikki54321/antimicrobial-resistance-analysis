@echo off
title AMR Prediction System - Setup and Start
echo ============================================
echo   AMR Prediction System - Single Script Start
echo ============================================
echo.

set ROOT_DIR=%~dp0
set BACKEND_DIR=%ROOT_DIR%backend
set FRONTEND_DIR=%ROOT_DIR%frontend

:: 1. Check if backend python virtual environment exists
if not exist "%BACKEND_DIR%\venv" (
    echo Creating Python virtual environment...
    python -m venv "%BACKEND_DIR%\venv"
    call "%BACKEND_DIR%\venv\Scripts\activate.bat"
    echo Installing backend dependencies...
    pip install -r "%BACKEND_DIR%\requirements.txt"
) else (
    call "%BACKEND_DIR%\venv\Scripts\activate.bat"
)

:: 2. Check if machine learning model is trained
if not exist "%BACKEND_DIR%\data\models\multi_rf_model.pkl" (
    echo.
    echo Training ML model ^(first run^)...
    cd /d "%BACKEND_DIR%"
    python -m app.ml.train
)

:: 3. Check if frontend packages are installed
if not exist "%FRONTEND_DIR%\node_modules" (
    echo.
    echo Installing frontend dependencies...
    cd /d "%FRONTEND_DIR%"
    call npm install
)

:: 4. Start the servers
echo.
echo ============================================
echo Starting Flask backend on localhost:5001...
start "AMR Backend Server (Flask)" cmd /k "cd /d "%BACKEND_DIR%" && call venv\Scripts\activate.bat && python run.py"

echo Starting Next.js frontend on localhost:3000...
start "AMR Frontend Server (Next.js)" cmd /k "cd /d "%FRONTEND_DIR%" && npm run dev"

echo.
echo ============================================
echo Both servers have been launched in separate windows!
echo.
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:5001
echo   API:      http://localhost:5001/api/predict
echo.
echo You can close this window now. The servers will keep running 
echo in their own command prompt windows.
echo ============================================
pause
