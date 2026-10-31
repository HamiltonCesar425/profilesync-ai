import type {
  FactualValue,
  TargetedResumePreviewResponse,
} from "../../types/targetedResume";

interface TargetedResumePreviewProps {
  preview: TargetedResumePreviewResponse;
}

function renderFactualValue(value: FactualValue["value"]): React.ReactNode {
  if (typeof value === "boolean") {
    return <code>{value ? "true" : "false"}</code>;
  }

  return value;
}

export function TargetedResumePreview({
  preview,
}: TargetedResumePreviewProps): React.JSX.Element {
  const { composition } = preview;

  return (
    <section
      className="compare-job-section targeted-resume-preview"
      aria-labelledby="targeted-resume-preview-title"
    >
      <header className="targeted-resume-preview-header">
        <div>
          <p className="page-eyebrow">Prévia factual</p>
          <h2 id="targeted-resume-preview-title">Currículo direcionado</h2>
        </div>

        <span className="targeted-resume-preview-state">{preview.state}</span>
      </header>

      <dl className="targeted-resume-metadata">
        <div>
          <dt>Identificação da prévia</dt>
          <dd>{preview.preview_id}</dd>
        </div>
        <div>
          <dt>Versão das regras</dt>
          <dd>{composition.ruleset_version}</dd>
        </div>
        <div>
          <dt>Perfil</dt>
          <dd>{composition.profile_id}</dd>
        </div>
        <div>
          <dt>Vaga</dt>
          <dd>{composition.job_id}</dd>
        </div>
      </dl>

      {composition.blocks.length === 0 ? (
        <p className="compare-job-empty-state" role="status">
          A prévia foi gerada, mas não contém blocos factuais.
        </p>
      ) : (
        <ol className="targeted-resume-block-list">
          {composition.blocks.map((block, blockIndex) => (
            <li key={`${block.section}-${blockIndex}`}>
              <article className="career-analysis-card targeted-resume-block">
                <h3>{block.section}</h3>

                {block.facts.length === 0 ? (
                  <p>Nenhum fato disponível neste bloco.</p>
                ) : (
                  <dl className="targeted-resume-fact-list">
                    {block.facts.map((fact, factIndex) => (
                      <div key={`${fact.name}-${factIndex}`}>
                        <dt>{fact.name}</dt>
                        <dd>{renderFactualValue(fact.value)}</dd>
                      </div>
                    ))}
                  </dl>
                )}

                <section className="targeted-resume-provenance">
                  <h4>Proveniência do bloco</h4>
                  <ul>
                    {block.provenance.map((reference, referenceIndex) => (
                      <li
                        key={`${reference.source_type}-${reference.source_id}-${referenceIndex}`}
                      >
                        <span>{reference.source_type}</span>
                        <span>Fonte {reference.source_id}</span>
                      </li>
                    ))}
                  </ul>
                </section>
              </article>
            </li>
          ))}
        </ol>
      )}

      <section
        className="targeted-resume-manifest"
        aria-labelledby="targeted-resume-manifest-title"
      >
        <h3 id="targeted-resume-manifest-title">Manifesto de fontes</h3>

        {composition.source_manifest.length === 0 ? (
          <p>Nenhuma fonte integra o manifesto desta prévia.</p>
        ) : (
          <ul>
            {composition.source_manifest.map((reference, referenceIndex) => (
              <li
                key={`${reference.source_type}-${reference.source_id}-${referenceIndex}`}
              >
                <span>{reference.source_type}</span>
                <span>Fonte {reference.source_id}</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </section>
  );
}
