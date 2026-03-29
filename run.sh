#!/bin/bash
echo "=========================================="
echo "Installing dependencies for Vision Price Net"
echo "=========================================="
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

echo "=========================================="
echo "Starting the Flask app..."
echo "=========================================="
# open browser automatically
xdg-open http://127.0.0.1:5000 2>/dev/null || open http://127.0.0.1:5000

python3 app.py

Notes:
xdg-open works on Linux, open works on macOS.
Make the script executable once

    .   chmod +x run.sh

Then you can run it with:
        . ./run.sh
