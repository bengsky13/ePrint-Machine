#!/bin/bash
export EPRINT_API_KEY="ASD"
cd /home/bengsky/capstone/ePrint-Machine
python3 app.py &
sleep 10
chromium-browser --start-fullscreen --app=http://localhost:5000
