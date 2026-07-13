import pytest
from pydantic import ValidationError

from schemas.ai_assistant_schema import (
    ImproveProfessionalDescriptionRequest,
    ImproveProfessionalDescriptionResponse,
)


def test_improve_professional_description_request() -> None:
    request = ImproveProfessionalDescriptionRequest(text="Desenvolvi APIs com Python.")

    assert request.text == "Desenvolvi APIs com Python."


def test_improve_professional_description_request_rejects_empty_text() -> None:
    with pytest.raises(ValidationError):
        ImproveProfessionalDescriptionRequest(text="")


def test_improve_professional_description_request_accepts_whitespace() -> None:
    request = ImproveProfessionalDescriptionRequest(text="   ")

    assert request.text == "   "


def test_improve_professional_description_response() -> None:
    response = ImproveProfessionalDescriptionResponse(
        original_text="Desenvolvi APIs com Python.",
        improved_text="Desenvolveu APIs robustas utilizando Python.",
    )

    assert response.original_text == "Desenvolvi APIs com Python."
    assert response.improved_text == "Desenvolveu APIs robustas utilizando Python."


def test_improve_professional_description_response_serialization() -> None:
    response = ImproveProfessionalDescriptionResponse(
        original_text="Criei integrações entre sistemas.",
        improved_text=("Desenvolveu integrações confiáveis entre sistemas."),
    )

    assert response.model_dump() == {
        "original_text": "Criei integrações entre sistemas.",
        "improved_text": ("Desenvolveu integrações confiáveis entre sistemas."),
    }


@pytest.mark.parametrize(
    "missing_field",
    [
        "original_text",
        "improved_text",
    ],
)
def test_improve_professional_description_response_requires_fields(
    missing_field: str,
) -> None:
    payload = {
        "original_text": "Texto original.",
        "improved_text": "Texto melhorado.",
    }
    payload.pop(missing_field)

    with pytest.raises(ValidationError):
        ImproveProfessionalDescriptionResponse(**payload)
