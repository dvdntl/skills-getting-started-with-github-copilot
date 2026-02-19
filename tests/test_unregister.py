"""
Tests for the unregister endpoint
"""

import pytest


def test_unregister_existing_participant(client):
    """Test successful unregistration of an existing participant"""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes the participant"""
    # Get initial participant
    response = client.get("/activities")
    initial_participants = response.json()["Chess Club"]["participants"]
    initial_count = len(initial_participants)
    
    # Unregister a participant
    client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    # Verify participant was removed
    response = client.get("/activities")
    new_participants = response.json()["Chess Club"]["participants"]
    new_count = len(new_participants)
    assert new_count == initial_count - 1
    assert "michael@mergington.edu" not in new_participants


def test_unregister_not_enrolled_participant(client):
    """Test that unregister fails for a student not enrolled"""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "notstudent@mergington.edu"}
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()


def test_unregister_nonexistent_activity(client):
    """Test that unregister fails for a non-existent activity"""
    response = client.delete(
        "/activities/Nonexistent Activity/unregister",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_then_signup_again(client):
    """Test that a student can sign up again after unregistering"""
    email = "flexible@mergington.edu"
    
    # Sign up
    client.post(
        "/activities/Tennis Club/signup",
        params={"email": email}
    )
    
    # Unregister
    response1 = client.delete(
        "/activities/Tennis Club/unregister",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up again
    response2 = client.post(
        "/activities/Tennis Club/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify the student is back
    response = client.get("/activities")
    assert email in response.json()["Tennis Club"]["participants"]


def test_unregister_multiple_participants(client):
    """Test unregistering one participant doesn't affect others"""
    # Get initial participants
    response = client.get("/activities")
    initial_participants = response.json()["Drama Club"]["participants"].copy()
    
    # Sign up a new participant
    new_email = "drama_buff@mergington.edu"
    client.post(
        "/activities/Drama Club/signup",
        params={"email": new_email}
    )
    
    # Unregister the new participant
    client.delete(
        "/activities/Drama Club/unregister",
        params={"email": new_email}
    )
    
    # Verify original participants remain
    response = client.get("/activities")
    final_participants = response.json()["Drama Club"]["participants"]
    for participant in initial_participants:
        assert participant in final_participants


def test_unregister_case_sensitive_email(client):
    """Test that unregister is case sensitive with emails"""
    email = "casematch@mergington.edu"
    
    # Sign up with lowercase
    client.post(
        "/activities/Art Studio/signup",
        params={"email": email}
    )
    
    # Try to unregister with different case (should fail)
    response = client.delete(
        "/activities/Art Studio/unregister",
        params={"email": email.upper()}
    )
    assert response.status_code == 400
