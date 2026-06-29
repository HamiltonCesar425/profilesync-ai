# ProfileSync AI — Roadmap

## Concluído — Fundação da API

- Estrutura FastAPI com camadas de rotas, schemas, serviços, repositórios e modelos.
- Persistência SQLite com SQLAlchemy.
- Logging básico e tratamento de erros de domínio.
- Testes automatizados com requisito mínimo de cobertura.
- Pipeline local de qualidade com Ruff e Pytest.

## Concluído — Identidade e controle de acesso

- Registro de usuários.
- Autenticação JWT.
- Login via contrato JSON documentado no Swagger/OpenAPI.
- Proteção de rotas autenticadas.
- Controle de posse de recursos por usuário.

## Concluído — Perfis profissionais

- CRUD autenticado de perfis profissionais.
- Relacionamento entre usuário e perfil profissional.
- Listagem de perfis por usuário autenticado.
- Validação de acesso para impedir leitura, alteração ou exclusão de perfis de terceiros.

## Concluído — Currículos

- CRUD autenticado de currículos por perfil.
- Relacionamento entre currículo, perfil e usuário proprietário.
- Controle de acesso para impedir manipulação de currículos pertencentes a outros usuários.
- Estrutura base para versionamento e evolução futura dos currículos.

## Concluído — Exportação de currículos

- Exportação de currículo em Markdown ATS-friendly.
- Exportação de currículo em PDF.
- Exportação de currículo em DOCX.
- Serviço de exportação desacoplado por formato.
- Testes automatizados para exportadores e rotas de exportação.

## Concluído — Validação ATS

- Estrutura extensível de regras ATS.
- Serviço de validação ATS.
- Cálculo de score ATS.
- Schemas específicos para resposta de validação ATS.
- Endpoint autenticado para validação ATS de currículo.
- Testes unitários para regras ATS.
- Testes de serviço para cálculo e resposta de validação.
- Testes de rota para validação ATS autenticada.

## Concluído — Modelo profissional estruturado (Fase 1)

- Modelagem da entidade Technology.
- CRUD autenticado de tecnologias por perfil.
- Controle de acesso por usuário.
- Camadas Model, Repository, Service e API implementadas.
- Cobertura completa por testes automatizados.

## Concluído — Modelo profissional estruturado (Fase 2)

- Modelagem de entidade Project.
- Relacionamento entre projetos, perfil e tecnologias.
- CRUD autenticado de projetos por perfil.
- Controle de acesso por usuário.
- Camadas Model, Repository, Service e API.
- Testes automatizados para repository, service e API.

## Próxima etapa — Geração e revisão de conteúdo

- Templates reutilizáveis de currículo e resumo profissional.
- Geração assistida por IA com transparência sobre origem e uso dos dados.
- Fluxo de revisão manual antes de qualquer uso externo.
- Histórico de versões de conteúdo profissional.
- Separação entre versões ATS-friendly e versões visuais/humanizadas.

## Evoluções posteriores

- Otimização ATS por palavras-chave de vaga.
- Comparação entre currículo e descrição de vaga.
- Sugestões de melhoria baseadas em lacunas de conteúdo.
- Histórico de exportações e otimizações.
- Migração para PostgreSQL.
- Migrations com Alembic.
- Frontend React integrado à API.
- Docker e docker-compose para ambiente de desenvolvimento.
- Deploy backend/frontend.
- Variáveis de ambiente por ambiente.
- Observabilidade com métricas, tracing e dashboards.
- Cache e integrações externas controladas.
- Matching de vagas e recomendações de posicionamento.

## Princípio de segurança e controle do usuário

Nenhuma integração futura deverá publicar, enviar, alterar ou distribuir conteúdo em serviços externos sem aprovação explícita do usuário.
