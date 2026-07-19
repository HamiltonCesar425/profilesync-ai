interface DashboardHeaderProps {
  onLogout: () => void;
}

export function DashboardHeader({
  onLogout,
}: DashboardHeaderProps): React.JSX.Element {
  return (
    <header>
      <div>
        <h1>ProfileSync AI</h1>
        <p>Visão geral da sua evolução profissional.</p>
      </div>

      <button type="button" onClick={onLogout}>
        Sair
      </button>
    </header>
  );
}
