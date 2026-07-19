interface RecommendationsCardProps {
  recommendations: string[];
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
            <li key={recommendation}>{recommendation}</li>
          ))}
        </ul>
      )}
    </section>
  );
}
