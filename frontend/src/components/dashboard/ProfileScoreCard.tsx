interface ProfileScoreCardProps {
  score: number;
}

export function ProfileScoreCard({
  score,
}: ProfileScoreCardProps): React.JSX.Element {
  return (
    <section aria-labelledby="profile-score-title">
      <h2 id="profile-score-title">Score do Perfil</h2>

      <p>
        <strong>{score}</strong>
        <span>/100</span>
      </p>
    </section>
  );
}
