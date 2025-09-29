from flask import Flask, request
import requests
import datetime
import time
import psutil

app = Flask(__name__)

@app.route('/status')
def status():
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds') + 'Z'
    uptime = round((time.time() - psutil.boot_time()) / 3600, 1)
    free_disk = round(psutil.disk_usage('/').free / (1024 * 1024))
    record1 = f"{timestamp}: uptime {uptime} hours, free disk in root: {free_disk} MBytes"

    # Log to Storage 
    try:
        requests.post('http://storage:5050/log', data=record1, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"Failed to log to Storage: {e}")

    # Log to vstorage 
    with open('/vstorage', 'a', encoding='utf-8') as f:
        f.write(record1 + '\n')

    try:
        resp2 = requests.get('http://service2:3000/status', timeout=5)
        record2 = resp2.text
    except requests.exceptions.RequestException as e:
        record2 = f"Error: Could not reach Service2 - {str(e)}"

    return record1 + '\n' + record2, 200, {'Content-Type': 'text/plain'}

@app.route('/log')
def log():
    try:
        resp = requests.get('http://storage:5050/log', timeout=5)
        return resp.text, 200, {'Content-Type': 'text/plain'}
    except requests.exceptions.RequestException as e:
        return f"Error: Could not reach Storage - {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8199)