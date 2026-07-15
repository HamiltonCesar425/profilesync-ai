# ProfileSync AI — Roadmap Comercial (MVP)

## Objetivo

Transformar o ProfileSync AI de uma plataforma técnica de
gestão profissional em um produto comercial capaz de gerar
valor mensurável para usuários reais.

A métrica principal deste roadmap é:

"Esta funcionalidade aumenta a chance de alguém pagar pelo produto?"

---

### Fundação da Plataforma

Concluído

- API FastAPI em arquitetura em camadas.
- Autenticação JWT.
- Gestão de usuários.
- Gestão de perfis.
- Gestão de currículos.
- Gestão de experiências.
- Gestão de projetos.
- Gestão de tecnologias.
- Exportação ATS-friendly.
- Validação ATS.
- Testes automatizados.
- Segurança automatizada.

---

### Estado atual do produto

Fase 1 — Concluída
Fase 2 — Concluída
Fase 3 — Concluída
Fase 4 — Concluída
Fase 5 — Planejada

---

Evoluções Pós-MVP

• Career Identity Engine
• (futuras funcionalidades)

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

Status: Concluído

Objetivo

Utilizar Inteligência Artificial como uma camada de aprimoramento da plataforma, preservando as regras de negócio como fonte principal de decisão.

Fluxo adotado:

Dados estruturados

→ Regras de negócio

→ Inteligência Artificial

→ Sugestão

→ Aprovação do usuário

Implementado
Integração com a API oficial da OpenAI utilizando o SDK oficial.
Camada de integração desacoplada (OpenAIClient).
Configuração do modelo de IA via variáveis de ambiente.
Arquitetura preparada para substituição ou expansão de provedores de IA.
Serviço AIAssistantService responsável pela orquestração das funcionalidades assistidas.
Endpoint autenticado para melhoria de descrições profissionais:
POST /ai-assistant/improve-professional-description
Melhoria automática de descrições profissionais mantendo o contexto informado pelo usuário.
Contratos específicos para requisição e resposta da IA.
Tratamento de exceções de domínio para falhas de configuração, indisponibilidade do provedor e respostas inválidas.
Cobertura completa por testes automatizados.
Validação estática com Ruff.
Compatibilidade com a arquitetura em camadas adotada pelo projeto.
Resultado

A Inteligência Artificial passa a atuar como um mecanismo de refinamento de conteúdo, preservando o conhecimento estruturado do usuário como principal ativo da plataforma e mantendo a IA como uma camada complementar de geração de valor.

---

---

| Evolução Estratégica — Career Identity Engine

| Status: Planejado (Pós-MVP)

Objetivo

Evoluir o mecanismo atual de comparação Perfil × Vaga para um modelo capaz de identificar e explicar a identidade profissional do usuário e da oportunidade analisada.

Funcionalidades previstas
Identificação automática da identidade profissional predominante da vaga.
Identificação automática da identidade profissional construída pelo usuário ao longo da carreira.
Explicação transparente dos fatores que geram aderência ou divergência entre ambos.
Recomendações de evolução profissional considerando contexto de carreira e não apenas competências técnicas.
Apoio à transição de carreira baseado em trajetória profissional.
Valor para o usuário

Responder perguntas como:

"Qual identidade profissional construí ao longo da minha carreira?"
"Esta vaga realmente representa minha especialização?"
"Por que minha experiência não transmite o posicionamento profissional que desejo?"
"Quais mudanças devo realizar para migrar para outra especialização?"
Justificativa comercial

Enquanto a maioria das plataformas compara apenas tecnologias ou palavras-chave, o ProfileSync AI evoluirá para comparar identidades profissionais, tornando a análise mais contextualizada, explicável e útil para decisões de carreira.

Essa funcionalidade reforça o posicionamento do produto como uma plataforma de inteligência profissional, ampliando seu diferencial competitivo.

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
