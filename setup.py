import argparse
import os
import sys
import requests

if os.geteuid() != 0:
    print("Please run the setup as sudo example: sudo python3 setup.py --key API_KEY")
    sys.exit(1)
parser = argparse.ArgumentParser(description='ePrint setup.')
parser.add_argument('--key', required=True, help='The API key for the application')

args = parser.parse_args()
key = args.key
## VERIFY APIKEY
req = requests.get("http://localhost:8000/api/VERIFY/status", headers={"X-API-KEY":"7404bdb5-2fea-424c-8bfa-6c42eca5102a"}).status_code
if req == 401:
    print("Invalid API KEY")
    sys.exit(1)
cwd = os.getcwd()
script = f"""#!/bin/bash
export EPRINT_API_KEY="{key}"
cd {cwd}
python3 app.py &
sleep 10
chromium-browser --start-fullscreen --app=http://localhost:5000
"""
with open("run.sh", "w") as f:
    f.write(script)
os.chmod("run.sh", current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
with open("/etc/xdg/lxsession/LXDE-pi/autostart", "a") as f:
    f.write("@"+cwd+"/run.sh")
print("Sucessfully setup")
print("Now you can try to reboot")