import { type SubmitEvent, useEffect, useState } from "react";

import type { Project, ProjectCreate } from "../../types/project";

interface ProjectFormProps {
  profileId: number;
  project?: Project | null;
  isSubmitting: boolean;
  onSubmit: (data: ProjectCreate) => Promise<void>;
  onCancel: () => void;
}

interface ProjectFormState {
  name: string;
  description: string;
  role: string;
  repositoryUrl: string;
  demoUrl: string;
  startDate: string;
  endDate: string;
  isCurrent: boolean;
}

const INITIAL_FORM_STATE: ProjectFormState = {
  name: "",
  description: "",
  role: "",
  repositoryUrl: "",
  demoUrl: "",
  startDate: "",
  endDate: "",
  isCurrent: false,
};

function normalizeOptionalValue(value: string): string | null {
  const normalizedValue = value.trim();

  return normalizedValue === "" ? null : normalizedValue;
}

export function ProjectForm({
  profileId,
  project = null,
  isSubmitting,
  onSubmit,
  onCancel,
}: ProjectFormProps) {
  const [formData, setFormData] =
    useState<ProjectFormState>(INITIAL_FORM_STATE);
  const [validationMessage, setValidationMessage] = useState("");

  useEffect(() => {
    if (project) {
      setFormData({
        name: project.name,
        description: project.description ?? "",
        role: project.role ?? "",
        repositoryUrl: project.repository_url ?? "",
        demoUrl: project.demo_url ?? "",
        startDate: project.start_date ?? "",
        endDate: project.end_date ?? "",
        isCurrent: project.is_current,
      });
    } else {
      setFormData(INITIAL_FORM_STATE);
    }

    setValidationMessage("");
  }, [project]);

  function handleChange(
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) {
    const { name, value, type } = event.target;
    const checked =
      event.target instanceof HTMLInputElement ? event.target.checked : false;

    setFormData((currentData) => ({
      ...currentData,
      [name]: type === "checkbox" ? checked : value,
      ...(name === "isCurrent" && checked ? { endDate: "" } : {}),
    }));

    setValidationMessage("");
  }

  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();

    const normalizedName = formData.name.trim();

    if (normalizedName.length < 2) {
      setValidationMessage(
        "O nome do projeto deve conter pelo menos 2 caracteres.",
      );
      return;
    }

    if (
      formData.startDate &&
      formData.endDate &&
      formData.endDate < formData.startDate
    ) {
      setValidationMessage(
        "A data de término não pode ser anterior à data de início.",
      );
      return;
    }

    if (formData.isCurrent && formData.endDate) {
      setValidationMessage(
        "Projetos em andamento não devem possuir data de término.",
      );
      return;
    }

    const projectData: ProjectCreate = {
      profile_id: profileId,
      name: normalizedName,
      description: normalizeOptionalValue(formData.description),
      role: normalizeOptionalValue(formData.role),
      repository_url: normalizeOptionalValue(formData.repositoryUrl),
      demo_url: normalizeOptionalValue(formData.demoUrl),
      start_date: normalizeOptionalValue(formData.startDate),
      end_date: formData.isCurrent
        ? null
        : normalizeOptionalValue(formData.endDate),
      is_current: formData.isCurrent,
    };

    await onSubmit(projectData);
  }

  return (
    <form className="project-form" onSubmit={handleSubmit} noValidate>
      <div className="form-group">
        <label htmlFor="project-name">Nome do projeto</label>
        <input
          id="project-name"
          name="name"
          type="text"
          minLength={2}
          maxLength={150}
          value={formData.name}
          onChange={handleChange}
          disabled={isSubmitting}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="project-role">Papel desempenhado</label>
        <input
          id="project-role"
          name="role"
          type="text"
          maxLength={120}
          value={formData.role}
          onChange={handleChange}
          disabled={isSubmitting}
          placeholder="Ex.: Desenvolvedor Full Stack"
        />
      </div>

      <div className="form-group">
        <label htmlFor="project-description">Descrição</label>
        <textarea
          id="project-description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          disabled={isSubmitting}
          rows={5}
        />
      </div>

      <div className="form-group">
        <label htmlFor="project-repository-url">URL do repositório</label>
        <input
          id="project-repository-url"
          name="repositoryUrl"
          type="url"
          value={formData.repositoryUrl}
          onChange={handleChange}
          disabled={isSubmitting}
          placeholder="https://github.com/usuario/projeto"
        />
      </div>

      <div className="form-group">
        <label htmlFor="project-demo-url">URL da demonstração</label>
        <input
          id="project-demo-url"
          name="demoUrl"
          type="url"
          value={formData.demoUrl}
          onChange={handleChange}
          disabled={isSubmitting}
          placeholder="https://projeto.exemplo.com"
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="project-start-date">Data de início</label>
          <input
            id="project-start-date"
            name="startDate"
            type="date"
            value={formData.startDate}
            onChange={handleChange}
            disabled={isSubmitting}
          />
        </div>

        <div className="form-group">
          <label htmlFor="project-end-date">Data de término</label>
          <input
            id="project-end-date"
            name="endDate"
            type="date"
            value={formData.endDate}
            onChange={handleChange}
            disabled={isSubmitting || formData.isCurrent}
            min={formData.startDate || undefined}
          />
        </div>
      </div>

      <label className="checkbox-field">
        <input
          name="isCurrent"
          type="checkbox"
          checked={formData.isCurrent}
          onChange={handleChange}
          disabled={isSubmitting}
        />
        Projeto em andamento
      </label>

      {validationMessage && (
        <p className="form-error" role="alert">
          {validationMessage}
        </p>
      )}

      <div className="project-form-actions">
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
            : project
              ? "Salvar alterações"
              : "Criar projeto"}
        </button>
      </div>
    </form>
  );
}
