from flask import Flask, request

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def append_log():
    log_file = 'storage_log.txt'
    
    record = request.data.decode('utf-8').strip()
    
    if record:
        with open(log_file, 'a') as f:
            f.write(record + '\n')
        return 'Log appended successfully', 200
    else:
        return 'No record provided', 400

@app.route('/log', methods=['GET'])
def get_log():
    log_file = 'storage_log.txt'
    
    try:
        with open(log_file, 'r') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/plain'}
    except FileNotFoundError:
        return 'No log entries yet', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)