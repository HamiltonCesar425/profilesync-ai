import type { Technology } from "../../types/technology";

interface TechnologyListProps {
  technologies: Technology[];
  isLoading: boolean;
  onEdit: (technology: Technology) => void;
  onDelete: (technology: Technology) => void;
}

function formatYearsExperience(yearsExperience: number | null): string {
  if (yearsExperience === null) {
    return "Não informado";
  }

  if (yearsExperience === 0) {
    return "Menos de 1 ano";
  }

  if (yearsExperience === 1) {
    return "1 ano";
  }

  return `${yearsExperience} anos`;
}

export function TechnologyList({
  technologies,
  isLoading,
  onEdit,
  onDelete,
}: TechnologyListProps) {
  if (isLoading) {
    return (
      <p className="technology-list-message" role="status">
        Carregando tecnologias...
      </p>
    );
  }

  if (technologies.length === 0) {
    return (
      <div className="technology-empty-state">
        <h2>Nenhuma tecnologia cadastrada</h2>

        <p>
          Cadastre as tecnologias e competências que fazem parte do seu perfil
          profissional.
        </p>
      </div>
    );
  }

  return (
    <div className="technology-list">
      {technologies.map((technology) => (
        <article className="technology-card" key={technology.id}>
          <div className="technology-card-header">
            <div>
              <h2>{technology.name}</h2>

              <p className="technology-category">{technology.category}</p>
            </div>

            <span className="technology-proficiency-badge">
              {technology.proficiency_level}
            </span>
          </div>

          <dl className="technology-details">
            <div>
              <dt>Experiência</dt>

              <dd>{formatYearsExperience(technology.years_experience)}</dd>
            </div>
          </dl>

          <div className="technology-card-actions">
            <button
              className="secondary-button"
              type="button"
              onClick={() => onEdit(technology)}
            >
              Editar
            </button>

            <button
              className="danger-button"
              type="button"
              onClick={() => onDelete(technology)}
            >
              Excluir
            </button>
          </div>
        </article>
      ))}
    </div>
  );
}
