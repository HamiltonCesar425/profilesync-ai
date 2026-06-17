from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "ProfileSync AI API is running"}


def test_create_profile() -> None:
    payload = {
        "full_name": "Test User",
        "professional_title": "Software Developer",
        "summary": "Professional profile",
        "location": "Test City",
        "linkedin_url": "https://linkedin.com/in/test-user",
        "github_url": "https://github.com/test-user",
    }

    response = client.post(
        "/profiles",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["full_name"] == payload["full_name"]
    assert data["professional_title"] == payload["professional_title"]


def test_list_profiles() -> None:
    response = client.get("/profiles")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_profile_by_id() -> None:
    payload = {
        "full_name": "Sample Profile",
        "professional_title": "Software Developer",
        "summary": "Sample profile summary",
    }

    create_response = client.post(
        "/profiles",
        json=payload,
    )

    profile_id = create_response.json()["id"]

    response = client.get(f"/profiles/{profile_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == profile_id
    assert data["full_name"] == "Sample Profile"


def test_get_profile_by_id_not_found() -> None:
    response = client.get("/profiles/999999")

    assert response.status_code == 404
    assert response.json() == {
        "error": "profile_not_found",
        "message": "Profile with id 999999 not found",
    }


def test_update_profile() -> None:
    create_payload = {
        "full_name": "Profile Update Test",
        "professional_title": "Software Developer",
        "summary": "Sample profile update summary",
    }

    create_response = client.post("/profiles", json=create_payload)
    profile_id = create_response.json()["id"]

    update_payload = {
        "full_name": "Updated Test Profile",
        "professional_title": "Senior Software Developer",
        "summary": "Updated sample profile summary for API test",
        "location": "Updated Test City",
        "linkedin_url": "https://linkedin.com/in/updated-profile",
        "github_url": "https://github.com/updated-profile",
    }

    response = client.put(f"/profiles/{profile_id}", json=update_payload)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == profile_id
    assert data["full_name"] == update_payload["full_name"]
    assert data["professional_title"] == update_payload["professional_title"]
    assert data["summary"] == update_payload["summary"]
    assert data["location"] == update_payload["location"]
    assert data["linkedin_url"] == update_payload["linkedin_url"]
    assert data["github_url"] == update_payload["github_url"]


def test_update_profile_not_found() -> None:
    payload = {
        "full_name": "Unknown Profile",
        "professional_title": "Software Developer",
        "summary": "Sample update payload for missing profile",
    }

    response = client.put("/profiles/999999", json=payload)

    assert response.status_code == 404
    assert response.json() == {"detail": "Profile not found"}


def test_delete_profile() -> None:
    payload = {
        "full_name": "Profile Delete Test",
        "professional_title": "Software Developer",
        "summary": "Sample profile delete summary",
    }

    create_response = client.post("/profiles", json=payload)
    profile_id = create_response.json()["id"]

    response = client.delete(f"/profiles/{profile_id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/profiles/{profile_id}")

    assert get_response.status_code == 404


def test_delete_profile_not_found() -> None:
    response = client.delete("/profiles/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Profile not found"}

