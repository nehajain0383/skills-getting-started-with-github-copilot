import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Fixture to reset activities before each test
@pytest.fixture(autouse=True)
def reset_activities():
    # Reset to initial state
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Practice and compete in basketball games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Soccer Club": {
            "description": "Train and play soccer matches",
            "schedule": "Wednesdays and Saturdays, 3:00 PM - 5:00 PM",
            "max_participants": 22,
            "participants": []
        },
        "Art Club": {
            "description": "Explore painting, drawing, and other visual arts",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Drama Club": {
            "description": "Act in plays and learn theater skills",
            "schedule": "Tuesdays and Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": []
        },
        "Debate Club": {
            "description": "Practice public speaking and argumentation",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": []
        },
        "Science Club": {
            "description": "Conduct experiments and learn about science",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        }
    })

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    assert response.url.path == "/static/index.html"

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert len(data["Chess Club"]["participants"]) == 2

def test_signup_success():
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up newstudent@mergington.edu for Chess Club" in data["message"]
    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]

def test_signup_duplicate():
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up" in data["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    response = client.delete("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered michael@mergington.edu from Chess Club" in data["message"]
    # Check if removed
    response = client.get("/activities")
    data = response.json()
    assert "michael@mergington.edu" not in data["Chess Club"]["participants"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess%20Club/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student not signed up" in data["detail"]

def test_unregister_invalid_activity():
    response = client.delete("/activities/Invalid%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]