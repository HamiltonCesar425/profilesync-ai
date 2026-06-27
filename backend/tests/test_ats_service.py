from types import SimpleNamespace

from schemas.ats_schema import ATSValidationStatus
from services.ats_validation_service import ATSValidationService


class FakeResumeRepository:
    def __init__(self, resume):
        self.resume = resume
        self.called_with = None

    def get_by_id_and_user_id(self, resume_id: int, user_id: int):
        self.called_with = {
            "resume_id": resume_id,
            "user_id": user_id,
        }
        return self.resume


def make_resume(**overrides):
    data = {
        "id": 1,
        "title": "Currículo Desenvolvedor Full Stack",
        "target_role": "Desenvolvedor Full Stack Python",
        "content": "Resumo Experiência Formação Competências Projetos Certificações "
        + ("Python FastAPI SQLAlchemy Pytest Docker " * 30),
    }
    data.update(overrides)
    return SimpleNamespace(**data)


def test_validate_resume_returns_ats_validation_response_with_score_100():
    resume = make_resume()
    repository = FakeResumeRepository(resume)
    service = ATSValidationService(repository)

    response = service.validate_resume(resume_id=1, user_id=10)

    assert response.resume_id == 1
    assert response.score == 100
    assert response.status == ATSValidationStatus.EXCELLENT
    assert response.passed is True
    assert response.issues == []
    assert response.suggestions == []
    assert repository.called_with == {
        "resume_id": 1,
        "user_id": 10,
    }


def test_validate_resume_returns_partial_score_when_some_rules_fail():
    resume = make_resume(
        target_role="",
        content="Resumo breve sem conteúdo suficiente.",
    )
    repository = FakeResumeRepository(resume)
    service = ATSValidationService(repository)

    response = service.validate_resume(resume_id=1, user_id=10)

    assert response.resume_id == 1
    assert response.score == 25
    assert response.status == ATSValidationStatus.POOR
    assert response.passed is False
    assert len(response.issues) == 3
    assert len(response.suggestions) == 3


def test_calculate_score_returns_zero_when_results_are_empty():
    score = ATSValidationService._calculate_score([])

    assert score == 0
