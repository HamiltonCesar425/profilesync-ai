import { createContext } from "react";

import type { LoginRequest } from "../api/auth";

export interface AuthContextValue {
    accessToken: string | null;
    isAuthenticated: boolean;
    login: (credentials: LoginRequest) => Promise<void>;
    logout: () => void;
}

export const AuthContext = createContext<AuthContextValue | undefined>(
    undefined,
);