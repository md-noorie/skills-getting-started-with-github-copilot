"""
Tests for the unregistration endpoint /activities/{activity_name}/signup (DELETE)
"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestUnregisterFromActivity:
    def test_unregister_success(self):
        # Arrange - first signup a student
        activity_name = "Programming Class"
        email = "testunregister@mergington.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Act
        response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

        # Verify the student was removed
        get_response = client.get("/activities")
        activities = get_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_activity_not_found(self):
        # Arrange
        activity_name = "NonExistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_not_signed_up(self):
        # Arrange
        activity_name = "Programming Class"
        email = "notsignedup@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"]