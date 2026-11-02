import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import {
  analyzeRegisteredJob,
  getDetectedCompetencies,
} from "../src/api/careerIntelligence";
import { createJob, listJobs } from "../src/api/jobs";
import { listProfiles } from "../src/api/profiles";
import { generateTargetedResumePreview } from "../src/api/targetedResumes";
import { CompareJobPage } from "../src/pages/CompareJobPage";
import type { TargetedResumePreviewResponse } from "../src/types/targetedResume";

const stateUpdateTracker = vi.hoisted(() => ({
  afterUnmount: false,
  calls: [] as unknown[],
}));

vi.mock("react", async (importOriginal) => {
  const actual = await importOriginal<typeof import("react")>();
  const useTrackedState = ((initialState: unknown) => {
    const [state, setState] = actual.useState<unknown>(initialState);
    const trackedSetState = (value: unknown): void => {
      if (stateUpdateTracker.afterUnmount) {
        stateUpdateTracker.calls.push(value);
      }

      setState(value);
    };

    return [state, trackedSetState];
  }) as typeof actual.useState;

  return { ...actual, useState: useTrackedState };
});

vi.mock("../src/api/careerIntelligence", () => ({
  analyzeRegisteredJob: vi.fn(),
  getDetectedCompetencies: vi.fn(),
}));

vi.mock("../src/api/jobs", () => ({
  createJob: vi.fn(),
  listJobs: vi.fn(),
}));

vi.mock("../src/api/profiles", () => ({
  listProfiles: vi.fn(),
}));

vi.mock("../src/api/targetedResumes", () => ({
  generateTargetedResumePreview: vi.fn(),
}));

interface Deferred<T> {
  promise: Promise<T>;
  resolve: (value: T) => void;
  reject: (reason?: unknown) => void;
}

function deferred<T>(): Deferred<T> {
  let resolve!: (value: T) => void;
  let reject!: (reason?: unknown) => void;
  const promise = new Promise<T>((promiseResolve, promiseReject) => {
    resolve = promiseResolve;
    reject = promiseReject;
  });

  return { promise, resolve, reject };
}

function preview(previewId: string, jobId: number): TargetedResumePreviewResponse {
  return {
    preview_id: previewId,
    state: "preview",
    composition: {
      profile_id: 1,
      job_id: jobId,
      ruleset_version: "test-ruleset",
      blocks: [],
      source_manifest: [],
    },
  };
}

async function renderReadyPage() {
  const rendered = render(
    <MemoryRouter initialEntries={["/compare-job"]}>
      <Routes>
        <Route path="/compare-job" element={<CompareJobPage />} />
        <Route path="/" element={<h1>Dashboard alcançado</h1>} />
      </Routes>
    </MemoryRouter>,
  );

  await waitFor(() => {
    const button = screen.getByRole("button", {
      name: "Visualizar prévia do currículo",
    }) as HTMLButtonElement;
    expect(button.disabled).toBe(false);
  });

  return rendered;
}

function startPreviewRequest(): void {
  fireEvent.click(
    screen.getByRole("button", {
      name: "Visualizar prévia do currículo",
    }),
  );
}

function selectJob(jobId: number): void {
  fireEvent.change(screen.getByLabelText("Vaga cadastrada"), {
    target: { value: String(jobId) },
  });
}

function expectPreviewRequest(callIndex: number, jobId: number): void {
  expect(generateTargetedResumePreview).toHaveBeenNthCalledWith(callIndex, {
    profile_id: 1,
    job_id: jobId,
  });
}

async function flushPromiseCallbacks(): Promise<void> {
  await Promise.resolve();
  await Promise.resolve();
}

beforeEach(() => {
  stateUpdateTracker.afterUnmount = false;
  stateUpdateTracker.calls = [];
  vi.resetAllMocks();

  vi.mocked(listJobs).mockResolvedValue([
    {
      id: 5,
      user_id: 1,
      title: "Vaga 5",
      company: null,
      description: "Descrição da vaga 5",
      created_at: "2026-01-01T00:00:00Z",
      updated_at: "2026-01-01T00:00:00Z",
    },
    {
      id: 1,
      user_id: 1,
      title: "Vaga 1",
      company: null,
      description: "Descrição da vaga 1",
      created_at: "2026-01-01T00:00:00Z",
      updated_at: "2026-01-01T00:00:00Z",
    },
  ]);
  vi.mocked(listProfiles).mockResolvedValue([
    {
      id: 1,
      user_id: 1,
      full_name: "Perfil 1",
      professional_title: "Engenheira de software",
      summary: "Resumo factual",
      location: null,
      linkedin_url: null,
      github_url: null,
    },
  ]);
  vi.mocked(getDetectedCompetencies).mockResolvedValue({
    competencies: ["TypeScript"],
  });
  vi.mocked(createJob).mockRejectedValue(new Error("not used"));
  vi.mocked(analyzeRegisteredJob).mockRejectedValue(new Error("not used"));
});

afterEach(() => {
  stateUpdateTracker.afterUnmount = false;
  cleanup();
});

describe("CompareJobPage asynchronous preview robustness", () => {
  it("R-002 ignores a stale successful response after the job changes", async () => {
    const requestA = deferred<TargetedResumePreviewResponse>();
    vi.mocked(generateTargetedResumePreview).mockReturnValueOnce(requestA.promise);
    await renderReadyPage();

    startPreviewRequest();
    expect(screen.getByText("Gerando prévia factual do currículo...")).toBeTruthy();

    selectJob(1);
    expect(generateTargetedResumePreview).toHaveBeenCalledTimes(1);
    expectPreviewRequest(1, 5);
    expect(screen.queryByText("Gerando prévia factual do currículo...")).toBeNull();

    await act(async () => {
      requestA.resolve(preview("preview-obsoleto", 5));
      await requestA.promise;
    });

    expect(screen.queryByText("preview-obsoleto")).toBeNull();
    expect(screen.queryByRole("alert")).toBeNull();
    expect(screen.queryByText("Gerando prévia factual do currículo...")).toBeNull();
  });

  it("R-002 ignores a stale rejected response after the job changes", async () => {
    const requestA = deferred<TargetedResumePreviewResponse>();
    vi.mocked(generateTargetedResumePreview).mockReturnValueOnce(requestA.promise);
    await renderReadyPage();

    startPreviewRequest();
    selectJob(1);
    expect(generateTargetedResumePreview).toHaveBeenCalledTimes(1);
    expectPreviewRequest(1, 5);

    await act(async () => {
      requestA.reject(new Error("erro obsoleto"));
      await flushPromiseCallbacks();
    });

    expect(screen.queryByRole("alert")).toBeNull();
    expect(screen.queryByText("Gerando prévia factual do currículo...")).toBeNull();
    expect(
      screen.getByRole("button", { name: "Visualizar prévia do currículo" }),
    ).toBeTruthy();
  });

  it("R-003 keeps the newer response when B resolves before A", async () => {
    const requestA = deferred<TargetedResumePreviewResponse>();
    const requestB = deferred<TargetedResumePreviewResponse>();
    vi.mocked(generateTargetedResumePreview)
      .mockReturnValueOnce(requestA.promise)
      .mockReturnValueOnce(requestB.promise);
    await renderReadyPage();

    startPreviewRequest();
    selectJob(1);
    startPreviewRequest();
    expect(generateTargetedResumePreview).toHaveBeenCalledTimes(2);
    expectPreviewRequest(1, 5);
    expectPreviewRequest(2, 1);

    await act(async () => {
      requestB.resolve(preview("preview-B", 1));
      await requestB.promise;
    });
    expect(screen.getByText("preview-B")).toBeTruthy();

    await act(async () => {
      requestA.resolve(preview("preview-A", 5));
      await requestA.promise;
    });

    expect(screen.getByText("preview-B")).toBeTruthy();
    expect(screen.queryByText("preview-A")).toBeNull();
  });

  it("R-003 preserves B loading when stale A completes first", async () => {
    const requestA = deferred<TargetedResumePreviewResponse>();
    const requestB = deferred<TargetedResumePreviewResponse>();
    vi.mocked(generateTargetedResumePreview)
      .mockReturnValueOnce(requestA.promise)
      .mockReturnValueOnce(requestB.promise);
    await renderReadyPage();

    startPreviewRequest();
    selectJob(1);
    startPreviewRequest();
    expect(generateTargetedResumePreview).toHaveBeenCalledTimes(2);
    expectPreviewRequest(1, 5);
    expectPreviewRequest(2, 1);

    await act(async () => {
      requestA.resolve(preview("preview-A", 5));
      await requestA.promise;
    });

    expect(screen.getByText("Gerando prévia factual do currículo...")).toBeTruthy();
    expect(
      (
        screen.getByRole("button", {
          name: "Gerando prévia...",
        }) as HTMLButtonElement
      ).disabled,
    ).toBe(true);
    expect(screen.queryByText("preview-A")).toBeNull();

    await act(async () => {
      requestB.resolve(preview("preview-B", 1));
      await requestB.promise;
    });

    expect(screen.getByText("preview-B")).toBeTruthy();
    expect(screen.queryByText("Gerando prévia factual do currículo...")).toBeNull();
  });

  it("R-004 executes no state update when the request resolves after unmount", async () => {
    const requestA = deferred<TargetedResumePreviewResponse>();
    vi.mocked(generateTargetedResumePreview).mockReturnValueOnce(requestA.promise);
    const rendered = await renderReadyPage();

    startPreviewRequest();
    rendered.unmount();
    stateUpdateTracker.afterUnmount = true;

    await act(async () => {
      requestA.resolve(preview("preview-after-unmount", 5));
      await requestA.promise;
    });

    expect(stateUpdateTracker.calls).toEqual([]);
  });

  it("R-004 executes no state update when the request rejects after unmount", async () => {
    const requestA = deferred<TargetedResumePreviewResponse>();
    vi.mocked(generateTargetedResumePreview).mockReturnValueOnce(requestA.promise);
    const rendered = await renderReadyPage();

    startPreviewRequest();
    rendered.unmount();
    stateUpdateTracker.afterUnmount = true;

    await act(async () => {
      requestA.reject(new Error("erro após desmontagem"));
      await flushPromiseCallbacks();
    });

    expect(stateUpdateTracker.calls).toEqual([]);
  });

  it("navigates safely to the Dashboard while a preview request is pending", async () => {
    const requestA = deferred<TargetedResumePreviewResponse>();
    vi.mocked(generateTargetedResumePreview).mockReturnValueOnce(requestA.promise);
    await renderReadyPage();

    startPreviewRequest();
    fireEvent.click(
      screen.getByRole("link", { name: "Voltar ao Dashboard" }),
    );
    expect(
      screen.getByRole("heading", { name: "Dashboard alcançado" }),
    ).toBeTruthy();
    stateUpdateTracker.afterUnmount = true;

    await act(async () => {
      requestA.resolve(preview("preview-after-navigation", 5));
      await requestA.promise;
    });

    expect(stateUpdateTracker.calls).toEqual([]);
  });
});
