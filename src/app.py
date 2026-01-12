from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# 1. Configure the Database (SQLite for now)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. Initialize Plugins
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 3. Define the Table (The Schema)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "db": "connected"}), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Fetch real data from DB
    tasks = Task.query.all()
    output = []
    for task in tasks:
        output.append({"id": task.id, "title": task.title, "done": task.done})
    return jsonify({"tasks": output}), 200

# Helper to create DB (only for local testing)
# NEW WAY: Create tables immediately using app_context
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) # nosec
