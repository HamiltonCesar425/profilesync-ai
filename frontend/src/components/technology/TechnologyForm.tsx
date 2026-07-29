import { type ChangeEvent, type SubmitEvent, useEffect, useState } from "react";

import type { Technology, TechnologyCreate } from "../../types/technology";

interface TechnologyFormProps {
  technology?: Technology | null;
  isSubmitting: boolean;
  onSubmit: (data: TechnologyCreate) => Promise<void>;
  onCancel: () => void;
}

const INITIAL_FORM_DATA: TechnologyCreate = {
  name: "",
  category: "",
  proficiency_level: "",
  years_experience: null,
};

const PROFICIENCY_LEVELS = [
  "Básico",
  "Intermediário",
  "Avançado",
  "Especialista",
] as const;

export function TechnologyForm({
  technology,
  isSubmitting,
  onSubmit,
  onCancel,
}: TechnologyFormProps) {
  const [formData, setFormData] = useState<TechnologyCreate>(INITIAL_FORM_DATA);

  const [validationMessage, setValidationMessage] = useState("");

  useEffect(() => {
    if (technology) {
      setFormData({
        name: technology.name,
        category: technology.category,
        proficiency_level: technology.proficiency_level,
        years_experience: technology.years_experience,
      });
    } else {
      setFormData(INITIAL_FORM_DATA);
    }

    setValidationMessage("");
  }, [technology]);

  function handleTextChange(
    event: ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) {
    const { name, value } = event.target;

    setFormData((currentData) => ({
      ...currentData,
      [name]: value,
    }));

    setValidationMessage("");
  }

  function handleYearsExperienceChange(event: ChangeEvent<HTMLInputElement>) {
    const { value } = event.target;

    setFormData((currentData) => ({
      ...currentData,
      years_experience: value === "" ? null : Number(value),
    }));

    setValidationMessage("");
  }

  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();

    const normalizedName = formData.name.trim();
    const normalizedCategory = formData.category.trim();
    const normalizedProficiencyLevel = formData.proficiency_level.trim();

    if (!normalizedName || !normalizedCategory || !normalizedProficiencyLevel) {
      setValidationMessage("Preencha todos os campos obrigatórios.");
      return;
    }

    if (
      formData.years_experience !== null &&
      (!Number.isInteger(formData.years_experience) ||
        formData.years_experience < 0)
    ) {
      setValidationMessage(
        "Os anos de experiência devem ser um número inteiro igual ou maior que zero.",
      );
      return;
    }

    await onSubmit({
      name: normalizedName,
      category: normalizedCategory,
      proficiency_level: normalizedProficiencyLevel,
      years_experience: formData.years_experience,
    });
  }

  return (
    <form className="technology-form" onSubmit={handleSubmit} noValidate>
      <div className="form-field">
        <label htmlFor="technology-name">Tecnologia</label>

        <input
          id="technology-name"
          name="name"
          type="text"
          value={formData.name}
          onChange={handleTextChange}
          minLength={1}
          maxLength={100}
          placeholder="Ex.: Python"
          autoComplete="off"
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="form-field">
        <label htmlFor="technology-category">Categoria</label>

        <input
          id="technology-category"
          name="category"
          type="text"
          value={formData.category}
          onChange={handleTextChange}
          minLength={1}
          maxLength={50}
          placeholder="Ex.: Linguagem de programação"
          autoComplete="off"
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="form-field">
        <label htmlFor="technology-proficiency-level">
          Nível de proficiência
        </label>

        <select
          id="technology-proficiency-level"
          name="proficiency_level"
          value={formData.proficiency_level}
          onChange={handleTextChange}
          required
          disabled={isSubmitting}
        >
          <option value="">Selecione um nível</option>

          {PROFICIENCY_LEVELS.map((level) => (
            <option key={level} value={level}>
              {level}
            </option>
          ))}
        </select>
      </div>

      <div className="form-field">
        <label htmlFor="technology-years-experience">Anos de experiência</label>

        <input
          id="technology-years-experience"
          name="years_experience"
          type="number"
          value={formData.years_experience ?? ""}
          onChange={handleYearsExperienceChange}
          min={0}
          step={1}
          inputMode="numeric"
          placeholder="Ex.: 2"
          disabled={isSubmitting}
        />
      </div>

      {validationMessage && (
        <p className="form-error-message" role="alert">
          {validationMessage}
        </p>
      )}

      <div className="technology-form-actions">
        <button
          className="secondary-button"
          type="button"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancelar
        </button>

        <button
          className="primary-button"
          type="submit"
          disabled={isSubmitting}
        >
          {isSubmitting
            ? "Salvando..."
            : technology
              ? "Salvar alterações"
              : "Cadastrar tecnologia"}
        </button>
      </div>
    </form>
  );
}
