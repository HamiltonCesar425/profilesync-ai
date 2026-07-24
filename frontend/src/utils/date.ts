export function formatDate(dateValue: string | null): string {
  if (!dateValue) {
    return "";
  }

  const [year, month, day] = dateValue.split("-").map(Number);

  if (!year || !month || !day) {
    return dateValue;
  }

  const date = new Date(year, month - 1, day);

  return new Intl.DateTimeFormat("pt-BR").format(date);
}
