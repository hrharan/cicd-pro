import pytest
import sys
import os

# Add 'src' to the python path so we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    rv = client.get('/health')
    assert rv.status_code == 200
    assert rv.json['status'] == 'healthy'

def test_task_list(client):
    rv = client.get('/tasks')
    assert rv.status_code == 200
    assert 'tasks' in rv.json
