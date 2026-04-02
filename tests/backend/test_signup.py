"""
Tests for the signup endpoint /activities/{activity_name}/signup
"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestSignupForActivity:
    def test_signup_success(self):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

        # Verify the student was added
        get_response = client.get("/activities")
        activities = get_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_activity_not_found(self):
        # Arrange
        activity_name = "NonExistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_already_signed_up(self):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_signup_at_max_capacity(self):
        # Arrange - fill an activity to max capacity
        activity_name = "Tennis Club"  # max_participants: 10
        base_email = "teststudent"
        domain = "@mergington.edu"

        # Add participants up to max
        for i in range(10 - len(client.get("/activities").json()[activity_name]["participants"])):
            email = f"{base_email}{i}{domain}"
            client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Now try to add one more (should succeed with current logic)
        extra_email = f"{base_email}extra{domain}"

        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": extra_email})

        # Assert - currently allows overbooking
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

        # Verify the extra student was added despite max capacity
        get_response = client.get("/activities")
        activities = get_response.json()
        assert extra_email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) > activities[activity_name]["max_participants"]