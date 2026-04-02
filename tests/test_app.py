import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Initial activities data for resetting between tests
initial_activities = {
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
    "Math Club": {
        "description": "Explore advanced mathematics and problem-solving techniques",
        "schedule": "Wednesdays, 3:45 PM - 4:45 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop critical thinking and public speaking skills through debate",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["sophia@mergington.edu", "marcus@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball training and matches",
        "schedule": "Tuesdays, Thursdays, Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu", "ryan@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis skills and compete in friendly matches",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 12,
        "participants": ["claire@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and various art mediums",
        "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Drama Club": {
        "description": "Perform in theatrical productions and develop acting skills",
        "schedule": "Mondays, Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["avery@mergington.edu", "noah@mergington.edu"]
    },
    "Music Band": {
        "description": "Learn and perform music in our school band",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 4:45 PM",
        "max_participants": 25,
        "participants": ["mia@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities data before each test to ensure isolation."""
    activities.clear()
    activities.update(initial_activities)

client = TestClient(app)

def test_get_activities():
    """Test GET /activities returns all activities with correct structure."""
    # Arrange
    # (TestClient initialized)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    for name, activity in data.items():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

def test_root_redirect():
    """Test GET / serves the static index page."""
    # Arrange
    # (TestClient initialized)

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert "Mergington High School" in response.text

def test_signup_valid():
    """Test POST /activities/{name}/signup with valid data."""
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_count = len(activities[activity]["participants"])

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]
    assert email in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == initial_count + 1

def test_signup_duplicate():
    """Test POST /activities/{name}/signup with duplicate email."""
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]

def test_signup_invalid_activity():
    """Test POST /activities/{name}/signup with non-existent activity."""
    # Arrange
    activity = "NonExistent Club"
    email = "test@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]

def test_unregister_valid():
    """Test DELETE /activities/{name}/signup with valid data."""
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    initial_count = len(activities[activity]["participants"])

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result["message"]
    assert email not in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == initial_count - 1

def test_unregister_not_signed_up():
    """Test DELETE /activities/{name}/signup when student not signed up."""
    # Arrange
    activity = "Chess Club"
    email = "notsignedup@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "not signed up" in result["detail"]

def test_unregister_invalid_activity():
    """Test DELETE /activities/{name}/signup with non-existent activity."""
    # Arrange
    activity = "NonExistent Club"
    email = "test@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]