import argparse
import os
import sys
import requests
import subprocess



if os.geteuid() != 0:
    print("Please run the setup as sudo example: sudo python3 setup.py --key API_KEY")
    sys.exit(1)
parser = argparse.ArgumentParser(description='ePrint setup.')
parser.add_argument('--key', required=True, help='The API key for the application')

args = parser.parse_args()
key = args.key
## VERIFY APIKEY
req = requests.get("http://eprints.id/api/VERIFY/status", headers={"X-API-KEY":key}).status_code
if req == 401:
    print("Invalid API KEY")
    sys.exit(1)
try:
    pip_install_command = [
    'sudo', '-u', 'pi', 'pip', 'install', '--user','--break-system-packages', '-r', 'requirements.txt'
    ]
    pip_install_command = [
    'apt-get','install','unclutter'
    ]
    subprocess.check_call(pip_install_command)
    cwd = os.getcwd()
    script = f"""#!/bin/bash
    export EPRINT_API_KEY="{key}"
    cd {cwd}
    python3 app.py &
    sleep 10
    chromium-browser --start-fullscreen --force-device-scale-factor=3 --app=http://localhost:5000
    """
    with open("run.sh", "w") as f:
        f.write(script)
    os.chmod("run.sh", 0o755)
    with open("/etc/xdg/lxsession/LXDE-pi/autostart", "a") as f:
        f.write("\n@unclutter -idle 0\n@"+cwd+"/run.sh\n")
    print("Sucessfully setup")
    print("Now you can try to reboot")
except:
    print("Setup Failed")