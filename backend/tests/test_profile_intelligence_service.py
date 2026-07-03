from services.profile_intelligence_service import ProfileIntelligenceService


def test_generate_complete_professional_diagnosis():
    service = ProfileIntelligenceService()

    diagnosis = service.generate_diagnosis(
        target_role="Python Backend Developer",
        technologies=["Python", "FastAPI", "Docker"],
        projects_count=2,
        experiences_count=2,
    )

    assert diagnosis.score == 75
    assert diagnosis.strengths
    assert diagnosis.recommendations
    assert not diagnosis.improvements


def test_generate_diagnosis_identifies_missing_information():
    service = ProfileIntelligenceService()

    diagnosis = service.generate_diagnosis(
        target_role="",
        technologies=[],
        projects_count=0,
        experiences_count=0,
    )

    assert diagnosis.score == 0
    assert diagnosis.improvements
    assert not diagnosis.strengths


def test_generate_diagnosis_score_never_exceeds_100():
    service = ProfileIntelligenceService()

    diagnosis = service.generate_diagnosis(
        target_role="Senior Software Engineer",
        technologies=[
            "Python",
            "FastAPI",
            "Docker",
            "Kubernetes",
            "AWS",
            "PostgreSQL",
            "Redis",
        ],
        projects_count=10,
        experiences_count=10,
    )

    assert diagnosis.score == 100
