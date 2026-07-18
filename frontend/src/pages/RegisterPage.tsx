import { isAxiosError } from "axios";
import { type SubmitEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { register } from "../api/auth";

interface ApiErrorResponse {
  detail?: string;
}

export function RegisterPage(): React.JSX.Element {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirmation, setPasswordConfirmation] = useState("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(
    event: SubmitEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    setErrorMessage(null);

    if (password.length < 8) {
      setErrorMessage("A senha deve possuir pelo menos 8 caracteres.");
      return;
    }

    if (password !== passwordConfirmation) {
      setErrorMessage("A confirmação da senha não corresponde à senha.");
      return;
    }

    setIsSubmitting(true);

    try {
      await register({ email, password });

      navigate("/login", {
        replace: true,
        state: {
          registrationSucceeded: true,
        },
      });
    } catch (error: unknown) {
      if (isAxiosError<ApiErrorResponse>(error)) {
        const apiMessage = error.response?.data?.detail;

        setErrorMessage(
          apiMessage ?? "Não foi possível criar a conta neste momento.",
        );
      } else {
        setErrorMessage("Não foi possível criar a conta neste momento.");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main>
      <h1>Criar conta</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="register-email">E-mail</label>
          <input
            id="register-email"
            type="email"
            value={email}
            autoComplete="email"
            required
            onChange={(event) => setEmail(event.target.value)}
          />
        </div>

        <div>
          <label htmlFor="register-password">Senha</label>
          <input
            id="register-password"
            type="password"
            value={password}
            autoComplete="new-password"
            minLength={8}
            required
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>

        <div>
          <label htmlFor="register-password-confirmation">
            Confirmar senha
          </label>
          <input
            id="register-password-confirmation"
            type="password"
            value={passwordConfirmation}
            autoComplete="new-password"
            minLength={8}
            required
            onChange={(event) => setPasswordConfirmation(event.target.value)}
          />
        </div>

        {errorMessage && <p role="alert">{errorMessage}</p>}

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Criando conta..." : "Criar conta"}
        </button>
      </form>

      <p>
        Já possui conta? <Link to="/login">Entrar</Link>
      </p>
    </main>
  );
}
