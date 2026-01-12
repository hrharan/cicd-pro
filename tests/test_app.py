import pytest
import sys
import os

# Add 'src' to the path so we can import the app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app, db, Task

@pytest.fixture
def client():
    # 1. Configure the app for testing
    app.config['TESTING'] = True
    # Use an in-memory SQLite DB (it vanishes after tests)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            # 2. Create the tables (Schema) inside the RAM database
            db.create_all()
            yield client
            # 3. Cleanup: Drop everything after the test finishes
            db.session.remove()
            db.drop_all()

def test_health(client):
    """Test the health check route"""
    rv = client.get('/health')
    assert rv.status_code == 200
    assert rv.json['db'] == 'connected'

def test_task_list_empty(client):
    """Test getting tasks when DB is empty"""
    rv = client.get('/tasks')
    assert rv.status_code == 200
    assert rv.json['tasks'] == []

def test_task_list_with_data(client):
    """Test getting tasks after inserting data"""
    # We must insert data inside an 'app_context'
    with app.app_context():
        new_task = Task(title="Learn CI/CD", done=False)
        db.session.add(new_task)
        db.session.commit()

    rv = client.get('/tasks')
    assert rv.status_code == 200
    assert len(rv.json['tasks']) == 1
    assert rv.json['tasks'][0]['title'] == "Learn CI/CD"
