import argparse
import os
import sys
import requests
import subprocess

def install_requirements(requirements_file):
    try:
        with open(requirements_file, 'r') as file:
            for line in file:
                package = line.strip()
                if package and not package.startswith('#'):
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    except Exception as e:
        print(f"An error occurred: {e}")


if os.geteuid() != 0:
    print("Please run the setup as sudo example: sudo python3 setup.py --key API_KEY")
    sys.exit(1)
parser = argparse.ArgumentParser(description='ePrint setup.')
parser.add_argument('--key', required=True, help='The API key for the application')

args = parser.parse_args()
key = args.key
## VERIFY APIKEY
req = requests.get("http://eprint.id/api/VERIFY/status", headers={"X-API-KEY":key}).status_code
if req == 401:
    print("Invalid API KEY")
    sys.exit(1)
requirements_file = 'requirements.txt'
install_requirements(requirements_file)
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
os.chmod("run.sh", 0o755)
with open("/etc/xdg/lxsession/LXDE-pi/autostart", "a") as f:
    f.write("\n@"+cwd+"/run.sh\n")
print("Sucessfully setup")
print("Now you can try to reboot")