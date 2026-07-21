import { useEffect, useState } from "react";

import { type DashboardData, getDashboardData } from "../api/dashboard";
import { useAuth } from "../auth/useAuth";
import { ActionPlanCard } from "../components/dashboard/ActionPlanCard";
import { DashboardHeader } from "../components/dashboard/DashboardHeader";
import { ProfileScoreCard } from "../components/dashboard/ProfileScoreCard";
import { ProfileSummaryCard } from "../components/dashboard/ProfileSummaryCard";
import { QuickActions } from "../components/dashboard/QuickActions";
import { RecommendationsCard } from "../components/dashboard/RecommendationsCard";

export function DashboardPage() {
  const { logout } = useAuth();

  const [dashboardData, setDashboardData] = useState<DashboardData | null>(
    null,
  );
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadDashboard(): Promise<void> {
      try {
        setIsLoading(true);
        setErrorMessage(null);

        const data = await getDashboardData();

        if (isMounted) {
          setDashboardData(data);
        }
      } catch {
        if (isMounted) {
          setErrorMessage("Não foi possível carregar os dados do dashboard.");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    void loadDashboard();

    return () => {
      isMounted = false;
    };
  }, []);

  if (isLoading) {
    return (
      <main>
        <DashboardHeader onLogout={logout} />

        <p role="status">Carregando dashboard...</p>
      </main>
    );
  }

  if (errorMessage !== null) {
    return (
      <main>
        <DashboardHeader onLogout={logout} />

        <p role="alert">{errorMessage}</p>
      </main>
    );
  }

  if (dashboardData === null) {
    return null;
  }

  return (
    <main>
      <DashboardHeader onLogout={logout} />

      <ProfileSummaryCard
        completionPercentage={dashboardData.profileSummary.completionPercentage}
        experiencesCount={dashboardData.profileSummary.experiencesCount}
        projectsCount={dashboardData.profileSummary.projectsCount}
        technologiesCount={dashboardData.profileSummary.technologiesCount}
      />

      <ProfileScoreCard score={dashboardData.profileScore} />

      <RecommendationsCard recommendations={dashboardData.recommendations} />

      <ActionPlanCard actions={dashboardData.actions} />

      <QuickActions />
    </main>
  );
}
