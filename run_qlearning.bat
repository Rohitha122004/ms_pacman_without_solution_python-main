@echo off
echo === PacMan Q-Learning Agent ===
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "src\Executer.py" (
    echo ERROR: Please run this from the PacMan RL project directory
    pause
    exit /b 1
)

echo Starting Q-Learning Agent...
echo.

REM Run the Q-learning script with default settings (visual mode)
python run_qlearning.py

echo.
echo Script completed.
pause
