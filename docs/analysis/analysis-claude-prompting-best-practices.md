# Analise: Claude Prompting Best Practices

**Documento analisado**: `claude-prompting-best-practices.md`
**Documento complementar**: `prompt-engineering-guide.md`
**Data da analise**: 2026-03-27

---

## 1. Sumario Executivo

O documento `claude-prompting-best-practices.md` e o guia oficial da Anthropic para engenharia de prompts com os modelos Claude 4.6 (Opus, Sonnet e Haiku 4.5). Ele cobre desde principios fundamentais de clareza e estruturacao ate tecnicas avancadas para sistemas agenticos, incluindo orquestracao de subagentes, gerenciamento de contexto multi-janela e controle de comportamento autonomo. O documento se diferencia de guias genericos de prompting por ser prescritivo e especifico para a familia Claude, trazendo exemplos concretos de prompts, configuracoes de API e padroes de migracao entre versoes de modelo.

A descoberta mais relevante para este projeto e que o documento formaliza, do lado da Anthropic, principios que convergem fortemente com as outras quatro fontes-ancora do projeto: orçamento de instrucoes, disclosure progressivo, minimalismo e a transicao de "prompt engineering" para "context engineering". A secao sobre sistemas agenticos e particularmente valiosa, pois fornece orientacoes diretamente aplicaveis a escrita de skills, regras path-scoped e prompts de subagentes — os artefatos centrais deste repositorio.

O `prompt-engineering-guide.md` complementa oferecendo uma visao academica e quantitativa com 58+ tecnicas documentadas, benchmarks comparativos e uma matriz de decisao por tipo de modelo e tarefa. A intersecao entre os dois documentos revela que muitas tecnicas classicas (few-shot extensivo, CoT explicito) podem ser contraproducentes em modelos de raciocinio avancados como Claude Opus 4.6, exigindo uma abordagem mais sofisticada e model-aware na escrita de infraestrutura de agentes.

---

## 2. Achados-Chave e Principios

### 2.1 Principios Gerais de Prompting

| Principio | Descricao | Citacao-chave |
|-----------|-----------|---------------|
| Clareza e direcionamento | Instrucoes explicitas superam instrucoes vagas. Pedir "above and beyond" explicitamente, nao esperar inferencia. | *"Think of Claude as a brilliant but new employee who lacks context on your norms and workflows."* |
| Regra de ouro | Teste o prompt com um colega sem contexto. Se confundir o humano, confundira o modelo. | *"Show your prompt to a colleague with minimal context on the task and ask them to follow it."* |
| Contexto motivacional | Explicar o "por que" melhora a aderencia. Claude generaliza a partir da explicacao. | *"Your response will be read aloud by a text-to-speech engine, so never use ellipses..."* |
| Exemplos (few-shot) | 3-5 exemplos diversos, relevantes, em tags `<example>` produzem os melhores resultados de formato e tom. | *"Include 3-5 examples for best results."* |
| Estruturacao XML | Tags XML desambiguam prompts complexos que misturam instrucoes, contexto, exemplos e inputs. | *"Use consistent, descriptive tag names across your prompts."* |
| Atribuicao de papel (role) | Uma unica sentenca de papel no system prompt foca comportamento e tom. | `"You are a helpful coding assistant specializing in Python."` |

### 2.2 Contexto Longo

O documento estabelece regras criticas para prompts com 20k+ tokens:

- **Dados longos no topo**: Documentos e inputs extensos devem preceder a query, instrucoes e exemplos. Queries ao final melhoram qualidade em ate 30%.
- **Estruturacao com XML**: Multiplos documentos em `<document index="n">` com `<source>` e `<document_content>`.
- **Fundamentacao em citacoes**: Pedir que Claude extraia citacoes relevantes antes de executar a tarefa reduz ruido — padrao `<quotes>` seguido de `<info>`.

### 2.3 Saida e Formatacao

Quatro estrategias de controle de formato:

1. **Dizer o que fazer, nao o que nao fazer**: Em vez de "Do not use markdown", usar "Your response should be composed of smoothly flowing prose paragraphs."
2. **Indicadores de formato XML**: Tags como `<smoothly_flowing_prose_paragraphs>` para seccionar a saida.
3. **Espelhar o estilo desejado**: O estilo do prompt influencia o estilo da resposta — remover markdown do prompt reduz markdown na saida.
4. **Instrucoes detalhadas para preferencias especificas**: Bloco `<avoid_excessive_markdown_and_bullet_points>` com regras granulares.

### 2.4 Uso de Ferramentas

Descobertas-chave sobre tool use com Claude 4.6:

- **Explicitude e acao**: Claude pode sugerir em vez de implementar se o prompt for ambiguo. Usar "Change this function" em vez de "Can you suggest some changes".
- **Bloco `<default_to_action>`**: Para comportamento proativo por padrao.
- **Bloco `<do_not_act_before_instructions>`**: Para comportamento conservador.
- **Calibracao de overtriggering**: Claude 4.6 e mais responsivo ao system prompt que versoes anteriores. Linguagem agressiva como "CRITICAL: You MUST use this tool when..." causa overtriggering. Usar linguagem normal: "Use this tool when..."
- **Paralelismo nativo**: Claude 4.6 executa chamadas de ferramentas em paralelo nativamente. Bloco `<use_parallel_tool_calls>` eleva taxa para ~100%.

### 2.5 Pensamento e Raciocinio

- **Adaptive thinking** (`thinking: {type: "adaptive"}`) e o padrao para Claude 4.6 — o modelo decide dinamicamente quando e quanto pensar.
- **Overthinking em Opus 4.6**: O modelo faz exploracao excessiva em effort alto. Solucao: "Choose an approach and commit to it. Avoid revisiting decisions unless you encounter new information that directly contradicts your reasoning."
- **Instrucoes gerais superam passos prescritivos**: "think thoroughly" produz melhor raciocinio do que um plano passo-a-passo escrito manualmente.
- **Exemplos few-shot com thinking**: Colocar tags `<thinking>` dentro de exemplos ensina o padrao de raciocinio.
- **Self-check**: "Before you finish, verify your answer against [test criteria]" funciona confiavelmente para codigo e matematica.

### 2.6 Sistemas Agenticos

Esta e a secao mais rica e diretamente aplicavel ao projeto:

**Raciocinio de longo horizonte e state tracking**:

- Claude mantem orientacao em sessoes estendidas focando em progresso incremental.
- Usar arquivos estruturados para estado (`tests.json`) e texto livre para progresso (`progress.txt`).
- Git como mecanismo de state tracking entre sessoes.
- Prompt de persistencia de contexto: *"Your context window will be automatically compacted as it approaches its limit... do not stop tasks early due to token budget concerns."*

**Workflows multi-janela de contexto**:

1. Primeira janela: setup (testes, scripts). Janelas futuras: iteracao sobre todo-list.
2. Testes em formato estruturado (`tests.json`) criados antes de comecar.
3. Scripts de qualidade de vida (`init.sh`) para evitar trabalho repetido.
4. Janela nova vs. compactacao: Claude 4.6 descobre estado do filesystem eficientemente.
5. Ferramentas de verificacao (Playwright MCP, computer use).

**Balanceamento autonomia/seguranca**:

- Classificar acoes por reversibilidade: locais/reversiveis = executar; destrutivas/compartilhadas = pedir confirmacao.
- Exemplo concreto: "Do not use destructive actions as a shortcut. For example, don't bypass safety checks (e.g. --no-verify)."

**Orquestracao de subagentes**:

- Claude 4.6 reconhece e delega a subagentes nativamente, sem instrucao explicita.
- Risco: **overuse de subagentes** — "Claude Opus 4.6 has a strong predilection for subagents and may spawn them in situations where a simpler, direct approach would suffice."
- Criterios para subagentes: tarefas paralelizaveis, contexto isolado, workstreams independentes. Para tarefas simples: trabalhar diretamente.

**Anti-padroes agenticos**:

- **Overeagerness**: Opus 4.5/4.6 tende a overengineer. Bloco com instrucoes de escopo, documentacao, defensive coding e abstracoes minimas.
- **Hard-coding**: Claude pode focar em fazer testes passarem ao inves de solucoes gerais. Prompt: "Tests are there to verify correctness, not to define the solution."
- **Alucinacoes em codigo**: Bloco `<investigate_before_answering>` — nunca especular sobre codigo nao lido.
- **Criacao excessiva de arquivos**: Claude usa arquivos como scratchpad. Prompt de cleanup ao final.

---

## 3. Pontos de Atencao

### 3.1 Nuancias Faceis de Errar

| Nuance | Risco | Mitigacao |
|--------|-------|-----------|
| Linguagem agressiva (ALL-CAPS, "CRITICAL", "MUST") | Overtriggering em Claude 4.6 — comportamento excessivamente literal e ansioso | Usar linguagem normal e conversacional. O guia de prompting confirma: *"Formatacao agressiva (ALL-CAPS, 'NUNCA', 'JAMAIS') + modelos Claude recentes: produz resultados piores."* |
| Prefill responses depreciadas | Prefills no ultimo turno do assistente nao funcionam mais em Claude 4.6 | Migrar para instrucoes diretas, structured outputs, ou tool calling |
| Palavra "think" com thinking desabilitado | Claude Opus 4.5 e particularmente sensivel — pode ativar raciocinio nao-desejado | Usar alternativas: "consider", "evaluate", "reason through" |
| Prompts anti-preguica de versoes anteriores | Claude 4.6 ja e proativo por padrao; prompts que incentivavam thoroughness agora causam overthinking | Remover ou suavizar instrucoes do tipo "If in doubt, use [tool]" |
| CoT explicito com modelos de raciocinio | O guia de engenharia de prompts documenta que CoT explicito *prejudica* modelos de raciocinio (o1, R1) com 2-3% de melhoria marginal e 20-80% mais latencia | Para Claude 4.6 com adaptive thinking, preferir instrucoes gerais ("think thoroughly") sobre passos prescritivos |
| Few-shot com modelos de raciocinio avancados | Exemplos podem restringir o processo de raciocinio interno | Confiar no adaptive thinking; exemplos sao mais uteis para formato/tom do que para raciocinio |

### 3.2 Armadilhas de Aplicacao em Infraestrutura de Agentes

- **Documentar estrutura de arquivos em CLAUDE.md/AGENTS.md**: O guia de prompting recomenda fundamentacao em citacoes, mas os guias de CLAUDE.md e AGENTS.md alertam que paths mudam constantemente e envenenam o contexto. A solucao correta e descrever capacidades, nao estrutura.
- **Confundir system prompt com user prompt**: O guia de engenharia e explicito — role e restricoes no system prompt (persistencia entre turnos), exemplos few-shot no user prompt (flexibilidade por tarefa). Em skills e regras, isso se traduz em: convencoes estáveis nas regras path-scoped, instrucoes dinamicas no corpo do SKILL.md.
- **Ignorar o custo de tokens de exemplos em subagentes**: O guia documenta que cada exemplo adiciona 50-200+ tokens, e "em sistemas multi-agentes, exemplos competem com o orcamento limitado da janela de contexto de subagentes." Subagentes devem ter prompts enxutos.

---

## 4. Casos de Uso e Escopo

### 4.1 System Prompts vs User Prompts

| Elemento | System Prompt | User Prompt |
|----------|---------------|-------------|
| Role/persona | Sim — persistente entre turnos | Nao |
| Restricoes de formato | Sim | Refinamento pontual |
| Exemplos few-shot | Nao (a menos que fixos) | Sim — flexibilidade por tarefa |
| Contexto de documentos | Nao | Sim — injetado dinamicamente |
| Guardrails de seguranca | Sim — sempre ativos | Nao |
| Query especifica | Nao | Sim — ao final, apos documentos |

### 4.2 Single-turn vs Multi-turn

- **Single-turn**: Foco em clareza, exemplos few-shot, XML structuring. Toda a informacao no prompt.
- **Multi-turn**: Foco em state tracking, context awareness, compactacao. O prompt precisa instruir sobre persistencia e recuperacao de estado.
- **Multi-window**: Adiciona scripts de setup, testes estruturados, e `progress.txt`. Primeira janela diferente das subsequentes.

### 4.3 Tarefas Simples vs Complexas

| Complexidade | Tecnicas Recomendadas | Configuracao de Thinking |
|--------------|----------------------|--------------------------|
| Simples (classificacao, QA) | Zero-shot, instrucoes diretas | Thinking desabilitado ou effort low |
| Moderada (geracao de codigo, analise) | Few-shot + XML tags, role prompting | Adaptive thinking, effort medium |
| Complexa (refatoracao, pesquisa, multi-step) | Prompt chaining, subagent orchestration, structured state | Adaptive thinking, effort high |
| Extrema (migracoes, pesquisa profunda) | Multi-window, subagentes paralelos, hipoteses competitivas | Opus 4.6, adaptive thinking, effort max |

---

## 5. Aplicabilidade a Infraestrutura de Agentes

### 5.1 Skills (SKILL.md)

As best practices do documento traduzem-se diretamente para a escrita de SKILL.md:

**Estruturacao por fases com XML implicito**:
O documento recomenda tags XML para desambiguar secoes. Em SKILL.md, as fases (`Phase 1: Codebase Analysis`, `Phase 2: Scope Detection`, etc.) servem como separadores semanticos equivalentes. Cada fase deve ter um objetivo unico e claro, seguindo o principio de prompt chaining:

> *"With adaptive thinking and subagent orchestration, Claude handles most multi-step reasoning internally. Explicit prompt chaining is still useful when you need to inspect intermediate outputs or enforce a specific pipeline structure."*

**Hard Rules como guardrails no system prompt**:
O bloco `<RULES>` no inicio do SKILL.md funciona como o system prompt do skill — restricoes que devem ser sempre atendidas. A recomendacao de *"Tell Claude what to do instead of what not to do"* aplica-se parcialmente: regras de proibicao (`NEVER`) sao aceitaveis quando o custo de violacao e alto (ex.: "NEVER exceed 200 lines per file"), mas devem ser complementadas com o que fazer positivamente.

**Contexto motivacional nas instrucoes**:
O `init-claude` SKILL.md ja exemplifica este principio com:
> *"Research shows that auto-generated comprehensive configuration files reduce agent task success by ~3% while increasing cost by 20%+"*

Esta motivacao ajuda Claude a entender *por que* deve ser minimalista, nao apenas que deve ser.

**Exemplos em references/**:
Ao inves de colocar exemplos few-shot diretamente no SKILL.md (consumindo orcamento), usa-se `references/` como progressive disclosure — carregados apenas quando a fase relevante e executada. Isto se alinha com: *"In-context examples are one of the most reliable ways to steer Claude's output format, tone, and structure"* sem pagar o custo de tokens permanentemente.

**Recomendacoes praticas para SKILL.md**:

```markdown
# Padrao recomendado para instrucoes de fase

### Phase N: [Nome da Fase]

[Contexto motivacional — por que esta fase existe e o que acontece se for feita errado]

[Instrucao direta e especifica — o que fazer, nao o que nao fazer]

[Referencia condicional — "Read `references/X.md` if the project uses Y"]

[Criterio de sucesso — verificacao explicita do resultado]
```

### 5.2 Hooks

Hooks executam antes ou depois de acoes do agente. Os padroes de prompting aplicaveis sao:

**Clareza e direcionamento absolutos**:
Hooks devem ser os prompts mais curtos e explicitos do sistema. Nao ha espaco para ambiguidade. O principio *"be specific about the desired output format and constraints"* e critico aqui.

**Structured output obrigatorio**:
Hooks frequentemente precisam de saida processavel por maquina. O documento recomenda duas etapas: raciocinio livre primeiro, formatacao estruturada depois. Para hooks, a formatacao deve ser a unica etapa — sem raciocinio, apenas verificacao e output.

**Anti-overtriggering**:
O documento alerta que Claude 4.6 e mais responsivo ao system prompt. Hooks que usam linguagem como "ALWAYS run this check" podem disparar em contextos irrelevantes. Usar condicoes especificas: "Run this check only when files in `src/api/` are modified."

### 5.3 Subagentes

O documento fornece orientacao direta sobre subagentes — esta e a secao mais rica para este projeto:

**Prompts de subagente devem ser auto-contidos**:
O principio de *"context isolation"* do LangChain e reforçado pelo documento. Cada subagente recebe um prompt completo com role, tarefa e formato de saida. Nao depender de contexto herdado do orquestrador.

**Role prompting como mecanismo de especializacao**:
O guia de engenharia de prompts e explicito: *"Role prompting e o mecanismo fundamental de especializacao em arquiteturas multi-agentes."* Cada subagente deve ter um papel claro no frontmatter (`description`) e no prompt de delegacao.

**Controle de escopo para evitar overuse**:

```text
# Padrao recomendado para prompt de delegacao a subagente
Analyze [scope specific]. Return ONLY [output format].
Do not [boundary — what is out of scope].
```

O documento alerta: *"Claude Opus 4.6 has a strong predilection for subagents and may spawn them in situations where a simpler, direct approach would suffice."* Isto significa que SKILL.md deve ser explicito sobre quando delegar vs. quando trabalhar diretamente.

**Orcamento de tokens em subagentes**:
O guia de engenharia documenta que exemplos few-shot consomem 50-200+ tokens cada e *"competem com o orcamento limitado da janela de contexto de subagentes"*. Subagentes devem receber zero-shot instructions com structured output, nao exemplos extensivos.

**Formato de saida estruturado**:
O documento recomenda structured outputs para comunicacao inter-agentes. O projeto ja implementa isto com formatos JSON no output dos subagentes (ex.: `codebase-analyzer` retornando analise estruturada).

### 5.4 Rules (`.claude/rules/`)

Regras path-scoped sao o equivalente a system prompts especializados por contexto. As best practices aplicaveis:

**Escopo preciso = contexto relevante**:
O principio de que *"every token in your AGENTS.md file gets loaded on every single request"* nao se aplica a rules — elas so carregam quando paths coincidem. Isto e progressive disclosure puro. Cada regra deve cobrir um topico unico, como o projeto ja faz (`git-commits.md`, `agent-files.md`, `plugin-skills.md`).

**Instrucoes especificas e acionaveis**:
O documento de context optimization cita: *"Vague instructions consume attention without guiding behavior."* Regras como `"model: sonnet — never haiku (too weak for analysis) or opus (too costly)"` sao exemplos de especificidade acionavel.

**Tom conversacional, nao imperativo agressivo**:
O guia de AGENTS.md recomenda *"light touch, no 'always,' no all-caps forcing. Just a conversational reference."* O documento de best practices confirma: linguagem agressiva causa overtriggering em Claude 4.6. Regras devem usar linguagem direta mas nao gritante.

**Padrao recomendado para rules**:

```markdown
---
paths:
  - "path/to/scope/**"
---
# [Topico Unico]

- [Instrucao especifica e acionavel]
- [Instrucao com motivacao quando nao-obvia]
- [Restricao com alternativa positiva]
```

### 5.5 Memory

O documento traz orientacoes especificas para gerenciamento de memoria em sistemas agenticos:

**Formatos estruturados para dados de estado**:
> *"Use structured formats for state data: When tracking structured information (like test results or task status), use JSON or other structured formats"*

**Texto livre para notas de progresso**:
> *"Use unstructured text for progress notes: Freeform progress notes work well for tracking general progress and context"*

**Git como mecanismo de memoria**:
> *"Git provides a log of what's been done and checkpoints that can be restored."*

**Memoria e context awareness**:
O memory tool da Anthropic e descrito como complemento natural ao context awareness. A instrucao *"save your current progress and state to memory before the context window refreshes"* e diretamente aplicavel a skills que operam em multi-window.

**Estruturacao de arquivos de memoria**:

- Arquivos de estado: JSON com schema definido (ex.: `tests.json` com campos `id`, `name`, `status`)
- Arquivos de progresso: Texto livre com timestamps e proximos passos
- Convencao de naming: descritivo e previsivel para que Claude descubra por filesystem exploration

---

## 6. Aplicabilidade do Guia de Engenharia de Prompts

### 6.1 Mapeamento entre Best Practices e Tecnicas de Raciocinio

| Tecnica (Guia de Eng.) | Best Practice Correspondente | Relacao |
|------------------------|-----------------------------|---------|
| **Role Prompting** | "Give Claude a role" | Alinhamento direto — ambos recomendam papel no system prompt. O guia academico adiciona: role prompting nao melhora acuracia factual, valor esta no estilo. |
| **Zero-Shot** | Estilo padrao de instrucoes no best practices | Base de quase todas as instrucoes. O best practices assume zero-shot como padrao e adiciona few-shot apenas para formato. |
| **Few-Shot** | "Use examples effectively" (3-5 em tags `<example>`) | Alinhamento direto. O guia academico adiciona nuance: *"a ordem dos exemplos importa significativamente"* (Lu et al., 2021) e *"o espaco de labels importa mais que a correcao dos labels"* (Min et al., 2022). |
| **Chain-of-Thought** | "Leverage thinking capabilities", "Manual CoT as a fallback" | Complementar — o best practices recomenda adaptive thinking como padrao, CoT manual apenas quando thinking esta desabilitado. O guia academico valida: CoT explicito e contraproducente em modelos de raciocinio avancados. |
| **Self-Consistency** | "Ask Claude to self-check" | Indiretamente relacionado — self-check e uma forma leve de self-consistency (verificacao, nao votacao majoritaria). O custo de self-consistency plena (5-30x tokens) e proibitivo para skills/subagentes. |
| **Tree of Thoughts** | "Research and information gathering" com hipoteses competitivas | Complementar — o prompt de pesquisa estruturada (*"develop several competing hypotheses"*) implementa uma versao leve de ToT. O custo completo de ToT (5-20x chamadas de API) e impraticavel para a maioria dos skills. |
| **ReAct** | Todo o framework de tool use + thinking | Alinhamento fundamental — Claude 4.6 com adaptive thinking e ferramentas implementa ReAct nativamente (Pensamento -> Acao -> Observacao). O best practices nao menciona ReAct por nome porque *e o comportamento padrao do modelo*. |
| **Prompt Chaining** | "Chain complex prompts", orquestracao de subagentes | Alinhamento direto. O best practices nota: *"With adaptive thinking and subagent orchestration, Claude handles most multi-step reasoning internally."* Chaining explicito e para inspecao e controle, nao para capacidade. |
| **Structured Output** | "Control the format of responses", XML tags | Alinhamento direto. O guia academico adiciona dado critico: *"Forcar JSON durante raciocinio degrada a acuracia em 10-15%"* — raciocinar livre primeiro, formatar depois. |
| **RAG Patterns** | "Long context prompting", documentos no topo + query ao final | Complementar — o best practices implementa padroes RAG sem nomeá-los. O *"dual prompt structure"* do guia academico mapeia diretamente para system prompt + user prompt com contexto. |
| **Meta-Prompting** | Nao mencionado diretamente | Lacuna — meta-prompting (LLM gerando/otimizando prompts) nao e coberto pelo best practices, mas e relevante para este projeto (skills que geram CLAUDE.md sao uma forma de meta-prompting). |
| **Constitutional AI** | "Balancing autonomy and safety", self-correction chaining | Indiretamente relacionado — o padrao gerar -> revisar -> refinar e uma implementacao pratica do loop critique -> revision da Constitutional AI. |
| **Step-Back Prompting** | Nao mencionado diretamente | Aplicavel a skills: antes de gerar um CLAUDE.md, perguntar "Quais sao os principios fundamentais de um bom CLAUDE.md?" (step-back) antes de analisar o projeto especifico. |

### 6.2 Onde Complementam vs. Onde Conflitam

**Complementaridade forte**:

- O guia academico fornece **benchmarks quantitativos** que justificam as recomendacoes qualitativas do best practices. Exemplo: *"queries ao final melhoram qualidade em ate 30%"* (mencionado no best practices) e corroborado pelo guia com dados do paper da Anthropic sobre system prompts vs user prompts.
- O guia academico documenta **quando NAO usar** cada tecnica, informacao ausente no best practices. Exemplo: few-shot prejudica modelos de raciocinio, CoT so funciona com modelos de 100B+ parametros.
- A **matriz de decisao por tier de modelo** do guia academico complementa as recomendacoes de effort level do best practices.

**Conflito aparente resolvido**:

- O best practices diz *"Include 3-5 examples for best results"* enquanto o guia academico diz few-shot prejudica modelos de raciocinio. A resolucao: exemplos sao para **formato e tom**, nao para raciocinio. Quando o objetivo e formato, few-shot e otimo. Quando o objetivo e raciocinio, confiar no adaptive thinking.

**Lacuna do best practices preenchida pelo guia**:

- **Custo de tokens**: O best practices nao discute otimizacao de custo. O guia documenta que *"performance de raciocinio comeca a degradar em torno de 3.000 tokens"* e que o sweet spot e *"150-300 palavras de prompt"*. Isto e critico para dimensionar rules e SKILL.md.
- **Chain of Draft (CoD)**: Alternativa ao CoT que *"iguala a acuracia usando apenas ~7,6% dos tokens"*. Aplicavel a subagentes com orcamento restrito.
- **Emotion Prompting**: *"Isto e muito importante para minha carreira"* melhora performance em >10%. Contra-intuitivo, mas potencialmente util em prompts de skills que precisam de alta qualidade.

---

## 7. Correlacoes com Outros Documentos Principais

### 7.1 research-llm-context-optimization.md

| Conceito | Context Optimization | Best Practices | Convergencia |
|----------|---------------------|---------------|--------------|
| Context rot | *"LLMs, like humans, lose focus as context grows"* | Dados longos no topo, queries ao final | Ambos reconhecem degradacao com contexto longo; best practices fornece a solucao pratica (posicionamento) |
| Lost-in-the-middle | Informacao no inicio ou fim performa melhor; meio degrada | Nao mencionado diretamente, mas a recomendacao de queries ao final e consistente | O best practices implementa implicitamente a mitigacao do efeito |
| Instruction budget (~150-200) | *"Frontier thinking LLMs can follow ~150-200 instructions"* | Nao quantifica, mas todas as instrucoes sao minimalistas por design | O best practices opera dentro do budget sem o nomear |
| Progressive disclosure | *"just in time context strategy"*, skills como mecanismo | Nao usa o termo, mas a secao de multi-window workflows implementa o conceito | Multi-window = progressive disclosure temporal; references/ = progressive disclosure estrutural |
| Hybrid strategy | CLAUDE.md always-loaded + tools on-demand | System prompt persistente + tool use dinamico | Mapeamento direto: system prompt = always-loaded; tool calls = on-demand |
| Compaction | Referencia ao memory tool e context awareness | Instrucoes de persistencia antes de compactacao | Best practices fornece o prompt exato; context optimization fornece a teoria |

### 7.2 Evaluating-AGENTS-paper.md (ETH Zurich)

| Achado do Paper | Conexao com Best Practices |
|----------------|---------------------------|
| *"LLM-generated context files tend to decrease agent performance by ~3%"* | Corrobora a recomendacao de minimalismo. O best practices diz para ser explicito e especifico, nao compreensivo. |
| *"Developer-written context files slightly improve (+4%)"* | Developer-written = instrucoes intencionais e focadas, alinhado com *"think of Claude as a brilliant but new employee"* |
| *"Context files lead to more thorough testing and exploration"* + *"increase costs by over 20%"* | Diretamente relacionado ao aviso de overthinking: *"Claude Opus 4.6 does significantly more upfront exploration than previous models"*. O custo de 20% mapeia para o overtriggering. |
| *"Unnecessary requirements from context files make tasks harder"* | Alinhado com a regra de *"Would removing this cause Claude to make mistakes? If not, cut it."* do context optimization |
| *"Human-written context files should describe only minimal requirements"* | Convergencia total com o best practices: ser direto, especifico, minimalista. |

### 7.3 a-guide-to-agents.md e a-guide-to-claude.md

| Principio dos Guias | Equivalente no Best Practices |
|---------------------|-------------------------------|
| *"One-sentence project description acts like a role-based prompt"* | *"Give Claude a role"* — system prompt com uma sentenca de papel |
| *"Stale documentation poisons context... describe capabilities, not structure"* | *"Ground responses in quotes"* — fundamentar em dados reais, nao em descricoes que podem estar desatualizadas |
| *"Progressive disclosure: give the agent only what it needs right now"* | Multi-window workflows: primeira janela setup, futuras janelas iteracao. References/ condicionais em SKILL.md. |
| *"No 'always', no all-caps forcing. Just a conversational reference."* | *"Claude is much better at appropriate refusals now. Clear prompting without prefill should be sufficient."* + calibracao de overtriggering |
| *"Instruction budget: ~150-200 instructions"* | Todas as recomendacoes de minimalismo; effort parameter como substituto para over-prompting |
| *"Never auto-generate your AGENTS.md"* | Convergencia total com o paper ETH Zurich e com o principio de intencionalidade |

---

## 8. Forcas e Limitacoes

### 8.1 Forcas

1. **Prescritivo e pratico**: Cada recomendacao vem com um prompt de exemplo copiavel. Nao e teoria — e um cookbook.
2. **Atualizacao para Claude 4.6**: Cobre migracoes especificas (prefill depreciado, adaptive thinking, effort parameter), tornando-o indispensavel para quem opera em producao.
3. **Secao agentica robusta**: Multi-window workflows, state tracking, subagent orchestration e anti-padroes (overeagerness, hard-coding, alucinacoes) cobrem cenarios reais de desenvolvimento com agentes.
4. **Calibracao explica de comportamento**: Fornece tanto o "acelerador" (`<default_to_action>`) quanto o "freio" (`<do_not_act_before_instructions>`), reconhecendo que diferentes use cases precisam de diferentes niveis de proatividade.
5. **Convergencia com pesquisa independente**: As recomendacoes alinham-se com os achados do paper ETH Zurich, da pesquisa de context optimization e dos guias da comunidade, sem citar essas fontes. Isto sugere que sao principios robustos, nao opinioes isoladas.

### 8.2 Limitacoes

1. **Ausencia de metricas de custo**: O documento nao discute otimizacao de tokens, custo por requisicao ou trade-offs de custo vs. qualidade. O guia de engenharia de prompts preenche esta lacuna com dados quantitativos.
2. **Nao menciona tecnicas negativas**: Nao documenta explicitamente quais tecnicas classicas *nao* usar com Claude 4.6 (ex.: CoT explicito com adaptive thinking, few-shot extensivo para raciocinio). O guia academico e necessario para este contra-ponto.
3. **Focado em API, nao em config files**: As recomendacoes sao para prompts de API, nao para CLAUDE.md/AGENTS.md. A traducao para config files requer cruzamento com os outros documentos-ancora.
4. **Exemplos centralizados em coding**: A maioria dos exemplos e de desenvolvimento de software. Aplicacoes nao-code (pesquisa, escrita, analise) tem menos cobertura.
5. **Migracoes especificas para Claude 4.5 -> 4.6**: Partes significativas do documento sao guia de migracao que terao vida util limitada quando novos modelos surgirem.
6. **Nao aborda meta-prompting**: Tecnica diretamente relevante para este projeto (gerar CLAUDE.md e uma forma de meta-prompting) nao e coberta.

---

## 9. Recomendacoes Praticas

### 9.1 Para Escrita de Skills (SKILL.md)

1. **Abrir com contexto motivacional**: Antes das instrucoes, explicar *por que* o skill existe e qual problema resolve. Claude generaliza melhor com motivacao.
2. **Fases como prompt chaining explicito**: Cada fase = um objetivo unico. Criterios de sucesso explicitos ao final de cada fase. Inspecionar output intermediario entre fases.
3. **Hard Rules como system prompt**: Bloco `<RULES>` com restricoes criticas no topo. Usar proibicoes (`NEVER`) apenas para violacoes de alto custo. Complementar com alternativas positivas.
4. **References/ como few-shot on-demand**: Exemplos e guias de referencia em arquivos separados, carregados condicionalmente. Nao poluir o SKILL.md principal com exemplos extensivos.
5. **Calibrar linguagem para Claude 4.6**: Evitar ALL-CAPS e linguagem agressiva. "Use X" em vez de "You MUST ALWAYS use X". Excecao: restricoes de seguranca/integridade podem usar linguagem forte.
6. **Self-check ao final**: Fase de validacao que le `references/validation-criteria.md` e verifica cada criterio. Alinhado com: *"Before you finish, verify your answer against [test criteria]."*
7. **Target de tamanho**: SKILL.md body ate 500 linhas (convencao do projeto), mas quanto menor, melhor. Cada instrucao deve passar o teste: "Would removing this cause Claude to make mistakes?"

### 9.2 Para Hooks

1. **Prompts ultra-curtos e especificos**: Hooks sao os prompts mais restritos do sistema. Uma instrucao, um formato de saida, uma condicao de trigger.
2. **Structured output sem raciocinio**: Hooks nao devem pedir que Claude "pense" — apenas que verifique e retorne resultado estruturado.
3. **Condicoes de trigger explicitas**: Em vez de "Always check X", usar "Check X when files matching `path/pattern` are modified."
4. **Linguagem neutra**: Zero linguagem agressiva. Claude 4.6 atendera condicoes especificas sem reforco emocional.

### 9.3 Para Subagentes

1. **Prompt auto-contido com role, tarefa e formato**: Nao depender de contexto herdado. O subagente deve poder executar com seu prompt isoladamente.
2. **Zero-shot instructions, nao few-shot**: O orcamento de tokens de subagentes e limitado. Usar instrucoes diretas com structured output, nao exemplos.
3. **Escopo estreito e explicito**: "Return ONLY [output format]. Do not [boundary]." Evitar tarefas abertas que levem a over-exploration.
4. **model: sonnet para analise, nao opus**: Convencao do projeto. Opus e muito caro para subagentes. Sonnet com instrucoes claras atende a maioria das analises.
5. **maxTurns limitado**: 15-20 turnos para evitar loops infinitos. Alinhado com o principio de *"choose an approach and commit to it"*.
6. **Ferramentas read-only**: `Read, Grep, Glob, Bash` — subagentes de analise nao devem modificar o sistema. Alinhado com *"consider the reversibility and potential impact of your actions."*

### 9.4 Para Rules (`.claude/rules/`)

1. **Uma regra, um topico, um arquivo**: Seguindo o principio de que cada instrucao deve ser especifica e acionavel.
2. **Paths precisos no frontmatter**: `paths: ["src/api/**"]` em vez de paths amplos. Quanto mais preciso o path, menos contexto desperdicado.
3. **Tom conversacional**: *"Use 2-space indentation"* em vez de *"YOU MUST ALWAYS USE 2-SPACE INDENTATION"*. Claude 4.6 e mais responsivo e nao precisa de linguagem agressiva.
4. **Incluir motivacao quando nao-obvia**: Se uma regra existe por uma razao contra-intuitiva, explicar o por que. *"Claude is smart enough to generalize from the explanation."*
5. **Target: 5-20 linhas por arquivo de regra**: Regras sao micro-system-prompts. Devem ser scaneaveis em um olhar.

### 9.5 Para Memory

1. **Separar estado estruturado de notas de progresso**: JSON para dados maquina (testes, status de tarefas). Texto livre para contexto humano (decisoes, proximos passos).
2. **Naming previsivel**: `tests.json`, `progress.txt`, `state.json` — nomes que Claude descobre via filesystem exploration.
3. **Instrucao de persistencia antes de compactacao**: Em skills de longo horizonte, incluir: *"Save your current progress and state to memory before the context window refreshes."*
4. **Git como memoria implicita**: Commits atomicos com mensagens descritivas servem como log de estado entre sessoes. Claude 4.6 *"performs especially well in using git to track state across multiple sessions."*
5. **Nao armazenar paths absolutos**: Paths mudam. Armazenar descricoes de capacidades e estados, nao localizacoes de arquivos.
