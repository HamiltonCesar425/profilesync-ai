import { formatDate } from "../utils/date";
import { useEffect, useState } from "react";

import {
  createProfessionalExperience,
  deleteProfessionalExperience,
  listProfessionalExperiences,
  updateProfessionalExperience,
} from "../api/professionalExperiences";
import { listProfiles } from "../api/profiles";
import { ProfessionalExperienceForm } from "../components/professional-experience/ProfessionalExperienceForm";
import type {
  ProfessionalExperience,
  ProfessionalExperienceCreate,
} from "../types/professionalExperience";
import type { Profile } from "../types/profile";

export function ProfessionalExperiencesPage() {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [selectedProfileId, setSelectedProfileId] = useState<number | null>(
    null,
  );

  const [experiences, setExperiences] = useState<ProfessionalExperience[]>([]);

  const [selectedExperience, setSelectedExperience] =
    useState<ProfessionalExperience | null>(null);

  const [isFormVisible, setIsFormVisible] = useState(false);
  const [isLoadingProfiles, setIsLoadingProfiles] = useState(true);
  const [isLoadingExperiences, setIsLoadingExperiences] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [deletingExperienceId, setDeletingExperienceId] = useState<
    number | null
  >(null);

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

    async function loadExperiences(): Promise<void> {
      if (selectedProfileId === null) {
        setExperiences([]);
        return;
      }

      setIsLoadingExperiences(true);
      setErrorMessage(null);

      try {
        const experienceList =
          await listProfessionalExperiences(selectedProfileId);

        if (isActive) {
          setExperiences(experienceList);
        }
      } catch {
        if (isActive) {
          setExperiences([]);
          setErrorMessage(
            "Não foi possível carregar as experiências profissionais.",
          );
        }
      } finally {
        if (isActive) {
          setIsLoadingExperiences(false);
        }
      }
    }

    void loadExperiences();

    return () => {
      isActive = false;
    };
  }, [selectedProfileId]);

  async function refreshExperiences(): Promise<void> {
    if (selectedProfileId === null) {
      setExperiences([]);
      return;
    }

    const experienceList = await listProfessionalExperiences(selectedProfileId);

    setExperiences(experienceList);
  }

  function handleProfileChange(profileId: number): void {
    setSelectedProfileId(profileId);
    setSelectedExperience(null);
    setIsFormVisible(false);
    setErrorMessage(null);
    setSuccessMessage(null);
  }

  function handleCreateClick(): void {
    setSelectedExperience(null);
    setIsFormVisible(true);
    setErrorMessage(null);
    setSuccessMessage(null);
  }

  function handleEditClick(experience: ProfessionalExperience): void {
    setSelectedExperience(experience);
    setIsFormVisible(true);
    setErrorMessage(null);
    setSuccessMessage(null);
  }

  function handleCancelForm(): void {
    setSelectedExperience(null);
    setIsFormVisible(false);
    setErrorMessage(null);
  }

  async function handleSubmit(
    payload: ProfessionalExperienceCreate,
  ): Promise<void> {
    if (selectedProfileId === null) {
      setErrorMessage("Selecione um perfil antes de salvar a experiência.");
      return;
    }

    setIsSubmitting(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      if (selectedExperience) {
        await updateProfessionalExperience(
          selectedProfileId,
          selectedExperience.id,
          payload,
        );

        setSuccessMessage("Experiência profissional atualizada com sucesso.");
      } else {
        await createProfessionalExperience(selectedProfileId, payload);

        setSuccessMessage("Experiência profissional criada com sucesso.");
      }

      await refreshExperiences();

      setSelectedExperience(null);
      setIsFormVisible(false);
    } catch {
      setErrorMessage(
        selectedExperience
          ? "Não foi possível atualizar a experiência profissional."
          : "Não foi possível criar a experiência profissional.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDelete(
    experience: ProfessionalExperience,
  ): Promise<void> {
    if (selectedProfileId === null) {
      return;
    }

    const confirmed = window.confirm(
      `Deseja realmente excluir a experiência em "${experience.company_name}"?`,
    );

    if (!confirmed) {
      return;
    }

    setDeletingExperienceId(experience.id);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      await deleteProfessionalExperience(selectedProfileId, experience.id);

      setExperiences((currentExperiences) =>
        currentExperiences.filter(
          (currentExperience) => currentExperience.id !== experience.id,
        ),
      );

      if (selectedExperience?.id === experience.id) {
        setSelectedExperience(null);
        setIsFormVisible(false);
      }

      setSuccessMessage("Experiência profissional excluída com sucesso.");
    } catch {
      setErrorMessage("Não foi possível excluir a experiência profissional.");
    } finally {
      setDeletingExperienceId(null);
    }
  }

  if (isLoadingProfiles) {
    return (
      <main className="professional-experiences-page">
        <p>Carregando perfis...</p>
      </main>
    );
  }

  if (profiles.length === 0) {
    return (
      <main>
        <h1>Experiências profissionais</h1>

        <p>
          Cadastre primeiro um perfil profissional para adicionar experiências.
        </p>
      </main>
    );
  }

  return (
    <main>
      <header className="professional-experiences-header">
        <div>
          <h1>Experiências profissionais</h1>

          <p>
            Registre seu histórico profissional, responsabilidades e principais
            resultados.
          </p>
        </div>

        <button
          type="button"
          onClick={handleCreateClick}
          disabled={
            selectedProfileId === null ||
            isSubmitting ||
            deletingExperienceId !== null
          }
        >
          Nova experiência
        </button>
      </header>

      {profiles.length > 1 && (
        <div className="professional-experiences-profile-selector">
          <label htmlFor="professional-profile">Perfil profissional</label>

          <select
            id="professional-profile"
            value={selectedProfileId ?? ""}
            onChange={(event) =>
              handleProfileChange(Number(event.target.value))
            }
            disabled={isSubmitting || deletingExperienceId !== null}
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

      {isFormVisible && (
        <ProfessionalExperienceForm
          experience={selectedExperience}
          isSubmitting={isSubmitting}
          onSubmit={handleSubmit}
          onCancel={handleCancelForm}
        />
      )}

      <section className="professional-experiences-list">
        <h2>Experiências cadastradas</h2>

        {isLoadingExperiences ? (
          <p>Carregando experiências...</p>
        ) : experiences.length === 0 ? (
          <p>Nenhuma experiência profissional cadastrada para este perfil.</p>
        ) : (
          <ul className="professional-experiences-items">
            {experiences.map((experience) => (
              <li className="professinal-experience-item" key={experience.id}>
                <article className="professional-experience-card">
                  <header className="professional-experience-card-header">
                    <div>
                      <h3>{experience.position}</h3>

                      <p>{experience.company_name}</p>
                    </div>

                    {experience.is_current && (
                      <span className="professional-experience-current">
                        Experiência atual
                      </span>
                    )}
                  </header>

                  <dl>
                    {experience.employment_type && (
                      <>
                        <dt>Tipo de contratação</dt>
                        <dd>{experience.employment_type}</dd>
                      </>
                    )}

                    {experience.work_model && (
                      <>
                        <dt>Modelo de trabalho</dt>
                        <dd>{experience.work_model}</dd>
                      </>
                    )}

                    {experience.location && (
                      <>
                        <dt>Localização</dt>
                        <dd>{experience.location}</dd>
                      </>
                    )}

                    <dt>Período</dt>
                    <dd>
                      {formatDate(experience.start_date)} -{" "}
                      {experience.is_current
                        ? "Atual"
                        : formatDate(experience.end_date)}
                    </dd>
                  </dl>

                  {experience.description && (
                    <p className="professional-experience-description">
                      {experience.description}
                    </p>
                  )}

                  <div className="professional-experience-actions">
                    <button
                      type="button"
                      onClick={() => handleEditClick(experience)}
                      disabled={isSubmitting || deletingExperienceId !== null}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      onClick={() => {
                        void handleDelete(experience);
                      }}
                      disabled={isSubmitting || deletingExperienceId !== null}
                    >
                      {deletingExperienceId === experience.id
                        ? "Excluindo..."
                        : "Excluir"}
                    </button>
                  </div>
                </article>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
