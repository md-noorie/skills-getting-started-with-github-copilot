"""
Tests for the /activities endpoint
"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestGetActivities:
    def test_get_activities_success(self):
        # Arrange - no special setup needed

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        # Check that some known activities are present
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_get_activities_structure(self):
        # Arrange - no special setup needed

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0

    def test_get_activities_data_integrity(self):
        # Arrange - no special setup needed

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        # Check that participants are lists of strings (emails)
        for activity_name, activity_data in data.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant  # Basic email check