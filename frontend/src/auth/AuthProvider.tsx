import { type ReactNode, useMemo, useState } from "react";

import { login as authenticate, type LoginRequest } from "../api/auth";

import { AuthContext } from "./AuthContext";
import { getAccessToken, removeAccessToken, setAccessToken } from "./storage";

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({
  children,
}: AuthProviderProps): React.JSX.Element {
  const [accessToken, setAccessTokenState] = useState<string | null>(
    getAccessToken,
  );

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
      login,
      logout,
    }),
    [accessToken],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
