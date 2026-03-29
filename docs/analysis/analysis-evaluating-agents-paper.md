# Analise: Evaluating AGENTS.md — Are Repository-Level Context Files Helpful for Coding Agents?

> **Documento analisado:** Gloaguen, T., Mundler, N., Muller, M., Raychev, V., & Vechev, M. (ETH Zurich / LogicStar.ai). Preprint, fevereiro de 2026. arXiv:2602.11988v1
>
> **Objetivo desta analise:** Extrair, interpretar e traduzir em orientacoes praticas todos os achados do paper, conectando-os a engenharia de prompts e a infraestrutura de agentes (skills, hooks, subagents, rules, memory).

---

## 1. Sumario Executivo

Este paper e a primeira investigacao rigorosa e em escala sobre o impacto real de arquivos de contexto (AGENTS.md, CLAUDE.md) na capacidade de agentes de codificacao resolverem tarefas de engenharia de software do mundo real. Ate entao, a adocao massiva desses arquivos (mais de 60.000 repositorios) baseava-se exclusivamente em recomendacoes de desenvolvedores de agentes e evidencias anedoticas. Os autores construiram um benchmark novo (AGENTBENCH, 138 instancias de 12 repositorios com arquivos de contexto escritos por desenvolvedores) e avaliaram quatro agentes (Claude Code com Sonnet 4.5, Codex com GPT-5.2 e GPT-5.1 Mini, Qwen Code com Qwen3-30B-Coder) em tres cenarios: sem contexto, com contexto gerado por LLM, e com contexto escrito por humanos.

O achado central e contra-intuitivo: **arquivos de contexto gerados por LLM tendem a reduzir a taxa de sucesso** (queda media de 0,5% no SWE-bench Lite e 2% no AGENTBENCH), enquanto **arquivos escritos por humanos oferecem apenas ganho marginal** (aumento medio de 4% no AGENTBENCH). Em todos os cenarios, arquivos de contexto aumentam consistentemente o numero de passos (+2,45 a +3,92 em media) e o custo de inferencia em mais de 20%. A analise de traces revela que as instrucoes dos arquivos sao de fato seguidas — o problema nao e desobediencia, mas sim que requisitos desnecessarios tornam as tarefas mais dificeis.

A implicacao pratica e clara: a recomendacao vigente de "sempre gerar um AGENTS.md via /init" deve ser questionada. Arquivos de contexto so sao justificaveis quando escritos manualmente, mantidos minimos, e focados em requisitos genuinamente necessarios que o agente nao conseguiria descobrir sozinho. Documentacao redundante com o que ja existe no repositorio nao apenas nao ajuda — ela atrapalha.

---

## 2. Achados e Principios-Chave

### 2.1. Arquivos gerados por LLM prejudicam mais do que ajudam

| Metrica | Sem Contexto | LLM-Gerado | Humano |
|---------|-------------|-------------|--------|
| Taxa de sucesso (AGENTBENCH, media) | Baseline | -2% | +4% |
| Taxa de sucesso (SWE-bench Lite, media) | Baseline | -0,5% | N/A |
| Custo por instancia | Baseline | +20-23% | +19% |
| Passos por instancia | Baseline | +2,45 a +3,92 | +3,34 |

> "LLM-generated context files have a marginal negative effect on task success rates, while developer-written ones provide a marginal performance gain."

**Principio derivado:** A geracao automatica de contexto via `/init` e, no melhor caso, neutra e, no caso tipico, prejudicial. O custo extra e consistente e inequivoco.

### 2.2. Overviews de codebase sao ineficazes

Apesar de 100% dos arquivos gerados por Sonnet 4.5 e ~99% dos gerados por GPT-5.2 conterem overviews de codebase, esses overviews **nao reduzem o numero de passos necessarios para o agente encontrar os arquivos relevantes**. O paper mede explicitamente isso (Figura 4) e conclui:

> "Context files, even developer-provided ones, are not effective at providing a repository overview."

**Principio derivado:** Listar diretorios e componentes no arquivo de contexto e desperdicio de tokens. Agentes ja sabem navegar repositorios via ferramentas (grep, find, read). O guia da Anthropic para CLAUDE.md ja alertava contra isso ("warns against listing components that are easily discoverable"), e este paper confirma empiricamente.

### 2.3. Instrucoes sao seguidas — esse e o problema

A analise de traces demonstra que agentes **seguem fielmente** as instrucoes dos arquivos de contexto:

- `uv` e usado 1,6 vezes por instancia quando mencionado vs. <0,01 quando nao mencionado
- Ferramentas especificas de repositorio sao usadas 2,5 vezes quando mencionadas vs. <0,05 quando nao
- Testes sao executados com mais frequencia quando o arquivo instrui a testar

> "Instructions in context files are typically followed [...] the absence of improvements with context files is not due to a lack of instruction-following."

**Principio derivado:** Cada instrucao adicionada ao arquivo de contexto sera executada. Se a instrucao nao for essencial para resolver a tarefa, ela consumira passos, tokens e custo sem contribuir para o resultado. A obediencia do agente transforma instrucoes desnecessarias em carga ativa.

### 2.4. Contexto adicional exige mais raciocinio

Modelos com raciocinio adaptativo (GPT-5.2, GPT-5.1 Mini) gastam significativamente mais tokens de raciocinio quando arquivos de contexto estao presentes:

- GPT-5.2: +22% de tokens de raciocinio no SWE-bench Lite com contexto LLM
- GPT-5.1 Mini: +14% no SWE-bench Lite com contexto LLM

> "Following context files requires more thinking [...] these additional instructions make the task harder."

**Principio derivado:** Mais contexto nao e mais ajuda — e mais carga cognitiva para o modelo. Isso alinha-se diretamente com a pesquisa sobre "context rot" e limites de janela de contexto documentados em `research-llm-context-optimization.md`.

### 2.5. Arquivos de contexto sao documentacao redundante

O experimento mais revelador: quando **toda a documentacao do repositorio e removida** (arquivos .md, docs/, exemplos), arquivos de contexto gerados por LLM passam a melhorar a performance em +2,7% em media e superam a documentacao original.

> "LLM-generated context files not only consistently improve performance [...] but also outperform developer-written documentation. This may explain anecdotal evidence reporting that coding agents perform better after adding context files, since many less popular repositories contain little to no documentation."

**Principio derivado:** Arquivos de contexto sao uteis quando substituem documentacao ausente — nao quando duplicam documentacao existente. Em repositorios bem documentados, sao redundantes. Em repositorios mal documentados, preenchem uma lacuna real.

### 2.6. Modelos mais fortes nao geram arquivos melhores

GPT-5.2 (via Codex) gerou contextos que melhoraram performance no SWE-bench Lite (+2% em media) mas pioraram no AGENTBENCH (-3% em media). O prompt usado (Codex vs. Claude Code) tambem nao faz diferenca consistente.

**Principio derivado:** O problema nao esta na qualidade da geracao, mas na natureza do que e gerado — informacao generica e redundante que o agente ja poderia descobrir.

### 2.7. GPT-5.1 Mini exibe comportamento patologico com arquivos de contexto

O paper documenta que GPT-5.1 Mini, quando detecta a presenca de arquivos de contexto, emite multiplos comandos para encontra-los e le-los repetidamente, mesmo quando ja estao no contexto do agente. Esse comportamento so ocorre quando arquivos de contexto existem.

**Principio derivado:** A mera existencia de um arquivo de contexto pode alterar o comportamento do agente de formas imprevisiveis, incluindo loops de leitura redundante. Isso reforça a recomendacao de so incluir arquivos quando estritamente necessario.

---

## 3. Pontos de Atencao (faceis de perder ou interpretar mal)

### 3.1. O paper NAO diz que arquivos de contexto sao inuteis

O paper diz que **na forma como estao sendo gerados e usados atualmente**, eles nao ajudam. Arquivos escritos por humanos **com conteudo minimal** mostram ganho marginal positivo. A conclusao e sobre a pratica atual, nao sobre o conceito.

### 3.2. O benchmark e centrado em Python

> "The current evaluation is focused heavily on Python. Since this is a language that is widely represented in the training data, much detailed knowledge about tooling, dependencies, and other repository specifics might be present in the models' parametric knowledge, nullifying the effect of context files."

Para linguagens menos representadas no treinamento (Rust, Zig, linguagens de nicho), o efeito de arquivos de contexto pode ser significativamente maior. Nao generalize esses resultados para todo ecossistema.

### 3.3. O paper avalia apenas resolucao de tarefas

> "We evaluate the impact of context files on task resolution rate. However, there are many other relevant aspects of coding agents, such as code efficiency and security."

Arquivos de contexto podem ser valiosos para **qualidade do codigo**, **aderencia a padroes**, **seguranca** e **experiencia do desenvolvedor** — dimensoes nao medidas aqui.

### 3.4. A metrica "mais testes" nao e automaticamente ruim

O paper mostra que contexto leva a mais testes e mais exploracao. Embora isso aumente custo sem melhorar resolucao, em cenarios de producao real, mais testes podem ser desejavel como garantia de qualidade — mesmo que nao mude a taxa de "patch correto" no benchmark.

### 3.5. Repositorios "niche" vs. "populares"

O SWE-bench Lite usa repositorios populares (bem conhecidos pelos modelos via treinamento). O AGENTBENCH usa repositorios de nicho. Os resultados diferem entre os dois: contexto humano melhora +4% no AGENTBENCH mas nao ajuda no SWE-bench Lite. Isso sugere que **quanto menos o modelo conhece o repositorio, mais util e o contexto** — uma intuicao que o paper confirma.

### 3.6. Os testes do AGENTBENCH sao gerados por LLM

75% de cobertura media nos testes gerados e alta, mas testes gerados por LLM podem ter vieses. Os autores fizeram validacao manual e melhoraram testes over-especificados, mas e um ponto de atencao metodologico.

### 3.7. Sub-agentes e compressao de contexto

Claude Code usa o Task tool que delega a Haiku 4.5 para sub-tarefas. Qwen Code usa compressao de chat a 60% do limite de contexto. Essas estrategias afetam como o contexto e processado e podem modular o impacto dos arquivos — mas o paper nao isola esses efeitos.

---

## 4. Casos de Uso e Escopo de Aplicacao

### Quando arquivos de contexto AJUDAM (baseado nas evidencias)

| Cenario | Razao | Evidencia no paper |
|---------|-------|--------------------|
| Repositorio sem documentacao | Substitui documentacao ausente | +2,7% quando docs removidos |
| Repositorio de nicho/pouco conhecido | Modelo tem pouco conhecimento parametrico | +4% no AGENTBENCH vs SWE-bench |
| Linguagens pouco representadas | Modelo precisa de orientacao sobre tooling | Secao 5 (Limitations) |
| Informacoes nao-descobriveis | Tooling especifico, CI/CD, convencoes nao-obvias | uv, repo_tool usados quando mencionados |
| Restricoes de seguranca/compliance | Agente nao inferiria sozinho | Secao 5 (Future Work) |

### Quando arquivos de contexto PREJUDICAM

| Cenario | Razao | Evidencia no paper |
|---------|-------|--------------------|
| Repositorio bem documentado | Redundancia com docs existentes | -0,5% a -2% com LLM-gerado |
| Overviews extensos de diretorio | Agente descobre sozinho via ferramentas | Figura 4, nenhuma reducao de passos |
| Instrucoes genericas ("use boas praticas") | Adicionam carga sem valor concreto | +22% tokens de raciocinio |
| Geracao automatica via /init | Conteudo generico e redundante | Degradacao consistente em 5/8 cenarios |
| Python em repositorios populares | Modelo ja conhece o ecossistema | SWE-bench Lite sem melhora |

---

## 5. Aplicabilidade a Infraestrutura de Agentes

### 5.1. Skills (criacao, evolucao, refatoracao, atualizacao)

**Principio central: skills devem encapsular conhecimento nao-descobrivel, nao repetir o que o agente ja sabe.**

- **Criacao:** Ao criar uma nova skill, perguntar: "O agente conseguiria descobrir isso navegando o repositorio?" Se sim, a skill e redundante e potencialmente prejudicial. Skills devem conter apenas instrucoes que o agente nao derivaria sozinho — convencoes de estilo nao-obvias, workflows especificos de CI/CD, restricoes de seguranca.

- **Evolucao:** O paper mostra que o impacto varia por repositorio (Figura 12, Apendice A.3). Skills devem ser avaliadas por impacto real: se uma skill nao esta melhorando resultados mensuravelmente, ela esta adicionando custo (+20% em media). Implementar metricas de uso e impacto.

- **Refatoracao:** Skills longas e abrangentes devem ser decompostas em unidades minimas focadas. O paper mostra que cada instrucao adicional gera passos adicionais e custo adicional. Remover instrucoes genericas ("mantenha codigo limpo", "siga boas praticas") que nao contem informacao concreta.

- **Atualizacao:** Documentacao stale e pior que nenhuma documentacao. O paper confirma que contexto incorreto ou desatualizado nao e ignorado — e seguido. Skills devem ter revisao periodica para remover informacao que se tornou descobrivel ou obsoleta.

**Acao concreta:** Antes de adicionar qualquer instrucao a uma skill, aplicar o teste: "Se eu remover esta instrucao, o agente falhara em algo que nao conseguiria descobrir sozinho?" Se a resposta for nao, nao adicionar.

### 5.2. Hooks (quando usar hooks vs. outros mecanismos)

**Principio central: hooks executam acoes automaticas sem consumir contexto, evitando o overhead documentado no paper.**

O paper demonstra que instrucoes como "rode testes antes de commitar" e "use uv para gerenciamento de dependencias" no arquivo de contexto:

1. Consomem tokens de contexto
2. Aumentam passos (+2,45 a +3,92)
3. Aumentam custo (+20-23%)
4. Sao seguidas fielmente — mas nao necessariamente no momento certo

**Hooks como alternativa superior a instrucoes de contexto:**

| Instrucao no Contexto | Hook Equivalente | Vantagem do Hook |
|------------------------|------------------|------------------|
| "Rode testes antes de commitar" | Pre-commit hook com pytest | Zero tokens de contexto, execucao garantida |
| "Use linter X no codigo" | Pre-commit hook com linter | Sem dependencia de obediencia do agente |
| "Verifique tipos com mypy" | Hook pos-save com mypy | Feedback imediato, sem instrucao explicita |
| "Formate com black/ruff" | Pre-commit hook de formatacao | Enforcement mecanico, nao instrucional |

**Regra decisoria:** Se uma instrucao pode ser transformada em hook, **sempre** prefira o hook. Hooks eliminam o custo de +20% de inferencia e garantem execucao. Reserve o arquivo de contexto para informacao que NAO pode ser automatizada (convencoes de arquitetura, decisoes de design, restricoes de dominio).

### 5.3. Subagentes (orquestracao, isolamento de contexto, padroes de delegacao)

**Principio central: subagentes devem receber apenas o contexto minimo necessario para sua sub-tarefa, nao o arquivo de contexto completo.**

O paper documenta que Claude Code usa o Task tool delegando a Haiku 4.5 para sub-tarefas (Apendice A.1). Isso e eficaz porque **isola o contexto**: o subagente recebe apenas a descricao da sub-tarefa, sem a carga do arquivo de contexto completo.

**Padroes derivados do paper:**

1. **Isolamento de contexto por sub-tarefa:** Nao propagar o CLAUDE.md completo para subagentes. O paper mostra que quanto mais instrucoes o agente recebe, mais passos ele executa sem melhoria proporcional. Cada subagente deve receber apenas as instrucoes relevantes a sua sub-tarefa especifica.

2. **Delegacao de exploracao:** O paper confirma que contexto NAO ajuda na navegacao do repositorio. Portanto, sub-tarefas de exploracao ("encontre os arquivos relevantes para X") podem ser delegadas sem nenhum contexto adicional — o subagente explorara via ferramentas tao eficientemente quanto com contexto.

3. **Contexto para sub-tarefas de tooling:** O unico cenario onde contexto importa para subagentes e quando a sub-tarefa envolve tooling nao-obvio. Se o subagente precisa usar `uv` ou uma ferramenta especifica do repositorio, inclua apenas essa instrucao.

4. **Custo de sub-agentes com contexto:** O aumento de 20% em custo por instancia se multiplica por cada subagente que recebe contexto desnecessario. Em uma arvore de subagentes, o overhead pode ser exponencial.

### 5.4. Rules (.claude/rules/ — path-scoped, configuracao modular)

**Principio central: rules path-scoped sao o mecanismo correto para entregar contexto just-in-time, evitando o overhead de contexto global.**

O paper demonstra o problema de contexto global: instrucoes aplicadas uniformemente aumentam custo sem beneficio proporcional. Rules path-scoped resolvem isso ao ativar instrucoes apenas quando o agente opera em caminhos relevantes.

**Padroes derivados:**

1. **Granularidade maxima:** Em vez de um CLAUDE.md dizendo "use pytest para testes e ruff para linting", criar:
   - `.claude/rules/testing.md` com regras de teste (ativado apenas em contexto de teste)
   - `.claude/rules/linting.md` com regras de formatacao (ativado apenas em contexto de codigo)

2. **Eliminacao de overviews:** O paper prova que overviews sao inuteis. Rules path-scoped eliminam a necessidade de overview porque o contexto relevante e entregue automaticamente quando o agente navega para aquele diretorio.

3. **Regras como substituto de contexto global:** A Tabela 2 mostra que o cenario "NONE" (sem contexto) tem menor custo em TODOS os 8 cenarios testados. Rules path-scoped aproximam-se do cenario "NONE" para a maioria das operacoes (sem overhead global), ativando contexto apenas quando necessario.

4. **Regras de tooling especifico por diretorio:**

   ```
   # .claude/rules/infra-terraform.md (ativado em /infrastructure/)
   Use `terraform fmt` e `terraform validate` antes de propor mudancas.
   ```

   Isso evita que a instrucao de terraform polua o contexto quando o agente trabalha em /src/.

### 5.5. Memory (auto memory, MEMORY.md, topic files)

**Principio central: memoria deve capturar o que o agente aprendeu sobre o repositorio ao longo do tempo, nao replicar documentacao estatica.**

O paper demonstra que documentacao estatica (overviews, listagem de componentes) nao ajuda. Memoria util e aquela que captura **conhecimento tacito** — o tipo de informacao que um desenvolvedor humano acumula ao longo de meses trabalhando no projeto.

**Padroes derivados:**

1. **Memoria como alternativa a geracao automatica:** Em vez de gerar um AGENTS.md via `/init`, deixar o agente construir memoria incrementalmente a partir de experiencias reais. Cada tarefa resolvida pode enriquecer a memoria com informacoes genuinamente uteis (ex: "o modulo X tem uma dependencia circular com Y que exige importacao lazy").

2. **Topic files para informacao nao-descobrivel:** Criar arquivos de memoria por topico para informacoes que nao estao em nenhuma documentacao:
   - `memory/deployment-quirks.md` — peculiaridades do processo de deploy
   - `memory/test-flakiness.md` — testes intermitentes conhecidos
   - `memory/api-compatibility.md` — restricoes de compatibilidade retroativa

3. **Poda ativa de memoria:** O paper mostra que mais contexto = mais custo sem mais qualidade. Memoria deve ser podada regularmente: informacoes que se tornaram obvias (por melhoria na documentacao ou no modelo) devem ser removidas.

4. **Auto-memory como aprendizado incremental:** O paper menciona na secao de trabalhos futuros:
   > "Several related works in the direction of planning and continuous learning from prior tasks may be applicable for this task. By tackling this challenge, future agents could gain a long-term capability at meaningful self-improvement."

   Auto-memory que registra padroes de sucesso e falha ao longo de multiplas sessoes representa o caminho mais promissor para contexto que genuinamente melhora performance.

---

## 6. Aplicabilidade do Guia de Engenharia de Prompts

### 6.1. Context Engineering > Prompt Engineering

O guia de engenharia de prompts documenta a transicao de "prompt engineering" para "context engineering":

> "O LLM e uma CPU, a janela de contexto e RAM, e voce e o sistema operacional." — Andrej Karpathy

O paper sobre AGENTS.md confirma empiricamente essa transicao: o problema nao e a qualidade do prompt usado para gerar o arquivo de contexto (a Secao 4.4 mostra que diferentes prompts produzem resultados similares), mas sim **o que entra no contexto e quando**.

**Conexao direta:** As quatro estrategias de contexto do LangChain mencionadas no guia — Write, Select, Compress, Isolate — sao diretamente aplicaveis:

| Estrategia LangChain | Aplicacao ao Problema do Paper |
|-----------------------|--------------------------------|
| **Write** (persistir externamente) | Mover informacao do CLAUDE.md para rules path-scoped e topic files |
| **Select** (recuperar via RAG) | Carregar apenas o contexto relevante para a tarefa atual |
| **Compress** (sumarizar) | Reduzir o conteudo do arquivo de contexto ao minimo essencial |
| **Isolate** (separar contextos) | Nao propagar contexto global para subagentes |

### 6.2. O Principio da Solucao Mais Simples

O guia documenta o principio dominante da Anthropic:

> "Encontrar a solucao mais simples possivel, so aumentando complexidade quando necessario."

O paper confirma: o cenario "NONE" (sem contexto) e consistentemente o mais barato e, em 5/8 cenarios com LLM-gerado, tambem o mais eficaz. A solucao mais simples (nao ter arquivo de contexto) e frequentemente a melhor.

### 6.3. Role Prompting e Especializacao de Subagentes

O guia documenta que role prompting e o mecanismo fundamental de especializacao em multi-agentes. O paper mostra que Claude Code usa subagentes especializados (Haiku 4.5 para sub-tarefas via Task tool). A conexao e:

- **Role prompting focado** para cada subagente e mais eficaz que contexto global generico
- Subagentes com role prompting especifico ("voce e um explorador de codebase — encontre os arquivos relacionados a X") nao precisam de arquivo de contexto
- O overhead de +20% em custo vem de contexto generico aplicado indiscriminadamente

### 6.4. Chain-of-Thought e o Aumento de Tokens de Raciocinio

O guia documenta que:

> "Performance de raciocinio comeca a degradar em torno de 3.000 tokens."

O paper confirma que arquivos de contexto aumentam tokens de raciocinio em +14% a +22%, potencialmente empurrando o modelo para alem do sweet spot de raciocinio. A combinacao "contexto longo + raciocinio complexo" e listada no guia como combinacao prejudicial.

**Tecnica aplicavel:** Chain of Draft (CoD) do guia, que iguala acuracia de CoT usando apenas ~7,6% dos tokens, e relevante para reduzir o overhead quando contexto adicional e inevitavel.

### 6.5. ReAct e o Loop de Exploracao

O guia documenta ReAct como "O padrao fundamental para agentes de IA modernos" (Pensamento -> Acao -> Observacao). O paper mostra que agentes com contexto executam mais acoes de exploracao (mais grep, mais leituras de arquivo, mais testes). Isso significa que o contexto esta adicionando iteracoes ao loop ReAct sem melhorar a resolucao.

**Implicacao:** Instrucoes no arquivo de contexto devem ser formuladas para **reduzir** iteracoes do loop ReAct (ex: "o entrypoint para testes e `pytest tests/unit/`", nao "explore o repositorio para entender a estrutura de testes").

### 6.6. Structured Outputs e Comunicacao Inter-Agentes

O guia documenta que structured outputs garantem comunicacao confiavel entre agentes. O paper usa JSON structures extensivamente nos prompts de benchmark (Apendice B). Para a geracao de contexto, estruturar o output em schema estrito poderia forcar a concisao e eliminar conteudo generico.

### 6.7. Modelos de Raciocinio e a Inversao de Paradigma

O guia documenta a descoberta contra-intuitiva:

> "Modelos de raciocinio avancados (o1, R1, GPT-5) frequentemente performam pior com tecnicas classicas como few-shot e CoT explicito."

O paper usa GPT-5.2 e GPT-5.1 Mini, que sao modelos com raciocinio adaptativo. Para esses modelos, **menos contexto e melhor**, confirmando que instrucoes explicitas de "como pensar" prejudicam modelos que ja possuem raciocinio interno robusto.

### 6.8. RAG como Alternativa a Contexto Pre-Carregado

O guia documenta a evolucao para Agentic RAG, onde o LLM decide quando recuperar contexto. Isso se alinha com a conclusao do paper: em vez de pre-carregar um arquivo de contexto completo, implementar um mecanismo onde o agente recupera informacao especifica apenas quando precisa.

### 6.9. Meta-Prompting e Geracao de Contexto

O guia documenta que meta-prompting (usar um modelo para gerar/otimizar prompts para outro) supera prompting manual. A Secao 4.4 do paper mostra que modelos mais fortes nao geram contextos melhores, sugerindo que o problema nao e a otimizacao do prompt de geracao, mas a natureza do que e gerado. Meta-prompting poderia ser aplicado para gerar contexto **minimal e nao-redundante**, em vez de contexto **abrangente**.

### 6.10. Automatic Prompt Engineering (APE/OPRO/DSPy)

O guia documenta que otimizacao automatica de prompts supera otimizacao manual. Para a geracao de arquivos de contexto, isso implica:

- Usar frameworks como DSPy para otimizar o conteudo do arquivo de contexto contra uma metrica de resolucao de tarefas
- Iterar automaticamente removendo seccoes que nao contribuem para a taxa de sucesso
- O paper fornece o benchmark (AGENTBENCH) que possibilita exatamente esse tipo de otimizacao

---

## 7. Correlacoes com Outros Documentos Principais

### 7.1. research-llm-context-optimization.md

Este e o documento com maior correlacao. O paper confirma empiricamente os seguintes principios documentados em `research-llm-context-optimization.md`:

| Principio do Research Doc | Confirmacao no Paper |
|---------------------------|---------------------|
| **Context rot** (retornos decrescentes com mais contexto) | Mais contexto = +20% custo, -0,5% a -2% performance |
| **Lost-in-the-middle effect** | GPT-5.1 Mini le contexto multiplas vezes; overviews nao reduzem passos |
| **Instruction budget (~150-200 instrucoes max)** | Cada instrucao adicional gera passos adicionais sem melhoria |
| **Quality over quantity** | Humano (minimal, curado) > LLM (abrangente, generico) |
| **Progressive disclosure** | Cenario NONE supera LLM; contexto deve ser entregue sob demanda |
| **Hybrid pre-loaded + on-demand** | Remover docs + manter contexto = melhor resultado |
| **Context poisoning from stale docs** | Instrucoes redundantes com docs existentes prejudicam |
| **Just-in-time documentation** | Contexto so ajuda quando substitui documentacao ausente |

**Divergencia notavel:** O research doc sugere <200 linhas por arquivo de configuracao. A media dos arquivos de contexto no AGENTBENCH e 641 palavras (~30-40 linhas), dentro do limite, mas ainda assim prejudicial quando redundante.

### 7.2. claude-prompting-best-practices.md

O guia de prompting da Anthropic recomenda:

- System prompts persistentes com role e restricoes
- Queries ao final do prompt apos contexto
- Prompt caching para system prompts repetidos

O paper confirma que o posicionamento do contexto importa: quando o contexto e injetado automaticamente, o agente o processa antes da tarefa. As recomendacoes de posicionamento (tarefa ao final) sao consistentes com a pratica atual dos agentes.

**Tensao:** O guia recomenda ser "explicito, detalhado e intencional" em prompts de subagentes. O paper mostra que detalhe excessivo no arquivo de contexto prejudica. A reconciliacao e: **prompts de subagentes devem ser detalhados e intencionais sobre a sub-tarefa especifica, nao sobre o contexto global do repositorio**.

### 7.3. a-guide-to-agents.md

O guia AGENTS.md enfatiza:

- Manter minimal
- Progressive disclosure
- Instruction budget
- Stale docs poison context
- Nao auto-gerar

O paper e a validacao empirica direta de todas essas recomendacoes:

| Recomendacao do Guia | Evidencia no Paper |
|----------------------|--------------------|
| Keep minimal | Contexto humano (curado) > contexto LLM (abrangente) |
| Progressive disclosure | Cenario NONE supera LLM; contexto sob demanda melhor |
| Instruction budget | Cada instrucao gera passos extras |
| Stale docs poison context | Redundancia com docs existentes = prejudicial |
| Nao auto-gerar | Confirmado: /init prejudica em 5/8 cenarios |

### 7.4. a-guide-to-claude.md

O guia CLAUDE.md segue os mesmos principios do AGENTS.md com foco em Claude Code. O paper testa explicitamente Claude Code (Sonnet 4.5) e confirma que:

- Claude Code com contexto LLM performa **pior** que sem contexto no AGENTBENCH
- O prompt de geracao do Claude Code avisa contra listar componentes descobriveis — e o paper prova que esse aviso e correto
- Claude Code e o agente mais caro entre os testados (custo medio de $1,30 por instancia), tornando o overhead de +20% particularmente impactante

---

## 8. Forcas e Limitacoes da Abordagem do Paper

### Forcas

1. **Primeira avaliacao rigorosa em escala:** 138 instancias proprias + 300 do SWE-bench Lite, 4 agentes, 3 cenarios. Nenhum trabalho anterior oferecia esse nivel de rigor.

2. **Benchmark complementar:** AGENTBENCH preenche uma lacuna real — repositorios de nicho com arquivos de contexto escritos por desenvolvedores. O SWE-bench Lite sozinho seria insuficiente (repositorios populares sem arquivos de contexto).

3. **Analise comportamental profunda:** Nao se limita a medir resolucao; analisa traces, contagem de ferramentas, tokens de raciocinio e intencoes de acoes. Isso permite entender **por que** o contexto nao ajuda.

4. **Ablacoes informativas:** Testar "sem documentacao + com contexto" versus "com documentacao + com contexto" revela o mecanismo causal (redundancia).

5. **Reproducibilidade:** Todos os prompts sao publicados nos apendices. O benchmark sera disponibilizado.

### Limitacoes

1. **Centrado em Python:** A linguagem mais representada nos dados de treinamento. Resultados podem nao generalizar para linguagens de nicho onde o efeito do contexto seria maior.

2. **Apenas resolucao de tarefas:** Nao mede qualidade do codigo, seguranca, aderencia a padroes, ou satisfacao do desenvolvedor. Esses podem ser os cenarios onde contexto mais importa.

3. **Testes gerados por LLM:** 75% de cobertura media e boa, mas testes gerados podem ter vieses sistematicos. Validacao manual em 10% das instancias mitiga mas nao elimina o risco.

4. **Temperatura zero em 3/4 agentes:** Reduz variancia experimental mas nao reflete uso real (onde temperatura > 0 e comum).

5. **Uma amostra por instancia:** Sem repeticao, a variancia estatistica de instancias individuais e alta. Os resultados sao robustos em agregado mas nao por instancia.

6. **Repositorios recentes:** Contextos files sao formalizados desde agosto 2025. Os repositorios e PRs sao muito recentes, possivelmente nao representando praticas maduras.

7. **Ausencia de contexto personalizado por tarefa:** O paper testa o mesmo arquivo de contexto para todas as tarefas de um repositorio. Contexto personalizado por tarefa (como rules path-scoped) poderia ter resultados diferentes.

8. **Nao testa composicao de mecanismos:** Rules + skills + hooks + memoria nao sao testados — apenas o arquivo de contexto monolitico.

---

## 9. Recomendacoes Praticas

### 9.1. Para quem mantem arquivos CLAUDE.md / AGENTS.md

1. **Nao use `/init` para gerar automaticamente.** O paper prova que contexto gerado por LLM e, no caso medio, prejudicial. Se precisar de um ponto de partida, escreva manualmente.

2. **Aplique o Teste de Necessidade para cada instrucao:** "O agente conseguiria resolver a tarefa sem esta instrucao?" Se sim, remova-a.

3. **Elimine overviews de codebase.** Eles nao reduzem passos de descoberta e consomem tokens. O agente navega via ferramentas.

4. **Foque em informacao nao-descobrivel:**
   - Tooling especifico e nao-obvio (ex: "use `uv` em vez de `pip`")
   - Convencoes de CI/CD que nao estao documentadas em lugar nenhum
   - Restricoes de compatibilidade retroativa
   - Decisoes arquiteturais que nao sao evidentes no codigo

5. **Remova qualquer informacao que duplique docs existentes.** Se esta no README, nos docstrings, ou nos comentarios, nao repita no arquivo de contexto.

6. **Mantenha abaixo de 200 palavras.** A media dos arquivos no AGENTBENCH e 641 palavras — e eles mal ajudam. Corte para um terco.

### 9.2. Para quem projeta sistemas de skills

1. **Prefira skills on-demand a contexto pre-carregado.** A skill deve ser invocada quando necessaria, nao injetada no contexto desde o inicio.

2. **Cada skill deve conter maximo 3-5 instrucoes acionaveis.** O paper mostra que cada instrucao gera ~0,5-1 passo adicional.

3. **Skills de exploracao nao precisam de contexto.** Delegue exploracao para subagentes sem contexto — o paper prova que contexto nao acelera descoberta.

4. **Implemente metricas de impacto por skill.** Meça taxa de resolucao com e sem cada skill. Se nao ha melhoria mensuravel, a skill esta adicionando custo.

### 9.3. Para quem configura hooks e rules

1. **Converta instrucoes automatizaveis em hooks.** Tudo que pode ser hook (linting, formatacao, testes) deve ser hook, nao instrucao no arquivo de contexto.

2. **Use rules path-scoped para contexto just-in-time.** Em vez de um CLAUDE.md monolitico, distribua regras por diretorio. Isso aproxima o cenario do "NONE" (baixo custo) quando o agente nao esta naquele diretorio.

3. **Regras devem ser imperativas e especificas, nao descritivas.** "Rode `pytest tests/unit/` para validar" e util. "O repositorio tem uma suite de testes abrangente usando pytest" nao e — o agente descobriria isso sozinho.

### 9.4. Para quem desenvolve sistemas de memoria

1. **Memoria incremental > geracao unica.** Em vez de gerar contexto uma vez, deixe o agente acumular aprendizados ao longo de multiplas sessoes.

2. **Poda ativa de memoria.** Remova regularmente informacoes que se tornaram obvias. O paper mostra que informacao redundante e ativamente prejudicial.

3. **Topic files para conhecimento tacito.** Capture quirks, workarounds e decisoes historicas que nao estao em nenhuma documentacao formal.

### 9.5. Para quem avalia e testa configuracoes de agentes

1. **Sempre compare com o baseline "sem contexto".** O paper prova que "mais contexto" nao e automaticamente "melhor". Toda configuracao deve superar o cenario vazio para justificar sua existencia.

2. **Meça custo alem de resolucao.** Um ganho de +4% em resolucao acompanhado de +20% em custo pode nao ser justificavel dependendo do volume de uso.

3. **Teste em repositorios de nicho, nao apenas em populares.** O beneficio de contexto e maior em repositorios menos conhecidos. Se voce so testa em repositorios populares, vai subestimar o valor de contexto bem escrito.

4. **Avalie dimensoes alem de resolucao.** Qualidade de codigo, seguranca, aderencia a padroes — o paper nao mede essas dimensoes, mas elas podem ser onde o contexto mais impacta.
