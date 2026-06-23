# ProfileSync AI — Arquitetura e Contratos Vigentes

## Visão geral

O ProfileSync AI é uma API REST para gerenciar usuários, perfis profissionais e versões de currículos. A API autentica usuários com JWT e permite exportar currículos em Markdown compatível com ATS.

```text
Cliente HTTP / Frontend → Bearer JWT → API FastAPI → Serviços → Repositórios → SQLAlchemy → SQLite
```

O banco local atual é SQLite em `backend/data/profilesync.db`. PostgreSQL é uma evolução planejada, não um requisito da implementação atual.

## Componentes implementados

| Componente | Responsabilidade |
| --- | --- |
| `api/v1` | Rotas HTTP para autenticação, perfis, currículos e exportação. |
| `schemas` | Contratos Pydantic de entrada e saída. |
| `services` | Regras de negócio e autorização por usuário. |
| `repositories` | Persistência com SQLAlchemy. |
| `models` | Tabelas `users`, `profiles` e `resumes`. |
| `exporters` | Renderização de currículos em Markdown. |
| `core` | Configuração, JWT, segurança e logging. |

## Modelo de dados atual

### User

| Campo | Tipo | Observação |
| --- | --- | --- |
| `id` | inteiro | Identificador do usuário. |
| `email` | string | Único; usado como identidade no JWT. |
| `hashed_password` | string | Interno; nunca retornado pela API. |
| `created_at` | datetime | Gerado na criação. |

### Profile

Um perfil pertence a um usuário e pode possuir vários currículos.

| Campo | Tipo | Regra |
| --- | --- | --- |
| `id`, `user_id` | inteiro | Gerados/retornados pela API. |
| `full_name` | string | 3–120 caracteres. |
| `professional_title` | string | 3–120 caracteres. |
| `summary` | string | 20–1000 caracteres. |
| `location` | string ou `null` | Máximo de 120 caracteres. |
| `linkedin_url`, `github_url` | string ou `null` | Máximo de 255 caracteres. |

### Resume

Um currículo pertence simultaneamente ao usuário autenticado e a um perfil desse usuário.

| Campo | Tipo | Regra |
| --- | --- | --- |
| `id`, `user_id`, `profile_id` | inteiro | IDs são retornados; `profile_id` é exigido na criação. |
| `title` | string | 2–120 caracteres. |
| `target_role` | string | 2–120 caracteres. |
| `content` | string | Mínimo de 10 caracteres; corpo livre do currículo. |
| `version` | inteiro | Mínimo 1; padrão `1`. |
| `created_at`, `updated_at` | datetime | Gerados pelo servidor. |

Os campos legados por seção (`experience`, `skills`, `education` etc.) não fazem parte do contrato da API atual. O conteúdo do currículo é armazenado em `content`.

## Autenticação

As rotas de perfis, currículos e exportação exigem `Authorization: Bearer <access_token>`.

| Método | Rota | Contrato |
| --- | --- | --- |
| `POST` | `/auth/register` | JSON: `email` válido e `password` com ao menos 8 caracteres. Retorna usuário e `201`. |
| `POST` | `/auth/login` | `application/x-www-form-urlencoded`: use o e-mail em `username` e a senha em `password`. Retorna `{ "access_token", "token_type": "bearer" }`. |

O Swagger usa OAuth2 Password Flow para `/auth/login`.

## Contratos HTTP

### Perfis

| Método | Rota | Resultado |
| --- | --- | --- |
| `POST` | `/profiles` | Cria um perfil do usuário autenticado. |
| `GET` | `/profiles` | Lista os perfis do usuário autenticado. |
| `GET` | `/profiles/{profile_id}` | Retorna um perfil pertencente ao usuário. |
| `PUT` | `/profiles/{profile_id}` | Atualização completa do perfil. |
| `DELETE` | `/profiles/{profile_id}` | Remove o perfil e seus currículos; responde `204`. |

```json
{
  "full_name": "Ana Souza",
  "professional_title": "Desenvolvedora Backend",
  "summary": "Desenvolvedora Python com experiência em APIs, bancos de dados e testes automatizados.",
  "location": "São Paulo, SP",
  "linkedin_url": "https://linkedin.com/in/ana-souza",
  "github_url": "https://github.com/ana-souza"
}
```

### Currículos

| Método | Rota | Resultado |
| --- | --- | --- |
| `POST` | `/resumes` | Cria um currículo para um perfil do usuário; responde `201`. |
| `GET` | `/resumes/profile/{profile_id}` | Lista os currículos do perfil. |
| `GET` | `/resumes/{resume_id}/profile/{profile_id}` | Retorna um currículo. |
| `PUT` | `/resumes/{resume_id}/profile/{profile_id}` | Atualização parcial: todos os campos são opcionais. |
| `DELETE` | `/resumes/{resume_id}/profile/{profile_id}` | Remove o currículo; responde `204`. |

```json
{
  "profile_id": 1,
  "title": "Currículo — Ana Souza",
  "target_role": "Desenvolvedora Backend Python",
  "content": "Desenvolvedora com experiência em FastAPI, SQLAlchemy e testes automatizados.",
  "version": 1
}
```

### Exportação

| Método | Rota | Resultado |
| --- | --- | --- |
| `GET` | `/exports/resumes/{resume_id}/markdown` | Retorna o currículo do usuário em `text/markdown`. |

O Markdown inclui título, cargo-alvo, conteúdo e versão. A exportação valida a posse do currículo pelo usuário autenticado; não requer `profile_id` na URL.

## Respostas de erro

- Falha de validação do FastAPI/Pydantic: `422`.
- Credenciais ausentes, inválidas ou expiradas: `401` com `WWW-Authenticate: Bearer`.
- Recurso inexistente ou não pertencente ao usuário: `404`.
- E-mail já cadastrado: `400`.

## Segurança e qualidade

- Senhas são persistidas somente em formato hash.
- A autorização é aplicada antes de acessar perfis, currículos e exportações.
- O projeto possui testes automatizados com `pytest` e requisito mínimo de 80% de cobertura.

## Evoluções planejadas

Ainda não fazem parte do contrato vigente: CRUD de projetos, tecnologias, experiências e skills; geração por IA; exportação PDF; PostgreSQL; integrações com GitHub ou plataformas de vagas; cache, métricas e rastreamento distribuído.
