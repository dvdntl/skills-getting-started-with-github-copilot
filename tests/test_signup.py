"""
Tests for the signup endpoint
"""

import pytest


def test_signup_new_student(client):
    """Test successful signup of a new student"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant(client):
    """Test that signup actually adds the participant to the activity"""
    # Get initial participant count
    response = client.get("/activities")
    initial_count = len(response.json()["Chess Club"]["participants"])
    
    # Sign up a new student
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "testplayer@mergington.edu"}
    )
    
    # Verify participant was added
    response = client.get("/activities")
    new_count = len(response.json()["Chess Club"]["participants"])
    assert new_count == initial_count + 1
    assert "testplayer@mergington.edu" in response.json()["Chess Club"]["participants"]


def test_signup_duplicate_student(client):
    """Test that signup fails for a student already enrolled"""
    # Try to sign up a student who's already enrolled
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower() or "already" in data["detail"].lower()


def test_signup_nonexistent_activity(client):
    """Test that signup fails for a non-existent activity"""
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_multiple_different_activities(client):
    """Test that a student can sign up for multiple different activities"""
    email = "multiactivity@mergington.edu"
    
    # Sign up for first activity
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up for second activity
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify both signups
    response = client.get("/activities")
    assert email in response.json()["Chess Club"]["participants"]
    assert email in response.json()["Programming Class"]["participants"]


def test_signup_with_special_characters_in_email(client):
    """Test signup with a valid email containing special characters"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student.name+tag@mergington.edu"}
    )
    assert response.status_code == 200


def test_signup_case_sensitive_email(client):
    """Test that emails are treated with case sensitivity"""
    email_lowercase = "casesensitive@mergington.edu"
    email_uppercase = "CASESENSITIVE@mergington.edu"
    
    # Sign up with lowercase
    response1 = client.post(
        "/activities/Drama Club/signup",
        params={"email": email_lowercase}
    )
    assert response1.status_code == 200
    
    # Sign up with uppercase (should succeed as different email)
    response2 = client.post(
        "/activities/Drama Club/signup",
        params={"email": email_uppercase}
    )
    assert response2.status_code == 200
