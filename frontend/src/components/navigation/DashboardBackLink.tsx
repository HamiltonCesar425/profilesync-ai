import { Link } from "react-router-dom";

export function DashboardBackLink(): React.JSX.Element {
  return (
    <Link className="secondary-button dashboard-back-link" to="/">
      Voltar ao Dashboard
    </Link>
  );
}
