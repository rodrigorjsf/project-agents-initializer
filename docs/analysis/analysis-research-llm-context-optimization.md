# Analise: Research LLM Context Optimization for AI Coding Agents

**Documento analisado**: `docs/research-llm-context-optimization.md`
**Documento complementar**: `docs/prompt-engineering-guide.md`
**Data da analise**: 27 de marco de 2026

---

## 1. Sumario Executivo

O documento **Research: LLM Context Optimization for AI Coding Agents** e uma sintese abrangente de pesquisas academicas, documentacao oficial da Anthropic e experiencia de praticantes sobre como otimizar o contexto fornecido a agentes de IA para codificacao. Sua contribuicao central e formalizar a ideia de que **contexto e um recurso finito com retornos marginais decrescentes** -- tratar cada token como precioso e curar agressivamente o contexto produz resultados dramaticamente melhores do que simplesmente preencher janelas de contexto grandes. O documento cobre sete areas de pesquisa: otimizacao de janela de contexto, orcamento de instrucoes, progressive disclosure, envenenamento de contexto, configuracao hierarquica/escopada, estruturacao de prompts para agentes, e documentacao just-in-time.

A forca do documento reside em sua capacidade de sintetizar fontes de primeira linha (blog de engenharia da Anthropic, papers academicos como "Lost in the Middle", documentacao oficial) em principios acionaveis e concretos. Ele nao apresenta pesquisa original, mas sim conecta evidencias dispersas em um framework coerente para autores de configuracao de agentes e arquitetos de sistemas agenticos. O resultado e um guia que transforma insight academico em recomendacoes praticas -- do limite de 200 linhas por arquivo de configuracao ate estrategias de compactacao de contexto.

A implicacao mais profunda do documento e a mudanca de paradigma de "prompt engineering" para "context engineering": a gestao holistica de todo o contexto que alimenta o modelo a cada passo, incluindo instrucoes, definicoes de ferramentas, memoria, resultados de acoes anteriores e saidas estruturadas. Esta transicao e o fio condutor que conecta todas as sete areas de pesquisa.

---

## 2. Achados e Principios Chave

### 2.1 Otimizacao de Janela de Contexto (Area 1)

#### O problema do "Context Rot"

O achado mais fundamental e que **LLMs perdem foco conforme o contexto cresce**, um fenomeno que a Anthropic formalizou como "context rot":

> "As the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases."

A causa arquitetural e clara: transformers criam **n^2 relacoes pareadas** para n tokens -- a atencao se "espalha" conforme o contexto cresce. O resultado nao e um penhasco abrupto, mas um **gradiente de performance** -- o modelo permanece capaz, mas com precisao reduzida.

**Principio derivado**: *"Good context engineering means finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."*

#### O efeito "Lost in the Middle"

O paper de Liu et al. (arXiv:2307.03172) demonstrou que:

- Performance e **mais alta quando informacao relevante esta no inicio ou no fim** do contexto
- Performance **degrada significativamente para informacao no meio** de contextos longos
- Isto vale **mesmo para modelos treinados especificamente para contextos longos**

**Implicacao para configuracao**: Instrucoes criticas devem estar no **inicio** dos arquivos de configuracao, com informacoes secundarias ao **final**. Nunca enterrar regras importantes no meio de documentos longos.

#### Vies de recencia (LongICLBench)

O benchmark LongICLBench (arXiv:2404.02060) confirmou um **vies em direcao a labels apresentados mais tarde nas sequencias** (recency bias). Modelos se saem bem em tarefas simples mas **lutam com tarefas complexas** (174 labels) mesmo dentro da janela de contexto.

#### Context Awareness (Claude 4.5+)

Claude Sonnet 4.5+ possui **consciencia de contexto embutida** -- o modelo rastreia seu orcamento de tokens restante durante a conversa. Analogia da Anthropic: *"For a model, lacking context awareness is like competing in a cooking show without a clock."*

### 2.2 Orcamento de Instrucoes (Area 2)

#### O conceito de "Attention Budget"

A Anthropic introduz o conceito de um **"orcamento de atencao"**:

> "LLMs have an 'attention budget' that they draw on when parsing large volumes of context. Every new token introduced depletes this budget by some amount."

Este nao e um limite rigido de tokens, mas uma funcao de:

| Fator | Impacto |
|-------|---------|
| Tamanho total do contexto | Mais tokens = menos atencao por instrucao |
| Especificidade da instrucao | Instrucoes vagas consomem atencao sem guiar comportamento |
| Conflitos entre instrucoes | Contradicoes causam comportamento arbitrario |

#### Limite pratico: ~200 linhas

A recomendacao explicita da Anthropic:

> **"Target under 200 lines per CLAUDE.md file."** Longer files consume more context and reduce adherence.

> "If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost."

O orcamento pratico de instrucoes por arquivo de configuracao e **~200 linhas (aproximadamente 2.000-4.000 tokens)**.

#### Heuristica de qualidade

> *"For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it."*

| Incluir | Excluir |
|---------|---------|
| Comandos bash que Claude nao pode adivinhar | Qualquer coisa que Claude descobre lendo o codigo |
| Regras de estilo que diferem dos padroes | Convencoes padrao que Claude ja conhece |
| Instrucoes de teste | Documentacao detalhada de API (linkar) |
| Etiqueta do repositorio | Informacao que muda frequentemente |
| Decisoes arquiteturais | Explicacoes longas ou tutoriais |
| Peculiaridades do ambiente de desenvolvimento | Descricoes arquivo-por-arquivo do codebase |
| Gotchas comuns | Praticas auto-evidentes como "escreva codigo limpo" |

#### Especificidade da instrucao

A "zona Goldilocks" entre dois modos de falha:

> "At one extreme, engineers hardcode complex, brittle logic. At the other extreme, engineers provide vague, high-level guidance... The optimal altitude strikes a balance."

Exemplos concretos:

- "Use 2-space indentation" vs. "Format code properly"
- "Run `npm test` before committing" vs. "Test your changes"
- "API handlers live in `src/api/handlers/`" vs. "Keep files organized"

### 2.3 Progressive Disclosure (Area 3)

#### Documentacao Just-In-Time

A Anthropic descreve formalmente a estrategia de contexto "just in time":

> "Rather than pre-processing all relevant data up front, agents built with the 'just in time' approach maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at runtime using tools."

A analogia com cognicao humana e poderosa:

> "We generally don't memorize entire corpuses of information, but rather introduce external organization systems like file systems, inboxes, and bookmarks to retrieve relevant information on demand."

#### Modelo hibrido (pre-carregado + sob demanda)

Claude Code implementa um sistema de duas camadas:

1. **Sempre carregado**: Regras criticas do projeto (CLAUDE.md) -- pequeno, essencial, sempre presente
2. **Sob demanda**: Documentacao detalhada, material de referencia -- carregado apenas quando relevante

> "CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time."

#### Skills como progressive disclosure

> "Claude sees skill descriptions at session start, but the full content only loads when a skill is used."

Features relevantes:

- `disable-model-invocation: true` -- mantem descricoes **fora do contexto** ate ativacao manual
- `context: fork` -- executa skill em **contexto isolado de subagente**
- Injecao dinamica com sintaxe `` !`command` `` -- busca dados frescos no momento da invocacao

#### Regras com escopo de caminho

```yaml
---
paths:
  - "src/api/**/*.ts"
---
# API Development Rules
- All API endpoints must include input validation
```

Regras com `paths` **disparam apenas quando Claude le arquivos correspondentes**, reduzindo ruido e economizando contexto.

#### Hierarquia de CLAUDE.md em subdiretorios

- **CLAUDE.md raiz**: Sempre carregado, regras do projeto inteiro
- **CLAUDE.md em subdiretorios**: Carregado sob demanda quando se trabalha naquela area
- **`~/.claude/CLAUDE.md`**: Sempre carregado, preferencias pessoais

### 2.4 Envenenamento de Contexto (Area 4)

#### Acumulo de abordagens falhas

> "Correcting over and over. Claude does something wrong, you correct it, it's still wrong, you correct again. Context is polluted with failed approaches."

> **Solucao**: "After two failed corrections, `/clear` and write a better initial prompt incorporating what you learned."

> "A clean session with a better prompt almost always outperforms a long session with accumulated corrections."

#### Anti-padrao "Kitchen Sink"

> "You start with one task, then ask Claude something unrelated, then go back to the first task. Context is full of irrelevant information."

#### Instrucoes contraditorias

> "If two rules contradict each other, Claude may pick one arbitrarily."

#### Documentacao desatualizada e pior que nenhuma

> "Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts."

Informacao que muda frequentemente e o vetor primario de envenenamento por documentacao desatualizada.

#### Configuracao hiper-especificada

> "The over-specified CLAUDE.md. If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise."

> **Solucao**: "Ruthlessly prune. If Claude already does something correctly without the instruction, delete it or convert it to a hook."

**Insight chave**: Converter instrucoes comportamentais em hooks deterministicos **remove-as do orcamento de contexto** enquanto garante enforcement.

### 2.5 Configuracao Escopada/Hierarquica (Area 5)

#### Hierarquia de cinco niveis do Claude Code

| Prioridade | Escopo | Localizacao | Compartilhado? |
|------------|--------|-------------|----------------|
| 1 (maior) | Managed | Nivel de sistema, MDM, servidor | Sim (IT) |
| 2 | CLI args | Linha de comando | Nao (sessao) |
| 3 | Local | `.claude/settings.local.json` | Nao (gitignored) |
| 4 | Projeto | `.claude/settings.json` | Sim (commitado) |
| 5 (menor) | Usuario | `~/.claude/settings.json` | Nao (pessoal) |

#### Sistema de regras modular

```
.claude/
  CLAUDE.md              # Instrucoes principais
  rules/
    code-style.md        # Diretrizes de estilo
    testing.md           # Convencoes de teste
    security.md          # Requisitos de seguranca
    frontend/
      react.md           # Regras especificas de frontend
```

Cada arquivo cobre **um topico**, e descoberto **recursivamente**, pode ter **escopo de caminho** com frontmatter YAML, e suporta **symlinks**.

#### Suporte a monorepos

`claudeMdExcludes` previne que configuracoes irrelevantes de outras equipes sejam carregadas:

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

### 2.6 Estruturacao Otima de Prompts para Agentes (Area 6)

#### Framework "Building Effective Agents" da Anthropic

Quatro padroes arquiteturais:

1. **Prompt Chaining**: Tarefas sequenciais com portoes de validacao
2. **Orchestrator-Workers**: LLM central decompoe tarefas e delega
3. **Evaluator-Optimizer**: Loop gerar -> avaliar -> refinar
4. **Subagent Architectures**: Janelas de contexto isoladas para trabalho focado

Tres principios fundamentais:
>
> 1. Manter **simplicidade** no design do agente
> 2. Priorizar **transparencia** mostrando explicitamente passos de planejamento
> 3. Projetar cuidadosamente a **ACI (agent-computer interface)**

#### O loop "Explore -> Plan -> Code -> Verify"

1. **Explore**: Entender o codebase
2. **Plan**: Criar estrategia (Plan Mode)
3. **Code**: Implementar a solucao
4. **Verify**: Rodar testes, comparar screenshots, validar saidas

> "Claude performs dramatically better when it can verify its own work."

#### Harnesses para agentes de longa duracao

Dois modos de falha criticos:

1. **One-shotting**: Agente tenta fazer tudo de uma vez, esgota o contexto
2. **Premature completion**: Agente ve progresso parcial e declara vitoria

**Solucao -- Arquitetura de dois agentes**:

| Agente | Papel |
|--------|-------|
| **Initializer** | Primeira sessao. Cria `init.sh`, `claude-progress.txt`, feature list (JSON), commit inicial |
| **Coding Agent** | Sessoes subsequentes. Progresso incremental, commits, atualizacoes de progresso |

**Tecnica chave -- Artefatos de estado estruturados**: Feature list em **JSON** (nao Markdown) -- o modelo tem menos tendencia a modificar JSON inapropriadamente.

#### Design de ferramentas como context engineering

> "Think about how much effort goes into human-computer interfaces (HCI), and plan to invest just as much effort in creating good agent-computer interfaces (ACI)."

Principios:

- Manter formato proximo do que modelos viram nos dados de treinamento
- Evitar overhead de formatacao (contar linhas, escapar strings)
- Dar ao modelo tokens para "pensar" antes de se comprometer com estrutura
- Descricoes de ferramentas devem incluir exemplos de uso, edge cases e limites claros

### 2.7 Documentacao Just-In-Time (Area 7)

#### Padroes de implementacao

| Padrao | Mecanismo | Exemplo |
|--------|-----------|---------|
| **Skills** | Descricao carregada; conteudo completo sob demanda | `.claude/skills/deploy/SKILL.md` |
| **Regras com escopo** | Disparadas quando arquivos correspondentes sao lidos | `.claude/rules/api-design.md` com `paths: ["src/api/**"]` |
| **CLAUDE.md em subdiretorios** | Carregado quando se trabalha naquele diretorio | `packages/frontend/CLAUDE.md` |
| **Imports de arquivos** | Referencias `@path` expandidas quando pai carrega | `@docs/git-instructions.md` |
| **Injecao dinamica** | Comandos shell em skills: `` !`gh pr diff` `` | Dados em tempo real na invocacao |
| **Subagentes** | Contexto isolado, retornam resumos | Agente de exploracao para pesquisa no codebase |
| **Auto memory** | Primeiras 200 linhas carregadas; arquivos de topicos sob demanda | `~/.claude/projects/<project>/memory/` |

#### Auto Memory como JIT emergente

- **MEMORY.md** (primeiras 200 linhas carregadas na inicializacao) funciona como um indice
- **Arquivos de topico** (debugging.md, api-conventions.md, etc.) carregados sob demanda
- Claude decide o que vale lembrar com base no valor cross-sessao
- Markdown puro -- editavel por humanos a qualquer momento

#### Compactacao como reciclagem de contexto

> "Passing the message history to the model to summarize and compress the most critical details. The model preserves architectural decisions, unresolved bugs, and implementation details while discarding redundant tool outputs."

Customizavel via CLAUDE.md e via `/compact <instructions>`.

#### A citacao de Boris Cherny sobre simplicidade

> "We had all these crazy ideas about memory architectures... But in the end, the thing we did is ship the simplest thing, which is a file that has some stuff."

> "When the model is so good, the simple thing usually works."

---

## 3. Pontos de Atencao

### 3.1 O que e facil perder ou interpretar erroneamente

1. **O limite de 200 linhas e empirico, nao experimental**. Nao existe pesquisa publicada que de numeros exatos para "quantas instrucoes um LLM pode seguir simultaneamente". O numero e derivado da experiencia pratica da Anthropic, nao de estudos controlados. Isso significa que o limite real pode variar por modelo, tarefa e complexidade das instrucoes.

2. **"Context rot" e um gradiente, nao um penhasco**. Muitos lerao o conceito e assumirao que existe um ponto de corte abrupto. Na verdade, a degradacao e gradual -- o modelo permanece capaz, mas com precisao reduzida. Isso torna o problema mais insidioso: nao ha sinal obvio de quando o contexto ficou "grande demais".

3. **Hooks e CLAUDE.md nao sao intercambiaveis**. O documento menciona que converter instrucoes comportamentais em hooks remove-as do orcamento de contexto. Mas hooks sao **deterministicos** e CLAUDE.md e **consultivo**. Isso significa que hooks garantem enforcement mas nao permitem julgamento, enquanto CLAUDE.md permite flexibilidade mas nao garante aderencia. A escolha entre os dois e uma decisao de design, nao simplesmente uma questao de economizar tokens.

4. **O efeito "Lost in the Middle" tem implicacoes nao-obvias para configuracao hierarquica**. Quando multiplos CLAUDE.md sao mesclados (raiz + subdiretorios + regras), o conteudo do "meio" pode ser justamente o material carregado por subdiretorios ou regras que foram injetados entre o cabecalho e o rodape. Isso sugere que a **ordem de injecao** de contexto e tao importante quanto o **conteudo**.

5. **A estrategia "hibrida" tem uma tensao inerente**. Pre-carregar CLAUDE.md "ingenuamente" na inicializacao (como descrito pelo documento) contradiz parcialmente o principio de JIT. O arquivo pre-carregado consome orcamento em todas as interacoes, mesmo quando irrelevante. A mitigacao e mante-lo curto, mas a tensao permanece.

6. **Compactacao nao e lossless**. Quando Claude resume o historico de mensagens, informacoes podem ser perdidas. A customizacao via CLAUDE.md (ex: "sempre preservar a lista de arquivos modificados") e uma mitigacao parcial, mas nao e possivel garantir preservacao completa de todo o contexto relevante.

7. **A recomendacao de "comecar do zero" presume filesystem como estado**. O conselho de que Claude 4.5+ e excelente em redescobrir estado a partir do filesystem so funciona se o estado relevante estiver efetivamente persistido no filesystem. Projetos que dependem de estado em memoria, variaveis de ambiente, ou configuracoes de sessao nao se beneficiam da mesma forma.

8. **Artefatos de estado em JSON vs Markdown nao e apenas preferencia de formato**. O documento explica que feature lists em JSON sao menos propensas a modificacao inapropriada pelo modelo. Isso aponta para uma propriedade mais ampla: **o formato do artefato influencia o comportamento do modelo em relacao a ele**. JSON e mais "rigido" perceptivamente, fazendo o modelo tratar os dados com mais cuidado.

---

## 4. Casos de Uso e Escopo

### 4.1 Context Engineering

O documento se aplica diretamente a qualquer profissional que projete o contexto fornecido a LLMs:

- **Autores de system prompts**: Os principios de orcamento de atencao, posicionamento de informacao (inicio/fim) e especificidade se aplicam diretamente
- **Arquitetos de pipelines RAG**: A estrategia hibrida (pre-carregado + sob demanda) e um padrao direto para RAG agentico
- **Engenheiros de ferramentas de IA**: O design de ACI e a eficiencia de tokens em saidas de ferramentas sao guias concretos

### 4.2 Design de Agentes

O documento e altamente relevante para:

- **Escolha entre agente unico e multi-agentes**: Os padroes da Anthropic (prompt chaining, orchestrator-workers, evaluator-optimizer, subagentes) fornecem um framework de decisao
- **Gerenciamento de sessoes longas**: A arquitetura de dois agentes (Initializer + Coding Agent) e as estrategias de compactacao sao diretamente implementaveis
- **Prevencao de modos de falha**: One-shotting e premature completion sao padroes anti-padroes concretos para monitorar

### 4.3 Autoria de Configuracao de Agentes

Este e o caso de uso mais direto:

- **Criacao de CLAUDE.md / AGENTS.md**: Limite de 200 linhas, heuristica de "removeria isso?", tabela include/exclude
- **Estruturacao de repositorios**: Hierarquia de configuracao, regras escopadas, subdiretorios
- **Manutencao de configuracao**: Revisao periodica, poda de instrucoes desatualizadas, deteccao de contradicoes

### 4.4 Onde o documento NAO se aplica

- **Treinamento ou fine-tuning de modelos**: O documento trata exclusivamente de otimizacao em tempo de inferencia
- **Modelos de raciocinio avancado** (o1, R1): O prompt engineering guide mostra que estes modelos frequentemente performam pior com tecnicas classicas; o documento de pesquisa nao aborda essa distincao
- **Linguagens pouco representadas nos dados de treinamento**: O documento reconhece a lacuna, e o paper Evaluating-AGENTS confirma que Python (bem representado) pode tornar context files menos necessarios
- **Avaliacao quantitativa rigorosa**: O documento sintetiza recomendacoes, mas nao conduz experimentos controlados

---

## 5. Aplicabilidade a Infraestrutura de Agentes

### 5.1 Skills

**Como a otimizacao de contexto afeta o design de skills:**

Skills sao o mecanismo mais puro de progressive disclosure identificado no documento. As implicacoes concretas para design de skills:

1. **Descricoes de skills devem ser minimas e de alta-sinalizacao**. Como descricoes sao carregadas na inicializacao da sessao, cada token compete com o orcamento de atencao. A descricao ideal usa 1-2 frases que permitem ao modelo decidir **quando** invocar a skill, sem revelar **como** ela funciona.

2. **Use `disable-model-invocation: true` para skills de baixa frequencia**. Skills que sao invocadas raramente (ex: deploy, migracao de banco) devem ficar completamente fora do contexto automatico. Isso economiza orcamento para skills mais frequentes.

3. **Use `context: fork` para skills que geram muita saida**. Skills de exploracao de codebase ou pesquisa que leem muitos arquivos devem rodar em contexto isolado de subagente. A saida retorna como resumo, protegendo o contexto principal de "context rot" por acumulo de saidas.

4. **Injecao dinamica (`` !`command` ``) e JIT puro**. Para skills que dependem de estado atual (ex: diff do PR, status de CI), use comandos shell inline que buscam dados frescos no momento da invocacao. Isso evita documentacao desatualizada.

5. **Estruture skills em camadas de progressive disclosure**:
   - **SKILL.md**: Ponto de entrada minimo com instrucoes de fase
   - **references/**: Guias de analise carregados sob demanda por fase
   - **assets/templates/**: Templates de saida carregados apenas na fase de geracao

6. **Posicione instrucoes criticas no inicio e fim de SKILL.md** (efeito "Lost in the Middle"). O meio do arquivo deve conter contexto de suporte, nao regras obrigatorias.

### 5.2 Hooks

**Convertendo instrucoes comportamentais em hooks deterministicos:**

O insight mais acionavel do documento para hooks:

> "If Claude already does something correctly without the instruction, delete it or convert it to a hook."

Orientacoes concretas:

1. **Identifique instrucoes de enforcement em CLAUDE.md que devem ser garantidas**. Qualquer regra que diz "SEMPRE faca X" ou "NUNCA faca Y" e candidata a hook. Exemplos: "sempre rode linter antes de commit", "nunca commite .env files".

2. **Hooks removem instrucoes do orcamento de atencao**. Cada instrucao convertida em hook libera linhas do limite de ~200 linhas. Em projetos com muitas regras de enforcement, isso pode liberar dezenas de linhas para instrucoes que realmente precisam de julgamento do modelo.

3. **Hooks sao deterministicos, CLAUDE.md e consultivo**. Use hooks para regras binarias (faz/nao faz) e CLAUDE.md para heuristicas que exigem julgamento (ex: "quando o teste for complexo, considere mockar dependencias externas").

4. **Hooks de pre-commit sao os candidatos mais naturais**. Validacao de formato, execucao de linters, verificacao de tipos -- tudo que pode ser expresso como script e mais confiavel como hook do que como instrucao textual.

5. **Documente hooks minimamente no CLAUDE.md**. Uma unica linha como "hooks de pre-commit verificam formatacao e tipos automaticamente" e suficiente para que o modelo saiba que nao precisa fazer essas verificacoes manualmente.

### 5.3 Subagentes

**Isolamento de contexto e trabalho focado:**

1. **Subagentes previnem context rot no contexto principal**. Ao delegar tarefas exploratoras ou de pesquisa a subagentes, o contexto principal permanece limpo e focado na tarefa atual. O subagente retorna apenas um resumo, nao todo o material bruto que processou.

2. **Cada subagente deve receber contexto minimo e especifico**. Nao repassar todo o CLAUDE.md do projeto para um subagente de pesquisa. Dar apenas a pergunta, o escopo, e as ferramentas necessarias.

3. **Use subagentes para a fase "Explore" do loop Explore -> Plan -> Code -> Verify**. A exploracao do codebase e a atividade que mais gera "lixo de contexto" -- leitura de muitos arquivos, grep de multiplos padroes. Isolar isso em subagente protege o contexto de implementacao.

4. **Subagentes devem retornar artefatos estruturados, nao narrativas longas**. Um resumo de 5-10 linhas com paths relevantes, padroes encontrados e decisoes sugeridas e mais util ao contexto principal do que um relatorio detalhado de 200 linhas.

5. **Cuidado com over-delegation**. O documento de prompting best practices alerta:
   > "Claude Opus 4.6 has a strong predilection for subagents and may spawn them in situations where a simpler, direct approach would suffice."

6. **Use role prompting para especializar subagentes**. Cada subagente deve receber uma persona especifica via system prompt. Do guia de prompt engineering:
   > "Role prompting e o mecanismo fundamental de especializacao em arquiteturas multi-agentes."

### 5.4 Rules (.claude/rules/)

**Regras com escopo de caminho como progressive disclosure:**

1. **Regras sem `paths` frontmatter carregam incondicionalmente** -- sao equivalentes a linhas no CLAUDE.md raiz. Use `paths` sempre que a regra se aplica apenas a parte do codebase.

2. **Organize regras por topico, nao por arquivo**. Um arquivo `security.md` que cobre todas as regras de seguranca e melhor que regras de seguranca espalhadas por `api.md`, `frontend.md`, `database.md`.

3. **Regras sao a forma mais granular de progressive disclosure**. Enquanto subdiretorios CLAUDE.md carregam por area, regras com paths podem ser tao especificas quanto `"src/api/v2/handlers/**/*.ts"`.

4. **Use regras para mover instrucoes do CLAUDE.md raiz**. Se o CLAUDE.md raiz esta perto do limite de 200 linhas, mover instrucoes especificas de area para `.claude/rules/` com frontmatter de paths e a forma mais direta de reduzir o tamanho.

5. **Revise regras periodicamente para detectar contradicoes**. Conforme regras sao adicionadas por diferentes desenvolvedores, contradicoes se acumulam. O documento alerta:
   > "Review your CLAUDE.md files, nested CLAUDE.md files in subdirectories, and `.claude/rules/` periodically to remove outdated or conflicting instructions."

6. **Regras com escopo implementam o principio JIT da pesquisa**. Regras so aparecem no contexto quando o modelo toca arquivos relevantes -- e exatamente o padrao "manter identificadores leves e carregar dados dinamicamente em runtime".

### 5.5 Memory

**Auto memory como documentacao JIT e estrategias de compactacao:**

1. **MEMORY.md como indice, nao como enciclopedia**. As primeiras 200 linhas sao carregadas na inicializacao -- use-as como indice para arquivos de topico que serao carregados sob demanda. Nao coloque conteudo detalhado nas primeiras 200 linhas.

2. **Arquivos de topico sao JIT puro**. `debugging.md`, `api-conventions.md`, `architecture-decisions.md` -- cada um carregado apenas quando Claude decide que e relevante. Isso implementa progressive disclosure para conhecimento acumulado cross-sessao.

3. **Compactacao deve preservar artefatos criticos**. Adicione ao CLAUDE.md instrucoes como:
   > "When compacting, always preserve the full list of modified files and any test commands"

4. **Compactacao seletiva via `/compact <instructions>`** permite focar a preservacao em aspectos especificos:
   - `/compact Focus on the API changes` -- preserva mudancas de API
   - `/compact Keep the debugging findings` -- preserva achados de debugging

5. **Prefira sessao limpa quando possivel**. O documento recomenda:
   > "Start fresh rather than compact when possible -- Claude 4.5+ excels at rediscovering state from filesystem."

6. **A simplicidade vence**. Boris Cherny demonstrou que as solucoes mais simples (arquivo de texto para memoria, sumarizacao para compactacao) superam arquiteturas sofisticadas quando o modelo e suficientemente capaz. Resista a tentacao de criar sistemas de memoria complexos.

---

## 6. Aplicabilidade do Guia de Prompt Engineering

### 6.1 Chain-of-Thought (CoT) e Context Engineering

CoT e diretamente relevante para agentes de codificacao nos seguintes cenarios:

- **Fase "Plan" do loop Explore -> Plan -> Code -> Verify**: CoT estruturado (com tags `<thinking>` e `<answer>`) e a tecnica ideal para a fase de planejamento. O modelo externaliza seu raciocinio, criando um plano inspecionavel.

- **Compactacao inteligente**: Ao compactar contexto, o modelo usa implicitamente CoT para decidir o que preservar. Instrucoes de compactacao no CLAUDE.md podem ser vistas como "prompt de CoT para sumarizacao".

- **Limitacao critica**: CoT explicitamente pedido pode ser **contraproducente com modelos de raciocinio avancados**. Um estudo da Wharton (2025) encontrou apenas 2-3% de melhoria marginal com 20-80% de aumento no tempo de resposta. Em agentes que usam Claude Opus 4.6 com adaptive thinking, **nao instrua CoT explicito** -- o modelo ja raciocina internamente.

- **Performance degrada apos ~3.000 tokens** de raciocinio (Levy, Jacoby & Goldberg, 2024). Isso tem implicacao direta para configuracao de agentes: prompts de planejamento complexos nao devem incentivar cadeias de raciocinio infinitas.

### 6.2 ReAct e Agentes de Codificacao

ReAct (Pensamento -> Acao -> Observacao) e **o padrao fundamental dos agentes de IA modernos**:

- **Claude Code ja implementa ReAct nativamente**. O loop agentico do Claude Code (gather context -> take action -> verify results) e uma instancia de ReAct. Isso significa que a configuracao do agente deve **facilitar** o ciclo, nao tentar substitui-lo.

- **Implicacao para CLAUDE.md**: Instrucoes devem ser orientadas a acao, nao descritivas. Em vez de explicar a arquitetura do projeto, fornecer **comandos acionaveis** que o agente pode executar no ciclo ReAct (ex: "para verificar tipos, rode `npm run typecheck`").

- **Ferramentas bem projetadas sao a outra metade do ReAct**. O guia de prompt engineering enfatiza: *"A medida que o numero de ferramentas cresce, modelos cometem mais erros."* Isso valida a recomendacao do documento de pesquisa de manter conjuntos de ferramentas **minimos, claros e nao-sobrepostos**.

### 6.3 Tree of Thoughts (ToT) e Planejamento de Agentes

ToT e relevante para cenarios especificos de agentes:

- **Resolucao de problemas complexos com backtracking**: Quando um agente encontra um bug que pode ter multiplas causas raiz, ToT permite explorar caminhos diferentes e voltar atras. No entanto, o custo e 5-20x mais chamadas de API.

- **Aplicacao pratica em context engineering**: ToT pode ser usado na fase de **planejamento** para gerar e avaliar multiplas estrategias de implementacao antes de se comprometer com uma. Isso alinha-se com o principio "separar exploracao de execucao".

- **Limitacao**: Para a maioria das tarefas de codificacao (que sao lineares e nao requerem backtracking), ToT e overkill. CoT ou zero-shot sao suficientes.

### 6.4 Self-Consistency e Verificacao

Self-Consistency (votar entre multiplos caminhos de raciocinio) tem aplicacao direta em context engineering:

- **Validacao de planos**: Gerar 3-5 planos de implementacao diferentes e selecionar o mais consistente antes de executar. Isso implementa o principio "verificar o proprio trabalho".

- **Reducao de alucinacoes**: Em tarefas de pesquisa agentica, Self-Consistency pode reduzir informacoes fabricadas ao exigir concordancia entre multiplas tentativas.

- **Trade-off de custo**: Multiplica o custo de tokens pelo numero de amostras (5-30x). Em agentes com orcamento de tokens limitado, use apenas para decisoes de alto impacto (ex: escolha de arquitetura, nao formatacao de codigo).

### 6.5 Least-to-Most e Decomposicao de Tarefas

Least-to-Most prompting (decompor problemas complexos em subproblemas simples) e diretamente implementado em patterns de agentes:

- **Prompt Chaining da Anthropic** e uma implementacao de Least-to-Most. A saida de um passo alimenta o proximo, e cada passo e um subproblema mais simples.

- **Para skills complexas**: Estruturar a skill em fases progressivas (fase 1: analise, fase 2: planejamento, fase 3: execucao) e aplicar Least-to-Most naturalmente.

- **Para harnesses de longa duracao**: A arquitetura "Initializer + Coding Agent" e Least-to-Most aplicado ao nivel de sessoes: a primeira sessao decompoe o problema, sessoes subsequentes resolvem um pedaco de cada vez.

### 6.6 PAL (Program-Aided Language Models) e Execucao de Codigo

PAL transforma raciocinio em codigo executavel. Implicacoes:

- **Agentes de codificacao ja implementam PAL nativamente**. Quando Claude Code escreve e executa um script para verificar uma hipotese, esta usando PAL.

- **Artefatos de estado em JSON** (recomendacao do documento) alinham-se com PAL: dados estruturados que podem ser lidos e manipulados programaticamente, nao prosa que precisa ser interpretada.

- **Tools como PAL amplificado**: O design de ferramentas do documento (manter formato proximo do treinamento, dar tokens para pensar antes de estruturar) e um refinamento do principio PAL aplicado a ACI.

### 6.7 Reflexion e Auto-Correcao

Reflexion (o agente reflete sobre fracassos e ajusta a estrategia) conecta-se diretamente a:

- **O ciclo Evaluator-Optimizer**: Gerar -> avaliar -> refinar e Reflexion aplicado a nivel de arquitetura.

- **Compactacao como Reflexion** parcial: Quando o modelo sumariza o historico, ele implicitamente reflete sobre o que foi importante e o que nao foi.

- **Prevencao de "accumulated failed approaches"**: O documento recomenda `/clear` apos duas correcoes falhas. Reflexion estruturada (anotar o que falhou e por que antes de recomecar) seria mais eficaz do que simplesmente limpar o contexto.

- **Auto memory como Reflexion persistente**: Quando Claude salva aprendizados em MEMORY.md cross-sessao, esta implementando Reflexion que persiste alem de uma sessao individual.

---

## 7. Correlacoes com Outros Documentos Principais

### 7.1 Evaluating-AGENTS-paper.md

O paper da ETH Zurich fornece **validacao empirica** dos principios do documento de pesquisa, mas tambem **desafia algumas suposicoes**:

**Validacoes:**

- O achado de que context files gerados por LLM **reduzem** performance em 3% na media confirma diretamente o aviso sobre envenenamento de contexto e documentacao desnecessaria: *"unnecessary requirements from context files make tasks harder."*
- O aumento de custo de **20%+** com context files confirma que tokens adicionais consomem orcamento de atencao sem retorno proporcional.
- A constatacao de que instrucoes sao **geralmente seguidas** (ex: `uv` usado 1.6x/instancia quando mencionado vs. 0.01x quando nao) valida que o orcamento de atencao funciona -- instrucoes sao processadas, mas a pergunta e se elas **ajudam**.

**Desafios e nuances:**

- Context files de **desenvolvedores humanos** tiveram ganho marginal de ~4%, enquanto o documento de pesquisa sugere que configuracao bem feita deveria ter impacto significativo. Isso sugere que o gap entre teoria e pratica e maior do que o documento admite.
- A conclusao do paper de que "context files do not provide effective overviews" contradiz a recomendacao do documento de incluir descricao do projeto. Porem, o paper testa overviews longos (media de 641 palavras, ate 29 secoes), nao o "one-liner" recomendado pelo guia a-guide-to-agents.
- O achado de que context files **aumentam exploracao e teste** mesmo sem melhorar a taxa de resolucao sugere que os principios de context engineering do documento podem precisar de uma dimensao adicional: **custo-efetividade da exploracao induzida**.

**Implicacao pratica**: O documento de pesquisa e o paper de avaliacao convergem na recomendacao de **minimalismo** -- apenas context files humanos, minimais, focados em requisitos especificos (tooling, comandos nao-obvios) mostram beneficio liquido.

### 7.2 a-guide-to-agents.md

Este guia e a **implementacao pratica direta** dos principios do documento de pesquisa. As correlacoes sao quase 1:1:

| Principio do documento de pesquisa | Recomendacao do guia a-guide-to-agents |
|-------------------------------------|----------------------------------------|
| Limite de ~200 linhas / orcamento de instrucoes | "~150-200 instructions with reasonable consistency" |
| Progressive disclosure JIT | "give the agent only what it needs right now" |
| Documentacao desatualizada envenena | "stale information actively poisons the context" |
| Especificidade da instrucao | "no 'always,' no all-caps forcing. Just a conversational reference" |
| Skills como progressive disclosure | "agent skills: the agent pulls in knowledge only when needed" |
| Hierarquia de configuracao | Monorepo AGENTS.md em subdiretorios |
| Nao auto-gerar | "Never use initialization scripts to auto-generate your AGENTS.md" |

A correlacao mais importante e a validacao mutua do conceito de **instruction budget**: ambos os documentos convergem em ~150-200 como o limite pratico, embora nenhum cite evidencia experimental direta.

O guia adiciona um insight nao presente no documento de pesquisa: **descrever capacidades em vez de estrutura de arquivos**. *"Instead of documenting structure, describe capabilities."* Isso e uma aplicacao do principio de evitar documentacao que muda frequentemente.

### 7.3 a-guide-to-claude.md

Este documento e essencialmente o mesmo que a-guide-to-agents mas especifico para Claude Code. As correlacoes adicionais relevantes:

- **Prompt de refatoracao de CLAUDE.md**: O guia fornece um prompt concreto para refatorar CLAUDE.md seguindo principios de progressive disclosure (encontrar contradicoes -> identificar essenciais -> agrupar o resto -> criar estrutura de arquivos). Isso e uma implementacao pratica da recomendacao do documento de pesquisa de "revisar e podar regularmente".

- **Hierarquia CLAUDE.md em monorepos**: O padrao Raiz + Package alinha-se com a hierarquia de cinco niveis documentada na pesquisa, mas com foco na perspectiva do usuario, nao da arquitetura do sistema.

### 7.4 claude-prompting-best-practices.md

Este documento da Anthropic e a **fonte primaria** para varias recomendacoes do documento de pesquisa. Correlacoes profundas:

**Posicionamento de informacao:**

- Pesquisa: "Put the most critical instructions at the start"
- Prompting: *"Put longform data at the top... Queries at the end can improve response quality by up to 30%."*

**XML tags para estruturacao:**

- Pesquisa: Usa XML como formato preferido para delimitacao
- Prompting: *"XML tags help Claude parse complex prompts unambiguously"* -- e um principio de design de prompt que se aplica diretamente a estruturacao de CLAUDE.md e skills

**Subagentes:**

- Pesquisa: Subagentes para isolamento de contexto
- Prompting: *"Claude Opus 4.6 has a strong predilection for subagents and may spawn them in situations where a simpler, direct approach would suffice."* -- Um aviso pratico que complementa a recomendacao teorica

**Multi-context window:**

- Pesquisa: Arquitetura Initializer + Coding Agent
- Prompting: Fornece implementacao detalhada com `tests.json`, `progress.txt`, `init.sh`, e git como mecanismo de rastreamento de estado. Adiciona o detalhe critico de que *"It is unacceptable to remove or edit tests."*

**Adaptive thinking vs CoT explicito:**

- Pesquisa: Recomenda separacao de raciocinio com tags `<thinking>` e `<answer>`
- Prompting: Claude 4.6 usa **adaptive thinking** que torna CoT explicito redundante. *"Prefer general instructions over prescriptive steps."* Isso atualiza a recomendacao da pesquisa para modelos mais recentes.

**Overengineering:**

- Pesquisa: Principio de simplicidade ("maintain simplicity")
- Prompting: *"Claude Opus 4.5 and Claude Opus 4.6 have a tendency to overengineer."* Fornece prompt concreto para mitigar, complementando o principio teorico com implementacao pratica.

---

## 8. Forcas e Limitacoes

### 8.1 Forcas

1. **Fontes de alta autoridade**. O documento baseia-se primariamente em pesquisa de primeira linha da Anthropic (criadores do Claude), papers academicos publicados (TACL, NeurIPS, ICLR), e documentacao oficial. Isso da peso as recomendacoes.

2. **Sintese coerente de fontes dispersas**. A principal contribuicao e conectar pesquisa academica (Lost in the Middle, LongICLBench), engenharia pratica (blog da Anthropic), e documentacao oficial em um framework unico e acionavel.

3. **Princípios acionáveis**. Cada secao termina com implicacoes praticas. A tabela include/exclude, o limite de 200 linhas, os padroes de implementacao JIT -- tudo e diretamente implementavel.

4. **Cobertura abrangente**. As sete areas de pesquisa cobrem desde fundamentos teoricos (por que contexto degrada) ate implementacao pratica (como configurar .claude/rules/). Pouco e deixado sem abordagem.

5. **Reconhecimento explicito de lacunas**. O documento honestamente lista seis areas que carecem de pesquisa formal, incluindo a base empirica do limite de 200 linhas e estudos formais de envenenamento de contexto.

6. **Indice de fontes organizado**. A tabela de fontes com URLs, tipos e autoridade facilita verificacao e aprofundamento.

### 8.2 Limitacoes

1. **Nenhuma pesquisa original**. O documento e uma sintese, nao um estudo. Nao conduz experimentos, nao apresenta dados novos, nao valida quantitativamente suas recomendacoes. A forca de suas conclusoes depende inteiramente das fontes citadas.

2. **Vies em direcao ao ecossistema Anthropic/Claude**. A maioria das fontes e recomendacoes e especifica para Claude Code e CLAUDE.md. Generalizacao para outros agentes (Codex, Qwen Code, Aider) nao e validada.

3. **O limite de 200 linhas carece de fundamentacao experimental**. O proprio documento admite: *"No published research gives exact numbers for 'how many instructions can an LLM follow simultaneously.'"* Este e o achado mais citavel do documento e, ironicamente, o menos fundamentado.

4. **Ausencia de analise de custo-beneficio**. O documento recomenda progressive disclosure, subagentes, skills, etc., mas nao analisa o custo de implementacao e manutencao dessas estrategias. Para equipes pequenas, a complexidade adicional pode nao compensar.

5. **Data de publicacao e contexto temporal**. Como sintese de pesquisas de 2024-2026, algumas recomendacoes podem se tornar obsoletas com novos modelos. O documento nao aborda como lidar com evolucoes de modelo (ex: Claude 4.6 com adaptive thinking torna CoT explicito contraproducente).

6. **Foco em Python e projetos de codigo aberto**. O paper Evaluating-AGENTS confirmou que resultados em Python (bem representado no treinamento) podem nao generalizar para linguagens menos comuns. O documento de pesquisa nao aborda essa limitacao.

7. **Ausencia de estudo comparativo de abordagens de configuracao**. O documento cita como lacuna a falta de comparacao sistematica entre configuracao flat vs. hierarquica vs. escopada por caminho, mas tambem nao oferece evidencia para preferir uma sobre outra alem de raciocinios logicos.

8. **Coordenacao multi-agente nao resolvida**. O documento reconhece que compartilhamento eficiente de contexto entre agentes paralelos e uma area aberta, mas oferece poucas orientacoes praticas para cenarios multi-agente complexos.

---

## 9. Recomendacoes Praticas

### 9.1 Para autores de configuracao (CLAUDE.md / AGENTS.md)

| # | Recomendacao | Fundamento |
|---|-------------|------------|
| 1 | **Mantenha sob 200 linhas** por arquivo de configuracao | Orcamento de atencao empirico da Anthropic |
| 2 | **Posicione instrucoes criticas no inicio e no fim** | Efeito "Lost in the Middle" (Liu et al.) |
| 3 | **Seja especifico e verificavel**: "Use 2-space indentation" vs. "Format code nicely" | Zona Goldilocks de especificidade |
| 4 | **Remova qualquer coisa que o modelo ja sabe**: nao ensine convencoes padrao | Heuristica "removeria isso causa erros?" |
| 5 | **Converta instrucoes de enforcement em hooks** quando o cumprimento deve ser garantido | Hooks sao deterministicos e nao consomem orcamento de contexto |
| 6 | **Revise e pode regularmente**: trate configuracao como codigo | Documentacao desatualizada envenena contexto |
| 7 | **Use hierarquia**: raiz para regras universais, subdiretorios para regras de area, `.claude/rules/` para topicos especificos | Hierarquia de cinco niveis + progressive disclosure |
| 8 | **Descreva capacidades, nao estrutura de arquivos** | Caminhos mudam constantemente; capacidades sao estaveis |
| 9 | **Nunca auto-gere CLAUDE.md/AGENTS.md** | Paper ETH Zurich: LLM-generated files reduzem performance em 3% |
| 10 | **Detecte e resolva contradicoes** periodicamente entre CLAUDE.md, subdiretorios e rules | Contradicoes causam comportamento arbitrario |

### 9.2 Para arquitetos de sistemas agenticos

| # | Recomendacao | Fundamento |
|---|-------------|------------|
| 1 | **Separe exploracao de execucao**: planeje primeiro, codifique depois | Loop Explore -> Plan -> Code -> Verify |
| 2 | **Use subagentes para investigacao**: mantenha o contexto principal limpo | Isolamento de contexto previne context rot |
| 3 | **Implemente progressive disclosure**: carregue documentacao apenas quando relevante | Estrategia hibrida pre-carregado + sob demanda |
| 4 | **Projete para progresso incremental**: uma feature por vez em tarefas longas | Arquitetura Initializer + Coding Agent |
| 5 | **Forneca mecanismos de verificacao**: testes, screenshots, linters | "Claude performs dramatically better when it can verify its own work" |
| 6 | **Use artefatos de estado estruturados**: JSON para estado de maquina, markdown para prosa | Modelos modificam JSON com mais cuidado |
| 7 | **Limpe contexto entre tarefas nao-relacionadas** | Anti-padrao "kitchen sink" |
| 8 | **Prefira sessao limpa quando possivel**: Claude 4.5+ redescobre estado do filesystem | Compactacao e lossy; filesystem e duravel |
| 9 | **Invista em ACI tanto quanto em HCI**: ferramentas com descricoes claras, exemplos, limites definidos | "If a human engineer can't say which tool, an AI can't either" |
| 10 | **Comece simples e so aumente complexidade quando demonstravelmente necessario** | Principio dominante da Anthropic ("simplest thing usually works") |

### 9.3 Para context engineering em geral

| # | Recomendacao | Fundamento |
|---|-------------|------------|
| 1 | **Trate contexto como recurso finito precioso** com retornos decrescentes | Principio central do documento |
| 2 | **Cure o menor conjunto de tokens de alta-sinalizacao** para cada interacao | "smallest possible set of high-signal tokens" |
| 3 | **Dados longos no topo, queries no final** | Melhoria de ate 30% na qualidade (Anthropic) |
| 4 | **Use XML tags** para delimitar secoes de prompts complexos | Claude treinado para reconhecer XML; 15-20% boost |
| 5 | **Implemente compactacao** para sessoes longas, preservando artefatos criticos | Reciclagem de contexto evita acumulo |
| 6 | **Projete ferramentas para serem eficientes em tokens** nas suas saidas | Saidas de ferramentas competem com orcamento |
| 7 | **Deixe agentes navegar metadados** (nomes de arquivo, estrutura de pastas) antes de carregar conteudo completo | Progressive disclosure via exploracao |
| 8 | **Nao use CoT explicito com modelos de raciocinio avancado** (Claude 4.6 com adaptive thinking) | CoT explicito e redundante e pode prejudicar |
| 9 | **Teste e meca**: otimizacao automatica de prompts supera otimizacao manual | APE, OPRO, DSPy produzem resultados melhores |
| 10 | **Monitore o custo total**: o prompt otimizado pode custar 70% menos que o naive com qualidade igual ou superior | Levy, Jacoby & Goldberg (2024): sweet spot ~150-300 palavras |

---

## Apendice: Mapa de Fontes Citadas no Documento

| # | Fonte | Tipo | Relevancia |
|---|-------|------|-----------|
| 1 | Effective Context Engineering for AI Agents (Anthropic) | Blog de Engenharia | Central -- define context rot, attention budget, JIT, progressive disclosure |
| 2 | Effective Harnesses for Long-Running Agents (Anthropic) | Blog de Engenharia | Arquitetura Initializer + Coding Agent, artefatos de estado |
| 3 | Building Effective Agents (Anthropic Research) | Pesquisa | Padroes arquiteturais (chaining, orchestrator-workers, evaluator-optimizer) |
| 4 | Claude Code Best Practices (Anthropic Docs) | Documentacao Oficial | Orcamento de instrucoes, anti-padroes, verificacao |
| 5 | Claude Code Memory (Anthropic Docs) | Documentacao Oficial | Hierarquia CLAUDE.md, regras escopadas, auto memory |
| 6 | Lost in the Middle (arXiv:2307.03172) | Paper Academico | Efeito de posicionamento de informacao em contextos longos |
| 7 | LongICLBench (arXiv:2404.02060) | Paper Academico | Vies de recencia, limites de tarefas complexas |
| 8 | Prompting Best Practices (Anthropic Docs) | Documentacao Oficial | Zona Goldilocks de especificidade, XML tags, dados longos no topo |
| 9 | Harper Reed's LLM Codegen Workflow | Blog de Praticante | Workflow Spec -> Plan -> Execute |
| 10 | Latent Space Podcast: Claude Code Episode | Entrevista | Filosofia de simplicidade de Boris Cherny |
