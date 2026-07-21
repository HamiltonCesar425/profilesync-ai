import { useNavigate } from "react-router-dom";

export function QuickActions(): React.JSX.Element {
  const navigate = useNavigate();

  return (
    <section aria-labelledby="quick-actions-title">
      <h2 id="quick-actions-title">Ações rápidas</h2>

      <div>
        <button type="button" onClick={() => navigate("/profile")}>
          Meu Perfil
        </button>

        <button type="button">Projetos</button>

        <button type="button">Tecnologias</button>

        <button type="button">Comparar Vaga</button>

        <button type="button">IA Assistida</button>
      </div>
    </section>
  );
}
