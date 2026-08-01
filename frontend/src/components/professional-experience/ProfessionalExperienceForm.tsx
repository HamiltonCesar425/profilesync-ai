import axios from "axios";
import { type SubmitEvent, useEffect, useState } from "react";

import { improveProfessionalDescription } from "../../api/aiAssistant";
import type {
  ProfessionalExperience,
  ProfessionalExperienceCreate,
} from "../../types/professionalExperience";

interface ProfessionalExperienceFormProps {
  experience?: ProfessionalExperience | null;
  isSubmitting: boolean;
  onSubmit: (data: ProfessionalExperienceCreate) => Promise<void>;
  onCancel: () => void;
}

interface ProfessionalExperienceFormState {
  companyName: string;
  position: string;
  employmentType: string;
  workModel: string;
  location: string;
  description: string;
  startDate: string;
  endDate: string;
  isCurrent: boolean;
}

type AIFeedback = {
  type: "success" | "error";
  message: string;
};

const EMPTY_FORM_STATE: ProfessionalExperienceFormState = {
  companyName: "",
  position: "",
  employmentType: "",
  workModel: "",
  location: "",
  description: "",
  startDate: "",
  endDate: "",
  isCurrent: false,
};

function getInitialFormState(
  experience?: ProfessionalExperience | null,
): ProfessionalExperienceFormState {
  if (!experience) {
    return EMPTY_FORM_STATE;
  }

  return {
    companyName: experience.company_name,
    position: experience.position,
    employmentType: experience.employment_type ?? "",
    workModel: experience.work_model ?? "",
    location: experience.location ?? "",
    description: experience.description ?? "",
    startDate: experience.start_date,
    endDate: experience.end_date ?? "",
    isCurrent: experience.is_current,
  };
}

function getTodayDate(): string {
  return new Date().toISOString().split("T")[0];
}

export function ProfessionalExperienceForm({
  experience,
  isSubmitting,
  onSubmit,
  onCancel,
}: ProfessionalExperienceFormProps) {
  const [formData, setFormData] = useState<ProfessionalExperienceFormState>(
    () => getInitialFormState(experience),
  );
  const [validationMessage, setValidationMessage] = useState<string | null>(
    null,
  );
  const [isImprovingDescription, setIsImprovingDescription] = useState(false);
  const [aiFeedback, setAIFeedback] = useState<AIFeedback | null>(null);

  const today = getTodayDate();

  useEffect(() => {
    setFormData(getInitialFormState(experience));
    setValidationMessage(null);
    setAIFeedback(null);
  }, [experience]);

  function updateField<K extends keyof ProfessionalExperienceFormState>(
    field: K,
    value: ProfessionalExperienceFormState[K],
  ): void {
    setFormData((currentFormData) => ({
      ...currentFormData,
      [field]: value,
    }));

    setValidationMessage(null);

    if (field === "description") {
      setAIFeedback(null);
    }
  }

  function handleCurrentExperienceChange(checked: boolean): void {
    setFormData((currentFormData) => ({
      ...currentFormData,
      isCurrent: checked,
      endDate: checked ? "" : currentFormData.endDate,
    }));

    setValidationMessage(null);
  }

  async function handleImproveDescription(): Promise<void> {
    const currentDescription = formData.description.trim();

    setAIFeedback(null);

    if (!currentDescription) {
      setAIFeedback({
        type: "error",
        message: "Escreva uma descrição antes de solicitar a melhoria com IA.",
      });
      return;
    }

    try {
      setIsImprovingDescription(true);

      const improvedDescription =
        await improveProfessionalDescription(currentDescription);

      setFormData((currentFormData) => ({
        ...currentFormData,
        description: improvedDescription,
      }));

      setAIFeedback({
        type: "success",
        message:
          "Descrição melhorada com sucesso. Revise o conteúdo antes de salvar.",
      });
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const detail = error.response?.data?.detail;

        if (typeof detail === "string") {
          setAIFeedback({
            type: "error",
            message: detail,
          });
          return;
        }
      }
      setAIFeedback({
        type: "error",
        message: "Não foi possível utilizar a IA neste momento.",
      });
    } finally {
      setIsImprovingDescription(false);
    }
  }

  async function handleSubmit(
    event: SubmitEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    if (isImprovingDescription) {
      return;
    }

    setValidationMessage(null);

    if (!formData.startDate) {
      setValidationMessage("Informe a data de início.");
      return;
    }

    if (formData.startDate > today) {
      setValidationMessage("A data de início não pode estar no futuro.");
      return;
    }

    if (!formData.isCurrent && !formData.endDate) {
      setValidationMessage(
        "Informe a data de término ou marque a experiência como atual.",
      );
      return;
    }

    if (!formData.isCurrent && formData.endDate > today) {
      setValidationMessage("A data de término não pode estar no futuro.");
      return;
    }

    if (!formData.isCurrent && formData.endDate < formData.startDate) {
      setValidationMessage(
        "A data de término não pode ser anterior à data de início.",
      );
      return;
    }

    const payload: ProfessionalExperienceCreate = {
      company_name: formData.companyName.trim(),
      position: formData.position.trim(),
      employment_type: formData.employmentType.trim() || null,
      work_model: formData.workModel.trim() || null,
      location: formData.location.trim() || null,
      description: formData.description.trim() || null,
      start_date: formData.startDate,
      end_date: formData.isCurrent ? null : formData.endDate || null,
      is_current: formData.isCurrent,
    };

    await onSubmit(payload);
  }

  const isEditing = Boolean(experience);
  const isFormBusy = isSubmitting || isImprovingDescription;
  const isDescriptionEmpty = !formData.description.trim();

  return (
    <form className="professional-experience-form" onSubmit={handleSubmit}>
      <h2>
        {isEditing
          ? "Editar experiência profissional"
          : "Nova experiência profissional"}
      </h2>

      <div className="professional-experience-field">
        <label htmlFor="company-name">Empresa</label>
        <input
          id="company-name"
          type="text"
          value={formData.companyName}
          onChange={(event) => updateField("companyName", event.target.value)}
          minLength={2}
          maxLength={200}
          required
          disabled={isFormBusy}
        />
      </div>

      <div className="professional-experience-field">
        <label htmlFor="position">Cargo</label>
        <input
          id="position"
          type="text"
          value={formData.position}
          onChange={(event) => updateField("position", event.target.value)}
          minLength={2}
          maxLength={150}
          required
          disabled={isFormBusy}
        />
      </div>

      <div className="professional-experience-field">
        <label htmlFor="employment-type">Tipo de contratação</label>
        <select
          id="employment-type"
          value={formData.employmentType}
          onChange={(event) =>
            updateField("employmentType", event.target.value)
          }
          disabled={isFormBusy}
        >
          <option value="">Não informado</option>
          <option value="CLT">CLT</option>
          <option value="PJ">PJ</option>
          <option value="Autônomo">Autônomo</option>
          <option value="Freelancer">Freelancer</option>
          <option value="Estágio">Estágio</option>
          <option value="Temporário">Temporário</option>
          <option value="Voluntário">Voluntário</option>
        </select>
      </div>

      <div className="professional-experience-field">
        <label htmlFor="work-model">Modelo de trabalho</label>
        <select
          id="work-model"
          value={formData.workModel}
          onChange={(event) => updateField("workModel", event.target.value)}
          disabled={isFormBusy}
        >
          <option value="">Não informado</option>
          <option value="Presencial">Presencial</option>
          <option value="Híbrido">Híbrido</option>
          <option value="Remoto">Remoto</option>
        </select>
      </div>

      <div className="professional-experience-field">
        <label htmlFor="location">Localização</label>
        <input
          id="location"
          type="text"
          value={formData.location}
          onChange={(event) => updateField("location", event.target.value)}
          maxLength={120}
          placeholder="Ex.: Campinas, SP"
          disabled={isFormBusy}
        />
      </div>

      <div className="professional-experience-field">
        <label htmlFor="start-date">Data de início</label>
        <input
          id="start-date"
          type="date"
          value={formData.startDate}
          onChange={(event) => updateField("startDate", event.target.value)}
          max={today}
          required
          disabled={isFormBusy}
        />
      </div>

      <div className="professional-experience-checkbox-field">
        <label htmlFor="current-experience">
          <input
            id="current-experience"
            type="checkbox"
            checked={formData.isCurrent}
            onChange={(event) =>
              handleCurrentExperienceChange(event.target.checked)
            }
            disabled={isFormBusy}
          />

          <span>Trabalho atualmente nesta empresa</span>
        </label>
      </div>

      <div className="professional-experience-field">
        <label htmlFor="end-date">Data de término</label>
        <input
          id="end-date"
          type="date"
          value={formData.endDate}
          onChange={(event) => updateField("endDate", event.target.value)}
          min={formData.startDate || undefined}
          max={today}
          required={!formData.isCurrent}
          disabled={formData.isCurrent || isFormBusy}
        />
      </div>

      {validationMessage && (
        <p className="feedback-message feedback-message-error" role="alert">
          {validationMessage}
        </p>
      )}

      <div className="professional-experience-field">
        <label htmlFor="description">Descrição</label>
        <textarea
          id="description"
          value={formData.description}
          onChange={(event) => updateField("description", event.target.value)}
          rows={6}
          disabled={isFormBusy}
          placeholder="Descreva suas principais responsabilidades, entregas e resultados."
        />

        <button
          className="secondary-button"
          type="button"
          onClick={handleImproveDescription}
          disabled={isFormBusy || isDescriptionEmpty}
          aria-describedby="ai-description-feedback"
        >
          {isImprovingDescription
            ? "Melhorando descrição..."
            : "Melhorar com IA"}
        </button>

        {aiFeedback && (
          <p
            id="ai-description-feedback"
            className={`feedback-message feedback-message-${aiFeedback.type}`}
            role={aiFeedback.type === "error" ? "alert" : "status"}
            aria-live="polite"
          >
            {aiFeedback.message}
          </p>
        )}
      </div>

      <div className="professional-experience-form-actions">
        <button className="primary-button" type="submit" disabled={isFormBusy}>
          {isSubmitting
            ? "Salvando..."
            : isEditing
              ? "Atualizar experiência"
              : "Criar experiência"}
        </button>

        <button
          className="secondary-button"
          type="button"
          onClick={onCancel}
          disabled={isFormBusy}
        >
          Cancelar
        </button>
      </div>
    </form>
  );
}
