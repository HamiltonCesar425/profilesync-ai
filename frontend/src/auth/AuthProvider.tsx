import { type ReactNode, useEffect, useMemo, useState } from "react";

import { login as authenticate, type LoginRequest } from "../api/auth";

import { AuthContext } from "./AuthContext";
import {
  AUTH_CHANGED_EVENT,
  getAccessToken,
  removeAccessToken,
  setAccessToken,
} from "./tokenStorage";

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({
  children,
}: AuthProviderProps): React.JSX.Element {
  const [accessToken, setAccessTokenState] = useState<string | null>(
    getAccessToken,
  );
  const [sessionInvalidated, setSessionInvalidated] = useState(false);

  useEffect(() => {
    function syncAccessToken(event: Event): void {
      setAccessTokenState(getAccessToken());
      setSessionInvalidated(
        event instanceof CustomEvent &&
          event.detail?.reason === "session-invalidated",
      );
    }

    window.addEventListener(AUTH_CHANGED_EVENT, syncAccessToken);
    window.addEventListener("storage", syncAccessToken);

    return () => {
      window.removeEventListener(AUTH_CHANGED_EVENT, syncAccessToken);
      window.removeEventListener("storage", syncAccessToken);
    };
  }, []);

  async function login(credentials: LoginRequest): Promise<void> {
    const response = await authenticate(credentials);

    setAccessToken(response.access_token);
    setAccessTokenState(response.access_token);
  }

  function logout(): void {
    removeAccessToken();
    setAccessTokenState(null);
  }

  const value = useMemo(
    () => ({
      accessToken,
      isAuthenticated: accessToken !== null,
      sessionInvalidated,
      login,
      logout,
    }),
    [accessToken, sessionInvalidated],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
