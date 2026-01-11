from flask import Flask, jsonify, request

app = Flask(__name__)

# A mock database (List of dictionaries)
tasks = [
    {"id": 1, "title": "Learn CI/CD", "done": False},
    {"id": 2, "title": "Build Docker", "done": True}
]

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks, "count": len(tasks)}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
