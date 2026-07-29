import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { listProfiles } from "../api/profiles";
import {
  createTechnology,
  deleteTechnology,
  listProfileTechnologies,
  updateTechnology,
} from "../api/technologies";
import { TechnologyList } from "../components/technology/TechnologyList";
import { TechnologyModal } from "../components/technology/TechnologyModal";
import type { Profile } from "../types/profile";
import type { Technology, TechnologyCreate } from "../types/technology";

export function TechnologiesPage() {
  const navigate = useNavigate();

  const [profile, setProfile] = useState<Profile | null>(null);
  const [technologies, setTechnologies] = useState<Technology[]>([]);

  const [selectedTechnology, setSelectedTechnology] =
    useState<Technology | null>(null);

  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const loadPageData = useCallback(async () => {
    setIsLoading(true);
    setErrorMessage("");

    try {
      const profiles = await listProfiles();
      const currentProfile = profiles[0] ?? null;

      setProfile(currentProfile);

      if (!currentProfile) {
        setTechnologies([]);
        return;
      }

      const profileTechnologies = await listProfileTechnologies(
        currentProfile.id,
      );

      setTechnologies(profileTechnologies);
    } catch {
      setErrorMessage(
        "Não foi possível carregar as tecnologias. Tente novamente.",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadPageData();
  }, [loadPageData]);

  function handleOpenCreateModal() {
    setSelectedTechnology(null);
    setErrorMessage("");
    setSuccessMessage("");
    setIsModalOpen(true);
  }

  function handleOpenEditModal(technology: Technology) {
    setSelectedTechnology(technology);
    setErrorMessage("");
    setSuccessMessage("");
    setIsModalOpen(true);
  }

  function handleCloseModal() {
    if (isSubmitting) {
      return;
    }

    setIsModalOpen(false);
    setSelectedTechnology(null);
  }

  async function handleSubmit(technologyData: TechnologyCreate): Promise<void> {
    if (!profile) {
      setErrorMessage("Crie seu perfil antes de cadastrar tecnologias.");
      return;
    }

    setIsSubmitting(true);
    setErrorMessage("");
    setSuccessMessage("");

    try {
      if (selectedTechnology) {
        const updatedTechnology = await updateTechnology(
          selectedTechnology.id,
          technologyData,
        );

        setTechnologies((currentTechnologies) =>
          currentTechnologies.map((technology) =>
            technology.id === updatedTechnology.id
              ? updatedTechnology
              : technology,
          ),
        );

        setSuccessMessage("Tecnologia atualizada com sucesso.");
      } else {
        const createdTechnology = await createTechnology(
          profile.id,
          technologyData,
        );

        setTechnologies((currentTechnologies) => [
          ...currentTechnologies,
          createdTechnology,
        ]);

        setSuccessMessage("Tecnologia cadastrada com sucesso.");
      }

      setIsModalOpen(false);
      setSelectedTechnology(null);
    } catch {
      setErrorMessage(
        selectedTechnology
          ? "Não foi possível atualizar a tecnologia."
          : "Não foi possível cadastrar a tecnologia.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDelete(technology: Technology): Promise<void> {
    const shouldDelete = window.confirm(
      `Deseja realmente excluir a tecnologia "${technology.name}"?`,
    );

    if (!shouldDelete) {
      return;
    }

    setErrorMessage("");
    setSuccessMessage("");

    try {
      await deleteTechnology(technology.id);

      setTechnologies((currentTechnologies) =>
        currentTechnologies.filter(
          (currentTechnology) => currentTechnology.id !== technology.id,
        ),
      );

      setSuccessMessage("Tecnologia excluída com sucesso.");
    } catch {
      setErrorMessage("Não foi possível excluir a tecnologia.");
    }
  }

  return (
    <main className="page-container technologies-page">
      <header className="page-header">
        <div>
          <p className="page-eyebrow">Perfil profissional</p>

          <h1>Tecnologias</h1>

          <p>
            Gerencie as tecnologias e competências que fazem parte da sua
            experiência profissional.
          </p>
        </div>

        <div className="page-header-actions">
          <button
            className="secondary-button"
            type="button"
            onClick={() => navigate("/")}
          >
            Voltar ao dashboard
          </button>

          <button
            className="primary-button"
            type="button"
            onClick={handleOpenCreateModal}
            disabled={!profile || isLoading}
          >
            Nova tecnologia
          </button>
        </div>
      </header>

      {!isLoading && !profile && (
        <section className="page-warning-card">
          <h2>Perfil necessário</h2>

          <p>
            Você precisa criar seu perfil profissional antes de cadastrar
            tecnologias.
          </p>

          <button
            className="primary-button"
            type="button"
            onClick={() => navigate("/profile")}
          >
            Criar perfil
          </button>
        </section>
      )}

      {errorMessage && (
        <p className="page-error-message" role="alert">
          {errorMessage}
        </p>
      )}

      {successMessage && (
        <p className="page-success-message" role="status">
          {successMessage}
        </p>
      )}

      {profile && (
        <TechnologyList
          technologies={technologies}
          isLoading={isLoading}
          onEdit={handleOpenEditModal}
          onDelete={(technology) => {
            void handleDelete(technology);
          }}
        />
      )}

      <TechnologyModal
        isOpen={isModalOpen}
        technology={selectedTechnology}
        isSubmitting={isSubmitting}
        onSubmit={handleSubmit}
        onClose={handleCloseModal}
      />
    </main>
  );
}
