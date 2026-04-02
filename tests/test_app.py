"""
Tests for the High School Management System API

Using AAA (Arrange-Act-Assert) testing pattern to structure tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


class TestGetActivities:
    """Test cases for getting activities"""

    def test_get_activities_success(self, client):
        # Arrange - Set up any preconditions (none needed for this endpoint)

        # Act - Make the request to get activities
        response = client.get("/activities")

        # Assert - Verify the response
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0
        assert "Chess Club" in activities
        assert "Programming Class" in activities

    def test_get_activities_structure(self, client):
        # Arrange - Set up any preconditions (none needed)

        # Act - Make the request
        response = client.get("/activities")

        # Assert - Verify the structure of activity data
        assert response.status_code == 200
        activities = response.json()
        chess_club = activities["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)


class TestSignupForActivity:
    """Test cases for signing up for activities"""

    def test_signup_success(self, client):
        # Arrange - Prepare test data
        activity_name = "Chess Club"
        email = "test@student.edu"

        # Act - Make the signup request
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert - Verify the signup was successful
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]
        assert activity_name in result["message"]

    def test_signup_activity_not_found(self, client):
        # Arrange - Use a non-existent activity
        activity_name = "NonExistent Activity"
        email = "test@student.edu"

        # Act - Attempt to signup
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert - Verify error response
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "Activity not found" in result["detail"]

    def test_signup_already_signed_up(self, client):
        # Arrange - First signup
        activity_name = "Programming Class"
        email = "existing@student.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Act - Try to signup again
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert - Verify error for duplicate signup
        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "already signed up" in result["detail"]


class TestUnregisterFromActivity:
    """Test cases for unregistering from activities"""

    def test_unregister_success(self, client):
        # Arrange - First signup a student
        activity_name = "Gym Class"
        email = "test@student.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Act - Unregister the student
        response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert - Verify successful unregistration
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]
        assert activity_name in result["message"]

    def test_unregister_activity_not_found(self, client):
        # Arrange - Use a non-existent activity
        activity_name = "NonExistent Activity"
        email = "test@student.edu"

        # Act - Attempt to unregister
        response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert - Verify error response
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "Activity not found" in result["detail"]

    def test_unregister_not_signed_up(self, client):
        # Arrange - Use an activity that exists but student isn't signed up
        activity_name = "Basketball Team"
        email = "notsignedup@student.edu"

        # Act - Attempt to unregister
        response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert - Verify error response
        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "not signed up" in result["detail"]


class TestRootEndpoint:
    """Test cases for the root endpoint"""

    def test_root_redirect(self, client):
        # Arrange - No special setup needed

        # Act - Access the root endpoint (disable redirect following)
        response = client.get("/", follow_redirects=False)

        # Assert - Verify redirect to static file
        assert response.status_code == 307  # Temporary redirect
        assert "/static/index.html" in response.headers.get("location", "")