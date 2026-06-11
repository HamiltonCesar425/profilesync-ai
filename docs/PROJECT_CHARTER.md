# ProfileSync AI — Project Charter

## 1. Visão Geral

O ProfileSync AI é uma plataforma para gestão e geração assistida de perfil profissional Dev.

O sistema tem como objetivo centralizar projetos, tecnologias, experiências práticas e evolução técnica do usuário, permitindo gerar materiais profissionais com apoio de IA, incluindo:

- Currículo Dev
- Resumos profissionais
- Biografia para LinkedIn
- Descrição de projetos
- Textos para plataformas de vagas
- Posicionamento técnico profissional

A plataforma deve priorizar controle manual do usuário, transparência e conformidade, evitando automações agressivas em plataformas externas.

---

## 2. Objetivo do Produto

Transformar histórico técnico e evolução prática em materiais profissionais organizados, atualizados e reutilizáveis.

A aplicação deverá funcionar como um hub pessoal de evolução profissional Dev.

---

## 3. Problema que o Produto Resolve

Profissionais de tecnologia frequentemente enfrentam:

- Currículos desatualizados
- Informações dispersas
- Dificuldade em traduzir experiência técnica em posicionamento profissional
- Retrabalho para atualizar múltiplas plataformas
- Falta de organização da evolução técnica

O ProfileSync AI busca reduzir esse problema através de gestão estruturada e geração assistida de conteúdo profissional.

---

## 4. Escopo Inicial (MVP)

### Funcionalidades da v1.0

- Cadastro de projetos
- Cadastro de tecnologias utilizadas
- Registro de entregas técnicas
- Registro de aprendizados
- Geração de resumo profissional
- Geração de descrição para currículo
- Geração de descrição para GitHub
- Exportação em Markdown

---

## 5. Fora do Escopo Inicial

A versão inicial NÃO deverá incluir:

- Publicação automática em LinkedIn
- Publicação automática em plataformas de vagas
- Scraping agressivo
- Automação de login externo
- Coleta invasiva de dados

---

## 6. Stack Tecnológica Inicial

### Backend

- Python
- FastAPI
- Pydantic

### Frontend

- React
- JavaScript

### Banco de Dados

- PostgreSQL

### Infraestrutura

- Docker
- GitHub
- Render
- Vercel

### Testes

- Pytest
- Playwright (futuro)

### Observabilidade (futuro)

- Prometheus
- Grafana
- OpenTelemetry

---

## 7. Arquitetura Inicial

A aplicação seguirá inicialmente arquitetura separada:

Frontend React
↓
API FastAPI
↓
PostgreSQL

O sistema deverá ser preparado para evolução futura em observabilidade, cache e integração com APIs externas.

---

## 8. Princípios Técnicos

- Código limpo e manutenível
- PEP8
- Separação de responsabilidades
- Contratos explícitos
- Versionamento contínuo
- Testabilidade
- Observabilidade progressiva
- Evolução incremental

---

## 9. Princípios Éticos

- Transparência no uso de IA
- Aprovação manual antes de publicação
- Respeito aos termos de uso das plataformas
- Proteção de dados profissionais do usuário
- Evitar automações abusivas

---

## 10. Objetivos de Evolução Técnica

O projeto deverá servir também como plataforma prática de evolução profissional nas áreas:

- Backend
- Frontend
- Banco de Dados
- Cloud
- Observabilidade
- Segurança
- Integração
- Produto

---

## 11. Roadmap Inicial

### Fase 1

- Estrutura inicial do projeto
- Modelagem de entidades
- API inicial
- CRUD de projetos

### Fase 2

- Geração de currículo
- Geração de resumo profissional
- Templates reutilizáveis

### Fase 3

- Exportação PDF
- Histórico de versões
- Melhorias de UX

### Fase 4

- Observabilidade
- Cache
- Integrações externas controladas
- Inteligência contextual

---

## 12. Visão de Longo Prazo

O ProfileSync AI deverá evoluir para uma plataforma inteligente de gestão de identidade profissional Dev, permitindo acompanhar evolução técnica, consolidar experiência prática e auxiliar no posicionamento profissional de forma estruturada e ética.
