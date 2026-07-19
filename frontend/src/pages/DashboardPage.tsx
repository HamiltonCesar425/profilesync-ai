import { useAuth } from "../auth/useAuth";
import { ActionPlanCard } from "../components/dashboard/ActionPlanCard";
import { DashboardHeader } from "../components/dashboard/DashboardHeader";
import { ProfileScoreCard } from "../components/dashboard/ProfileScoreCard";
import { ProfileSummaryCard } from "../components/dashboard/ProfileSummaryCard";
import { QuickActions } from "../components/dashboard/QuickActions";
import { RecommendationsCard } from "../components/dashboard/RecommendationsCard";

export function DashboardPage(): React.JSX.Element {
  const { logout } = useAuth();

  return (
    <main>
      <DashboardHeader onLogout={logout} />

      <ProfileSummaryCard
        completionPercentage={0}
        experiencesCount={0}
        projectsCount={0}
        technologiesCount={0}
      />

      <ProfileScoreCard score={0} />

      <RecommendationsCard
        recommendations={[
          "Complete seu perfil profissional.",
          "Adicione projetos relevantes.",
          "Inclua tecnologias recentes.",
        ]}
      />

      <ActionPlanCard
        actions={[
          "Cadastrar uma experiência profissional recente.",
          "Adicionar um projeto com tecnologias relevantes.",
          "Revisar a descrição profissional.",
        ]}
      />

      <QuickActions />
    </main>
  );
}
