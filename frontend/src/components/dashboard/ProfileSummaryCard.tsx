interface ProfileSummaryCardProps {
  completionPercentage: number;
  experiencesCount: number;
  projectsCount: number;
  technologiesCount: number;
}

interface SummaryMetric {
  label: string;
  value: number;
}

function normalizeNonNegativeInteger(value: number): number {
  if (!Number.isFinite(value)) {
    return 0;
  }

  return Math.max(0, Math.trunc(value));
}

function normalizePercentage(value: number): number {
  if (!Number.isFinite(value)) {
    return 0;
  }

  return Math.min(Math.max(Math.round(value), 0), 100);
}

function getCompletionLabel(completionPercentage: number): string {
  if (completionPercentage < 40) {
    return "Perfil inicial";
  }

  if (completionPercentage < 70) {
    return "Perfil em construção";
  }

  if (completionPercentage < 100) {
    return "Perfil bem estruturado";
  }

  return "Perfil completo";
}

export function ProfileSummaryCard({
  completionPercentage,
  experiencesCount,
  projectsCount,
  technologiesCount,
}: ProfileSummaryCardProps): React.JSX.Element {
  const normalizedCompletion = normalizePercentage(completionPercentage);

  const metrics: SummaryMetric[] = [
    {
      label: "Experiências",
      value: normalizeNonNegativeInteger(experiencesCount),
    },
    {
      label: "Projetos",
      value: normalizeNonNegativeInteger(projectsCount),
    },
    {
      label: "Tecnologias",
      value: normalizeNonNegativeInteger(technologiesCount),
    },
  ];

  const completionLabel = getCompletionLabel(normalizedCompletion);

  return (
    <section
      className="dashboard-card profile-summary-card"
      aria-labelledby="profile-summary-title"
    >
      <header className="profile-summary-card__header">
        <div>
          <span className="dashboard-card__eyebrow">Visão geral</span>

          <h2 id="profile-summary-title">Resumo do perfil</h2>
        </div>

        <span className="profile-summary-card__badge">{completionLabel}</span>
      </header>

      <div className="profile-summary-card__completion">
        <div className="profile-summary-card__completion-header">
          <span>Preenchimento do perfil</span>

          <strong>{normalizedCompletion}%</strong>
        </div>

        <div
          className="profile-summary-card__progress"
          role="progressbar"
          aria-label="Percentual de preenchimento do perfil"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={normalizedCompletion}
        >
          <span
            className="profile-summary-card__progress-bar"
            style={{ width: `${normalizedCompletion}%` }}
          />
        </div>
      </div>

      <dl className="profile-summary-card__metrics">
        {metrics.map((metric) => (
          <div key={metric.label} className="profile-summary-card__metric">
            <dt>{metric.label}</dt>
            <dd>{metric.value}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
