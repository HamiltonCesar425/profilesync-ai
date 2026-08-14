import axios from "axios";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { createProfile, listProfiles, updateProfile } from "../api/profiles";
import { ProfileForm } from "../components/profile/ProfileForm";
import { ProfileInfoPanel } from "../components/profile/ProfileInfoPanel";

import type { Profile, ProfilePayload } from "../types/profile";
import "./ProfilePage.css";

function getApiErrorMessage(error: unknown): string {
  if (!axios.isAxiosError(error)) {
    return "Ocorreu um erro inesperado. Tente novamente.";
  }

  const detail = error.response?.data?.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (error.response?.status === 401) {
    return "Sua sessão expirou. Faça login novamente.";
  }

  if (error.response?.status === 422) {
    return "Os dados informados são inválidos.";
  }

  if (!error.response) {
    return "Não foi possível conectar ao servidor.";
  }

  return "Não foi possível concluir a operação.";
}

export function ProfilePage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    let isActive = true;

    async function loadProfile(): Promise<void> {
      try {
        setErrorMessage(null);

        const profiles = await listProfiles();

        if (!isActive) {
          return;
        }

        setProfile(profiles[0] ?? null);
      } catch (error: unknown) {
        if (!isActive) {
          return;
        }

        setErrorMessage(getApiErrorMessage(error));
      } finally {
        if (isActive) {
          setIsLoading(false);
        }
      }
    }

    void loadProfile();

    return () => {
      isActive = false;
    };
  }, []);

  async function handleSubmit(payload: ProfilePayload): Promise<void> {
    try {
      setIsSubmitting(true);
      setErrorMessage(null);
      setSuccessMessage(null);

      const savedProfile = profile
        ? await updateProfile(profile.id, payload)
        : await createProfile(payload);

      setProfile(savedProfile);
      setSuccessMessage(
        profile
          ? "Perfil atualizado com sucesso."
          : "Perfil criado com sucesso.",
      );
    } catch (error: unknown) {
      setErrorMessage(getApiErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  }

  if (isLoading) {
    return (
      <main className="profile-page profile-page--loading">
        <p className="profile-page__loading" role="status">
          Carregando perfil...
        </p>
      </main>
    );
  }

  return (
    <main className="profile-page">
      <header className="profile-page__header">
        <div className="profile-page__heading">
          <p className="profile-page__eyebrow">ProfileSync AI</p>
          <h1>{profile ? "Editar perfil" : "Criar perfil"}</h1>
          <p className="profile-page__description">
            Cadastre suas informações profissionais para alimentar as análises e
            recomendações da plataforma.
          </p>
        </div>

        <Link className="profile-page__back-link" to="/dashboard">
          Voltar ao Dashboard
        </Link>
      </header>

      {errorMessage && (
        <p
          className="profile-page__feedback profile-page__feedback--error"
          role="alert"
        >
          {errorMessage}
        </p>
      )}

      {successMessage && (
        <p
          className="profile-page__feedback profile-page__feedback--success"
          role="status"
        >
          {successMessage}
        </p>
      )}

      <div className="profile-page__content">
        <ProfileForm
          profile={profile}
          isSubmitting={isSubmitting}
          onSubmit={handleSubmit}
        />

        <ProfileInfoPanel />
      </div>
    </main>
  );
}
