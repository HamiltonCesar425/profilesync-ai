import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { type ReactElement } from "react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import App from "../src/App";
import { listJobs } from "../src/api/jobs";
import { listProfessionalExperiences } from "../src/api/professionalExperiences";
import { listProfiles } from "../src/api/profiles";
import { getProjectsByProfile } from "../src/api/projects";
import { AuthProvider } from "../src/auth/AuthProvider";
import { CompareJobPage } from "../src/pages/CompareJobPage";
import { ProfessionalExperiencesPage } from "../src/pages/ProfessionalExperiencesPage";
import { ProfilePage } from "../src/pages/ProfilePage";
import { ProjectsPage } from "../src/pages/ProjectsPage";
import { TechnologiesPage } from "../src/pages/TechnologiesPage";

vi.mock("../src/api/careerIntelligence", () => ({
  analyzeRegisteredJob: vi.fn(),
  getDetectedCompetencies: vi.fn(),
}));

vi.mock("../src/api/jobs", () => ({
  createJob: vi.fn(),
  listJobs: vi.fn(),
}));

vi.mock("../src/api/professionalExperiences", () => ({
  createProfessionalExperience: vi.fn(),
  deleteProfessionalExperience: vi.fn(),
  listProfessionalExperiences: vi.fn(),
  updateProfessionalExperience: vi.fn(),
}));

vi.mock("../src/api/profiles", () => ({
  createProfile: vi.fn(),
  listProfiles: vi.fn(),
  updateProfile: vi.fn(),
}));

vi.mock("../src/api/projects", () => ({
  createProject: vi.fn(),
  deleteProject: vi.fn(),
  getProjectsByProfile: vi.fn(),
  updateProject: vi.fn(),
}));

vi.mock("../src/api/targetedResumes", () => ({
  generateTargetedResumePreview: vi.fn(),
}));

vi.mock("../src/api/technologies", () => ({
  createTechnology: vi.fn(),
  deleteTechnology: vi.fn(),
  listProfileTechnologies: vi.fn(),
  updateTechnology: vi.fn(),
}));

interface Deferred<T> {
  promise: Promise<T>;
  resolve: (value: T) => void;
}

const PROFILE = {
  id: 1,
  user_id: 1,
  full_name: "Perfil 1",
  professional_title: "Engenheira de software",
  summary: "Resumo profissional",
  location: null,
  linkedin_url: null,
  github_url: null,
};

function deferred<T>(): Deferred<T> {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((promiseResolve) => {
    resolve = promiseResolve;
  });

  return { promise, resolve };
}

function renderInternalPage(path: string, page: ReactElement): void {
  render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path={path} element={page} />
        <Route path="/" element={<h1>Dashboard alcançado</h1>} />
      </Routes>
    </MemoryRouter>,
  );
}

function getDashboardBackLink(): HTMLAnchorElement {
  const link = screen.getByRole("link", { name: "Voltar ao Dashboard" });
  expect(link.getAttribute("href")).toBe("/");
  return link as HTMLAnchorElement;
}

function navigateToDashboard(): void {
  fireEvent.click(getDashboardBackLink());
  expect(
    screen.getByRole("heading", { name: "Dashboard alcançado" }),
  ).toBeTruthy();
}

beforeEach(() => {
  sessionStorage.clear();
  vi.resetAllMocks();
});

afterEach(() => {
  cleanup();
  sessionStorage.clear();
});

describe("DashboardBackLink on authenticated internal pages", () => {
  it("is available while Profile is loading and navigates from its loaded state", async () => {
    const profilesRequest = deferred<[]>();
    vi.mocked(listProfiles).mockReturnValue(profilesRequest.promise);
    renderInternalPage("/profile", <ProfilePage />);

    expect(screen.getByRole("status").textContent).toBe("Carregando perfil...");
    getDashboardBackLink();

    await act(async () => {
      profilesRequest.resolve([]);
      await profilesRequest.promise;
    });
    await screen.findByRole("heading", { name: "Criar perfil" });
    navigateToDashboard();
  });

  it("is available while Experiences is loading and in its empty state", async () => {
    const profilesRequest = deferred<[]>();
    vi.mocked(listProfiles).mockReturnValue(profilesRequest.promise);
    renderInternalPage("/experiences", <ProfessionalExperiencesPage />);

    expect(screen.getByText("Carregando perfis...")).toBeTruthy();
    getDashboardBackLink();

    await act(async () => {
      profilesRequest.resolve([]);
      await profilesRequest.promise;
    });
    await screen.findByRole("heading", { name: "Experiências profissionais" });
    navigateToDashboard();
  });

  it("is available in the regular Experiences state", async () => {
    vi.mocked(listProfiles).mockResolvedValue([PROFILE]);
    vi.mocked(listProfessionalExperiences).mockResolvedValue([]);
    renderInternalPage("/experiences", <ProfessionalExperiencesPage />);

    await screen.findByRole("button", { name: "Nova experiência" });
    getDashboardBackLink();
  });

  it("is available while Projects is loading and in its empty state", async () => {
    const profilesRequest = deferred<[]>();
    vi.mocked(listProfiles).mockReturnValue(profilesRequest.promise);
    renderInternalPage("/projects", <ProjectsPage />);

    expect(screen.getByText("Carregando perfis...")).toBeTruthy();
    getDashboardBackLink();

    await act(async () => {
      profilesRequest.resolve([]);
      await profilesRequest.promise;
    });
    await screen.findByRole("heading", { name: "Projetos" });
    navigateToDashboard();
  });

  it("is available in the regular Projects state", async () => {
    vi.mocked(listProfiles).mockResolvedValue([PROFILE]);
    vi.mocked(getProjectsByProfile).mockResolvedValue([]);
    renderInternalPage("/projects", <ProjectsPage />);

    await screen.findByRole("button", { name: "Novo projeto" });
    getDashboardBackLink();
  });

  it("is available while Technologies is loading and navigates from its empty state", async () => {
    const profilesRequest = deferred<[]>();
    vi.mocked(listProfiles).mockReturnValue(profilesRequest.promise);
    renderInternalPage("/technologies", <TechnologiesPage />);

    getDashboardBackLink();

    await act(async () => {
      profilesRequest.resolve([]);
      await profilesRequest.promise;
    });
    await screen.findByRole("heading", { name: "Perfil necessário" });
    navigateToDashboard();
  });

  it("is available while Compare Job is loading and navigates from its empty state", async () => {
    const jobsRequest = deferred<[]>();
    const profilesRequest = deferred<[]>();
    vi.mocked(listJobs).mockReturnValue(jobsRequest.promise);
    vi.mocked(listProfiles).mockReturnValue(profilesRequest.promise);
    renderInternalPage("/compare-job", <CompareJobPage />);

    expect(screen.getByText("Carregando vagas...")).toBeTruthy();
    getDashboardBackLink();

    await act(async () => {
      jobsRequest.resolve([]);
      profilesRequest.resolve([]);
      await Promise.all([jobsRequest.promise, profilesRequest.promise]);
    });
    await screen.findByRole("heading", { name: "Nenhuma vaga cadastrada" });
    navigateToDashboard();
  });
});

describe("authenticated route protection", () => {
  it.each([
    "/profile",
    "/experiences",
    "/projects",
    "/technologies",
    "/compare-job",
  ])("redirects an unauthenticated visit to %s to login", async (path) => {
    render(
      <MemoryRouter initialEntries={[path]}>
        <AuthProvider>
          <App />
        </AuthProvider>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "Entrar" })).toBeTruthy();
    });
  });
});
