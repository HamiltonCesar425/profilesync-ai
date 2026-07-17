import { type SubmitEvent, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "../auth/useAuth";

interface LoginLocationState {
  from?: {
    pathname: string;
  };
}
export function LoginPage() {
  const { login } = useAuth();

  const navigate = useNavigate();
  const location = useLocation();

  const locationState = location.state as LoginLocationState | null;
  const destination = locationState?.from?.pathname ?? "/";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();

    setErrorMessage(null);
    setIsSubmitting(true);

    try {
      await login({ email, password });

      navigate(destination, { replace: true });
    } catch {
      setErrorMessage("Não foi possível realizar o login.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main>
      <h1>Entrar</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">E-mail</label>
          <input
            id="email"
            type="email"
            value={email}
            autoComplete="email"
            required
            onChange={(event) => setEmail(event.target.value)}
          />
        </div>

        <div>
          <label htmlFor="password">Senha</label>
          <input
            id="password"
            type="password"
            value={password}
            autoComplete="current-password"
            required
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>

        {errorMessage && <p role="alert">{errorMessage}</p>}

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </main>
  );
}
