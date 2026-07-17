import { useAuth } from "../auth/useAuth";

export function DashboardPage(): React.JSX.Element {
  const { logout } = useAuth();

  return (
    <main>
      <h1>ProfileSync AI</h1>
      <p>Área autenticada.</p>

      <button type="button" onClick={logout}>
        Sair
      </button>
    </main>
  );
}
