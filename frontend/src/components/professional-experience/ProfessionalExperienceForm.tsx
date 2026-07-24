import { type SubmitEvent, useEffect, useState } from "react";

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

  useEffect(() => {
    setFormData(getInitialFormState(experience));
    setValidationMessage(null);
  }, [experience]);

  function updateField<K extends keyof ProfessionalExperienceFormState>(
    field: K,
    value: ProfessionalExperienceFormState[K],
  ): void {
    setFormData((currentFormData) => ({
      ...currentFormData,
      [field]: value,
    }));
  }

  function handleCurrentExperienceChange(checked: boolean): void {
    setFormData((currentFormData) => ({
      ...currentFormData,
      isCurrent: checked,
      endDate: checked ? "" : currentFormData.endDate,
    }));
  }

  async function handleSubmit(
  event: SubmitEvent<HTMLFormElement>,
): Promise<void> {
  event.preventDefault();

  setValidationMessage(null);

  if (
    !formData.isCurrent &&
    formData.endDate &&
    formData.endDate < formData.startDate
  ) {
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
    end_date: formData.isCurrent
      ? null
      : formData.endDate || null,
    is_current: formData.isCurrent,
  };

  await onSubmit(payload);
}

  const isEditing = Boolean(experience);

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
          disabled={isSubmitting}
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
          disabled={isSubmitting}
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
          disabled={isSubmitting}
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
          disabled={isSubmitting}
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
          disabled={isSubmitting}
        />
      </div>

      <div className="professional-experience-field">
        <label htmlFor="start-date">Data de início</label>
        <input
          id="start-date"
          type="date"
          value={formData.startDate}
          onChange={(event) => updateField("startDate", event.target.value)}
          required
          disabled={isSubmitting}
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
            disabled={isSubmitting}
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
          required={!formData.isCurrent}
          disabled={formData.isCurrent || isSubmitting}
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
          disabled={isSubmitting}
          placeholder="Descreva suas principais responsabilidades, entregas e resultados."
        />
      </div>

      <div className="professional-experience-field">
        <button
          className="primary-button"
          type="submit"
          disabled={isSubmitting}
        >
          {isSubmitting
            ? "Salvando..."
            : isEditing
              ? "Atualizar experiência"
              : "Criar experiência"}
        </button>

        <button 
          className="secondy-button"
          type="button"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancelar
        </button>
      </div>
    </form>
  );
}
