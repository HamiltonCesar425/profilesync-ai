interface ProfileSummaryCardProps {
  completionPercentage: number;
  experiencesCount: number;
  projectsCount: number;
  technologiesCount: number;
}

export function ProfileSummaryCard({
  completionPercentage,
  experiencesCount,
  projectsCount,
  technologiesCount,
}: ProfileSummaryCardProps): React.JSX.Element {
  return (
    <section aria-labelledby="profile-summary-title">
      <h2 id="profile-summary-title">Resumo do perfil</h2>

      <dl>
        <div>
          <dt>Perfil completo</dt>
          <dd>{completionPercentage}%</dd>
        </div>

        <div>
          <dt>Experiências</dt>
          <dd>{experiencesCount}</dd>
        </div>

        <div>
          <dt>Projetos</dt>
          <dd>{projectsCount}</dd>
        </div>

        <div>
          <dt>Tecnologias</dt>
          <dd>{technologiesCount}</dd>
        </div>
      </dl>
    </section>
  );
}
