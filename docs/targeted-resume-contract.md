# Targeted Resume Contract v1

## 1. Objetivo

Este documento define o contrato funcional e arquitetural para a geração de
currículos direcionados no ProfileSync AI.

O objetivo é garantir que um currículo direcionado a uma vaga seja produzido
exclusivamente a partir de informações profissionais persistidas, autorizadas
e rastreáveis do usuário.

A geração do currículo deve preservar a integridade factual dos dados de
origem. Nenhuma etapa de composição, análise de carreira, otimização ATS ou
futura assistência por inteligência artificial pode introduzir fatos
profissionais que não possuam suporte nos dados persistidos do usuário.

Este contrato estabelece as regras para a transição:

Profile + Professional Experiences + Projects + Technologies + Job
→ Career Analysis
→ Targeted Resume
→ ATS Validation
→ Export

## 2. Escopo

O contrato abrange:

- identificação das fontes factuais permitidas;
- utilização da vaga como contexto de direcionamento;
- utilização da Career Analysis para seleção e priorização de informações;
- composição determinística do currículo;
- rastreabilidade das fontes utilizadas;
- geração de preview antes da persistência definitiva;
- aprovação do currículo pelo usuário;
- persistência do currículo aprovado;
- integração posterior com a validação ATS existente;
- integração posterior com os mecanismos de exportação existentes;
- requisitos mínimos de usabilidade e acessibilidade do novo fluxo;
- preparação arquitetural para futura internacionalização.

Este contrato não redefine os domínios existentes de Profile,
Professional Experience, Project, Technology, Job, ATS ou Export, exceto
quando uma alteração for indispensável para garantir as invariantes aqui
definidas.

## 3. Princípios

### 3.1 Integridade factual

A fidelidade aos dados profissionais persistidos tem precedência sobre
otimização textual, score ATS, aderência à vaga ou qualquer recomendação
gerada pelo sistema.

Informações ausentes devem ser omitidas ou sinalizadas ao usuário, nunca
inferidas ou fabricadas.

### 3.2 Fonte de verdade

Os registros profissionais persistidos e autorizados do usuário constituem
a fonte de verdade para os fatos apresentados no currículo direcionado.

O conteúdo enviado pelo frontend não deve ser tratado como fonte de verdade
para fatos profissionais durante a geração do currículo direcionado.

### 3.3 Separação entre fato e análise

Career Analysis, gaps, recomendações, planos de ação e scores são informações
analíticas.

Essas informações podem orientar seleção, ordenação ou priorização de fatos
existentes, mas não podem ser convertidas em fatos profissionais do usuário.

### 3.4 Determinismo

A geração básica do currículo direcionado deve funcionar sem dependência de
modelos de inteligência artificial.

Para o mesmo conjunto relevante de dados de origem e regras de composição,
o sistema deve produzir resultado equivalente e verificável.

### 3.5 Rastreabilidade

Os fatos utilizados na composição devem possuir origem identificável nos
registros profissionais autorizados.

A rastreabilidade mínima adotada neste contrato é:

- `source_type`
- `source_id`

Não é exigida rastreabilidade por token, palavra ou sentença.

### 3.6 Aprovação explícita

Um currículo direcionado deve ser apresentado ao usuário para revisão antes
de ser considerado aprovado e disponibilizado para o fluxo definitivo de
ATS e exportação.

### 3.7 Evolução controlada

A arquitetura deve permitir evolução futura, incluindo assistência por IA e
internacionalização, sem tornar essas capacidades dependências obrigatórias
da geração básica definida neste contrato.

## 4. Definições

### 4.1 Fato profissional

Informação sobre o histórico, experiência, projeto, tecnologia ou atributo
profissional do usuário que possua suporte em uma fonte factual autorizada.

### 4.2 Fonte factual

Registro persistido pertencente ao usuário que pode fornecer informações
para o conteúdo factual do currículo direcionado.

### 4.3 Fonte contextual

Informação utilizada para orientar a seleção ou priorização de fatos, mas que
não comprova que determinado fato profissional pertence ao usuário.

A vaga (`Job`) é uma fonte contextual.

### 4.4 Fonte analítica

Resultado calculado pelo sistema a partir das fontes factuais e contextuais.

São exemplos:

- score de aderência;
- forças;
- gaps;
- recomendações;
- plano de ação;
- impactos estimados.

Fontes analíticas não constituem evidência factual sobre o histórico
profissional do usuário.

### 4.5 Currículo direcionado

Currículo composto para uma vaga específica a partir das fontes factuais
autorizadas do usuário, utilizando a vaga e a análise de carreira apenas
para orientar seleção, ordenação e priorização.

### 4.6 Proveniência

Identificação da origem de uma informação utilizada na composição do
currículo.

Neste contrato, a proveniência mínima é representada por
`source_type + source_id`.

### 4.7 Preview

Representação temporária do currículo direcionado apresentada ao usuário
antes de sua aprovação e persistência definitiva.

## 5. Entradas e fontes autorizadas

### 5.1 Entradas obrigatórias

A operação de geração de um currículo direcionado deve receber como entrada
mínima:

- `profile_id`
- `job_id`

O backend deve validar que o perfil e a vaga existem e pertencem ao usuário
autenticado antes de iniciar qualquer composição.

O frontend não deve fornecer o conteúdo factual final do currículo como
entrada da operação de geração.

### 5.2 Fontes factuais autorizadas

As seguintes entidades persistidas podem fornecer fatos profissionais para
a composição:

- `Profile`
- `ProfessionalExperience`
- `Project`
- `Technology`

Somente registros pertencentes ao perfil autorizado podem ser utilizados.

Cada registro utilizado deve conservar proveniência mínima por meio de:

- `source_type`
- `source_id`

### 5.3 Fonte contextual autorizada

`Job` é uma fonte contextual.

Os dados da vaga podem orientar:

- relevância;
- seleção;
- ordenação;
- priorização dos fatos profissionais existentes.

Os requisitos da vaga não constituem evidência de que o usuário possui
determinada competência, experiência, resultado ou qualificação.

### 5.4 Fontes analíticas permitidas

A `CareerAnalysis` e seus resultados derivados podem orientar a estratégia
de composição.

Podem ser utilizados para seleção e priorização:

- forças;
- gaps;
- recomendações;
- plano de ação;
- scores e impactos estimados.

Esses elementos não são fontes factuais e não podem, isoladamente, originar
conteúdo apresentado como fato profissional no currículo.

### 5.5 Fontes proibidas como evidência factual

Não podem ser utilizadas como evidência de fatos profissionais:

- requisitos existentes apenas na vaga;
- gaps identificados pela análise;
- recomendações;
- ações futuras;
- scores;
- impactos estimados;
- conteúdo inferido pelo sistema sem fonte persistida;
- conteúdo criado por modelo de IA sem correspondência factual verificável;
- conteúdo factual arbitrário enviado pelo frontend.

## 6. Invariantes de integridade factual

As invariantes desta seção são obrigatórias.

Uma implementação que viole qualquer uma delas não está em conformidade com
este contrato, mesmo que produza melhor score ATS, maior aderência textual à
vaga ou texto aparentemente mais completo.

### TR-INV-001 — Fato persistido como pré-condição

Nenhum fato profissional pode aparecer no currículo direcionado sem possuir
suporte em uma fonte factual autorizada, persistida e pertencente ao usuário.

**Regra:** no persisted fact → no resume fact.

### TR-INV-002 — Informação ausente não deve ser inferida

Quando uma informação profissional necessária ou desejável não possuir fonte
factual suficiente, ela deve ser omitida ou sinalizada ao usuário como
ausente.

O sistema não deve completar lacunas por suposição.

### TR-INV-003 — Requisito da vaga não é competência do usuário

Uma tecnologia, competência, qualificação ou experiência mencionada pela vaga
não pode ser atribuída ao usuário somente porque aparece nos requisitos da
vaga.

Se não houver suporte factual, o requisito pode permanecer como gap, mas não
pode aparecer no currículo como competência do usuário.

### TR-INV-004 — Gap não pode se tornar fato profissional

Gaps, recomendações e itens do plano de ação não podem ser convertidos em
experiências, competências, qualificações, resultados ou demais fatos do
currículo.

### TR-INV-005 — Proibição de fabricação de métricas e resultados

O sistema não pode criar números, percentuais, valores financeiros,
quantidades, métricas de desempenho, resultados ou impactos que não estejam
suportados pelas fontes factuais.

Scores e impactos calculados internamente pelo ProfileSync AI não representam
resultados profissionais do usuário.

### TR-INV-006 — Preservação de identidade factual

Transformações de texto podem melhorar organização, concisão e clareza, mas
não podem alterar:

- empresa;
- cargo;
- vínculo;
- período;
- projeto;
- tecnologia;
- nível de proficiência declarado;
- tempo de experiência declarado;
- resultado;
- métrica;
- responsabilidade;
- demais atributos factuais relevantes.

### TR-INV-007 — ATS subordinado à integridade factual

Nenhuma regra ou recomendação ATS pode justificar a introdução de informação
sem fonte factual.

Quando uma informação necessária para melhorar a avaliação ATS estiver
ausente, o sistema deve sinalizar a ausência em vez de fabricar conteúdo.

### TR-INV-008 — Proveniência obrigatória

Todo bloco factual incluído no currículo direcionado deve ser rastreável a
pelo menos uma fonte factual autorizada por meio de `source_type` e
`source_id`.

Uma composição que não consiga identificar a origem de determinado bloco
factual deve rejeitar esse bloco.

### TR-INV-009 — Autorização precede composição

Nenhuma fonte pode participar da composição antes da validação de propriedade
e autorização.

Registros pertencentes a outro usuário ou a outro perfil não podem ser
utilizados, ainda que seus identificadores sejam fornecidos pelo cliente.

### TR-INV-010 — Geração básica independente de IA

A geração básica do currículo direcionado deve funcionar integralmente sem
modelo de inteligência artificial.

A indisponibilidade de um provedor de IA não pode impedir a composição
determinística definida neste contrato.

### TR-INV-011 — IA não pode ampliar a verdade factual

Quando assistência por IA for futuramente habilitada, sua saída não poderá
introduzir novos fatos.

Toda saída assistida deverá ser validada antes de substituir ou complementar
conteúdo derivado deterministicamente.

Um prompt instruindo o modelo a não inventar informações não constitui, por
si só, mecanismo suficiente de validação factual.

### TR-INV-012 — Aprovação não autoriza alteração factual arbitrária

A aprovação de um preview não autoriza o frontend a substituir o conteúdo
factual por texto arbitrário.

O backend deve garantir que o currículo persistido corresponda ao resultado
aprovado produzido a partir das fontes autorizadas.

### TR-INV-013 — Integridade factual prevalece sobre completude

Um currículo factual incompleto é preferível a um currículo aparentemente
completo contendo informação sem suporte.

A ausência de dados deve ser tratada como informação a ser corrigida pelo
usuário na fonte apropriada, e não como autorização para inferência.

## 7. Regras de composição determinística

A composição determinística é responsável por transformar as fontes factuais
autorizadas em um currículo direcionado à vaga, preservando as invariantes
definidas neste contrato.

O compositor não é uma fonte de fatos. Sua responsabilidade é selecionar,
organizar e representar fatos já existentes.

### 7.1 Entradas da composição

A composição deve operar exclusivamente sobre dados previamente carregados,
autorizados e classificados de acordo com este contrato.

O conjunto relevante de entrada deve incluir:

- `Profile`;
- registros de `ProfessionalExperience` pertencentes ao perfil;
- registros de `Project` pertencentes ao perfil;
- registros de `Technology` pertencentes ao perfil;
- `Job` autorizado como fonte contextual;
- resultados da `CareerAnalysis`, quando utilizados exclusivamente para
  seleção, ordenação ou priorização.

O compositor não deve consultar ou incorporar fontes factuais arbitrárias
fornecidas diretamente pelo cliente.

### 7.2 Operações permitidas

O compositor pode realizar sobre os fatos autorizados:

- seleção;
- ordenação;
- agrupamento;
- priorização;
- omissão;
- formatação;
- normalização estrutural;
- resumo conservador;
- reescrita semanticamente equivalente.

Essas operações não podem alterar a identidade factual da informação de
origem.

### 7.3 Seleção orientada pela vaga

A vaga pode ser utilizada para determinar quais fatos profissionais existentes
são mais relevantes para o currículo direcionado.

Uma correspondência entre requisito da vaga e fato profissional existente
pode aumentar a prioridade desse fato.

A ausência de correspondência não autoriza a criação de um novo fato.

### 7.4 Ordenação e priorização

Fatos considerados mais relevantes para a vaga podem receber maior destaque
ou aparecer antes de fatos menos relevantes.

A priorização deve alterar apenas a apresentação do conteúdo, nunca sua
veracidade.

A Career Analysis pode contribuir para essa priorização, desde que seus
resultados não sejam apresentados como fatos profissionais.

### 7.5 Omissão

O compositor pode omitir informações:

- sem relevância suficiente para a vaga;
- redundantes;
- opcionais e ausentes;
- que não possuam suporte factual suficiente;
- que não possam ser representadas sem violar alguma invariante.

A omissão de um fato válido não autoriza sua substituição por informação
inferida ou fabricada.

### 7.6 Resumo conservador

Descrições extensas de experiências ou projetos podem ser resumidas quando
necessário para melhorar clareza, concisão ou adequação estrutural.

O resumo deve preservar o significado factual essencial da fonte.

O resumo não pode:

- adicionar responsabilidades;
- adicionar resultados;
- adicionar tecnologias;
- adicionar métricas;
- ampliar senioridade;
- transformar participação em liderança;
- transformar conhecimento declarado em experiência comprovada;
- transformar atividade planejada em atividade realizada.

Quando não for possível resumir uma informação com segurança, o conteúdo
original deve prevalecer ou a informação deve ser omitida.

### 7.7 Reescrita semanticamente equivalente

A redação de um fato pode ser ajustada para melhorar legibilidade,
consistência e objetividade.

A reescrita deve manter equivalência semântica com a informação de origem.

Uma reescrita não pode tornar uma afirmação:

- mais forte;
- mais específica;
- mais quantitativa;
- mais abrangente;
- mais conclusiva

do que a fonte factual permite sustentar.

### 7.8 Skills e tecnologias

Uma tecnologia ou competência somente pode ser apresentada como pertencente
ao usuário quando houver suporte em fonte factual autorizada.

A presença de uma tecnologia apenas na descrição da vaga não constitui
suporte suficiente.

Quando uma tecnologia possuir fonte factual válida e também for relevante
para a vaga, ela pode receber maior prioridade na composição.

A composição não deve elevar automaticamente nível de proficiência ou tempo
de experiência além do que estiver declarado nas fontes autorizadas.

### 7.9 Métricas e resultados

Métricas e resultados somente podem ser utilizados quando estiverem
suportados pelas fontes factuais.

O compositor não deve calcular, estimar ou extrapolar resultados profissionais
para melhorar impacto textual.

Valores derivados internamente pelo ProfileSync AI, como scores de aderência,
impactos estimados ou projeções, não podem ser apresentados como resultados
profissionais do usuário.

### 7.10 Informações ausentes

Quando uma seção ou informação desejável não possuir fonte factual, o
compositor deve omiti-la do conteúdo factual.

A ausência pode ser apresentada separadamente ao usuário como oportunidade de
completar o perfil, mas não deve ser preenchida automaticamente.

Essa regra também se aplica quando a ausência reduzir completude ou score ATS.

### 7.11 Estrutura independente do idioma

Os conceitos estruturais utilizados pelo compositor não devem depender de
rótulos textuais específicos da interface.

Identificadores internos de seções devem representar conceitos estáveis,
independentemente do idioma de apresentação.

Exemplos conceituais incluem:

- `SUMMARY`;
- `EXPERIENCE`;
- `PROJECTS`;
- `TECHNOLOGIES`;
- `EDUCATION`.

A existência de um identificador estrutural não autoriza a geração da
respectiva seção quando não houver fonte factual adequada.

A tradução ou localização dos rótulos de apresentação deve permanecer
separada das regras factuais de composição.

### 7.12 Resultado determinístico

Para o mesmo conjunto relevante de fontes autorizadas, contexto da vaga,
regras de composição e versão da composição, a geração básica deve produzir
resultado equivalente e verificável.

A composição básica não deve depender de:

- modelo de inteligência artificial;
- resposta probabilística externa;
- RAG;
- embeddings;
- banco vetorial;
- agentes.

Dependências futuras desse tipo devem permanecer opcionais e fora do caminho
necessário para a geração determinística.

### 7.13 Falha segura

Quando o compositor não conseguir determinar com segurança se determinada
informação pode ser utilizada sem violar este contrato, deve preferir:

1. não incluir a informação no conteúdo factual;
2. preservar evidência suficiente para diagnóstico;
3. sinalizar a situação para tratamento apropriado.

Incerteza não constitui autorização para inferência.

## 8. Proveniência e rastreabilidade

A composição de um currículo direcionado deve preservar evidência suficiente
para identificar quais fontes factuais autorizadas sustentam o conteúdo
produzido.

A proveniência faz parte da integridade do currículo direcionado e não deve
depender apenas do texto final apresentado ao usuário.

### 8.1 Manifesto de fontes

Cada currículo direcionado deve possuir um manifesto das fontes factuais
utilizadas em sua composição.

A representação mínima de uma referência de origem deve conter:

- `source_type`;
- `source_id`.

Exemplo conceitual:

```json
{
  "source_type": "professional_experience",
  "source_id": 12
}
```

### 8.2 Tipos de fonte permitidos

O manifesto de proveniência factual deve utilizar somente tipos de fonte explicitamente autorizados por este contrato.

Na versão atual, os tipos conceitualmente permitidos correspondem a:

- `profile`;
- `professional_experience`;
- `project`;
- `technology`.

A representação física desses tipos pode variar durante a implementação, desde que seja possível determinar de maneira inequívoca qual domínio factual originou a referência.

`Job`, `CareerAnalysis`, gaps, recomendações, planos de ação, scores e impactos estimados não devem ser registrados como fontes factuais do conteúdo profissional.

### 8.3 Validade de uma referência de proveniência

Uma referência de proveniência somente é válida quando a fonte correspondente:

1. existe;
2. está persistida;
3. pertence ao perfil autorizado;
4. pertence ao contexto do usuário autenticado;
5. corresponde a um tipo permitido como fonte factual;
6. pode sustentar o conteúdo factual ao qual foi associada.

A existência de um source_id válido não constitui, isoladamente, evidência suficiente de autorização ou suporte factual.

### 8.4 Proveniência dos blocos factuais

Todo bloco factual incluído no currículo direcionado deve possuir pelo menos uma referência válida de proveniência.

Quando um bloco depender de mais de uma fonte factual, o manifesto pode associá-lo a múltiplas referências.

A proveniência deve permitir responder, no mínimo:

Quais registros profissionais autorizados sustentam este conteúdo?

Um bloco factual cuja origem não possa ser demonstrada não deve integrar o currículo direcionado.

### 8.5 Proveniência após transformação

Operações de composição, resumo conservador, normalização ou reescrita semanticamente equivalente não criam uma nova fonte factual.

O conteúdo transformado deve permanecer associado às fontes factuais que sustentavam o conteúdo de origem.

A existência de uma referência válida não autoriza a transformação a introduzir informações que a fonte referenciada não sustenta.

Por exemplo, uma experiência profissional que demonstre atuação como desenvolvedor não pode sustentar uma afirmação de liderança apenas porque seu source_id foi corretamente associado ao bloco.

### 8.6 Granularidade da proveniência

A implementação deve manter proveniência em granularidade suficiente para identificar as fontes factuais que sustentam cada bloco factual relevante do currículo.

Para esta versão do contrato, rastreabilidade em nível de bloco é suficiente.

---

Não são requisitos:

- proveniência por token;
- proveniência por palavra;
- proveniência por fragmento textual;
- proveniência por sentença;
- claim graph;
- event sourcing para rastreamento factual.

Granularidade adicional pode ser introduzida futuramente quando existir necessidade demonstrada, sem reduzir as garantias mínimas aqui estabelecidas.

### 8.7 Persistência do manifesto

Quando um currículo direcionado for aprovado e persistido, seu manifesto de proveniência deve ser persistido de forma correspondente à mesma composição.

Conteúdo aprovado e manifesto não podem representar composições diferentes.

Uma alteração posterior no conteúdo que produza nova composição não deve reutilizar silenciosamente um manifesto antigo como se ele ainda representasse o novo resultado.

### 8.8 Alteração posterior das fontes

As fontes profissionais podem ser alteradas depois da aprovação de um currículo direcionado.

Essas alterações não devem modificar retroativamente a proveniência ou o conteúdo de uma versão anteriormente aprovada.

Uma nova composição deve utilizar o estado atual autorizado das fontes e produzir o manifesto correspondente ao novo resultado.

O manifesto de uma versão persistida representa as fontes utilizadas naquela composição, e não uma garantia de que essas fontes permanecerão imutáveis no futuro.

### 8.9 Proveniência do preview

O preview deve utilizar o mesmo modelo conceitual de proveniência exigido para o currículo direcionado persistido.

Durante a revisão, a composição candidata deve possuir informação suficiente para que o backend consiga verificar quais fontes sustentam seu conteúdo.

A aprovação não deve:

- introduzir novas fontes factuais arbitrariamente;
- substituir fontes autorizadas por referências fornecidas pelo cliente;
  -remover as verificações de proveniência aplicáveis.

Quando o preview aprovado for persistido, o manifesto deve corresponder às fontes da composição efetivamente aprovada.

### 8.10 Proveniência não substitui validação factual

Proveniência e validade factual são garantias relacionadas, mas distintas.

Uma referência tecnicamente válida não torna verdadeira qualquer afirmação associada a ela.

O sistema deve verificar não apenas que uma fonte existe e está autorizada, mas também que ela é capaz de sustentar o conteúdo factual correspondente.

---

Exemplo conceitual:

ProfessionalExperience #12:

Desenvolvedor Python

---

Afirmação:

Liderou uma equipe de 15 engenheiros Python

Proveniência:

professional_experience #12

---

A referência existe, mas não sustenta liderança, quantidade de profissionais ou qualquer outro detalhe não registrado na fonte.

Portanto, essa afirmação continua inválida.

---

### 8.11 Falha segura de proveniência

Quando o sistema não conseguir demonstrar proveniência factual válida e suficiente para determinado conteúdo, deve preferir:

- rejeitar o bloco;
- omitir o conteúdo factual;
- sinalizar a inconsistência para tratamento apropriado;

em vez de aceitar conteúdo cuja origem ou suporte factual não possa ser demonstrado.

Incerteza de proveniência não constitui autorização para inclusão.

## 9. Preview e aprovação

O currículo direcionado deve passar por uma etapa explícita de preview antes
de sua persistência definitiva.

O preview permite ao usuário revisar o resultado da composição sem transferir
ao frontend autoridade sobre os fatos profissionais ou sobre a integridade da
composição.

### 9.1 Geração do preview

A geração do preview deve receber como entradas mínimas:

- `profile_id`;
- `job_id`.

O backend deve:

1. autenticar o usuário;
2. autorizar o acesso ao perfil e à vaga;
3. carregar as fontes factuais autorizadas;
4. obter ou recalcular os dados analíticos necessários;
5. executar a composição determinística;
6. validar as invariantes factuais;
7. produzir o manifesto de proveniência;
8. retornar o resultado para revisão.

O frontend não deve enviar o conteúdo factual final que será utilizado para
construir o preview.

### 9.2 Natureza temporária do preview

O preview representa uma composição candidata e ainda não constitui o
currículo direcionado definitivamente aprovado.

Sua geração não deve, por si só, tornar o currículo disponível para o fluxo
definitivo de exportação.

O mecanismo utilizado para representar temporariamente o preview deve
permitir verificar sua identidade durante a aprovação.

### 9.3 Identidade do preview

Cada preview deve possuir uma identidade verificável capaz de distinguir uma
composição de outra.

A implementação pode utilizar mecanismo determinístico apropriado, como hash,
identificador de preview ou solução equivalente, desde que seja possível
detectar divergência entre o resultado apresentado e o resultado submetido à
aprovação.

Este contrato não exige uma tecnologia específica para essa finalidade.

### 9.4 Conteúdo apresentado para revisão

O preview deve apresentar ao usuário o currículo direcionado resultante da
composição.

A interface deve permitir distinguir claramente:

- conteúdo que será utilizado no currículo;
- informações ausentes relevantes, quando sinalizadas;
- gaps ou recomendações apresentados apenas como apoio à decisão;
- estados de validação ou erro.

Gaps, recomendações e demais informações analíticas exibidas durante a revisão
não passam a integrar o conteúdo factual do currículo por estarem visíveis no
mesmo fluxo.

### 9.5 Aprovação explícita

A persistência definitiva do currículo direcionado deve depender de uma ação
explícita de aprovação pelo usuário.

Visualizar o preview não constitui aprovação.

A aprovação deve identificar de maneira inequívoca qual preview está sendo
aprovado.

### 9.6 Dados aceitos na aprovação

A operação de aprovação não deve aceitar conteúdo factual arbitrário como
substituto do resultado produzido pelo backend.

O cliente deve enviar somente os identificadores e dados de controle
necessários para identificar a composição aprovada.

O backend permanece responsável por determinar o conteúdo factual que pode ser
persistido.

### 9.7 Revalidação antes da persistência

Antes de persistir o currículo aprovado, o backend deve confirmar que a
composição continua válida.

A implementação deve garantir que o conteúdo persistido corresponda ao
preview aprovado.

Caso a estratégia adotada seja recompor o currículo durante a aprovação, o
backend deve utilizar as fontes autorizadas e verificar a identidade ou
equivalência da composição resultante.

### 9.8 Alteração das fontes entre preview e aprovação

As fontes profissionais podem ser alteradas depois da geração de um preview.

Se uma alteração relevante modificar o resultado que seria produzido pela
composição, o backend não deve persistir silenciosamente um currículo
diferente daquele revisado pelo usuário.

Nesse caso, o preview anterior deve ser considerado inválido para aprovação,
e uma nova composição deve ser apresentada para revisão.

### 9.9 Divergência na aprovação

Quando o backend detectar divergência entre:

- preview aprovado;
- fontes atualmente autorizadas;
- resultado recomposto;
- manifesto de proveniência;

a operação deve falhar de forma segura.

O sistema deve solicitar uma nova geração de preview em vez de persistir
conteúdo cuja equivalência não possa ser demonstrada.

### 9.10 Persistência após aprovação

Somente após aprovação válida o currículo direcionado deve ser persistido como
resultado definitivo daquela composição.

A persistência deve manter, no mínimo, associação com:

- `profile_id`;
- `job_id`;
- conteúdo aprovado;
- manifesto de proveniência;
- versão necessária para distinguir a composição persistida.

Os detalhes físicos do modelo de persistência serão definidos durante a
implementação, desde que preservem as garantias deste contrato.

### 9.11 Edição posterior

Um currículo direcionado aprovado não deve permitir substituição arbitrária
de seu conteúdo factual por meio de uma operação genérica de atualização.

Alterações factuais devem ocorrer nas respectivas fontes profissionais e
originar nova composição.

Caso sejam futuramente permitidas edições textuais controladas no currículo,
elas deverão preservar equivalência factual, proveniência e todas as
invariantes deste contrato.

### 9.12 Relação com ATS e exportação

O fluxo definitivo de ATS e exportação deve operar sobre um currículo
direcionado validamente aprovado e persistido.

ATS ou exportação não devem constituir mecanismos alternativos para contornar
a etapa de aprovação.

A exportação deve utilizar a versão aprovada correspondente ao currículo
solicitado.

### 9.13 Requisitos mínimos de usabilidade e acessibilidade

O fluxo de preview e aprovação deve permitir que o usuário compreenda o estado
do currículo antes de aprová-lo.

A interface deve:

- identificar claramente a ação de aprovação;
- diferenciar preview de currículo definitivamente aprovado;
- apresentar erros e estados de validação de forma compreensível;
- não depender exclusivamente de cor para comunicar estado ou erro;
- utilizar elementos semanticamente adequados sempre que aplicável;
- permitir operação por teclado das ações essenciais do fluxo.

Esses requisitos representam o mínimo necessário para esta funcionalidade e
não substituem uma futura avaliação transversal de usabilidade e
acessibilidade do ProfileSync AI.

### 9.14 Falha segura

Falhas de autorização, identidade do preview, proveniência, recomposição,
validação factual ou equivalência devem impedir a persistência definitiva.

Na impossibilidade de demonstrar que o currículo persistido será equivalente
ao currículo aprovado, o sistema deve exigir nova revisão pelo usuário.

## 10. Persistência e versionamento

A persistência de um currículo direcionado deve preservar as garantias de
integridade factual, proveniência, aprovação e associação com a vaga
estabelecidas neste contrato.

Um currículo direcionado persistido representa o resultado aprovado de uma
composição específica e não apenas um documento textual associado ao perfil.

### 10.1 Identificação do currículo direcionado

O sistema deve ser capaz de distinguir um currículo direcionado sujeito a
este contrato de outras modalidades de currículo que possam existir na
aplicação.

Essa distinção não deve depender da interpretação do conteúdo textual.

A estratégia física utilizada para representar essa distinção será definida
durante a implementação.

### 10.2 Associação obrigatória

Um currículo direcionado persistido deve manter associação inequívoca com,
no mínimo:

- `profile_id`;
- `job_id`;
- conteúdo aprovado;
- manifesto de proveniência;
- versão da composição persistida.

A persistência deve permitir determinar para qual perfil e para qual vaga o
currículo foi produzido.

### 10.3 Conteúdo persistido

O conteúdo persistido deve corresponder ao resultado validamente aprovado pelo
usuário.

O backend não deve utilizar conteúdo factual arbitrário enviado pelo cliente
como substituto da composição aprovada.

O conteúdo persistido permanece sujeito a todas as invariantes definidas
neste contrato.

### 10.4 Manifesto persistido

O manifesto de proveniência correspondente à composição aprovada deve ser
persistido junto ao currículo direcionado.

O manifesto deve representar as fontes utilizadas naquela versão específica
do currículo.

Conteúdo e manifesto não podem representar composições diferentes.

### 10.5 Versionamento

Alterações que produzam nova composição factual ou estruturalmente relevante
devem resultar em nova versão do currículo direcionado ou em mecanismo
equivalente que preserve a identidade da composição aprovada anteriormente.

Uma nova versão pode ser necessária quando ocorrer, por exemplo:

- alteração relevante nas fontes factuais;
- alteração da vaga utilizada como contexto;
- nova composição solicitada pelo usuário;
- mudança nas regras de composição que altere o resultado;
- edição textual controlada que exija nova validação e aprovação.

A estratégia técnica de versionamento será definida durante a implementação,
desde que preserve as garantias deste contrato.

### 10.6 Imutabilidade lógica da versão aprovada

Uma versão aprovada deve ser tratada como um registro lógico do conteúdo que
foi efetivamente revisado e aprovado.

Alterações posteriores nas fontes factuais não devem modificar
silenciosamente uma versão já aprovada.

Uma nova composição deve produzir nova versão ou equivalente, sem reescrever
retroativamente o conteúdo anteriormente aprovado.

### 10.7 Alteração das fontes profissionais

`Profile`, `ProfessionalExperience`, `Project` e `Technology` continuam sendo
as fontes de verdade e podem evoluir independentemente dos currículos já
persistidos.

Quando essas fontes forem alteradas:

- currículos anteriormente aprovados não devem ser silenciosamente alterados;
- novas composições devem utilizar o estado atual autorizado das fontes;
- o novo resultado deve possuir proveniência correspondente;
- alterações relevantes devem passar novamente por preview e aprovação.

### 10.8 Alteração da vaga

A vaga é parte do contexto que determinou a composição do currículo
direcionado.

Uma alteração relevante na vaga ou a utilização de outra vaga deve exigir
nova composição quando modificar seleção, ordenação, priorização ou conteúdo
do currículo.

Um currículo direcionado a uma vaga não deve ser silenciosamente
reclassificado como direcionado a outra.

### 10.9 Atualização do currículo direcionado

Operações genéricas de atualização não devem permitir substituição arbitrária
do conteúdo factual de um currículo direcionado aprovado.

Alterações factuais devem ocorrer nas fontes profissionais correspondentes e
originar nova composição.

Alterações textuais controladas, caso sejam futuramente permitidas, devem:

- preservar equivalência factual;
- preservar ou recalcular proveniência;
- passar pelas validações aplicáveis;
- exigir nova aprovação quando modificarem o conteúdo apresentado ao usuário.

### 10.10 Compatibilidade com currículos existentes

A introdução do currículo direcionado não exige que currículos existentes
sejam automaticamente considerados conformes com este contrato.

Currículos criados pelo fluxo manual ou genérico anterior não devem receber
retroativamente garantias de proveniência ou integridade que não possam ser
demonstradas.

A implementação deve evitar atribuir a um currículo legado o estado de
currículo direcionado validado sem que ele tenha passado pelo fluxo definido
neste contrato.

### 10.11 Migração e retrocompatibilidade

Mudanças necessárias no domínio `Resume` devem preservar dados existentes
sempre que tecnicamente razoável.

Entretanto, retrocompatibilidade não pode justificar a redução das garantias
de integridade exigidas para novos currículos direcionados.

Caso o fluxo legado permaneça disponível, sua distinção em relação ao fluxo
direcionado deve ser explícita no domínio e não apenas visual.

### 10.12 Exclusão

A exclusão de um currículo direcionado deve respeitar as regras de autorização
da aplicação.

A exclusão do currículo não deve exigir a exclusão das fontes profissionais
que o originaram.

Da mesma forma, a exclusão ou alteração posterior de uma fonte não deve
reescrever silenciosamente versões de currículos anteriormente aprovadas.

### 10.13 Concorrência e consistência

A implementação deve impedir que alterações relevantes ocorridas entre
preview, aprovação e persistência produzam silenciosamente um currículo
diferente daquele revisado pelo usuário.

Quando não for possível demonstrar a equivalência da composição, a operação
deve falhar de forma segura e exigir novo preview.

### 10.14 Histórico e auditoria mínima

Para cada versão persistida de um currículo direcionado, o sistema deve
preservar informação suficiente para determinar:

- qual perfil originou o currículo;
- qual vaga orientou a composição;
- qual conteúdo foi aprovado;
- quais fontes factuais foram utilizadas;
- qual versão da composição foi persistida.

Este contrato não exige event sourcing, histórico completo de alterações por
campo ou infraestrutura especializada de auditoria.

## 11. Integração com ATS

A validação ATS deve operar sobre o currículo direcionado aprovado e
persistido, respeitando integralmente as invariantes de integridade factual
definidas neste contrato.

O ATS é um mecanismo de avaliação e orientação. Ele não constitui fonte
factual e não possui autoridade para introduzir, modificar ou fabricar
informações profissionais.

### 11.1 Pré-condição para validação ATS

O fluxo definitivo de validação ATS de um currículo direcionado deve receber
uma versão validamente aprovada e persistida.

A validação ATS não deve substituir:

- composição determinística;
- validação factual;
- proveniência;
- preview;
- aprovação.

### 11.2 Autoridade limitada do ATS

O ATS pode avaliar características do currículo, incluindo:

- presença ou ausência de seções;
- estrutura;
- organização;
- comprimento;
- completude;
- correspondência textual;
- demais critérios suportados pelas regras ATS da aplicação.

O resultado dessa avaliação não altera a classificação das fontes definida
neste contrato.

Regras ATS são regras de avaliação, não evidências sobre o histórico
profissional do usuário.

### 11.3 Integridade factual prevalece sobre score ATS

A melhoria do score ATS não pode justificar:

- criação de competências inexistentes;
- criação de experiências;
- criação de projetos;
- criação de formação acadêmica;
- criação de certificações;
- criação de responsabilidades;
- criação de métricas ou resultados;
- alteração de cargos ou períodos;
- qualquer outro fato sem suporte nas fontes autorizadas.

Quando houver conflito entre uma recomendação ATS e uma invariante factual,
a invariante factual deve prevalecer.

### 11.4 Informação exigida pelo ATS, mas ausente

Quando uma regra ATS esperar informação para a qual não exista fonte factual
autorizada, o sistema deve sinalizar a ausência.

A informação não deve ser criada apenas para satisfazer a regra.

Exemplo conceitual:

Se o ATS recomendar uma seção de formação acadêmica e nenhuma fonte factual
de formação estiver disponível, o sistema pode informar que a seção está
ausente e orientar o usuário a completar seus dados quando essa fonte estiver
disponível.

O sistema não deve gerar formação acadêmica fictícia para aumentar o score.

### 11.5 Recomendações ATS

Recomendações produzidas pela validação ATS devem permanecer separadas do
conteúdo factual aprovado.

Uma recomendação ATS pode orientar uma futura ação do usuário ou uma nova
composição, mas não pode modificar silenciosamente o currículo aprovado.

Quando a aplicação de uma recomendação exigir alteração do conteúdo, a
mudança deve respeitar as fontes factuais, as regras de composição e o fluxo
de aprovação aplicável.

### 11.6 Palavras-chave

A presença de uma palavra-chave na vaga ou em uma recomendação ATS não
autoriza sua inclusão no currículo como competência do usuário.

Uma palavra-chave somente pode ser incorporada ao conteúdo factual quando
houver suporte em fonte factual autorizada e sua utilização preservar o
significado da informação de origem.

O sistema não deve realizar keyword stuffing por meio de termos sem suporte
factual.

### 11.7 Revalidação após nova composição

Quando uma recomendação ATS resultar em nova composição validamente
solicitada, o novo currículo deve passar novamente pelas validações previstas
neste contrato.

Uma nova composição que altere o conteúdo aprovado deve exigir novo preview
e nova aprovação antes de substituir ou originar uma nova versão destinada
ao fluxo definitivo.

### 11.8 Score ATS e proveniência

O score ATS e seus componentes são dados analíticos.

Eles não devem ser registrados no manifesto como fontes factuais do currículo.

A proveniência do conteúdo continua limitada às fontes factuais autorizadas,
independentemente do resultado da avaliação ATS.

### 11.9 ATS e versões do currículo

A avaliação ATS deve estar associada à versão do currículo efetivamente
avaliada.

Um resultado ATS produzido para uma versão não deve ser apresentado como
resultado garantido de outra versão cujo conteúdo seja diferente.

Quando nova versão relevante do currículo for produzida, sua avaliação ATS
deve ser recalculada quando necessária.

### 11.10 Falha segura

Falhas na validação ATS não devem provocar alteração automática do conteúdo
factual aprovado.

Se uma recomendação ATS não puder ser aplicada sem violar este contrato, ela
deve permanecer como recomendação não aplicada.

O sistema deve preferir score ATS inferior a conteúdo factual incorreto.

## 12. Integração com Export

A exportação de um currículo direcionado deve produzir uma representação do
conteúdo aprovado e persistido sem introduzir, remover ou modificar fatos
profissionais de maneira semanticamente relevante.

O mecanismo de exportação é responsável pela representação do currículo em
um formato de saída. Ele não constitui fonte factual, mecanismo de composição
ou etapa adicional de otimização profissional.

### 12.1 Pré-condição para exportação

O fluxo definitivo de exportação de um currículo direcionado deve operar
sobre uma versão validamente aprovada e persistida.

A exportação não deve substituir:

- composição determinística;
- validação factual;
- proveniência;
- preview;
- aprovação;
- persistência.

Um preview ainda não aprovado não deve ser tratado como versão definitiva
exportável pelo fluxo normal do produto.

### 12.2 Fonte do conteúdo exportado

O conteúdo factual utilizado na exportação deve ser obtido da versão
persistida do currículo direcionado solicitado.

O frontend não deve fornecer conteúdo factual arbitrário para substituir o
conteúdo persistido durante a solicitação de exportação.

O backend deve autorizar o acesso ao currículo antes de disponibilizar sua
exportação.

### 12.3 Transformações permitidas

O processo de exportação pode realizar transformações necessárias à
representação do documento, incluindo:

- aplicação de layout;
- tipografia;
- espaçamento;
- paginação;
- hierarquia visual;
- cabeçalhos e rodapés;
- conversão de marcação;
- adaptação estrutural necessária ao formato de saída.

Essas transformações não devem modificar o significado factual do conteúdo
aprovado.

### 12.4 Transformações proibidas

A exportação não deve:

- acrescentar competências;
- acrescentar experiências;
- acrescentar projetos;
- acrescentar formação ou certificações;
- criar métricas ou resultados;
- alterar cargos, períodos ou responsabilidades;
- reescrever conteúdo de maneira semanticamente mais forte;
- inserir palavras-chave da vaga sem suporte factual;
- executar otimização factual adicional para ATS;
- utilizar IA para modificar silenciosamente o conteúdo aprovado.

Se uma transformação necessária ao formato exigir alteração semanticamente
relevante, ela deve ocorrer antes da exportação por meio do fluxo apropriado
de nova composição, preview e aprovação.

### 12.5 Formatos de saída

O currículo direcionado pode ser exportado nos formatos suportados pela
aplicação, como:

- Markdown;
- PDF;
- DOCX;
- outros formatos que venham a ser adicionados.

A adição de um novo formato não altera as garantias de integridade factual
definidas neste contrato.

Todos os formatos devem representar semanticamente a mesma versão aprovada.

### 12.6 Equivalência entre formatos

Diferenças de apresentação entre formatos são permitidas quando necessárias
às características técnicas de cada formato.

Entretanto, a conversão não deve produzir divergência factual entre
representações da mesma versão.

Por exemplo, PDF, DOCX e Markdown podem possuir diferenças de layout,
paginação ou estilo, mas não devem apresentar experiências, competências,
métricas ou demais fatos profissionais diferentes.

### 12.7 Relação com a versão

Cada exportação deve ser produzida a partir de uma versão identificável do
currículo direcionado.

Quando uma nova versão for aprovada, exportações futuras dessa nova versão
devem utilizar seu conteúdo correspondente.

Uma exportação anteriormente produzida não deve ser apresentada como
representação garantida de uma versão posterior diferente.

### 12.8 Proveniência e exportação

O manifesto de proveniência deve permanecer associado à versão do currículo
que originou a exportação.

Este contrato não exige que identificadores internos como `source_type` e
`source_id` sejam exibidos no documento entregue ao usuário ou ao recrutador.

A ausência dessas informações na representação visual exportada não elimina
a rastreabilidade mantida internamente pelo sistema.

### 12.9 ATS e exportação

A exportação não deve recalcular, reinterpretar ou modificar o conteúdo com o
objetivo de aumentar score ATS.

Quando existir avaliação ATS associada ao currículo, ela deve corresponder à
versão cujo conteúdo está sendo exportado.

Alterações semanticamente relevantes destinadas a melhorar o currículo devem
originar nova composição e nova aprovação antes da exportação.

### 12.10 Falhas de exportação

Falhas técnicas na geração de um formato não devem alterar o currículo
persistido.

Uma falha na geração de PDF, DOCX, Markdown ou outro formato deve ser tratada
como falha de representação, e não como autorização para modificar o conteúdo
factual.

A tentativa de exportação pode ser repetida sem necessidade de alterar a
versão aprovada, desde que seu conteúdo permaneça o mesmo.

### 12.11 Integridade do documento exportado

O sistema deve preferir falhar na geração de uma exportação quando não puder
representar corretamente o conteúdo aprovado.

Não deve ser produzido silenciosamente um documento factual ou
semanticamente diferente apenas para concluir a operação de exportação.

## 13. Uso de IA

O uso de Inteligência Artificial no fluxo de currículo direcionado é
opcional e subordinado às regras de integridade factual, autorização,
proveniência, composição, aprovação e versionamento definidas neste contrato.

A IA não constitui fonte factual sobre o usuário.

Nenhuma resposta produzida por modelo de IA deve ser considerada verdadeira
apenas por ter sido gerada pelo modelo ou por apresentar linguagem plausível.

### 13.1 Independência da composição básica

A geração básica do currículo direcionado deve funcionar sem dependência de
IA generativa.

A indisponibilidade, remoção, falha ou mudança de um provedor de IA não deve
impedir a execução da composição determinística definida neste contrato.

A IA deve representar uma capacidade adicional do produto, e não uma
pré-condição para a integridade ou funcionamento básico do currículo
direcionado.

### 13.2 Autoridade da IA

A IA pode auxiliar operações controladas, incluindo:

- melhoria de clareza textual;
- concisão;
- padronização de linguagem;
- sugestões de redação;
- reorganização textual permitida;
- outras transformações que preservem equivalência factual.

A IA não possui autoridade para decidir que uma informação profissional é
verdadeira.

A existência de uma sugestão gerada por IA não autoriza sua incorporação
automática ao currículo.

### 13.3 Contexto fornecido à IA

Quando IA for utilizada para transformar conteúdo factual, seu contexto deve
ser limitado às informações necessárias para executar a operação autorizada.

Sempre que aplicável, a IA deve receber fatos provenientes de fontes
autorizadas já identificadas pelo backend.

Informações analíticas ou contextuais podem ser fornecidas quando necessárias
à tarefa, desde que sua classificação seja preservada e elas não sejam
tratadas como fatos profissionais.

### 13.4 Requisitos da vaga

Informações provenientes da vaga podem ser utilizadas pela IA para compreender
contexto, relevância ou terminologia.

A presença de uma competência, tecnologia, responsabilidade ou qualificação
na vaga não autoriza a IA a atribuí-la ao usuário.

A IA não deve transformar requisitos da vaga em fatos profissionais do
candidato sem suporte em fonte factual autorizada.

### 13.5 Career Analysis

Resultados de `CareerAnalysis` podem ser utilizados como contexto para
priorização, explicação ou sugestão.

Entretanto:

- gaps não são competências;
- recomendações não são realizações;
- ações planejadas não são experiências concluídas;
- scores não são resultados profissionais;
- impactos estimados não são métricas profissionais realizadas.

A IA não deve converter essas informações analíticas em fatos do currículo.

### 13.6 Transformação factual permitida

Uma transformação assistida por IA somente pode ser aceita quando o resultado
permanecer semanticamente compatível com as fontes factuais que sustentam o
conteúdo original.

A transformação pode melhorar a forma de expressão, mas não deve tornar uma
afirmação:

- mais forte;
- mais específica;
- mais quantitativa;
- mais abrangente;
- mais conclusiva;
- mais sênior;

do que as fontes autorizadas permitem demonstrar.

### 13.7 Conteúdo proibido

A IA não deve introduzir sem suporte factual autorizado:

- empresas;
- cargos;
- períodos;
- experiências;
- projetos;
- tecnologias;
- competências;
- níveis de proficiência;
- anos de experiência;
- formação acadêmica;
- certificações;
- responsabilidades;
- liderança;
- métricas;
- resultados;
- impactos;
- clientes;
- volumes;
- valores financeiros;
- percentuais;
- qualquer outra afirmação profissional factual.

A plausibilidade da informação não constitui evidência.

### 13.8 Validação da saída

Toda saída de IA destinada a integrar conteúdo factual do currículo deve ser
validada antes de sua aceitação.

O sistema não deve depender exclusivamente de instruções no prompt para
garantir integridade factual.

Regras como "não invente informações" são orientações úteis ao modelo, mas
não substituem validação realizada pela aplicação.

Quando o sistema não puder demonstrar que a saída preserva as invariantes
aplicáveis, o conteúdo gerado não deve ser incorporado automaticamente.

### 13.9 Proveniência

O uso de IA não cria nova proveniência factual.

Uma transformação assistida por IA deve permanecer vinculada às fontes
factuais que sustentavam o conteúdo transformado.

O modelo, o prompt, a resposta da IA ou o provedor utilizado não devem ser
registrados como fontes factuais do histórico profissional do usuário.

### 13.10 Sugestão versus conteúdo aprovado

Sugestões de IA devem ser claramente distinguíveis de conteúdo factual
aprovado quando apresentadas ao usuário.

Uma sugestão não deve modificar silenciosamente uma versão aprovada do
currículo.

Quando uma sugestão aceita modificar conteúdo relevante do currículo, o
resultado deve passar pelas validações e pelo fluxo de aprovação aplicáveis
antes de constituir nova versão definitiva.

### 13.11 Falha, indisponibilidade ou resposta inválida

Falha de provedor, timeout, resposta vazia, conteúdo inválido ou violação das
regras factuais pela IA não devem comprometer o currículo persistido nem
obrigar o sistema a aceitar uma resposta inadequada.

Quando a operação assistida por IA falhar, o sistema deve:

1. preservar os dados factuais existentes;
2. rejeitar o resultado inválido;
3. informar a falha de maneira adequada;
4. permitir que o fluxo determinístico continue quando aplicável.

### 13.12 Troca de modelo ou provedor

As garantias deste contrato não devem depender do comportamento específico de
um determinado modelo ou provedor de IA.

A troca de modelo, versão ou fornecedor não reduz as invariantes de
integridade factual.

Diferenças probabilísticas entre modelos devem permanecer subordinadas às
mesmas regras de validação da aplicação.

### 13.13 Segurança e minimização de dados

A integração com serviços de IA deve enviar somente os dados necessários para
a finalidade da operação solicitada.

Dados que não sejam necessários ao processamento não devem ser incluídos no
contexto apenas por estarem disponíveis na aplicação.

Credenciais, tokens, segredos internos ou outros dados que não façam parte da
finalidade autorizada não devem ser enviados ao modelo.

Requisitos mais amplos de privacidade, proteção de dados e segurança devem ser
tratados pelas políticas transversais da aplicação.

### 13.14 IA e ATS

A IA não deve introduzir palavras-chave ou informações sem suporte factual
com o objetivo de aumentar score ATS.

Sugestões de melhoria ATS assistidas por IA continuam subordinadas às fontes
factuais e às invariantes deste contrato.

Score superior não constitui justificativa para redução da integridade
factual.

### 13.15 IA e exportação

A etapa de exportação não deve acionar IA para modificar silenciosamente o
conteúdo aprovado.

Caso uma transformação assistida por IA seja desejada, ela deve ocorrer antes
da aprovação definitiva ou originar nova composição sujeita às validações
aplicáveis.

### 13.16 Evoluções futuras

Recursos futuros podem ampliar o uso de IA no currículo direcionado, desde que
preservem as garantias deste contrato.

A introdução de:

- novos modelos;
- agentes;
- RAG;
- embeddings;
- recuperação semântica;
- novos provedores;
- novas técnicas de geração;

não autoriza redução das regras de autorização, integridade factual,
proveniência, validação e aprovação.

Complexidade adicional somente deve ser introduzida quando resolver uma
necessidade demonstrada do produto.

### 13.17 Falha segura

Quando houver dúvida sobre a compatibilidade factual de uma saída produzida
por IA, o sistema deve rejeitar, omitir ou submeter o conteúdo à revisão
apropriada.

Incerteza não autoriza inferência.

O sistema deve preferir uma redação menos otimizada a uma afirmação
profissional não demonstrável.

## 14. Segurança, autorização e isolamento de dados

Todas as operações do fluxo de currículo direcionado devem respeitar a
identidade do usuário autenticado, a propriedade dos recursos envolvidos e o
isolamento entre usuários e perfis.

A existência ou o conhecimento de um identificador interno não constitui
autorização para acessar ou utilizar o recurso correspondente.

As garantias desta seção aplicam-se às etapas de composição, preview,
aprovação, persistência, ATS, exportação e uso opcional de IA.

### 14.1 Autenticação como pré-condição

Operações relacionadas ao currículo direcionado devem exigir contexto de
usuário autenticado sempre que manipularem recursos privados.

A ausência de autenticação válida deve impedir o acesso ao fluxo protegido.

Autenticação identifica o usuário, mas não substitui as verificações de
autorização sobre cada recurso solicitado.

### 14.2 Autorização por recurso

Todo recurso utilizado no fluxo deve ser autorizado individualmente antes de
participar da operação.

Isso inclui, quando aplicável:

- perfil;
- experiências profissionais;
- projetos;
- tecnologias;
- vaga;
- preview;
- currículo direcionado persistido;
- versão do currículo;
- resultado ATS;
- exportação.

A autorização não deve ser inferida apenas porque outro recurso relacionado
já foi autorizado.

### 14.3 Isolamento entre usuários

Dados pertencentes a um usuário não devem participar da composição,
visualização, aprovação, avaliação ATS ou exportação de recursos pertencentes
a outro usuário.

O sistema deve impedir acesso cruzado mesmo quando identificadores válidos de
outros usuários forem fornecidos diretamente pelo cliente.

Exemplo conceitual:

```text
Usuário A autenticado
        ↓
profile_id do Usuário A
job_id do Usuário B
        ↓
REJEITAR
```

### 14.4 Isolamento entre perfis

Mesmo dentro do contexto de um único usuário, dados pertencentes a um
perfil não devem ser utilizados na composição de currículo direcionado
associado a outro perfil sem vínculo explicitamente autorizado pelo
domínio.

A autorização do usuário sobre ambos os perfis não elimina a necessidade
de preservar a associação correta entre:

- perfil;

- fontes factuais;

- vaga;

- preview;

- currículo direcionado;

- versões derivadas.

Uma fonte factual pertencente a outro perfil deve ser rejeitada quando
não fizer parte do contexto autorizado da composição.

### 14.5 Autorização das fontes factuais

Cada `ProfessionalExperience`, `Project` e `Technology` utilizado na
composição deve ser validado como pertencente ao perfil autorizado antes
de fornecer qualquer fato profissional.

A existência de um identificador válido não é suficiente.

O backend deve determinar a relação entre a fonte solicitada, o perfil e
o usuário autenticado a partir do estado persistido da aplicação.

Fontes não autorizadas devem ser rejeitadas antes da composição e não
apenas filtradas depois que seu conteúdo já tiver sido processado.

### 14.6 Autorização da vaga

A vaga utilizada como contexto deve ser acessível ao usuário autenticado
segundo as regras de propriedade e autorização do domínio `Job`.

O conhecimento de um `job_id` não autoriza sua utilização.

Uma vaga não autorizada não deve participar:

- da Career Analysis;

- da seleção ou priorização de fatos;

- da geração de preview;

- da composição;

- da avaliação ATS associada ao currículo direcionado.

A falha de autorização da vaga deve impedir o início ou a continuidade
da operação correspondente.

### 14.7 Objetos derivados

A autorização de objetos derivados não deve ser presumida apenas porque
eles foram produzidos a partir de recursos originalmente autorizados.

Objetos como:

- Career Analysis;

- preview;

- currículo direcionado;

- versão persistida;

- resultado ATS;

- artefato de exportação;

devem permanecer associados ao contexto de usuário, perfil e vaga que
lhes deu origem quando essas associações forem aplicáveis.

Um objeto derivado não deve ser reutilizado em contexto incompatível.

### 14.8 Autorização do preview

Um preview somente pode ser visualizado ou aprovado dentro do contexto
autorizado em que foi produzido.

O backend deve impedir que um usuário aprove:

- preview pertencente a outro usuário;

- preview pertencente a outro perfil incompatível;

- preview associado a vaga não autorizada;

- preview cuja identidade não corresponda à composição submetida à
  aprovação.

O identificador do preview é um mecanismo de referência, não uma
credencial de autorização.

### 14.9 Autorização da aprovação

A operação de aprovação deve revalidar o contexto de autorização
necessário antes da persistência definitiva.

A autorização válida durante a geração do preview não deve ser tratada
como garantia permanente de que todas as condições continuam válidas no
momento da aprovação.

Quando a autorização necessária não puder ser demonstrada, a aprovação
deve falhar de forma segura.

### 14.10 Currículo direcionado e versões

O acesso a um currículo direcionado persistido e às suas versões deve
respeitar a propriedade do recurso e o contexto autorizado.

Uma versão não deve se tornar acessível apenas porque seu identificador
é conhecido.

Operações de leitura, validação, exportação ou evolução de uma versão
devem verificar autorização sobre o currículo correspondente.

A associação entre versão e currículo não pode ser determinada
exclusivamente por dados fornecidos pelo cliente.

### 14.11 Autorização do ATS

A validação ATS deve exigir autorização sobre a versão do currículo que
será avaliada.

Um usuário não deve conseguir submeter à validação ATS currículo ou
versão pertencente a outro contexto apenas manipulando identificadores.

Resultados ATS devem permanecer associados ao recurso autorizado que foi
efetivamente avaliado.

A autorização para consultar um resultado ATS deve respeitar a
autorização do currículo e da versão correspondentes.

### 14.12 Autorização da exportação

A exportação deve exigir autorização sobre o currículo direcionado e a
versão solicitada.

O backend não deve aceitar identificadores arbitrários do cliente como
prova de que o recurso pode ser exportado.

Uma tentativa de exportar currículo ou versão não autorizados deve ser
rejeitada antes da disponibilização do documento.

URLs, nomes de arquivo ou referências de artefatos de exportação não
devem funcionar como substitutos das verificações de autorização
aplicáveis.

### 14.13 Uso de IA e isolamento

Quando IA for utilizada, somente dados pertencentes ao contexto
autorizado da operação podem ser enviados ao provedor.

A integração não deve ampliar o conjunto de dados acessíveis apenas
porque o modelo poderia utilizar contexto adicional.

Antes do envio, a aplicação deve preservar:

- autorização;

- isolamento entre usuários e perfis;

- minimização de dados;

- classificação entre fonte factual, contextual e analítica.

A resposta do modelo não deve ser utilizada para contornar verificações
de autorização realizadas pelo backend.

### 14.14 Dados fornecidos pelo cliente

Dados recebidos do frontend devem ser tratados como entrada não
confiável para fins de autorização.

Identificadores, associações, `source_type`, `source_id`, conteúdo
textual, estado de aprovação ou referências de versão enviados pelo
cliente não devem ser aceitos como prova de propriedade ou permissão.

O backend deve derivar ou validar as relações relevantes a partir de
dados persistidos e do contexto autenticado.

Validação de formato não substitui autorização.

### 14.15 Enumeração e manipulação de identificadores

A implementação deve considerar que identificadores podem ser
descobertos, enumerados, reutilizados ou alterados deliberadamente pelo
cliente.

As regras de autorização não devem depender da dificuldade de adivinhar
um identificador.

Trocar:

- `profile_id`;

- `job_id`;

- `source_id`;

- identificador de preview;

- `resume_id`;

- identificador de versão;

por um valor válido pertencente a outro contexto não deve conceder
acesso ao recurso correspondente.

### 14.16 Exposição mínima de dados

Respostas de erro e operações rejeitadas não devem expor dados
profissionais de recursos não autorizados.

Quando uma operação falhar por inexistência ou falta de autorização, a
implementação deve evitar revelar conteúdo do recurso, suas fontes, seu
currículo, sua análise ou demais informações privadas.

O contrato não prescreve um código HTTP específico para todos os casos,
mas a resposta não deve transformar a validação de autorização em
mecanismo de exposição indevida de dados.

### 14.17 Tratamento de erros de autorização

Falhas de autenticação ou autorização devem interromper a operação
protegida.

O sistema não deve:

- continuar a composição parcialmente;

- substituir silenciosamente o recurso por outro;

- utilizar fontes já carregadas depois de detectar incompatibilidade;

- persistir resultado parcial;

- exportar conteúdo;

- recorrer à IA para completar a operação.

Erros devem ser tratados de forma consistente com as políticas de
segurança da aplicação e sem reduzir as garantias deste contrato.

### 14.18 Operações em lote e extensões futuras

Qualquer operação futura que processe múltiplos perfis, vagas,
currículos, versões ou fontes deve aplicar as mesmas verificações de
autorização a cada recurso participante.

A autorização de um item não deve ser propagada automaticamente aos
demais itens de um lote.

Novos endpoints, integrações, workers, tarefas assíncronas ou mecanismos
de processamento não podem criar caminhos alternativos que ignorem as
fronteiras definidas nesta seção.

### 14.19 Falha segura

Quando a aplicação não conseguir demonstrar de forma suficiente que um
recurso pertence ao contexto autorizado, deve rejeitar sua utilização.

Dúvida sobre propriedade, associação ou autorização não constitui
permissão.

O sistema deve preferir interromper a operação a:

- utilizar dados de outro usuário;

- misturar fontes entre perfis incompatíveis;

- aprovar preview não autorizado;

- validar currículo não autorizado;

- exportar recurso não autorizado;

- enviar dados não autorizados a serviços externos.

Falhas de autorização devem preservar o isolamento dos dados e não
produzir efeitos persistentes sobre recursos protegidos.

## 15. Critérios de aceite e conformidade

Uma implementação do currículo direcionado somente deve ser considerada
conforme com este contrato quando demonstrar, por comportamento verificável,
que preserva as garantias funcionais, factuais, de autorização, proveniência,
aprovação e persistência aqui definidas.

A existência de código, endpoints, interfaces ou testes isolados não é
suficiente para declarar conformidade quando o comportamento integrado viola
uma das invariantes obrigatórias.

### 15.1 Regra geral de conformidade

A implementação deve satisfazer simultaneamente:

- as invariantes definidas neste contrato;
- as regras de autorização;
- as restrições sobre fontes factuais;
- as regras de composição determinística;
- os requisitos de proveniência;
- o fluxo de preview e aprovação;
- as regras de persistência e versionamento;
- as restrições aplicáveis ao ATS;
- as restrições aplicáveis à exportação;
- as restrições aplicáveis ao uso opcional de IA.

A violação de uma invariante obrigatória torna o comportamento correspondente
não conforme, mesmo quando as demais funcionalidades operarem corretamente.

### 15.2 Critério de integridade factual

A implementação deve demonstrar que nenhum fato profissional pode aparecer no
currículo direcionado sem suporte em fonte factual autorizada.

Devem ser rejeitados ou omitidos conteúdos que dependam exclusivamente de:

- requisitos da vaga;
- gaps;
- recomendações;
- planos de ação;
- scores;
- impactos estimados;
- inferências não persistidas;
- conteúdo arbitrário enviado pelo cliente;
- geração de IA sem suporte factual verificável.

### 15.3 Critério de ausência de fabricação

A implementação deve demonstrar que não fabrica informações para melhorar:

- completude do currículo;
- aderência à vaga;
- qualidade textual;
- score ATS;
- aparência de senioridade;
- impacto profissional percebido.

Isso inclui, entre outros, métricas, percentuais, valores, quantidades,
resultados, responsabilidades, competências, experiências, formação,
certificações e liderança sem suporte factual.

### 15.4 Critério de separação entre fato e análise

A implementação deve demonstrar que dados analíticos podem influenciar
seleção, ordenação e priorização sem serem convertidos em fatos profissionais.

Em especial:

- gap permanece gap;
- recomendação permanece recomendação;
- ação futura permanece ação futura;
- score permanece dado analítico;
- impacto estimado permanece estimativa.

A apresentação ou utilização desses dados no fluxo não altera sua natureza.

### 15.5 Critério de autorização

A implementação deve demonstrar que somente recursos pertencentes ao contexto
autorizado podem participar da operação.

Devem existir verificações capazes de impedir, no mínimo:

- utilização de perfil de outro usuário;
- utilização de vaga não autorizada;
- utilização de fonte factual pertencente a outro perfil;
- aprovação de preview não autorizado;
- acesso a currículo ou versão não autorizados;
- validação ATS de recurso não autorizado;
- exportação de recurso não autorizado.

A alteração manual de identificadores pelo cliente não deve contornar essas
verificações.

### 15.6 Critério de proveniência

Todo bloco factual do currículo direcionado deve possuir proveniência válida e
suficiente para identificar suas fontes autorizadas.

A implementação deve demonstrar que:

- referências inexistentes são rejeitadas;
- referências não autorizadas são rejeitadas;
- tipos não permitidos como fontes factuais são rejeitados;
- conteúdo sem proveniência válida não é aceito como fato;
- a presença de uma referência válida não autoriza afirmações que a fonte não
  sustenta.

### 15.7 Critério de determinismo

A composição básica deve produzir resultado equivalente e verificável quando
executada com:

- as mesmas fontes relevantes;
- o mesmo contexto de vaga;
- as mesmas regras de composição;
- a mesma versão da composição.

A geração básica não deve depender de resposta probabilística de IA para
produzir um currículo válido.

### 15.8 Critério de preview

A implementação deve demonstrar que o preview:

- é produzido pelo backend a partir de fontes autorizadas;
- possui identidade verificável;
- não constitui automaticamente versão aprovada;
- permanece associado ao perfil e à vaga corretos;
- não pode ser utilizado para contornar autorização;
- contém proveniência compatível com sua composição.

### 15.9 Critério de aprovação

A implementação deve demonstrar que:

- aprovação exige ação explícita do usuário;
- o preview aprovado é identificável;
- conteúdo factual arbitrário do frontend não substitui a composição;
- alterações relevantes entre preview e aprovação são detectadas;
- divergência relevante exige novo preview;
- conteúdo persistido corresponde ao conteúdo efetivamente aprovado.

### 15.10 Critério de persistência

Uma versão persistida do currículo direcionado deve permitir determinar, no
mínimo:

- perfil correspondente;
- vaga correspondente;
- conteúdo aprovado;
- manifesto de proveniência;
- identidade ou versão da composição.

Alterações posteriores nas fontes não devem reescrever silenciosamente uma
versão já aprovada.

### 15.11 Critério de versionamento

Quando uma alteração relevante produzir nova composição, a implementação deve
preservar a distinção entre o resultado anteriormente aprovado e o novo
resultado.

Uma nova versão não deve substituir retroativamente a evidência do conteúdo
que havia sido aprovado anteriormente.

### 15.12 Critério de ATS

A implementação deve demonstrar que o ATS avalia o currículo sem possuir
autoridade para fabricar conteúdo.

Em especial:

- informação ausente deve permanecer ausente ou ser sinalizada;
- requisito da vaga não deve virar competência;
- recomendação ATS não deve alterar silenciosamente o currículo;
- score ATS não deve prevalecer sobre integridade factual;
- resultado ATS deve corresponder à versão efetivamente avaliada.

### 15.13 Critério de exportação

A implementação deve demonstrar que os formatos exportados representam
semanticamente a versão aprovada correspondente.

Diferenças de layout são permitidas.

Diferenças factuais entre representações da mesma versão não são permitidas.

Falha de exportação não deve modificar o conteúdo persistido.

### 15.14 Critério de uso de IA

Quando IA for utilizada, a implementação deve demonstrar que:

- seu uso é opcional para a composição básica;
- a IA não é tratada como fonte factual;
- requisitos da vaga não são convertidos em fatos;
- dados analíticos não são convertidos em fatos;
- transformações preservam equivalência factual;
- saída inválida pode ser rejeitada;
- falha do provedor não compromete dados persistidos;
- prompt não é utilizado como única garantia de integridade.

### 15.15 Critério de falha segura

Sempre que a aplicação não puder demonstrar autorização, proveniência,
integridade factual ou equivalência necessária à operação, deve falhar de
forma segura.

A falha segura deve preferir:

- rejeição;
- omissão controlada;
- solicitação de novo preview;
- sinalização ao usuário;

em vez de inferência, fabricação ou persistência silenciosa de conteúdo
incerto.

### 15.16 Critério de usabilidade do fluxo crítico

O usuário deve conseguir distinguir os estados essenciais do fluxo:

- preview;
- aguardando aprovação;
- aprovado;
- erro ou invalidação;
- versão persistida.

A ação de aprovação deve ser identificável e não deve ocorrer implicitamente
como consequência de simples visualização.

### 15.17 Critério mínimo de acessibilidade

As ações essenciais de preview e aprovação devem ser operáveis sem dependência
exclusiva de dispositivo apontador.

Estados, erros e ações críticas não devem depender exclusivamente de cor para
serem compreendidos.

Elementos interativos devem utilizar semântica adequada sempre que aplicável.

### 15.18 Critério de regressão

Uma alteração futura no compositor, ATS, exportação, integração de IA,
persistência ou fluxo de aprovação não deve ser considerada aceitável quando
fizer uma garantia anteriormente satisfeita deixar de ser cumprida.

As invariantes deste contrato devem possuir proteção automatizada suficiente
para detectar regressões críticas.

### 15.19 Evidência de conformidade

A conformidade deve ser demonstrável por evidências técnicas apropriadas,
incluindo, conforme aplicável:

- testes unitários;
- testes de serviço;
- testes de integração;
- testes de autorização;
- testes de API;
- testes de regressão;
- validação funcional do fluxo.

Não é requisito que toda regra seja comprovada pelo mesmo nível ou tipo de
teste.

A estratégia deve utilizar o nível mais adequado para verificar cada
comportamento.

### 15.20 Critério para conclusão da implementação

A implementação do fluxo de currículo direcionado não deve ser considerada
concluída apenas porque o caminho nominal funciona.

Antes da conclusão, deve existir evidência de que os principais caminhos de
falha e abuso previstos por este contrato também foram verificados.

Isso inclui, no mínimo:

- tentativa de utilizar dados de outro usuário;
- requisito da vaga sem suporte factual;
- gap tratado indevidamente como competência;
- tentativa de fabricação de métrica;
- proveniência inválida;
- alteração das fontes entre preview e aprovação;
- tentativa de persistir conteúdo arbitrário enviado pelo cliente;
- falha ou saída inválida de IA, quando IA participar do fluxo;
- tentativa de exportar recurso não autorizado.

### 15.21 Regra final de aceite

Quando houver conflito entre aparência de completude, otimização textual,
aderência ATS ou conveniência de implementação e uma garantia obrigatória
deste contrato, a garantia obrigatória deve prevalecer.

Um currículo factual, rastreável e eventualmente incompleto é um resultado
válido.

Um currículo aparentemente completo, mas sustentado por fatos não
demonstráveis, não é um resultado conforme.

## 16. Matriz de invariantes e testes

As invariantes definidas na Seção 6 representam propriedades obrigatórias do
currículo direcionado e devem possuir evidência automatizada suficiente para
detectar violações e regressões.

Esta matriz estabelece o conjunto mínimo de comportamentos que devem ser
protegidos por testes.

Os nomes de testes apresentados são referências conceituais. A implementação
pode utilizar nomenclatura diferente, desde que preserve de maneira explícita
a propriedade verificada.

### 16.1 Estratégia de teste

Os testes devem priorizar comportamento observável e propriedades do domínio,
não detalhes internos de implementação.

Sempre que possível, uma invariante deve ser verificada no nível mais baixo
capaz de demonstrá-la com segurança.

Testes de integração ou API devem complementar testes unitários quando a
garantia depender de:

- autenticação;
- autorização;
- persistência;
- transações;
- associação entre recursos;
- comportamento entre múltiplas camadas.

A existência de um teste não torna a implementação conforme quando o teste não
representa adequadamente a propriedade definida pela invariante.

### 16.2 TR-INV-001 — Fato persistido como pré-condição

**Propriedade**
Nenhum fato profissional pode participar do currículo sem suporte em fonte
factual persistida e autorizada.

**Cenário mínimo**
Dado um conteúdo profissional não existente nas fontes autorizadas, quando o
currículo for composto, então esse conteúdo não deve aparecer como fato.

**Referência de teste**
`test_composer_does_not_include_unpersisted_fact`

### 16.3 TR-INV-002 — Informação ausente não deve ser inferida

**Propriedade**
Informação ausente deve permanecer ausente ou ser sinalizada, nunca inferida
como fato.

**Cenário mínimo**
Dado um perfil sem determinada informação profissional, quando a composição
for executada, então o sistema não deve completar essa informação por
inferência.

**Referência de teste**
`test_composer_does_not_infer_missing_information`

### 16.4 TR-INV-003 — Requisito da vaga não é competência do usuário

**Propriedade**
Um requisito existente somente na vaga não pode ser convertido em competência
do candidato.

**Cenário mínimo**
Dada uma vaga que exige uma tecnologia inexistente nas fontes factuais do
perfil, quando o currículo for composto, então a tecnologia não deve aparecer
como competência do usuário.

**Referência de teste**
`test_job_requirement_does_not_become_candidate_skill`

### 16.5 TR-INV-004 — Gap não pode se tornar fato profissional

**Propriedade**
Gap, recomendação ou ação futura não pode ser convertido em experiência,
competência, qualificação ou resultado profissional.

**Cenário mínimo**
Dado um gap identificado pela análise de carreira, quando o currículo for
composto, então o gap não deve aparecer como competência adquirida.

**Referência de teste**
`test_career_gap_does_not_become_resume_fact`

Testes complementares podem verificar recomendações e itens do plano de ação.

### 16.6 TR-INV-005 — Proibição de fabricação de métricas e resultados

**Propriedade**
O compositor não pode criar métricas, percentuais, quantidades, valores ou
resultados que não estejam sustentados pelas fontes factuais.

**Cenário mínimo**
Dada uma experiência sem resultado quantitativo persistido, quando o currículo
for composto, então nenhuma métrica deve ser adicionada para aumentar impacto
textual.

**Referência de teste**
`test_composer_does_not_fabricate_metrics`

### 16.7 TR-INV-006 — Preservação de identidade factual

**Propriedade**
Transformações de redação não podem alterar a identidade factual da fonte.

**Cenário mínimo**
Dada uma experiência com empresa, cargo, período, responsabilidades e
tecnologias definidos, quando o conteúdo for transformado, então esses fatos
devem permanecer semanticamente compatíveis com a fonte.

**Referência de teste**
`test_composer_preserves_factual_identity`

Casos complementares devem verificar, quando aplicável:

- empresa;
- cargo;
- período;
- tipo de vínculo;
- projeto;
- tecnologia;
- proficiência;
- anos de experiência;
- responsabilidade;
- resultado.

### 16.8 TR-INV-007 — ATS subordinado à integridade factual

**Propriedade**
Uma regra ou recomendação ATS não pode produzir fato profissional inexistente.

**Cenário mínimo**
Dada uma regra ATS que espera informação ausente nas fontes factuais, quando a
validação for executada, então a ausência deve ser sinalizada sem fabricação
de conteúdo.

**Referência de teste**
`test_ats_does_not_fabricate_missing_fact`

Um caso obrigatório deve cobrir informação de formação acadêmica enquanto não
existir fonte factual correspondente.

### 16.9 TR-INV-008 — Proveniência obrigatória

**Propriedade**
Todo bloco factual deve possuir proveniência válida.

**Cenário mínimo**
Dado um bloco factual sem referência de origem válida, quando a composição for
validada, então o bloco deve ser rejeitado ou excluído do resultado factual.

**Referência de teste**
`test_factual_block_requires_valid_provenance`

Testes complementares devem verificar:

- `source_type` inválido;
- `source_id` inexistente;
- fonte não autorizada;
- múltiplas fontes quando necessárias;
- referência válida que não sustenta a afirmação.

### 16.10 TR-INV-009 — Autorização precede composição

**Propriedade**
Nenhuma fonte pode participar da composição antes de sua autorização.

**Cenário mínimo**
Dada uma fonte factual pertencente a outro usuário ou perfil, quando seu
identificador for fornecido à operação, então a fonte deve ser rejeitada antes
da composição.

**Referência de teste**
`test_composer_rejects_cross_user_source`

Testes complementares devem verificar:

- perfil de outro usuário;
- vaga não autorizada;
- fonte de outro perfil;
- preview de outro usuário;
- currículo de outro usuário.

### 16.11 TR-INV-010 — Geração básica independente de IA

**Propriedade**
O currículo direcionado básico deve poder ser produzido sem serviço de IA
generativa.

**Cenário mínimo**
Dadas fontes válidas e contexto de vaga válido, quando nenhum provedor de IA
estiver disponível, então a composição determinística deve continuar
funcionando.

**Referência de teste**
`test_targeted_resume_generation_does_not_require_ai`

### 16.12 TR-INV-011 — IA não pode ampliar a verdade factual

**Propriedade**
Uma transformação assistida por IA não pode introduzir fatos ou fortalecer
semanticamente afirmações além do suporte das fontes.

**Cenário mínimo**
Dada uma saída de IA que acrescenta liderança, métrica ou competência não
existente na fonte, quando a saída for validada, então ela deve ser rejeitada.

**Referência de teste**
`test_ai_output_cannot_expand_factual_claims`

Testes complementares devem incluir respostas:

- vazias;
- inválidas;
- semanticamente mais fortes;
- contendo requisito exclusivo da vaga;
- contendo métrica fabricada.

### 16.13 TR-INV-012 — Aprovação não autoriza alteração factual arbitrária

**Propriedade**
A operação de aprovação não pode permitir que o cliente substitua o resultado
composto por conteúdo factual arbitrário.

**Cenário mínimo**
Dado um preview válido, quando o cliente tentar aprová-lo enviando conteúdo
factual diferente, então o backend não deve persistir esse conteúdo como
substituto do preview aprovado.

**Referência de teste**
`test_approval_rejects_arbitrary_client_content`

Um teste adicional deve demonstrar correspondência entre preview aprovado e
conteúdo persistido:

`test_approved_preview_matches_persisted_resume`

### 16.14 TR-INV-013 — Integridade factual prevalece sobre completude

**Propriedade**
O sistema deve aceitar ausência de informação em vez de completar o currículo
com conteúdo sem suporte factual.

**Cenário mínimo**
Dado um currículo incompleto por ausência de determinada fonte, quando a
composição for executada, então o resultado deve permanecer incompleto em vez
de receber conteúdo fabricado.

**Referência de teste**
`test_factual_integrity_precedes_resume_completeness`

### 16.15 Testes do ciclo Preview → Approval → Persistence

Além dos testes diretamente associados às invariantes, o fluxo crítico deve
possuir proteção integrada para demonstrar que:

1. preview é produzido a partir de fontes autorizadas;
2. preview possui identidade verificável;
3. simples visualização não constitui aprovação;
4. aprovação identifica o preview correto;
5. alteração relevante das fontes invalida aprovação incompatível;
6. conteúdo persistido corresponde ao conteúdo aprovado;
7. manifesto persistido corresponde à mesma composição.

Referências conceituais:

- `test_preview_requires_authorized_sources`;
- `test_preview_is_not_implicitly_approved`;
- `test_changed_sources_invalidate_stale_preview`;
- `test_approved_preview_matches_persisted_resume`;
- `test_persisted_manifest_matches_approved_composition`.

### 16.16 Testes de versionamento

O sistema deve demonstrar que uma versão aprovada não é silenciosamente
reescrita quando suas fontes forem alteradas.

Referências conceituais:

- `test_source_update_does_not_mutate_approved_version`;
- `test_new_composition_preserves_previous_version`;
- `test_ats_result_is_bound_to_resume_version`;
- `test_export_uses_requested_approved_version`.

### 16.17 Testes de isolamento e autorização

Devem existir testes negativos que tentem deliberadamente atravessar as
fronteiras de autorização.

Referências conceituais:

- `test_user_cannot_use_another_users_profile`;
- `test_user_cannot_use_unauthorized_job`;
- `test_user_cannot_use_source_from_another_profile`;
- `test_user_cannot_approve_another_users_preview`;
- `test_user_cannot_validate_another_users_resume`;
- `test_user_cannot_export_another_users_resume`.

Esses testes devem manipular identificadores como um cliente potencialmente
hostil faria, em vez de depender apenas do caminho nominal da interface.

### 16.18 Testes de ATS

Além de `TR-INV-007`, devem existir testes que demonstrem que:

- score pertence à versão avaliada;
- recomendação não modifica silenciosamente conteúdo;
- palavra-chave sem suporte factual não é incorporada;
- informação ausente é sinalizada;
- nova versão exige avaliação correspondente quando necessário.

Referências conceituais:

- `test_ats_score_is_bound_to_resume_version`;
- `test_ats_recommendation_does_not_mutate_resume`;
- `test_ats_keyword_requires_factual_support`;
- `test_ats_reports_missing_information_without_fabrication`.

### 16.19 Testes de exportação

A exportação deve possuir testes capazes de demonstrar que a transformação de
formato não modifica semanticamente o currículo.

Referências conceituais:

- `test_export_uses_approved_persisted_content`;
- `test_export_does_not_accept_arbitrary_client_content`;
- `test_export_formats_preserve_factual_content`;
- `test_export_failure_does_not_mutate_resume`.

Não é necessário exigir identidade binária ou visual entre formatos
diferentes.

O requisito é equivalência factual da versão representada.

### 16.20 Testes de IA

Quando recursos de IA participarem do fluxo, devem existir testes sem chamadas
reais ao provedor para os principais comportamentos de domínio.

Dependências externas devem ser substituídas por doubles apropriados quando o
objetivo do teste for validar regras da aplicação.

Devem ser cobertos, no mínimo:

- resposta válida e equivalente;
- resposta vazia;
- erro do provedor;
- timeout ou falha equivalente;
- conteúdo fabricado;
- fortalecimento semântico;
- requisito da vaga convertido indevidamente em competência.

Chamadas reais a provedores externos não devem ser necessárias para comprovar
as invariantes do domínio.

### 16.21 Testes determinísticos

Testes das invariantes devem ser determinísticos.

A aprovação da suíte não deve depender de:

- variabilidade de LLM;
- disponibilidade de serviço externo;
- resposta probabilística;
- conexão de rede desnecessária;
- dados pertencentes a ambiente de produção.

Fixtures, factories, mocks, fakes ou outras técnicas podem ser utilizadas para
criar condições reproduzíveis.

### 16.22 Nomenclatura e rastreabilidade dos testes

Sempre que tecnicamente razoável, testes que protejam diretamente uma
invariante devem permitir identificar qual propriedade normativa está sendo
verificada.

Isso pode ser realizado por:

- nome explícito do teste;
- organização por módulo;
- comentário ou documentação;
- marcador;
- outra convenção consistente adotada pelo projeto.

Não é obrigatório incluir o identificador `TR-INV-XXX` no nome físico de cada
teste.

### 16.23 Cobertura

Cobertura de código continua sendo uma métrica de qualidade útil, mas não
constitui isoladamente evidência de conformidade com este contrato.

Uma linha executada durante um teste não demonstra necessariamente que sua
regra de domínio foi validada.

A estratégia de testes deve priorizar propriedades e riscos antes de perseguir
percentuais de cobertura sem significado comportamental.

### 16.24 Regressão

Uma vez implementado e validado um comportamento associado a uma invariante,
seu teste deve integrar a suíte de regressão aplicável.

Alterações futuras não devem remover ou enfraquecer silenciosamente essas
proteções apenas para acomodar nova implementação.

Quando uma invariante for deliberadamente alterada, a mudança deve ocorrer
primeiro no contrato e ser revisada antes da adaptação correspondente dos
testes e da implementação.

### 16.25 Matriz resumida

| Invariante   | Garantia principal                            | Referência mínima de teste                             |
| ------------ | --------------------------------------------- | ------------------------------------------------------ |
| `TR-INV-001` | Somente fatos persistidos e autorizados       | `test_composer_does_not_include_unpersisted_fact`      |
| `TR-INV-002` | Ausência não gera inferência factual          | `test_composer_does_not_infer_missing_information`     |
| `TR-INV-003` | Requisito da vaga não vira competência        | `test_job_requirement_does_not_become_candidate_skill` |
| `TR-INV-004` | Gap não vira fato profissional                | `test_career_gap_does_not_become_resume_fact`          |
| `TR-INV-005` | Métricas e resultados não são fabricados      | `test_composer_does_not_fabricate_metrics`             |
| `TR-INV-006` | Identidade factual é preservada               | `test_composer_preserves_factual_identity`             |
| `TR-INV-007` | ATS não supera integridade factual            | `test_ats_does_not_fabricate_missing_fact`             |
| `TR-INV-008` | Todo bloco factual possui proveniência válida | `test_factual_block_requires_valid_provenance`         |
| `TR-INV-009` | Autorização ocorre antes da composição        | `test_composer_rejects_cross_user_source`              |
| `TR-INV-010` | Geração básica funciona sem IA                | `test_targeted_resume_generation_does_not_require_ai`  |
| `TR-INV-011` | IA não amplia fatos                           | `test_ai_output_cannot_expand_factual_claims`          |
| `TR-INV-012` | Aprovação não aceita conteúdo arbitrário      | `test_approval_rejects_arbitrary_client_content`       |
| `TR-INV-013` | Integridade prevalece sobre completude        | `test_factual_integrity_precedes_resume_completeness`  |

### 16.26 Regra de manutenção da matriz

Esta matriz deve evoluir juntamente com as invariantes do contrato.

Uma nova invariante obrigatória deve possuir estratégia de verificação
correspondente antes de sua implementação ser considerada concluída.

A remoção ou alteração de uma invariante deve ser tratada como mudança do
contrato, e não apenas como manutenção de testes.

## 17. Fora de escopo

Esta seção estabelece os limites da versão atual do contrato de currículo
direcionado.

Funcionalidades, técnicas ou comportamentos mencionados como fora de escopo
não são necessariamente proibidos permanentemente. Eles apenas não constituem
requisitos para a implementação atual e não podem ser utilizados para
contornar as garantias obrigatórias definidas neste contrato.

### 17.1 Casos proibidos consolidados

Independentemente da estratégia técnica adotada, a implementação não deve:

- inventar fatos profissionais;
- inferir como verdadeiro um dado profissional ausente;
- transformar requisito da vaga em competência do usuário;
- transformar gap em competência;
- transformar recomendação em realização;
- transformar ação futura em experiência concluída;
- transformar score ou impacto estimado em resultado profissional;
- fabricar métricas, percentuais, valores, volumes ou resultados;
- ampliar senioridade sem suporte factual;
- atribuir liderança não demonstrada pelas fontes;
- utilizar fonte factual pertencente a outro usuário ou perfil;
- utilizar recurso não autorizado apenas porque seu identificador é conhecido;
- persistir bloco factual sem proveniência válida;
- utilizar uma referência de proveniência para justificar afirmação que a
  fonte não sustenta;
- aceitar conteúdo factual arbitrário do frontend como substituto da
  composição autorizada;
- persistir silenciosamente conteúdo diferente daquele aprovado;
- reutilizar preview incompatível após alteração relevante das fontes;
- modificar silenciosamente versão anteriormente aprovada;
- fabricar conteúdo para aumentar score ATS;
- realizar keyword stuffing com competências não sustentadas;
- utilizar IA como fonte factual;
- confiar exclusivamente em prompt para garantir integridade factual;
- permitir que IA amplie a verdade suportada pelas fontes;
- utilizar exportação como oportunidade para modificar semanticamente o
  currículo aprovado;
- reduzir garantias de autorização, proveniência ou integridade por
  conveniência de implementação.

Esta lista consolida comportamentos proibidos já derivados das invariantes e
das demais seções do contrato. Ela não substitui regras mais específicas
definidas anteriormente.

### 17.2 Funcionalidades fora de escopo da versão atual

Não são requisitos para a implementação inicial desta transição:

- RAG;
- embeddings;
- banco vetorial;
- agentes autônomos;
- recuperação semântica de evidências;
- claim graph;
- proveniência por token;
- proveniência por palavra;
- proveniência por sentença;
- event sourcing;
- histórico completo de alterações por campo;
- infraestrutura especializada de auditoria;
- geração obrigatoriamente dependente de IA;
- múltiplos provedores de IA;
- seleção dinâmica de modelos;
- otimização automática baseada em experimentação com LLMs.

A ausência dessas capacidades não caracteriza incompletude do fluxo definido
por este contrato.

### 17.3 Edição livre de currículo direcionado

Edição factual livre de um currículo direcionado aprovado não faz parte do
escopo atual.

Alterações factuais devem ocorrer prioritariamente nas fontes profissionais
correspondentes e originar nova composição.

Uma futura funcionalidade de edição textual controlada somente poderá ser
introduzida se preservar:

- equivalência factual;
- proveniência;
- autorização;
- versionamento;
- validação;
- aprovação.

### 17.4 Novas fontes profissionais

A criação de novos domínios estruturados, como:

- formação acadêmica;
- certificações;
- idiomas;
- publicações;
- prêmios;
- outras qualificações;

não faz parte obrigatória desta transição, salvo quando posteriormente
incorporada de forma explícita ao escopo.

A inexistência dessas fontes não autoriza sua fabricação.

Quando novos tipos de fonte forem introduzidos, sua classificação como fonte
factual deve ser definida explicitamente antes de sua utilização pelo
compositor.

### 17.5 Internacionalização e localização completas

A implementação completa de internacionalização e localização não faz parte
do escopo obrigatório desta transição.

Entretanto, a implementação não deve introduzir acoplamentos desnecessários
que impeçam futura internacionalização.

Conceitos estruturais do domínio devem permanecer independentes dos rótulos
apresentados ao usuário sempre que aplicável.

A introdução futura de idiomas ou mercados específicos deve ocorrer em camada
apropriada sem alterar a verdade factual representada pelo currículo.

### 17.6 Auditoria transversal de acessibilidade e usabilidade

Este contrato estabelece requisitos mínimos de usabilidade e acessibilidade
para o fluxo crítico de preview e aprovação.

Uma auditoria completa de acessibilidade e usabilidade de toda a aplicação não
faz parte do escopo deste módulo.

Os requisitos mínimos aqui definidos, entretanto, não são opcionais por esse
motivo.

### 17.7 Segurança transversal da aplicação

Este contrato estabelece requisitos de autenticação, autorização, isolamento
e minimização diretamente necessários ao currículo direcionado.

Não fazem parte de seu escopo detalhado as políticas transversais completas
da aplicação, incluindo, entre outras:

- política de senhas;
- ciclo de vida completo de tokens;
- política global de CORS;
- política global de CSP;
- criptografia em repouso;
- gestão completa de segredos;
- backup;
- disaster recovery;
- retenção global de dados;
- monitoramento de segurança;
- resposta a incidentes.

Esses temas devem ser tratados nos requisitos transversais apropriados do
ProfileSync AI.

A exclusão desses assuntos deste contrato não reduz sua importância para o
produto.

### 17.8 LGPD e privacidade transversal

Este contrato aplica princípios de autorização e minimização necessários ao
fluxo, mas não constitui política completa de conformidade com a LGPD.

Requisitos transversais de:

- base legal;
- transparência;
- direitos do titular;
- retenção;
- eliminação;
- compartilhamento;
- operadores e controladores;
- transferências aplicáveis;
- demais obrigações regulatórias;

devem ser tratados na governança apropriada da aplicação.

Nenhuma funcionalidade futura pode interpretar esta exclusão de escopo como
autorização para reduzir obrigações legais aplicáveis.

### 17.9 Implementação física não prescrita

Este contrato define propriedades e comportamentos obrigatórios, mas não
prescreve, salvo quando explicitamente necessário:

- nomes de tabelas;
- nomes de classes;
- nomes de serviços;
- nomes de endpoints;
- estrutura física do banco;
- estratégia específica de hash;
- mecanismo específico de preview;
- biblioteca;
- framework;
- provedor de IA;
- algoritmo interno específico.

A implementação pode escolher soluções técnicas adequadas desde que todas as
garantias normativas sejam preservadas.

### 17.10 Não objetivos do currículo direcionado

O currículo direcionado não tem como objetivo:

- garantir contratação;
- garantir entrevista;
- garantir aprovação em processo seletivo;
- garantir determinado score ATS;
- simular experiência profissional inexistente;
- ocultar deliberadamente gaps por fabricação de conteúdo;
- representar o usuário como mais experiente do que suas fontes demonstram;
- substituir avaliação humana do recrutador;
- substituir o desenvolvimento real das competências identificadas como gaps.

O produto deve auxiliar o usuário a representar melhor sua realidade
profissional, não criar uma realidade profissional fictícia.

### 17.11 Evoluções futuras

Itens atualmente fora de escopo podem ser incorporados futuramente quando
existir necessidade demonstrada do produto.

Sua introdução deve:

1. preservar as invariantes existentes ou alterar explicitamente o contrato;
2. definir novas fontes e fronteiras quando necessário;
3. possuir critérios de aceite;
4. possuir estratégia de testes;
5. não reduzir silenciosamente garantias existentes.

Complexidade técnica adicional deve responder a uma necessidade concreta, e
não constituir objetivo por si mesma.

### 17.12 Definition of Done da transição

A transição Career Analysis → Targeted Resume somente pode ser considerada
concluída quando, no mínimo:

- o fluxo definido neste contrato estiver implementado;
- fontes factuais autorizadas forem utilizadas como única base de fatos
  profissionais;
- a vaga atuar apenas como contexto;
- Career Analysis atuar apenas dentro de sua classificação permitida;
- a composição básica for determinística e independente de IA;
- proveniência mínima estiver implementada;
- preview estiver implementado;
- aprovação explícita estiver implementada;
- persistência preservar conteúdo aprovado e proveniência;
- versões aprovadas não forem silenciosamente reescritas;
- ATS respeitar integridade factual;
- exportação operar sobre versão aprovada;
- autorização e isolamento estiverem protegidos;
- todas as invariantes obrigatórias possuírem testes automatizados;
- caminhos negativos críticos estiverem cobertos;
- validação funcional do fluxo estiver concluída;
- nenhuma violação conhecida de invariante obrigatória permanecer aberta.

Quantidade de código, número de endpoints, percentual de conclusão visual ou
existência de um caminho nominal funcional não substituem esses critérios.

### 17.13 Governança do contrato

Este documento é normativo para a implementação do fluxo de currículo
direcionado.

Quando uma mudança futura exigir comportamento incompatível com uma regra ou
invariante deste contrato, a mudança não deve ser resolvida silenciosamente
apenas no código.

O procedimento esperado é:

1. identificar o conflito;
2. revisar a justificativa da mudança;
3. alterar explicitamente o contrato quando a mudança for aceita;
4. atualizar os critérios e testes correspondentes;
5. somente então adaptar a implementação.

Testes não devem ser enfraquecidos apenas para acomodar comportamento que
continua proibido pelo contrato.

### 17.14 Precedência normativa

Para o fluxo de currículo direcionado, este contrato define o comportamento
alvo esperado.

O código existente representa o estado atual da aplicação e não deve ser
interpretado automaticamente como comportamento correto quando divergir deste
contrato.

Documentação anterior que descreva o estado atual também não substitui as
garantias normativas aqui estabelecidas.

Durante a implementação, divergências entre estado atual e estado alvo devem
ser tratadas explicitamente como gaps a resolver.

### 17.15 Alterações no contrato

Mudanças neste documento devem ser revisáveis e registradas no controle de
versão.

Alterações que afetem invariantes, fontes factuais, autorização, proveniência,
aprovação ou demais garantias críticas devem ser tratadas como mudanças
semânticas do contrato, e não apenas como correções editoriais.

Correções de redação que não alterem significado podem ser tratadas como
manutenção documental.

### 17.16 Regra final

Nenhuma funcionalidade, otimização ou evolução técnica do currículo
direcionado deve reduzir silenciosamente a confiança nas informações
profissionais apresentadas.

Quando houver conflito entre produzir um currículo mais convincente e
preservar um currículo demonstravelmente verdadeiro, o sistema deve preservar
a verdade demonstrável.
