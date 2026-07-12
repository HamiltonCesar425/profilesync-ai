# ProfileSync AI — Roadmap Comercial (MVP)

## Objetivo

Transformar o ProfileSync AI de uma plataforma técnica de
gestão profissional em um produto comercial capaz de gerar
valor mensurável para usuários reais.

A métrica principal deste roadmap é:

"Esta funcionalidade aumenta a chance de alguém pagar pelo produto?"

---

### Estado atual do produto

### Fundação concluída

- API FastAPI estruturada em camadas.
- Autenticação JWT.
- Gestão de usuários.
- Gestão de perfis profissionais.
- Gestão de currículos.
- Gestão de experiências.
- Gestão de projetos.
- Gestão de tecnologias.
- Exportação ATS-friendly.
- Validação ATS.
- Testes automatizados.
- Segurança e qualidade automatizada.

O produto possui base técnica suficiente para iniciar a transição
para MVP comercial.

---

#### Fase 1 concluída — Profile Intelligence Engine

- Diagnóstico profissional estruturado.
- Score de maturidade profissional.
- Identificação de forças.
- Identificação de gaps técnicos.
- Análise de compatibilidade com objetivo de carreira.
- Recomendações priorizadas por impacto.
- Exposição da análise via API autenticada.
- Proteção por autenticação JWT.
- Integração com perfis profissionais do usuário.
- Testes automatizados.

Validação:

- Ruff aprovado.
- Testes automatizados aprovados.
- Cobertura mantida acima de 98%.
- Auditoria de segurança sem vulnerabilidades conhecidas.

---

#### Fase 2 — Comparação Perfil × Vaga

Status: Concluído

Objetivo:

Responder:

"Estou preparado para esta oportunidade?"

Implementado:

- Cadastro estruturado de vagas profissionais.
- Persistência de vagas associadas ao usuário autenticado.
- CRUD completo de oportunidades profissionais.
- Camada de modelo, schema, repositório, serviço e API.
- Controle de acesso e isolamento de dados por usuário autenticado.
- Extração automática de requisitos técnicos a partir da descrição da vaga.
- Career Intelligence Engine para análise de compatibilidade.
- API autenticada de análise profissional.
- Endpoint de análise manual:
  - POST /career-intelligence/analyze
- Endpoint de análise baseada em vaga cadastrada:
  - POST /career-intelligence/jobs/{job_id}/analyze
- Comparação entre requisitos da vaga e competências profissionais.
- Cálculo de score de compatibilidade.
- Identificação de competências alinhadas.
- Identificação de gaps profissionais.
- Recomendações priorizadas de evolução profissional.
- Proteção contra acesso a análises de vagas pertencentes a outros usuários.
- Testes automatizados das camadas implementadas.

---

#### Fase 3 — Career Action Plan Engine

Status: Concluído

Objetivo:

Responder:

"O que devo fazer para conquistar esta oportunidade?"

Implementado:

- CareerActionPlanService.
- Geração automática de planos de ação personalizados.
- Priorização das ações por impacto.
- Recomendações organizadas em etapas.
- Definição de prazos sugeridos.
- Integração ao Career Intelligence Engine.
- Exposição do plano de ação via API autenticada.
- Contratos específicos para resposta do plano de ação.
- Testes automatizados das novas regras de negócio.

Resultado:

O ProfileSync AI passa a orientar o usuário sobre quais competências desenvolver e em qual ordem, transformando a análise de compatibilidade em um plano prático de evolução profissional.

---

#### Fase 4 — IA Assistida

Objetivo:

Utilizar IA como camada de melhoria, não como fonte única.

Fluxo:

Dados estruturados
→ Regras internas
→ IA
→ Sugestão
→ Aprovação do usuário

Funcionalidades:

- Melhorar descrições profissionais.
- Otimizar currículo.
- Gerar versões específicas por vaga.

Status:

Planejado.

---

#### Fase 5 — Interface MVP

Objetivo:

Disponibilizar fluxo completo para usuário real.

Fluxo mínimo:

1. Criar conta.
2. Criar perfil.
3. Definir objetivo profissional.
4. Receber diagnóstico.
5. Gerar currículo otimizado.

Status:

Planejado.

---

#### Fase 6 — Validação Comercial

Objetivo:

Validar mercado antes de expandir.

Critérios:

- Primeiros usuários reais.
- Feedback coletado.
- Ajustes baseados em uso.
- Definição de modelo de cobrança.

---

##### Fora do MVP inicial

As seguintes funcionalidades ficam adiadas:

- Integrações automáticas externas.
- LinkedIn automático.
- Aplicativo mobile.
- Dashboards avançados.
- Recursos corporativos.
- Customizações complexas.

---

##### Qualidade e Segurança

- Validação automatizada com Ruff.
- Suíte completa de testes automatizados.
- 188 testes aprovados.
- Configuração centralizada de pytest na raiz do projeto.
- Cobertura automatizada acima do requisito mínimo definido.
- Auditoria de dependências com pip-audit.
- Migração da autenticação JWT de python-jose para PyJWT.
- Remoção de dependências transitivas vulneráveis e desnecessárias.
