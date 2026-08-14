import "./ProfileInfoPanel.css";

const PROFILE_BENEFITS = [
  "Gerar análises personalizadas",
  "Comparar seu perfil com vagas",
  "Criar recomendações relevantes",
  "Identificar oportunidades de crescimento",
];

export function ProfileInfoPanel() {
  return (
    <aside
      className="profile-info-panel"
      aria-labelledby="profile-info-panel-title"
    >
      <header className="profile-info-panel__header">
        <span className="profile-info-panel__icon" aria-hidden="true">
          ✦
        </span>

        <h2 id="profile-info-panel-title" className="profile-info-panel__title">
          Por que essas informações são importantes?
        </h2>
      </header>

      <p className="profile-info-panel__description">
        Os dados profissionais informados nesta página são utilizados para:
      </p>

      <ul className="profile-info-panel__list">
        {PROFILE_BENEFITS.map((benefit) => (
          <li key={benefit} className="profile-info-panel__item">
            <span className="profile-info-panel__check" aria-hidden="true">
              ✓
            </span>

            <span>{benefit}</span>
          </li>
        ))}
      </ul>

      <div className="profile-info-panel__notice">
        <strong>Uso transparente dos dados</strong>

        <p>
          Suas informações profissionais são utilizadas para melhorar as
          análises e recomendações oferecidas dentro da plataforma.
        </p>
      </div>
    </aside>
  );
}
