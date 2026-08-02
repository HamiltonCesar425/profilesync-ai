interface ProfileScoreCardProps {
  score: number;
}

interface ScoreMetadata {
  label: string;
  description: string;
  level: "critical" | "attention" | "good" | "excellent";
}

function normalizeScore(score: number): number {
  return Math.min(Math.max(Math.round(score), 0), 100);
}

function getScoreMetadata(score: number): ScoreMetadata {
  if (score < 40) {
    return {
      label: "Perfil incompleto",
      description:
        "Complete as informações essenciais para melhorar a qualidade do perfil.",
      level: "critical",
    };
  }

  if (score < 70) {
    return {
      label: "Perfil em evolução",
      description:
        "Seu perfil possui uma boa base, mas ainda existem pontos importantes a desenvolver.",
      level: "attention",
    };
  }

  if (score < 90) {
    return {
      label: "Perfil competitivo",
      description:
        "Seu perfil apresenta boa consistência e está próximo de um nível de destaque.",
      level: "good",
    };
  }

  return {
    label: "Perfil de destaque",
    description:
      "Seu perfil apresenta alto nível de completude e consistência profissional.",
    level: "excellent",
  };
}

export function ProfileScoreCard({
  score,
}: ProfileScoreCardProps): React.JSX.Element {
  const normalizedScore = normalizeScore(score);
  const metadata = getScoreMetadata(normalizedScore);

  return (
    <section
      className={`dashboard-card profile-score-card profile-score-card--${metadata.level}`}
      aria-labelledby="profile-score-title"
    >
      <header className="profile-score-card__header">
        <div>
          <span className="dashboard-card__eyebrow">
            Inteligência de perfil
          </span>

          <h2 id="profile-score-title">Score do Perfil</h2>
        </div>

        <span
          className={`profile-score-card__badge profile-score-card__badge--${metadata.level}`}
        >
          {metadata.label}
        </span>
      </header>

      <div className="profile-score-card__content">
        <div
          className="profile-score-card__score"
          aria-label={`Score do perfil: ${normalizedScore} de 100`}
        >
          <strong>{normalizedScore}</strong>
          <span>/100</span>
        </div>

        <div className="profile-score-card__details">
          <div
            className="profile-score-card__progress"
            role="progressbar"
            aria-label="Progresso do score do perfil"
            aria-valuemin={0}
            aria-valuemax={100}
            aria-valuenow={normalizedScore}
          >
            <span
              className="profile-score-card__progress-bar"
              style={{ width: `${normalizedScore}%` }}
            />
          </div>

          <p className="profile-score-card__description">
            {metadata.description}
          </p>
        </div>
      </div>
    </section>
  );
}
