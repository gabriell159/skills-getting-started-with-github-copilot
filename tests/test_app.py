def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_for_activity_adds_participant(client):
    email = "test_student@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"]
    assert email in participants


def test_duplicate_signup_returns_400(client):
    email = "michael@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_delete_participant_removes_student(client):
    email = "daniel@mergington.edu"
    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"

    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"]
    assert email not in participants


def test_delete_nonexistent_participant_returns_404(client):
    email = "unknown@mergington.edu"
    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
