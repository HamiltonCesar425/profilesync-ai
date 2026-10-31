import { Navigate, Outlet, useLocation } from "react-router-dom";

import { useAuth } from "./useAuth";

export function ProtectedRoute(): React.JSX.Element {
  const { isAuthenticated, sessionInvalidated } = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    return (
      <Navigate
        to="/login"
        replace
        state={{ from: location, sessionInvalidated }}
      />
    );
  }

  return <Outlet />;
}
