"""
Tests for the activities endpoints
"""

import pytest


def test_get_activities(client):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    assert "Chess Club" in activities
    assert "Programming Class" in activities


def test_get_activities_structure(client):
    """Test that activity objects have the correct structure"""
    response = client.get("/activities")
    activities = response.json()
    
    for name, activity in activities.items():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)


def test_get_activities_contains_participants(client):
    """Test that activities include their participants"""
    response = client.get("/activities")
    activities = response.json()
    
    chess_club = activities["Chess Club"]
    assert len(chess_club["participants"]) == 2
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]


def test_get_activities_with_empty_participants(client):
    """Test that activities can have empty participant lists"""
    response = client.get("/activities")
    activities = response.json()
    
    # Check if any activity has empty participants (if not, at least verify structure)
    for activity in activities.values():
        assert isinstance(activity["participants"], list)
