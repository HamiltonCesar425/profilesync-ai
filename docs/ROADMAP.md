# ProfileSync AI — Roadmap

## Concluído — Fundação da API

- Estrutura FastAPI com camadas de rotas, schemas, serviços, repositórios e modelos.
- Persistência SQLite com SQLAlchemy.
- Logging básico e tratamento de erros de domínio.
- Testes automatizados com requisito de cobertura.

## Concluído — Identidade e currículos

- Registro e autenticação JWT.
- CRUD autenticado de perfis profissionais.
- CRUD autenticado de currículos por perfil.
- Controle de posse de perfis e currículos por usuário.
- Exportação de currículo em Markdown ATS-friendly.
- Exportação de currículo em PDF.
- Exportação de currículo em DOCX.

## Próxima etapa — Experiência profissional estruturada

- Modelar projetos, tecnologias, experiências/entregas e skills.
- Relacionar esses dados ao perfil do usuário.
- Criar contratos, CRUDs e testes para as novas entidades.
- Definir como esse contexto alimentará o campo `content` dos currículos.

## Próxima etapa — Geração e revisão de conteúdo

- Templates reutilizáveis de currículo e resumo profissional.
- Geração assistida por IA com transparência sobre origem e uso dos dados.
- Fluxo de revisão manual e histórico de versões.

## Evoluções posteriores

- Score ATS e otimização por palavras-chave.
- Histórico de exportações e otimizações.
- Migração para PostgreSQL e migrations.
- Frontend React integrado à API.
- Docker, deploy e variáveis de ambiente por ambiente.
- Observabilidade: métricas, tracing e dashboards.
- Cache e integrações externas controladas.
- Matching de vagas e recomendações de posicionamento.

Nenhuma integração futura deverá publicar conteúdo em serviços externos sem aprovação explícita do usuário.
