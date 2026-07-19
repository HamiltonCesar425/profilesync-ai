interface ActionPlanCardProps {
  actions: string[];
}

export function ActionPlanCard({
  actions,
}: ActionPlanCardProps): React.JSX.Element {
  return (
    <section aria-labelledby="action-plan-title">
      <h2 id="action-plan-title">Plano de ação</h2>

      {actions.length === 0 ? (
        <p>Nenhuma ação recomendada no momento.</p>
      ) : (
        <ol>
          {actions.map((action) => (
            <li key={action}>{action}</li>
          ))}
        </ol>
      )}
    </section>
  );
}
