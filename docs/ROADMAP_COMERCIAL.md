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

Status: Em desenvolvimento avançado

Objetivo:

Responder:

"Estou preparado para esta oportunidade?"

Implementado:

- Cadastro estruturado de vagas.
- Persistência de vagas associadas ao usuário autenticado.
- CRUD completo de oportunidades profissionais.
- Camada de modelo, schema, repositório, serviço e API.
- Controle de acesso por usuário autenticado.
- Extração inicial de requisitos técnicos da vaga.
- Comparação entre requisitos da vaga e perfil profissional existente.
- Cálculo de score de compatibilidade.
- Identificação de requisitos atendidos.
- Identificação de gaps profissionais.
- Recomendações de evolução profissional.
- Testes automatizados das camadas implementadas.

Qualidade e segurança:

- Validação automatizada com Ruff.
- Cobertura de testes automatizados.
- Auditoria de dependências com pip-audit.
- Migração de autenticação JWT de python-jose para PyJWT.
- Remoção de dependências transitivas vulneráveis/desnecessárias.

Próximo:

- Refinar algoritmo de compatibilidade.
- Melhorar análise semântica de requisitos.
- Preparar integração futura com IA assistida.

---

#### Fase 3 — IA Assistida

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

#### Fase 4 — Interface MVP

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

#### Fase 5 — Validação Comercial

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
