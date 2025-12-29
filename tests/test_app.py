from fastapi.testclient import TestClient
import pytest

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    # make a shallow copy of participants lists to restore after each test
    original = {k: v["participants"][:] for k, v in activities.items()}
    yield
    for name, parts in original.items():
        activities[name]["participants"] = parts[:]


def test_get_activities():
    client = TestClient(app)
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    client = TestClient(app)
    activity = "Chess Club"
    email = "test_student@example.com"

    # Ensure email not present
    resp = client.get("/activities")
    assert email not in resp.json()[activity]["participants"]

    # Sign up
    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200
    assert email in activities[activity]["participants"]

    # Verify appears in GET
    resp = client.get("/activities")
    assert email in resp.json()[activity]["participants"]

    # Unregister
    unreg = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert unreg.status_code == 200
    assert email not in activities[activity]["participants"]
