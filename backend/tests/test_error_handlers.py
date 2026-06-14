from fastapi.testclient import TestClient

from domain.exceptions import DomainError, InvalidProfileDataError
from main import app


@app.get("/test-invalid-profile-data")
def raise_invalid_profile_data_error() -> None:
    raise InvalidProfileDataError("Invalid profile payload")


@app.get("/test-domain-error")
def raise_domain_error() -> None:
    raise DomainError("Generic domain error")


client = TestClient(app)


def test_invalid_profile_data_error_handler() -> None:
    response = client.get("/test-invalid-profile-data")

    assert response.status_code == 400
    assert response.json() == {
        "error": "invalid_profile_data",
        "message": "Invalid profile payload",
    }


def test_domain_error_handler() -> None:
    response = client.get("/test-domain-error")

    assert response.status_code == 400
    assert response.json() == {
        "error": "domain_error",
        "message": "Generic domain error",
    }
