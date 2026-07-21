import { type SubmitEvent, useEffect, useState } from "react";

import type { Profile, ProfilePayload } from "../../types/profile";

interface ProfileFormProps {
  profile: Profile | null;
  isSubmitting: boolean;
  onSubmit: (payload: ProfilePayload) => Promise<void>;
}

const EMPTY_FORM: ProfilePayload = {
  full_name: "",
  professional_title: "",
  summary: "",
  location: null,
  linkedin_url: null,
  github_url: null,
};

export function ProfileForm({
  profile,
  isSubmitting,
  onSubmit,
}: ProfileFormProps) {
  const [formData, setFormData] = useState<ProfilePayload>(EMPTY_FORM);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!profile) {
      setFormData(EMPTY_FORM);
      return;
    }

    setFormData({
      full_name: profile.full_name,
      professional_title: profile.professional_title,
      summary: profile.summary,
      location: profile.location,
      linkedin_url: profile.linkedin_url,
      github_url: profile.github_url,
    });
  }, [profile]);

  function updateField(field: keyof ProfilePayload, value: string): void {
    const nullableFields: Array<keyof ProfilePayload> = [
      "location",
      "linkedin_url",
      "github_url",
    ];

    setFormData((current) => ({
      ...current,
      [field]: nullableFields.includes(field) ? value || null : value,
    }));
  }

  async function handleSubmit(
    event: SubmitEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    const fullName = formData.full_name.trim();
    const professionalTitle = formData.professional_title.trim();
    const summary = formData.summary.trim();

    if (fullName.length < 3) {
      setErrorMessage("O nome completo deve ter ao menos 3 caracteres.");
      return;
    }

    if (professionalTitle.length < 3) {
      setErrorMessage("O título profissional deve ter ao menos 3 caracteres.");
      return;
    }

    if (summary.length < 20) {
      setErrorMessage("O resumo profissional deve ter ao menos 20 caracteres.");
      return;
    }

    await onSubmit({
      full_name: fullName,
      professional_title: professionalTitle,
      summary,
      location: formData.location?.trim() || null,
      linkedin_url: formData.linkedin_url?.trim() || null,
      github_url: formData.github_url?.trim() || null,
    });
  }

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="full_name">Nome completo</label>
        <input
          id="full_name"
          name="full_name"
          type="text"
          minLength={3}
          maxLength={120}
          required
          value={formData.full_name}
          onChange={(event) => updateField("full_name", event.target.value)}
        />
      </div>

      <div>
        <label htmlFor="professional_title">Título profissional</label>
        <input
          id="professional_title"
          name="professional_title"
          type="text"
          minLength={3}
          maxLength={120}
          required
          value={formData.professional_title}
          onChange={(event) =>
            updateField("professional_title", event.target.value)
          }
        />
      </div>

      <div>
        <label htmlFor="summary">Resumo profissional</label>
        <textarea
          id="summary"
          name="summary"
          minLength={20}
          maxLength={1000}
          required
          value={formData.summary}
          onChange={(event) => updateField("summary", event.target.value)}
        />
      </div>

      <div>
        <label htmlFor="location">Localização</label>
        <input
          id="location"
          name="location"
          type="text"
          maxLength={120}
          value={formData.location ?? ""}
          onChange={(event) => updateField("location", event.target.value)}
        />
      </div>

      <div>
        <label htmlFor="linkedin_url">LinkedIn</label>
        <input
          id="linkedin_url"
          name="linkedin_url"
          type="url"
          maxLength={255}
          value={formData.linkedin_url ?? ""}
          onChange={(event) => updateField("linkedin_url", event.target.value)}
        />
      </div>

      <div>
        <label htmlFor="github_url">GitHub</label>
        <input
          id="github_url"
          name="github_url"
          type="url"
          maxLength={255}
          value={formData.github_url ?? ""}
          onChange={(event) => updateField("github_url", event.target.value)}
        />
      </div>

      {errorMessage && <p role="alert">{errorMessage}</p>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting
          ? "Salvando..."
          : profile
            ? "Atualizar perfil"
            : "Criar perfil"}
      </button>
    </form>
  );
}
