from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tasks = []

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'description' not in data:
        return jsonify({'error': 'Description required'}), 400

    task = {'id': len(tasks) + 1, 'description': data['description']}
    tasks.append(task)
    return jsonify(task)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
