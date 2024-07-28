import os
from flask import Flask, render_template
from flask_cors import CORS
import cups
import time
import requests

baseURL = "https://eprints.id/api"
API_KEY = os.getenv("EPRINT_API_KEY")
app = Flask(__name__)
CORS(app)
headers = {
    "X-API-KEY": API_KEY
}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/init')
def init():
    headers = {
        "X-API-KEY": API_KEY
    }
    request = requests.get(f"{baseURL}/initialize", headers=headers, verify=False)
    return request.json()

@app.route('/api/<id>/status')
def checkSession(id):
    request = requests.get(f"{baseURL}/{id}/status", headers=headers, verify=False)
    data = request.json()
    # time.sleep(1)
    if data['status'] == 0:
        time.sleep(1)
    elif data['status'] == 4:
        requests.post(f"{baseURL}/{id}/update", data={"status":5}, headers=headers, verify=False)
        conn = cups.Connection()
        printers = conn.getPrinters()
        printer_name = list(printers.keys())[0]
        printer_name = 'EPSON_L120_Series'
        options = {
        'print-quality': '5',
        'print-color-mode': 'color' if data['color'] == 2 else 'monochrome'
        }
        document_path = f'{baseURL}/../uploads/{id}/file.pdf'
        response = requests.get(document_path, verify=False)
        file_path = '/tmp/'+id
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print_job_id = conn.printFile(printer_name, file_path, f"JOB-{id}", {})
    elif data['status'] == 5:
        conn = cups.Connection()
        jobs = conn.getJobs()
        if str(jobs) == "{}":
            requests.post(f"{baseURL}/{id}/update", data={"status":6}, headers=headers, verify=False)
    else:
        time.sleep(3)
    return request.json()

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
