import os
from flask import Flask, render_template
from flask_cors import CORS
import cups
import time
import requests

baseURL = "http://localhost:8000/api"
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
    request = requests.get(f"{baseURL}/initialize", headers=headers)
    return request.json()

@app.route('/api/<id>/status')
def checkSession(id):
    request = requests.get(f"{baseURL}/{id}/status", headers=headers)
    data = request.json()
    # time.sleep(1)
    if data['status'] == 0:
        time.sleep(1)
    elif data['status'] == 3:
        request = requests.post(f"{baseURL}/{id}/status", data={"status":4}, headers=headers)
        conn = cups.Connection()
        printers = conn.getPrinters()
        printer_name = 'PRINTER-1'
        document_path = f'{baseURL}/uploads/{id}/file.pdf'
        print_job_id = conn.printFile(printer_name, document_path, f"JOB-{id}", {})
    else:
        time.sleep(3)
    return request.json()

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
