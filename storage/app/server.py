from flask import Flask, request
import os

app = Flask(__name__)
LOG_FILE = os.path.join(os.path.dirname(__file__), 'storage_log.txt')

@app.route('/log', methods=['POST'])
def add_log():
    print(f"Raw data: {request.data}")  # Debug raw input
    record = request.data.decode('utf-8')  # Try decoding raw data
    if not record:  
        record = request.get_data().decode('utf-8')  
    # print(f"Received: {record}")  
    with open(LOG_FILE, 'a', encoding='utf-8') as f:  
        f.write(record + '\n')
    return '', 200

@app.route('/log', methods=['GET'])
def get_log():
    if os.path.exists(LOG_FILE):  
        with open(LOG_FILE, 'r') as f:  
            return f.read(), 200, {'Content-Type': 'text/plain'}  
    return '', 200  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)