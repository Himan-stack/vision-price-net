@echo off
echo ==========================================
echo Installing dependencies for Vision Price Net
echo ==========================================
pip install --upgrade pip
pip install -r requirements.txt

echo ==========================================
echo Starting the Flask app...
echo ==========================================
start http://127.0.0.1:5000
python app.py

pause

Notes:

start http://127.0.0.1:5000 opens your default browser automatically.

pause keeps the terminal open so you can see logs/errors.