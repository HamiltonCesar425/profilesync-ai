import { useEffect, useState } from "react";

import { listProfiles } from "../api/profiles";
import {
  createProject,
  deleteProject,
  getProjectsByProfile,
  updateProject,
} from "../api/projects";
import { ProjectForm } from "../components/project/ProjectForm";
import { ProjectList } from "../components/project/ProjectList";
import type { Profile } from "../types/profile";
import type { Project, ProjectCreate, ProjectUpdate } from "../types/project";

export function ProjectsPage() {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [selectedProfileId, setSelectedProfileId] = useState<number | null>(
    null,
  );

  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  const [isFormVisible, setIsFormVisible] = useState(false);
  const [isLoadingProfiles, setIsLoadingProfiles] = useState(true);
  const [isLoadingProjects, setIsLoadingProjects] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [deletingProjectId, setDeletingProjectId] = useState<number | null>(
    null,
  );

  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    let isActive = true;

    async function loadProfiles(): Promise<void> {
      setIsLoadingProfiles(true);
      setErrorMessage(null);

      try {
        const profileList = await listProfiles();

        if (!isActive) {
          return;
        }

        setProfiles(profileList);

        setSelectedProfileId((currentProfileId) => {
          if (
            currentProfileId !== null &&
            profileList.some((profile) => profile.id === currentProfileId)
          ) {
            return currentProfileId;
          }

          return profileList[0]?.id ?? null;
        });
      } catch {
        if (isActive) {
          setErrorMessage("Não foi possível carregar os perfis profissionais.");
        }
      } finally {
        if (isActive) {
          setIsLoadingProfiles(false);
        }
      }
    }

    void loadProfiles();

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    async function loadProjects(): Promise<void> {
      if (selectedProfileId === null) {
        setProjects([]);
        return;
      }

      setIsLoadingProjects(true);
      setErrorMessage(null);

      try {
        const projectList = await getProjectsByProfile(selectedProfileId);

        if (isActive) {
          setProjects(projectList);
        }
      } catch {
        if (isActive) {
          setProjects([]);
          setErrorMessage("Não foi possível carregar os projetos.");
        }
      } finally {
        if (isActive) {
          setIsLoadingProjects(false);
        }
      }
    }

    void loadProjects();

    return () => {
      isActive = false;
    };
  }, [selectedProfileId]);

  async function refreshProjects(): Promise<void> {
    if (selectedProfileId === null) {
      setProjects([]);
      return;
    }

    const projectList = await getProjectsByProfile(selectedProfileId);

    setProjects(projectList);
  }

  function handleProfileChange(profileId: number): void {
    setSelectedProfileId(profileId);
    setSelectedProject(null);
    setIsFormVisible(false);
    setErrorMessage(null);
    setSuccessMessage(null);
  }

  function handleCreateClick(): void {
    setSelectedProject(null);
    setIsFormVisible(true);
    setErrorMessage(null);
    setSuccessMessage(null);
  }

  function handleEditClick(project: Project): void {
    setSelectedProject(project);
    setIsFormVisible(true);
    setErrorMessage(null);
    setSuccessMessage(null);
  }

  function handleCancelForm(): void {
    setSelectedProject(null);
    setIsFormVisible(false);
    setErrorMessage(null);
  }

  async function handleSubmit(payload: ProjectCreate): Promise<void> {
    if (selectedProfileId === null) {
      setErrorMessage("Selecione um perfil antes de salvar o projeto.");
      return;
    }

    setIsSubmitting(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      if (selectedProject) {
        const updatePayload: ProjectUpdate = {
          name: payload.name,
          description: payload.description,
          role: payload.role,
          repository_url: payload.repository_url,
          demo_url: payload.demo_url,
          start_date: payload.start_date,
          end_date: payload.end_date,
          is_current: payload.is_current,
        };

        await updateProject(
          selectedProfileId,
          selectedProject.id,
          updatePayload,
        );

        setSuccessMessage("Projeto atualizado com sucesso.");
      } else {
        await createProject(payload);

        setSuccessMessage("Projeto criado com sucesso.");
      }

      await refreshProjects();

      setSelectedProject(null);
      setIsFormVisible(false);
    } catch {
      setErrorMessage(
        selectedProject
          ? "Não foi possível atualizar o projeto."
          : "Não foi possível criar o projeto.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDelete(project: Project): Promise<void> {
    if (selectedProfileId === null) {
      return;
    }

    setDeletingProjectId(project.id);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      await deleteProject(selectedProfileId, project.id);

      setProjects((currentProjects) =>
        currentProjects.filter(
          (currentProject) => currentProject.id !== project.id,
        ),
      );

      if (selectedProject?.id === project.id) {
        setSelectedProject(null);
        setIsFormVisible(false);
      }

      setSuccessMessage("Projeto excluído com sucesso.");
    } catch {
      setErrorMessage("Não foi possível excluir o projeto.");
    } finally {
      setDeletingProjectId(null);
    }
  }

  if (isLoadingProfiles) {
    return (
      <main className="projects-page">
        <p>Carregando perfis...</p>
      </main>
    );
  }

  if (profiles.length === 0) {
    return (
      <main className="projects-page">
        <h1>Projetos</h1>

        {errorMessage && (
          <p className="feedback-message feedback-message-error" role="alert">
            {errorMessage}
          </p>
        )}

        <p>Cadastre primeiro um perfil profissional para adicionar projetos.</p>
      </main>
    );
  }

  return (
    <main className="projects-page">
      <header className="projects-header">
        <div>
          <h1>Projetos</h1>

          <p>
            Registre projetos que demonstrem suas competências técnicas,
            responsabilidades e resultados.
          </p>
        </div>

        <button
          type="button"
          onClick={handleCreateClick}
          disabled={
            selectedProfileId === null ||
            isSubmitting ||
            deletingProjectId !== null
          }
        >
          Novo projeto
        </button>
      </header>

      {profiles.length > 1 && (
        <div className="projects-profile-selector">
          <label htmlFor="project-profile">Perfil profissional</label>

          <select
            id="project-profile"
            value={selectedProfileId ?? ""}
            onChange={(event) =>
              handleProfileChange(Number(event.target.value))
            }
            disabled={isSubmitting || deletingProjectId !== null}
          >
            {profiles.map((profile) => (
              <option key={profile.id} value={profile.id}>
                {profile.full_name} — {profile.professional_title}
              </option>
            ))}
          </select>
        </div>
      )}

      {errorMessage && (
        <p className="feedback-message feedback-message-error" role="alert">
          {errorMessage}
        </p>
      )}

      {successMessage && (
        <p className="feedback-message feedback-message-sucess" role="status">
          {successMessage}
        </p>
      )}

      {isFormVisible && selectedProfileId !== null && (
        <ProjectForm
          profileId={selectedProfileId}
          project={selectedProject}
          isSubmitting={isSubmitting}
          onSubmit={handleSubmit}
          onCancel={handleCancelForm}
        />
      )}

      <section className="projects-section">
        <h2>Projetos cadastrados</h2>

        {isLoadingProjects ? (
          <p>Carregando projetos...</p>
        ) : (
          <ProjectList
            projects={projects}
            deletingProjectId={deletingProjectId}
            onEdit={handleEditClick}
            onDelete={handleDelete}
          />
        )}
      </section>
    </main>
  );
}
