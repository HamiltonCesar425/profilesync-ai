import { type FormEvent, useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  analyzeRegisteredJob,
  getDetectedCompetencies,
} from "../api/careerIntelligence";
import { createJob, listJobs } from "../api/jobs";
import { listProfiles } from "../api/profiles";
import type { CareerAnalysis } from "../types/careerAnalysis";
import type { Job, JobCreate } from "../types/job";
import type { Profile } from "../types/profile";

const INITIAL_JOB_FORM: JobCreate = {
  title: "",
  company: null,
  description: "",
};

export function CompareJobPage(): React.JSX.Element {
  const navigate = useNavigate();

  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJobId, setSelectedJobId] = useState<number | null>(null);

  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [selectedProfileId, setSelectedProfileId] = useState<number | null>(
    null,
  );
  const [detectedCompetencies, setDetectedCompetencies] = useState<string[]>(
    [],
  );

  const [jobForm, setJobForm] = useState<JobCreate>(INITIAL_JOB_FORM);

  const [analysis, setAnalysis] = useState<CareerAnalysis | null>(null);

  const [isLoadingData, setIsLoadingData] = useState(true);
  const [isLoadingCompetencies, setIsLoadingCompetencies] = useState(false);
  const [isCreatingJob, setIsCreatingJob] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const loadComparisonData = useCallback(async () => {
    setIsLoadingData(true);
    setErrorMessage("");

    try {
      const [registeredJobs, registeredProfiles] = await Promise.all([
        listJobs(),
        listProfiles(),
      ]);

      setJobs(registeredJobs);
      setProfiles(registeredProfiles);
      setSelectedJobId((currentJobId) => {
        if (
          currentJobId &&
          registeredJobs.some((job) => job.id === currentJobId)
        ) {
          return currentJobId;
        }

        return registeredJobs[0]?.id ?? null;
      });
      setSelectedProfileId((currentProfileId) => {
        if (
          currentProfileId &&
          registeredProfiles.some(
            (profile) => profile.id === currentProfileId,
          )
        ) {
          return currentProfileId;
        }

        return registeredProfiles[0]?.id ?? null;
      });
    } catch {
      setErrorMessage("Não foi possível carregar vagas e perfis cadastrados.");
    } finally {
      setIsLoadingData(false);
    }
  }, []);

  useEffect(() => {
    void loadComparisonData();
  }, [loadComparisonData]);

  useEffect(() => {
    if (selectedProfileId === null) {
      setDetectedCompetencies([]);
      return;
    }

    let isCurrentRequest = true;
    setIsLoadingCompetencies(true);

    void getDetectedCompetencies(selectedProfileId)
      .then((response) => {
        if (isCurrentRequest) {
          setDetectedCompetencies(response.competencies);
        }
      })
      .catch(() => {
        if (isCurrentRequest) {
          setDetectedCompetencies([]);
          setErrorMessage(
            "Não foi possível detectar as competências do perfil.",
          );
        }
      })
      .finally(() => {
        if (isCurrentRequest) {
          setIsLoadingCompetencies(false);
        }
      });

    return () => {
      isCurrentRequest = false;
    };
  }, [selectedProfileId]);

  function handleJobFormChange(field: keyof JobCreate, value: string): void {
    setJobForm((currentForm) => ({
      ...currentForm,
      [field]: field === "company" ? value || null : value,
    }));
  }

  async function handleCreateJob(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    const title = jobForm.title.trim();
    const description = jobForm.description.trim();
    const company = jobForm.company?.trim() || null;

    if (title.length < 2) {
      setErrorMessage("O título da vaga deve possuir pelo menos 2 caracteres.");
      return;
    }

    if (description.length < 2) {
      setErrorMessage(
        "A descrição da vaga deve possuir pelo menos 2 caracteres.",
      );
      return;
    }

    setIsCreatingJob(true);
    setErrorMessage("");
    setSuccessMessage("");
    setAnalysis(null);

    try {
      const createdJob = await createJob({
        title,
        company,
        description,
      });

      setJobs((currentJobs) => [createdJob, ...currentJobs]);
      setSelectedJobId(createdJob.id);
      setJobForm(INITIAL_JOB_FORM);
      setSuccessMessage("Vaga cadastrada e selecionada com sucesso.");
    } catch {
      setErrorMessage("Não foi possível cadastrar a vaga.");
    } finally {
      setIsCreatingJob(false);
    }
  }

  async function handleAnalyzeJob(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    if (!selectedJobId) {
      setErrorMessage("Selecione ou cadastre uma vaga antes de analisar.");
      return;
    }

    if (!selectedProfileId) {
      setErrorMessage("Selecione ou cadastre um perfil antes de analisar.");
      return;
    }

    setIsAnalyzing(true);
    setErrorMessage("");
    setSuccessMessage("");
    setAnalysis(null);

    try {
      const result = await analyzeRegisteredJob(selectedJobId, {
        profile_id: selectedProfileId,
      });

      setAnalysis(result);
      setSuccessMessage("Análise concluída com sucesso.");
    } catch {
      setErrorMessage(
        "Não foi possível comparar seu perfil com a vaga selecionada.",
      );
    } finally {
      setIsAnalyzing(false);
    }
  }

  const selectedJob = jobs.find((job) => job.id === selectedJobId) ?? null;

  return (
    <main className="page-container compare-job-page">
      <header className="page-header compare-job-header">
        <div>
          <p className="page-eyebrow">Inteligência profissional</p>

          <h1>Comparar vaga</h1>

          <p>
            Cadastre ou selecione uma vaga e analise a compatibilidade com suas
            competências profissionais.
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
        </div>
      </header>

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

      <section className="compare-job-section">
        <div className="compare-job-section-header">
          <div>
            <p className="page-eyebrow">Etapa 1</p>
            <h2>Cadastrar uma vaga</h2>
          </div>

          <p>
            Cole a descrição completa da oportunidade para preservar os
            requisitos usados na análise.
          </p>
        </div>

        <form className="compare-job-form" onSubmit={handleCreateJob}>
          <div className="compare-job-field">
            <label htmlFor="job-title">Título da vaga</label>

            <input
              id="job-title"
              type="text"
              value={jobForm.title}
              minLength={2}
              maxLength={150}
              disabled={isCreatingJob}
              onChange={(event) =>
                handleJobFormChange("title", event.target.value)
              }
              placeholder="Ex.: Desenvolvedor Python Backend"
              required
            />
          </div>

          <div className="compare-job-field">
            <label htmlFor="job-company">Empresa</label>

            <input
              id="job-company"
              type="text"
              value={jobForm.company ?? ""}
              maxLength={150}
              disabled={isCreatingJob}
              onChange={(event) =>
                handleJobFormChange("company", event.target.value)
              }
              placeholder="Ex.: Empresa de Tecnologia"
            />
          </div>

          <div className="compare-job-field">
            <label htmlFor="job-description">Descrição da vaga</label>

            <textarea
              id="job-description"
              value={jobForm.description}
              minLength={2}
              disabled={isCreatingJob}
              onChange={(event) =>
                handleJobFormChange("description", event.target.value)
              }
              placeholder="Cole aqui a descrição completa da vaga..."
              required
            />
          </div>

          <div className="compare-job-form-actions">
            <button
              className="primary-button"
              type="submit"
              disabled={isCreatingJob}
            >
              {isCreatingJob ? "Cadastrando..." : "Cadastrar vaga"}
            </button>
          </div>
        </form>
      </section>

      <section className="compare-job-section">
        <div className="compare-job-section-header">
          <div>
            <p className="page-eyebrow">Etapa 2</p>
            <h2>Executar comparação</h2>
          </div>

          <p>
            Escolha o perfil e a vaga. As competências cadastradas e detectadas
            serão reutilizadas automaticamente na análise.
          </p>
        </div>

        {isLoadingData ? (
          <p className="compare-job-empty-state">Carregando vagas...</p>
        ) : jobs.length === 0 ? (
          <div className="compare-job-empty-state">
            <h3>Nenhuma vaga cadastrada</h3>
            <p>Cadastre uma vaga acima para iniciar a comparação.</p>
          </div>
        ) : profiles.length === 0 ? (
          <div className="compare-job-empty-state">
            <h3>Nenhum perfil cadastrado</h3>
            <p>
              Cadastre seu perfil, experiências, projetos e tecnologias antes
              de iniciar a comparação.
            </p>
          </div>
        ) : (
          <form className="compare-job-form" onSubmit={handleAnalyzeJob}>
            <div className="compare-job-field">
              <label htmlFor="comparison-profile">Perfil profissional</label>

              <select
                id="comparison-profile"
                value={selectedProfileId ?? ""}
                disabled={isAnalyzing || isLoadingCompetencies}
                onChange={(event) => {
                  setSelectedProfileId(Number(event.target.value));
                  setAnalysis(null);
                  setSuccessMessage("");
                }}
              >
                {profiles.map((profile) => (
                  <option key={profile.id} value={profile.id}>
                    {profile.full_name} — {profile.professional_title}
                  </option>
                ))}
              </select>
            </div>

            <div className="compare-job-field">
              <label htmlFor="registered-job">Vaga cadastrada</label>

              <select
                id="registered-job"
                value={selectedJobId ?? ""}
                disabled={isAnalyzing}
                onChange={(event) => {
                  setSelectedJobId(Number(event.target.value));
                  setAnalysis(null);
                  setSuccessMessage("");
                }}
              >
                {jobs.map((job) => (
                  <option key={job.id} value={job.id}>
                    {job.title}
                    {job.company ? ` — ${job.company}` : ""}
                  </option>
                ))}
              </select>
            </div>

            {selectedJob && (
              <article className="selected-job-summary">
                <h3>{selectedJob.title}</h3>

                {selectedJob.company && <p>{selectedJob.company}</p>}

                <p>{selectedJob.description}</p>
              </article>
            )}

            <section className="detected-competencies" aria-live="polite">
              <h3>Competências detectadas</h3>

              {isLoadingCompetencies ? (
                <p>Detectando competências do perfil...</p>
              ) : detectedCompetencies.length > 0 ? (
                <ul>
                  {detectedCompetencies.map((competency) => (
                    <li key={competency.toLocaleLowerCase("pt-BR")}>
                      {competency}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>
                  Nenhuma competência detectada. Cadastre tecnologias ou
                  detalhe suas experiências e projetos.
                </p>
              )}
            </section>

            <div className="compare-job-form-actions">
              <button
                className="primary-button"
                type="submit"
                disabled={
                  isAnalyzing ||
                  isLoadingCompetencies ||
                  !selectedJobId ||
                  !selectedProfileId ||
                  detectedCompetencies.length === 0
                }
              >
                {isAnalyzing ? "Analisando..." : "Comparar com a vaga"}
              </button>
            </div>
          </form>
        )}
      </section>

      {analysis && (
        <section
          className="career-analysis-results"
          aria-labelledby="analysis-result-title"
        >
          <div className="career-analysis-header">
            <div>
              <p className="page-eyebrow">Resultado</p>

              <h2 id="analysis-result-title">{analysis.target_role}</h2>
            </div>

            <div
              className="compatibility-score"
              aria-label={`Compatibilidade de ${analysis.compatibility_score} por cento`}
            >
              <strong>{analysis.compatibility_score}%</strong>
              <span>Compatibilidade</span>
            </div>
          </div>

          <div className="career-analysis-grid">
            <article className="career-analysis-card">
              <h3>Pontos fortes</h3>

              {analysis.strengths.length > 0 ? (
                <ul>
                  {analysis.strengths.map((strength) => (
                    <li key={strength}>{strength}</li>
                  ))}
                </ul>
              ) : (
                <p>Nenhum ponto forte identificado.</p>
              )}
            </article>

            <article className="career-analysis-card">
              <h3>Lacunas profissionais</h3>

              {analysis.gaps.length > 0 ? (
                <ul>
                  {analysis.gaps.map((gap) => (
                    <li key={gap}>{gap}</li>
                  ))}
                </ul>
              ) : (
                <p>Nenhuma lacuna identificada.</p>
              )}
            </article>
          </div>

          <article className="career-analysis-card">
            <h3>Recomendações de impacto</h3>

            {analysis.recommendations.length > 0 ? (
              <div className="recommendation-list">
                {analysis.recommendations.map((recommendation) => (
                  <section
                    className="recommendation-item"
                    key={`${recommendation.skill}-${recommendation.priority}`}
                  >
                    <div className="recommendation-item-header">
                      <h4>{recommendation.skill}</h4>

                      <span>{recommendation.impact_score} pontos</span>
                    </div>

                    <p>
                      <strong>Prioridade:</strong> {recommendation.priority}
                    </p>

                    <p>{recommendation.reason}</p>
                  </section>
                ))}
              </div>
            ) : (
              <p>Nenhuma recomendação necessária.</p>
            )}
          </article>

          <article className="career-analysis-card">
            <div className="action-plan-score">
              <div>
                <span>Score atual</span>
                <strong>{analysis.action_plan.current_score}%</strong>
              </div>

              <div>
                <span>Estimativa após as ações</span>
                <strong>
                  {analysis.action_plan.estimated_score_after_actions}%
                </strong>
              </div>
            </div>

            <h3>Plano de ação</h3>

            {analysis.action_plan.actions.length > 0 ? (
              <ol className="action-plan-list">
                {analysis.action_plan.actions.map((action) => (
                  <li
                    className="action-plan-item"
                    key={`${action.priority}-${action.title}`}
                  >
                    <div className="action-plan-item-header">
                      <h4>{action.title}</h4>

                      <span>Prioridade {action.priority}</span>
                    </div>

                    <p>{action.description}</p>

                    <dl>
                      <div>
                        <dt>Categoria</dt>
                        <dd>{action.category}</dd>
                      </div>

                      <div>
                        <dt>Esforço estimado</dt>
                        <dd>{action.estimated_effort}</dd>
                      </div>

                      <div>
                        <dt>Impacto</dt>
                        <dd>{action.impact_score} pontos</dd>
                      </div>
                    </dl>
                  </li>
                ))}
              </ol>
            ) : (
              <p>Nenhuma ação adicional foi recomendada.</p>
            )}
          </article>
        </section>
      )}
    </main>
  );
}
