import type { Project } from "../../types/project";

import { ProjectCard } from "./ProjectCard";

interface ProjectListProps {
  projects: Project[];
  deletingProjectId: number | null;
  onEdit: (project: Project) => void;
  onDelete: (project: Project) => Promise<void>;
}

export function ProjectList({
  projects,
  deletingProjectId,
  onEdit,
  onDelete,
}: ProjectListProps) {
  if (projects.length === 0) {
    return (
      <div className="empty-state">
        <h3>Nenhum projeto cadastrado</h3>
        <p>
          Registre projetos que demonstrem suas competências, responsabilidades
          e resultados profissionais.
        </p>
      </div>
    );
  }

  return (
    <div className="project-list">
      {projects.map((project) => (
        <ProjectCard
          key={project.id}
          project={project}
          isDeleting={deletingProjectId === project.id}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
