import type { Project } from "../../types/project";
import { formatDate } from "../../utils/date";

interface ProjectCardProps {
  project: Project;
  isDeleting: boolean;
  onEdit: (project: Project) => void;
  onDelete: (project: Project) => Promise<void>;
}

function formatProjectPeriod(project: Project): string {
  const startDate = project.start_date
    ? formatDate(project.start_date)
    : "Data de início não informada";

  if (project.is_current) {
    return `${startDate} — Em andamento`;
  }

  const endDate = project.end_date
    ? formatDate(project.end_date)
    : "Data de término não informada";

  return `${startDate} — ${endDate}`;
}

export function ProjectCard({
  project,
  isDeleting,
  onEdit,
  onDelete,
}: ProjectCardProps) {
  async function handleDelete() {
    const confirmed = window.confirm(
      `Deseja realmente excluir o projeto "${project.name}"?`,
    );

    if (!confirmed) {
      return;
    }

    await onDelete(project);
  }

  return (
    <article className="project-card">
      <div className="project-card-header">
        <div>
          <h3>{project.name}</h3>

          {project.role && <p className="project-role">{project.role}</p>}
        </div>

        {project.is_current && (
          <span className="status-badge">Em andamento</span>
        )}
      </div>

      <p className="project-period">{formatProjectPeriod(project)}</p>

      {project.description && (
        <p className="project-description">{project.description}</p>
      )}

      {(project.repository_url || project.demo_url) && (
        <div className="project-links">
          {project.repository_url && (
            <a href={project.repository_url} target="_blank" rel="noreferrer">
              Ver repositório
            </a>
          )}

          {project.demo_url && (
            <a href={project.demo_url} target="_blank" rel="noreferrer">
              Ver demonstração
            </a>
          )}
        </div>
      )}

      <div className="project-card-actions">
        <button
          className="secondary-button"
          type="button"
          onClick={() => onEdit(project)}
          disabled={isDeleting}
        >
          Editar
        </button>

        <button
          className="danger-button"
          type="button"
          onClick={handleDelete}
          disabled={isDeleting}
        >
          {isDeleting ? "Excluindo..." : "Excluir"}
        </button>
      </div>
    </article>
  );
}
