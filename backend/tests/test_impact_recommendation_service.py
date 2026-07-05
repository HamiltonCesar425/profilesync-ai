from services.impact_recommendation_service import (
    ImpactRecommendationService,
)


def test_generate_prioritized_recommendations():
    service = ImpactRecommendationService()

    result = service.generate(
        gaps=["tests", "docker"],
    )

    assert len(result.recommendations) == 2
    assert result.recommendations[0].skill == "docker"
    assert result.recommendations[0].priority == "high"
    assert result.recommendations[0].impact_score == 90


def test_generate_recommendation_for_unknown_gap():
    service = ImpactRecommendationService()

    result = service.generate(
        gaps=["kubernetes"],
    )

    recommendation = result.recommendations[0]

    assert recommendation.skill == "kubernetes"
    assert recommendation.priority == "low"
    assert recommendation.impact_score == 50


def test_generate_returns_empty_list_when_no_gaps():
    service = ImpactRecommendationService()

    result = service.generate(gaps=[])

    assert result.recommendations == []


def test_generate_normalizes_gap_names():
    service = ImpactRecommendationService()

    result = service.generate(
        gaps=[" Docker "],
    )

    recommendation = result.recommendations[0]

    assert recommendation.skill == "docker"
    assert recommendation.priority == "high"
