import type { ImpactRecommendation } from "../../api/dashboard";

interface RecommendationsCardProps {
  recommendations: ImpactRecommendation[];
}

const PRIORITY_LABELS = {
  high: "Alta prioridade",
  medium: "Média prioridade",
  low: "Baixa prioridade",
} as const;

function formatSkillName(skill: string): string {
  return skill
    .split(" ")
    .filter(Boolean)
    .map(
      (word) => `${word.charAt(0).toUpperCase()}${word.slice(1).toLowerCase()}`,
    )
    .join(" ");
}

export function RecommendationsCard({
  recommendations,
}: RecommendationsCardProps): React.JSX.Element {
  return (
    <section aria-labelledby="recommendations-title">
      <h2 id="recommendations-title">Recomendações</h2>

      {recommendations.length === 0 ? (
        <p>Nenhuma recomendação disponível no momento.</p>
      ) : (
        <ul>
          {recommendations.map((recommendation) => (
            <li key={`${recommendation.skill}-${recommendation.priority}`}>
              <article>
                <header>
                  <span>{PRIORITY_LABELS[recommendation.priority]}</span>
                  <span>Impacto: {recommendation.impact_score}</span>
                </header>

                <h3>{formatSkillName(recommendation.skill)}</h3>

                <p>{recommendation.reason}</p>
              </article>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
