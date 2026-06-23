# ProfileSync AI — Project Charter

## Visão do produto

O ProfileSync AI organiza a identidade profissional de pessoas desenvolvedoras e permite manter perfis e currículos versionados, com exportação manual em Markdown. A aplicação prioriza controle do usuário, dados sob sua posse e integrações futuras sem publicação automática.

## Escopo implementado

- Cadastro e autenticação de usuários com JWT.
- CRUD de perfis profissionais vinculados ao usuário autenticado.
- CRUD de currículos vinculados a um perfil do próprio usuário.
- Currículo estruturado por título, cargo-alvo, conteúdo livre e versão.
- Exportação autenticada em Markdown ATS-friendly.
- Persistência local com SQLite, SQLAlchemy e testes automatizados.

## Fora do escopo atual

- CRUD de projetos, tecnologias, experiências, entregas e skills.
- Geração de conteúdo por IA ou recomendações automáticas.
- Publicação automática em LinkedIn, GitHub ou plataformas de vagas.
- Exportação PDF, cache, observabilidade e integração com serviços externos.
- Migração para PostgreSQL.

## Princípios

- Autorização por usuário em todo dado profissional.
- Contratos HTTP explícitos e validados por Pydantic.
- Revisão humana antes de qualquer uso externo do material produzido.
- Separação entre API, serviço, repositório e persistência.
- Evolução incremental, com testes como rede de segurança.

## Stack atual

- Backend: Python, FastAPI, Pydantic, SQLAlchemy e PyJWT.
- Dados: SQLite local.
- Qualidade: Pytest e cobertura mínima configurada de 80%.

## Direção de evolução

O produto poderá expandir o contexto profissional com projetos e experiências, gerar materiais com IA, oferecer PDF e integrar plataformas externas somente com aprovação explícita do usuário.
