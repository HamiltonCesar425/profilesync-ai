import { httpClient } from "./httpClient";

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface RegisterResponse {
  id: number;
  email: string;
  created_at: string;
}

export async function login(credentials: LoginRequest): Promise<LoginResponse> {
  const formData = new URLSearchParams();

  formData.append("username", credentials.email);
  formData.append("password", credentials.password);

  const response = await httpClient.post<LoginResponse>(
    "/auth/login",
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    },
  );

  return response.data;
}

export async function register(
  userData: RegisterRequest,
): Promise<RegisterResponse> {
  const response = await httpClient.post<RegisterResponse>(
    "/auth/register",
    userData,
  );

  return response.data;
}
