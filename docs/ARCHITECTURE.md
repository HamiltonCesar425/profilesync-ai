# ProfileSync AI — Architecture

## 1. Visão Arquitetural

O ProfileSync AI será desenvolvido como uma aplicação web full stack, com separação clara entre frontend, backend e banco de dados.

A arquitetura inicial seguirá o modelo:

```text
Frontend React
↓
API FastAPI
↓
Camada de Serviços
↓
Camada de Repositórios
↓
PostgreSQL
```

O objetivo é manter uma estrutura simples, testável e preparada para evolução futura.

---

## 2. Componentes Principais

### Frontend

Responsável pela interface do usuário.

Principais responsabilidades:

* Exibir dashboard profissional
* Permitir cadastro de projetos
* Permitir cadastro de tecnologias
* Permitir registro de entregas técnicas
* Exibir conteúdos gerados
* Permitir revisão manual antes de exportação

Tecnologia inicial:

* React
* JavaScript
* React Router

---

### Backend

Responsável pela regra de negócio, APIs e integração entre frontend, banco de dados e camada de geração assistida.

Principais responsabilidades:

* Expor endpoints REST
* Validar dados de entrada
* Aplicar regras de negócio
* Persistir informações
* Gerar conteúdos profissionais
* Preparar integração futura com IA

Tecnologia inicial:

* Python
* FastAPI
* Pydantic
* SQLAlchemy

---

### Banco de Dados

Responsável pela persistência das informações profissionais do usuário.

Tecnologia inicial:

* PostgreSQL

Entidades iniciais previstas:

* ProfessionalProfile
* Project
* Technology
* Experience
* Skill
* GeneratedContent

---

## 3. Separação de Camadas do Backend

A estrutura inicial do backend deverá seguir separação por responsabilidade:

```text
backend/
└── src/
    ├── main.py
    ├── core/
    ├── api/
    ├── schemas/
    ├── models/
    ├── services/
    ├── repositories/
    └── database/
```

### core/

Configurações centrais da aplicação.

Responsabilidades:

* Variáveis de ambiente
* Configuração da aplicação
* Logging
* Constantes globais

---

### api/

Camada de rotas HTTP.

Responsabilidades:

* Definir endpoints
* Receber requisições
* Retornar respostas
* Encaminhar chamadas para services

---

### schemas/

Contratos de entrada e saída da API.

Responsabilidades:

* Validar payloads
* Definir DTOs
* Padronizar respostas

---

### models/

Modelos de banco de dados.

Responsabilidades:

* Representar tabelas
* Definir colunas
* Definir relacionamentos

---

### services/

Camada de regra de negócio.

Responsabilidades:

* Orquestrar casos de uso
* Aplicar validações de domínio
* Preparar dados para geração de conteúdo
* Coordenar chamadas entre repositories e geradores

---

### repositories/

Camada de acesso a dados.

Responsabilidades:

* Consultar banco
* Criar registros
* Atualizar registros
* Remover registros
* Isolar SQLAlchemy da regra de negócio

---

### database/

Configuração de persistência.

Responsabilidades:

* Criar engine
* Gerenciar sessões
* Configurar conexão com PostgreSQL

---

## 4. Fluxo Principal da Aplicação

Fluxo esperado da versão inicial:

```text
Usuário cadastra perfil profissional
↓
Usuário cadastra projetos
↓
Usuário associa tecnologias aos projetos
↓
Usuário registra entregas técnicas
↓
Backend organiza os dados
↓
Camada de geração cria conteúdo profissional
↓
Usuário revisa o conteúdo
↓
Sistema exporta em Markdown
```

---

## 5. Entidades Iniciais

### ProfessionalProfile

Representa o perfil profissional base do usuário.

Campos previstos:

* id
* name
* title
* location
* summary
* github_url
* linkedin_url
* created_at
* updated_at

---

### Project

Representa um projeto profissional ou de portfólio.

Campos previstos:

* id
* name
* description
* objective
* status
* repository_url
* deploy_url
* created_at
* updated_at

---

### Technology

Representa uma tecnologia usada nos projetos.

Campos previstos:

* id
* name
* category
* created_at

Categorias possíveis:

* Backend
* Frontend
* Database
* Cloud
* Observability
* Security
* Integration
* Product
* Data/AI

---

### Experience

Representa uma entrega, aprendizado ou marco técnico.

Campos previstos:

* id
* project_id
* title
* description
* impact
* date
* created_at

---

### Skill

Representa uma competência profissional consolidada.

Campos previstos:

* id
* name
* category
* level
* evidence
* created_at

---

### GeneratedContent

Representa um conteúdo profissional gerado pela aplicação.

Campos previstos:

* id
* content_type
* title
* content
* source_context
* created_at
* updated_at

Tipos possíveis:

* CV
* LinkedIn Bio
* GitHub Project Description
* Job Platform Summary
* Technical Summary

---

## 6. Princípios Arquiteturais

A arquitetura deverá seguir os seguintes princípios:

* Separação clara de responsabilidades
* Baixo acoplamento entre camadas
* Código simples antes de código sofisticado
* Contratos explícitos com Pydantic
* Regras de negócio fora das rotas
* Acesso ao banco isolado em repositories
* Evolução incremental
* Testabilidade desde o início
* Segurança e conformidade como preocupação transversal

---

## 7. Segurança e Conformidade

Desde a primeira versão, o sistema deverá evitar:

* armazenamento desnecessário de dados sensíveis
* automação agressiva em plataformas externas
* publicação automática sem aprovação manual
* coleta invasiva de dados

Diretrizes iniciais:

* uso de variáveis de ambiente
* proteção de chaves e tokens
* `.env` fora do versionamento
* revisão manual antes de qualquer publicação externa
* transparência no uso de IA

---

## 8. Observabilidade Futura

A aplicação deverá ser preparada para evolução futura com:

* logging estruturado
* métricas Prometheus
* dashboards Grafana
* rastreamento OpenTelemetry
* monitoramento de latência
* monitoramento de erros

Esses recursos não fazem parte obrigatória da primeira versão, mas devem ser considerados na organização do backend.

---

## 9. Integrações Futuras

Integrações planejadas para fases posteriores:

* GitHub API
* Exportação PDF
* APIs de IA generativa
* Plataformas de vagas, com aprovação manual
* Serviços de autenticação
* Redis para cache
* OpenTelemetry para rastreamento

A primeira versão não deverá automatizar login ou publicação direta em plataformas externas.

---

## 10. Decisões Técnicas Iniciais

### Decisão 1 — FastAPI no backend

Motivo:

* alta produtividade
* tipagem com Pydantic
* boa documentação automática
* aderência ao histórico técnico do projeto

---

### Decisão 2 — React no frontend

Motivo:

* aderência ao portfólio atual
* boa aceitação no mercado
* facilidade para criação de interfaces modernas

---

### Decisão 3 — PostgreSQL como banco principal

Motivo:

* banco relacional robusto
* forte presença em ambientes profissionais
* boa compatibilidade com SQLAlchemy
* adequado para modelagem estruturada

---

### Decisão 4 — Publicação manual

Motivo:

* reduzir riscos de segurança
* respeitar termos de uso de plataformas externas
* manter controle humano sobre identidade profissional

---

## 11. Evolução Arquitetural Esperada

A arquitetura deverá evoluir gradualmente:

```text
MVP local
↓
API + banco
↓
Frontend integrado
↓
Exportação de conteúdo
↓
Deploy
↓
Testes automatizados
↓
Observabilidade
↓
Integrações externas controladas
↓
IA contextual
```

---

## 12. Status Atual

O projeto está em fase inicial de documentação, planejamento arquitetural e preparação do ambiente de desenvolvimento.
