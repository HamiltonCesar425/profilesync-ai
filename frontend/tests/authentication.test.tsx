import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import {
  AxiosError,
  AxiosHeaders,
  type InternalAxiosRequestConfig,
} from "axios";
import { MemoryRouter, Route, Routes, useLocation } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { login as authenticate } from "../src/api/auth";
import { httpClient } from "../src/api/httpClient";
import { AuthProvider } from "../src/auth/AuthProvider";
import { ProtectedRoute } from "../src/auth/ProtectedRoute";
import {
  AUTH_CHANGED_EVENT,
  getAccessToken,
  removeAccessToken,
  setAccessToken,
} from "../src/auth/tokenStorage";
import { LoginPage } from "../src/pages/LoginPage";

vi.mock("../src/api/auth", () => ({
  login: vi.fn(),
}));

const SESSION_INVALID_MESSAGE =
  "Sua sessão não é mais válida. Entre novamente para continuar.";

interface Deferred<T> {
  promise: Promise<T>;
  resolve: (value: T) => void;
}

function deferred<T>(): Deferred<T> {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((promiseResolve) => {
    resolve = promiseResolve;
  });

  return { promise, resolve };
}

function unauthorizedError(
  config: InternalAxiosRequestConfig,
): AxiosError {
  return new AxiosError(
    "Unauthorized",
    "ERR_BAD_REQUEST",
    config,
    undefined,
    {
      config,
      data: {},
      headers: new AxiosHeaders(),
      status: 401,
      statusText: "Unauthorized",
    },
  );
}

async function rejectWithUnauthorized(
  config: InternalAxiosRequestConfig,
): Promise<never> {
  throw unauthorizedError(config);
}

function controlledUnauthorizedAdapter() {
  const started = deferred<InternalAxiosRequestConfig>();
  const release = deferred<void>();

  return {
    adapter: async (config: InternalAxiosRequestConfig): Promise<never> => {
      started.resolve(config);
      await release.promise;
      throw unauthorizedError(config);
    },
    release,
    started,
  };
}

function observeAuthChanges(): {
  listener: ReturnType<typeof vi.fn>;
  stop: () => void;
} {
  const listener = vi.fn();
  window.addEventListener(AUTH_CHANGED_EVENT, listener);

  return {
    listener,
    stop: () => window.removeEventListener(AUTH_CHANGED_EVENT, listener),
  };
}

function ProtectedProbe(): React.JSX.Element {
  const location = useLocation();
  const currentLocation = `${location.pathname}${location.search}${location.hash}`;

  return (
    <main>
      <p>Local atual: {currentLocation}</p>
      <button
        type="button"
        onClick={() =>
          void httpClient
            .get("/test-authentication", { adapter: rejectWithUnauthorized })
            .catch(() => undefined)
        }
      >
        Simular resposta 401
      </button>
    </main>
  );
}

function renderAuthenticationFlow(initialEntry: string): void {
  render(
    <MemoryRouter initialEntries={[initialEntry]}>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/protected" element={<ProtectedProbe />} />
          </Route>
        </Routes>
      </AuthProvider>
    </MemoryRouter>,
  );
}

async function invalidateAuthenticatedSession(): Promise<void> {
  await act(async () => {
    fireEvent.click(
      screen.getByRole("button", { name: "Simular resposta 401" }),
    );
  });

  const alert = await screen.findByRole("alert");
  expect(alert.textContent).toBe(SESSION_INVALID_MESSAGE);
}

beforeEach(() => {
  sessionStorage.clear();
  vi.resetAllMocks();
});

afterEach(() => {
  cleanup();
  sessionStorage.clear();
});

describe("authentication session invalidation", () => {
  it("removes the token and explains a 401 received after authentication", async () => {
    setAccessToken("existing-session-token");
    renderAuthenticationFlow("/protected");

    await invalidateAuthenticatedSession();

    expect(getAccessToken()).toBeNull();
    expect(screen.getByText(SESSION_INVALID_MESSAGE)).toBeTruthy();
  });

  it("does not show an invalid-session message on an initial login visit", () => {
    renderAuthenticationFlow("/login");

    expect(screen.queryByText(SESSION_INVALID_MESSAGE)).toBeNull();
  });

  it("returns to pathname, search, and hash after authenticating again", async () => {
    setAccessToken("existing-session-token");
    renderAuthenticationFlow("/protected?mode=preview#details");
    await invalidateAuthenticatedSession();
    vi.mocked(authenticate).mockResolvedValue({
      access_token: "replacement-session-token",
      token_type: "bearer",
    });

    fireEvent.change(screen.getByLabelText("E-mail"), {
      target: { value: "user@example.com" },
    });
    fireEvent.change(screen.getByLabelText("Senha"), {
      target: { value: "strong-password" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Entrar" }));

    await waitFor(() => {
      expect(
        screen.getByText("Local atual: /protected?mode=preview#details"),
      ).toBeTruthy();
    });
    expect(authenticate).toHaveBeenCalledWith({
      email: "user@example.com",
      password: "strong-password",
    });
    expect(getAccessToken()).toBe("replacement-session-token");
  });
});

describe("401 token generation concurrency", () => {
  it("invalidates the session when the failed request used the current token", async () => {
    setAccessToken("token-A");
    const controlled = controlledUnauthorizedAdapter();
    const request = httpClient
      .get("/current-token", { adapter: controlled.adapter })
      .catch((error: unknown) => error);
    const requestConfig = await controlled.started.promise;
    expect(requestConfig.headers.get("Authorization")).toBe("Bearer token-A");
    const events = observeAuthChanges();

    controlled.release.resolve(undefined);
    await request;

    expect(getAccessToken()).toBeNull();
    expect(events.listener).toHaveBeenCalledTimes(1);
    const sessionInvalidatedEvent = events.listener.mock.calls[0]?.[0];
    expect(sessionInvalidatedEvent).toBeInstanceOf(CustomEvent);
    if (!(sessionInvalidatedEvent instanceof CustomEvent)) {
      throw new TypeError("Expected an authentication CustomEvent");
    }
    expect(sessionInvalidatedEvent.detail).toEqual({
      reason: "session-invalidated",
    });
    events.stop();
  });

  it("preserves a newer token when an older request returns 401", async () => {
    setAccessToken("token-A");
    const controlled = controlledUnauthorizedAdapter();
    const request = httpClient
      .get("/stale-token", { adapter: controlled.adapter })
      .catch((error: unknown) => error);
    const requestConfig = await controlled.started.promise;
    expect(requestConfig.headers.get("Authorization")).toBe("Bearer token-A");
    setAccessToken("token-B");
    const events = observeAuthChanges();

    controlled.release.resolve(undefined);
    await request;

    expect(getAccessToken()).toBe("token-B");
    expect(events.listener).not.toHaveBeenCalled();
    events.stop();
  });

  it("does not invalidate again after the session was voluntarily closed", async () => {
    setAccessToken("token-A");
    const controlled = controlledUnauthorizedAdapter();
    const request = httpClient
      .get("/logged-out-session", { adapter: controlled.adapter })
      .catch((error: unknown) => error);
    await controlled.started.promise;
    removeAccessToken();
    const events = observeAuthChanges();

    controlled.release.resolve(undefined);
    await request;

    expect(getAccessToken()).toBeNull();
    expect(events.listener).not.toHaveBeenCalled();
    events.stop();
  });

  it("preserves a current token after a 401 from an unauthenticated request", async () => {
    const controlled = controlledUnauthorizedAdapter();
    const request = httpClient
      .get("/unauthenticated-request", { adapter: controlled.adapter })
      .catch((error: unknown) => error);
    const requestConfig = await controlled.started.promise;
    expect(requestConfig.headers.get("Authorization")).toBeUndefined();
    setAccessToken("token-B");
    const events = observeAuthChanges();

    controlled.release.resolve(undefined);
    await request;

    expect(getAccessToken()).toBe("token-B");
    expect(events.listener).not.toHaveBeenCalled();
    events.stop();
  });
});
