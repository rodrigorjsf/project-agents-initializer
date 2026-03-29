# Analise: A Complete Guide To CLAUDE.md

## 1. Sumario Executivo

O guia "A Complete Guide To CLAUDE.md" apresenta uma filosofia de configuracao minimalista especifica para o ecossistema Claude Code. Embora compartilhe principios fundamentais com o guia de AGENTS.md (minimalismo, progressive disclosure, instruction budget), o CLAUDE.md opera dentro de uma arquitetura significativamente mais rica e sofisticada. O Claude Code oferece mecanismos nativos como subdirectory CLAUDE.md com merge automatico, `.claude/rules/` com path-scoping, `@imports`, skills com contexto isolado, hooks deterministicos e um sistema de memoria auto-gerenciado -- cada um representando uma camada distinta de progressive disclosure que nao existe no padrao aberto AGENTS.md.

O documento parte da mesma premissa central: arquivos CLAUDE.md massivos sao contraproducentes. A mesma dinamica de "ball of mud" se aplica, com o agravante de que o Claude Code processa o CLAUDE.md em uma posicao especifica na hierarquia de contexto -- logo abaixo do system prompt. Isso significa que um CLAUDE.md inflado compete diretamente com o espaco necessario para a tarefa, ferramentas e raciocinio do modelo. A recomendacao da Anthropic de manter cada arquivo CLAUDE.md com **menos de 200 linhas** reforça a urgencia do minimalismo.

O aspecto mais distintivo deste guia, em contraste com o de AGENTS.md, e a profundidade do ecossistema de progressive disclosure disponivel. Enquanto o AGENTS.md depende fundamentalmente de arquivos markdown em subdiretorios e referencias textuais, o CLAUDE.md pode delegar para rules (carregadas condicionalmente por path), skills (com contexto isolado via `context: fork`), hooks (enforcement deterministico fora do contexto), subdirectory CLAUDE.md (merge automatico quando o agente trabalha naquele diretorio), e @imports (composicao modular). Cada mecanismo tem um perfil distinto de custo de contexto, timing de carregamento e nivel de enforcement. Dominar essa taxonomia e a chave para uma configuracao CLAUDE.md eficaz.

---

## 2. Principais Achados e Principios

### 2.1 O Anti-Padrao do "Ball of Mud" no Contexto Claude Code

O guia identifica o mesmo ciclo de feedback do AGENTS.md:

> "1. The agent does something you don't like / 2. You add a rule to prevent it / 3. Repeat hundreds of times over months / 4. File becomes a 'ball of mud'"

No contexto do Claude Code, esse problema e amplificado por dois fatores adicionais: (a) o Claude Code carrega automaticamente o CLAUDE.md raiz em **toda sessao**, sem possibilidade de carregamento condicional; e (b) diferentes escopos de CLAUDE.md (user, project, subdirectory) fazem merge, podendo criar contradicoes nao obvias entre niveis.

A condenacao de auto-geracao e igualmente enfatica:

> "Never use initialization scripts to auto-generate your CLAUDE.md. They flood the file with things that are 'useful for most scenarios' but would be better progressively disclosed."

Isso e particularmente relevante porque o Claude Code oferece nativamente o comando `/init` para gerar o CLAUDE.md, e a Anthropic recomenda essa pratica em sua documentacao oficial -- criando tensao direta com o principio deste guia.

### 2.2 O Orcamento de Instrucoes

A referencia ao artigo de Kyle da Humanlayer e identica:

> "Frontier thinking LLMs can follow ~ 150-200 instructions with reasonable consistency."

Porem, no contexto do Claude Code, esse orcamento e compartilhado entre multiplas fontes: CLAUDE.md raiz, subdirectory CLAUDE.md, `.claude/rules/` (carregadas), e conteudo de skills invocadas. A implicacao e que o orcamento efetivo para o CLAUDE.md raiz e **menor** do que 150-200, porque parte da capacidade sera consumida por rules e outras fontes de instrucao carregadas durante a sessao.

### 2.3 Documentacao Obsoleta Envenena o Contexto

O guia repete a advertencia sobre documentacao obsoleta:

> "For AI agents that read documentation on every request, stale information actively _poisons_ the context."

No ecossistema Claude Code, isso tem implicacao adicional: o sistema de memoria auto-gerenciado pode criar informacoes que conflitam com o CLAUDE.md se este nao for mantido atualizado. O Claude pode memorizar padroes de uma sessao que contradizem instrucoes obsoletas no CLAUDE.md, criando um ciclo de confusao.

A recomendacao especifica permanece: **descrever capacidades, nao estruturas**. No Claude Code, isso e ainda mais relevante porque o agente tem ferramentas nativas (glob, grep, Read) para explorar a estrutura do projeto em tempo real, tornando mapeamentos estaticos duplamente redundantes.

### 2.4 O Minimo Absoluto

Identico ao AGENTS.md:

1. **Descricao do projeto em uma frase**
2. **Gerenciador de pacotes** (se nao npm)
3. **Comandos de build/typecheck** (se nao padrao)

> "That's honestly it. Everything else should go elsewhere."

No Claude Code, "elsewhere" significa um ecossistema muito mais rico do que simples arquivos markdown.

### 2.5 Progressive Disclosure com Mecanismos Nativos

O guia apresenta progressive disclosure em tres niveis basicos, mas o Claude Code estende isso significativamente:

1. **Referencias a arquivos separados**: `"For TypeScript conventions, see docs/TYPESCRIPT.md"` -- o agente carrega sob demanda
2. **Aninhamento de referencias**: arvore de recursos descobrivel
3. **Skills de agentes**: descritas como "commands or workflows the agent can invoke to learn how to do something specific"

O que o guia nao detalha (mas a documentacao do Claude Code oferece) sao os mecanismos adicionais:

- **`.claude/rules/`**: regras modulares, opcionalmente com path-scoping via YAML frontmatter
- **Subdirectory CLAUDE.md**: merge automatico quando o Claude trabalha em subdiretorios
- **`@imports`**: composicao modular com `@path/to/import` syntax (max 5 hops)
- **Skills com `context: fork`**: execucao em contexto isolado de subagente
- **Skills com `disable-model-invocation: true`**: descricoes mantidas fora do contexto ate invocacao manual
- **Hooks**: enforcement deterministico completamente fora do contexto LLM

### 2.6 CLAUDE.md em Monorepos

A hierarquia de dois niveis e identica ao AGENTS.md:

| Nivel | Conteudo |
|-------|----------|
| **Root** | Proposito do monorepo, navegacao entre pacotes, ferramentas compartilhadas |
| **Package** | Proposito do pacote, tech stack especifica, convencoes do pacote |

Com a advertencia: **"Don't overload any level."** No Claude Code, monorepos tem suporte adicional via `claudeMdExcludes` em settings.json para evitar carregamento de CLAUDE.md de times irrelevantes.

---

## 3. Pontos de Atencao

### 3.1 O Perigo da Linguagem Imperativa

O guia faz a mesma observacao sobre tom:

> "Notice the light touch, no 'always,' no all-caps forcing. Just a conversational reference."

Isso e particularmente importante no Claude Code porque a documentacao oficial de prompting confirma que modelos Claude recentes respondem pior a linguagem coercitiva:

> "Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'" (claude-prompting-best-practices.md)

O Claude Opus 4.6 e descrito como "more responsive to the system prompt than previous models", o que significa que instrucoes anteriormente necessarias para forcar compliance agora causam overtriggering.

### 3.2 A Tensao entre Minimalismo e Ecossistema Rico

O Claude Code oferece tantos mecanismos de configuracao que o risco real nao e so um CLAUDE.md inflado, mas um **sistema de configuracao fragmentado** onde instrucoes estao espalhadas entre CLAUDE.md, rules, skills, hooks e memoria sem uma visao clara do todo. O guia foca no CLAUDE.md isoladamente, mas na pratica a complexidade total do sistema de instrucoes inclui todas essas fontes.

### 3.3 Merge Automatico de CLAUDE.md Hierarquicos

O guia menciona que subdirectory CLAUDE.md "merge with the root level", mas nao aborda as implicacoes de conflitos entre niveis. A documentacao da Anthropic alerta:

> "If two rules contradict each other, Claude may pick one arbitrarily."

Isso significa que um subdirectory CLAUDE.md que contradiz o raiz pode causar comportamento imprevisivel. Em monorepos com muitos times, essa e uma fonte de bugs sutil.

### 3.4 O Custo Oculto de Rules sem Path-Scoping

Rules no diretorio `.claude/rules/` sem frontmatter `paths:` sao carregadas **incondicionalmente** -- equivalente a estar no CLAUDE.md raiz. Desenvolvedores que movem conteudo do CLAUDE.md para rules pensando que estao fazendo progressive disclosure podem, na verdade, estar apenas fragmentando o mesmo conteudo always-loaded.

### 3.5 A Armadilha do `/init`

O comando `/init` do Claude Code gera um CLAUDE.md automaticamente. O paper "Evaluating AGENTS.md" mostra que 100% dos arquivos gerados pelo Sonnet-4.5 incluem overviews de codebase, e que esses overviews nao sao eficazes. A recomendacao do guia contra auto-geracao se aplica com forca total ao `/init` do Claude Code.

### 3.6 Memoria vs CLAUDE.md

O sistema de auto-memoria do Claude Code cria uma camada adicional de "instrucoes" que pode interferir com o CLAUDE.md. Se o Claude memoriza um padrao durante uma sessao e o CLAUDE.md e atualizado posteriormente, a memoria obsoleta pode prevalecer sobre a instrucao atualizada. Nao ha mecanismo automatico de sincronizacao entre CLAUDE.md e memoria.

---

## 4. Casos de Uso e Escopo

### 4.1 Projetos Exclusivamente Claude Code

Quando toda a equipe usa Claude Code, o CLAUDE.md e o mecanismo primario de configuracao. O ecossistema completo (rules, skills, hooks, memoria, subdirectory CLAUDE.md) esta disponivel, permitindo a implementacao mais sofisticada de progressive disclosure.

### 4.2 Monorepos com Multiplos Times

O suporte a subdirectory CLAUDE.md com merge automatico, combinado com `claudeMdExcludes`, torna o CLAUDE.md especialmente adequado para monorepos. Cada time pode manter seu proprio CLAUDE.md sem afetar outros times, e o root CLAUDE.md fornece contexto comum.

### 4.3 Projetos com Requisitos de Enforcement

O Claude Code oferece hooks para enforcement deterministico. Para projetos onde certas regras **devem** ser seguidas (seguranca, compliance, padrao de codigo), a combinacao de CLAUDE.md minimalista + hooks e a abordagem mais robusta. O CLAUDE.md documenta o "por que", hooks garantem o "o que".

### 4.4 Projetos com Workflows Complexos

Skills do Claude Code permitem encapsular workflows complexos (deploy, migracao de banco, geracao de codigo) como unidades invocaveis sob demanda. Para projetos com muitos workflows, skills substituem a necessidade de documentar procedimentos no CLAUDE.md.

### 4.5 Projetos Open Source com Usuarios Claude Code

Repositorios open source que querem oferecer experiencia otimizada para usuarios do Claude Code podem incluir CLAUDE.md alem do AGENTS.md. O symlink inverso (`ln -s CLAUDE.md AGENTS.md`) garante que usuarios de outras ferramentas tambem se beneficiem.

### 4.6 Cenarios Menos Apropriados

- Projetos que precisam suportar multiplas ferramentas igualmente (AGENTS.md e mais universal)
- Equipes em transicao de ferramentas (o investimento em rules, skills, hooks e Claude Code-specific)
- Projetos com desenvolvedores que nao usam Claude Code (a configuracao nao sera utilizada)

---

## 5. Aplicabilidade a Infraestrutura de Agentes

### 5.1 Skills

O guia menciona skills como progressive disclosure:

> "Many tools support 'agent skills' - commands or workflows the agent can invoke to learn how to do something specific."

No Claude Code, skills tem um modelo de execucao sofisticado que o guia nao detalha:

**Impacto no design de skills:**

- **Descricao vs conteudo completo**: Claude ve descricoes de skills no inicio da sessao, mas o conteudo completo so carrega quando a skill e usada. A descricao deve ser suficiente para que o Claude saiba **quando** invocar a skill, sem consumir tokens desnecessarios.
- **`context: fork`**: skills com contexto isolado executam em subagentes independentes. Isso e a forma mais pura de progressive disclosure -- o conteudo da skill tem impacto **zero** no contexto principal. O CLAUDE.md deve orientar o uso dessas skills sem duplicar seu conteudo.
- **`disable-model-invocation: true`**: skills que nao sao visíveis ate invocacao manual. Ideal para workflows raros que nao devem competir pelo orcamento de atencao.
- **Conteudo dinamico com `` !`command` ``**: skills podem injetar dados em tempo real (ex: `!`gh pr diff``), implementando JIT documentation a nivel de skill.
- **Relacao com CLAUDE.md**: o CLAUDE.md nao deve documentar o que skills ja encapsulam. Se existe uma skill para deploy, o CLAUDE.md nao precisa de instrucoes de deploy -- no maximo uma referencia: "Para deploy, use a skill de deploy."

### 5.2 Hooks

O guia nao menciona hooks, mas a logica de minimalismo no CLAUDE.md implica uma estrategia de conversao fundamental para o ecossistema Claude Code:

- **Hooks removem instrucoes do orcamento de contexto**: uma instrucao como "sempre execute testes antes de commit" consumida como texto no CLAUDE.md pode ser convertida em um hook pre-commit que executa testes automaticamente. O hook e deterministico (garantido) e nao consome tokens.
- **O principio da pesquisa de otimizacao de contexto**: "Converting behavioral instructions to deterministic hooks removes them from the context budget entirely while guaranteeing enforcement." Isso e documentado explicitamente no research-llm-context-optimization.md.
- **Tipos de hooks relevantes**:
  - `PreToolUse`: antes de execucao de ferramentas (ex: validar antes de git push)
  - `PostToolUse`: apos execucao (ex: lint depois de editar arquivo)
  - `Notification`: alertas sobre comportamento (ex: notificar quando Claude tenta acessar producao)
  - `SessionStart`/`SessionEnd`: setup e cleanup de sessao
- **Decisao hook vs instrucao**: se a instrucao e do tipo "ALWAYS" ou "NEVER", e candidata a hook. Se envolve julgamento ou contexto ("prefira X quando Y"), mantenha como instrucao. A documentacao da Anthropic sugere: "If Claude already does something correctly without the instruction, delete it or convert it to a hook."

### 5.3 Subagentes

O principio de minimalismo do CLAUDE.md se aplica criticamente ao design de contexto de subagentes:

- **Context isolation**: subagentes via `context: fork` recebem contexto proprio. O CLAUDE.md raiz **nao** e automaticamente herdado por subagentes em contexto isolado -- o prompt do subagente deve conter apenas o necessario para sua tarefa.
- **Descricao de uma frase como role prompt**: a mesma tecnica do CLAUDE.md se aplica ao prompt de cada subagente -- uma frase definindo escopo e proposito.
- **Progressive disclosure para subagentes**: subagentes podem ter suas proprias hierarquias de contexto. Um subagente de exploracao pode receber referencias a documentacao que ele carrega sob demanda.
- **Claude Opus 4.6 e orquestracao nativa**: a documentacao de prompting alerta que o Opus 4.6 "has a strong predilection for subagents and may spawn them in situations where a simpler, direct approach would suffice." O CLAUDE.md pode incluir orientacao sobre quando subagentes sao e nao sao apropriados: "Use subagents when tasks can run in parallel, require isolated context, or involve independent workstreams."
- **Impacto na instruction budget**: cada subagente tem seu proprio orcamento de instrucoes. Subagentes focados com instrucoes minimas performam melhor que subagentes sobrecarregados de contexto.

### 5.4 Rules (`.claude/rules/`)

Rules sao o mecanismo de progressive disclosure mais diretamente ligado ao CLAUDE.md:

- **Rules sem paths = always-loaded**: equivalente a estar no CLAUDE.md raiz. Mover conteudo do CLAUDE.md para rules sem path-scoping nao economiza contexto -- apenas fragmenta.
- **Rules com paths = condicional**: `paths: ["src/api/**/*.ts"]` garante que a rule so carrega quando o Claude le arquivos API. Isso e genuine progressive disclosure.
- **Relacao com o CLAUDE.md**: o CLAUDE.md raiz deve conter regras universais (aplicaveis a qualquer tarefa). Rules path-scoped devem conter regras de dominio (API, frontend, testes). Nunca duplique: se esta no CLAUDE.md, nao precisa estar em rules.
- **Modularidade**: cada arquivo em `.claude/rules/` cobre um topico com filename descritivo. Isso facilita manutencao comparado a um CLAUDE.md monolitico.
- **Simlinks**: rules suportam symlinks para compartilhamento entre projetos, permitindo reutilizacao de convencoes organizacionais.
- **Descoberta recursiva**: rules em subdiretorios de `.claude/rules/` sao descobertas recursivamente, permitindo organizacao hierarquica: `.claude/rules/frontend/react.md`, `.claude/rules/backend/api.md`.

### 5.5 Memoria

A relacao entre CLAUDE.md e o sistema de memoria do Claude Code e de camadas complementares:

- **CLAUDE.md**: instrucoes estáticas, versionadas, compartilhadas pela equipe, commited no Git
- **Memoria auto-gerenciada**: informacoes dinâmicas, emergentes de sessoes, podendo ser pessoais ou de projeto
- **MEMORY.md**: as primeiras 200 linhas sao carregadas no startup, funcionando como indice. Topicos adicionais carregam sob demanda.
- **Nao duplique entre CLAUDE.md e memoria**: se algo e uma decisao de equipe, vai no CLAUDE.md (ou rules). Se e um padrao descoberto durante uso, vai na memoria.
- **Risco de conflito**: memoria pode conter informacoes que contradizem CLAUDE.md atualizado. Revisao periodica de memoria e necessaria.
- **Compactacao e memoria**: quando o contexto e compactado, instrucoes do CLAUDE.md sao preservadas (relidas do arquivo), mas informacoes de memoria inline podem ser perdidas. A diretriz de compactacao pode ser configurada no proprio CLAUDE.md: "When compacting, always preserve the full list of modified files and any test commands."
- **Boris Cherny sobre simplicidade**: o lead engineer do Claude Code descreveu a arquitetura de memoria como "the simplest thing, which is a file that has some stuff. And it's auto-read into context." Isso reforça que ate a memoria segue o principio de simplicidade maxima.

---

## 6. Aplicabilidade do Guia de Engenharia de Prompts

### 6.1 Role Prompting na Descricao do Projeto

A "one-sentence project description" do guia funciona como role prompting, mas no Claude Code tem implicacao adicional: essa descricao e injetada no inicio do contexto, logo apos o system prompt. O guia de prompts confirma que role prompting no system prompt "focuses Claude's behavior and tone for your use case."

No Claude Code, a descricao no CLAUDE.md ocupa uma posicao analoga ao system prompt para o contexto de projeto. E o mecanismo com melhor relacao custo-beneficio (10-30 tokens) para ancorar o comportamento do agente.

### 6.2 Structured Prompting e XML Tags no CLAUDE.md

O guia de prompts da Anthropic recomenda XML tags para estruturar prompts complexos:

> "XML tags help Claude parse complex prompts unambiguously, especially when your prompt mixes instructions, context, examples, and variable inputs."

No contexto do CLAUDE.md, isso significa que instrucoes podem se beneficiar de tags XML para separar secoes:

```xml
<project>
React component library for accessible data visualization.
</project>

<build>
pnpm build && pnpm typecheck
</build>
```

Porem, o guia recomenda "light touch" e markdown simples. A escolha entre XML e markdown no CLAUDE.md depende da complexidade: para os tres itens minimos, markdown basta. Para CLAUDE.md mais elaborados, XML tags podem melhorar a parsing.

A documentacao de prompting confirma que Claude foi treinado especificamente para reconhecer XML, com "15-20% de boost de performance" em comparacao com outros formatos.

### 6.3 Few-Shot via Exemplos em Rules ou Skills

O guia de prompts recomenda 3-5 exemplos diversos para estabilizar formato e comportamento. No CLAUDE.md, exemplos consomem orcamento valioso. A solucao e delegar exemplos para progressive disclosure:

- **Rules path-scoped**: exemplos de codigo API ficam em `.claude/rules/api-patterns.md` com `paths: ["src/api/**"]`
- **Skills**: exemplos de workflow complexo ficam encapsulados em skills, carregados apenas quando invocados
- **Arquivos referenciados**: `"For code examples, see docs/examples/PATTERNS.md"` mantém o CLAUDE.md enxuto

### 6.4 Chain-of-Thought e Instrucoes Procedurais

O guia de prompts mostra que CoT melhora raciocinio multi-passo mas com custo significativo de tokens. Para CLAUDE.md:

- Instrucoes devem ser declarativas ("Use 2-space indentation"), nao procedurais ("First check the current indentation, then...")
- Se o agente precisa seguir um procedimento multi-passo, esse procedimento deve estar em uma skill ou documento referenciado
- O Claude Opus 4.6 usa adaptive thinking internamente -- instrucoes explicitas de "pense passo a passo" sao contraproducentes e consomem tokens: "Prefer general instructions over prescriptive steps. A prompt like 'think thoroughly' often produces better reasoning than a hand-written step-by-step plan."

### 6.5 ReAct e a Arquitetura do Claude Code

O padrao ReAct (Pensamento -> Acao -> Observacao) e o loop central do Claude Code. O CLAUDE.md alimenta a fase de "Pensamento" -- fornecendo contexto para decisoes. Instrucoes bem escritas no CLAUDE.md melhoram a qualidade do "Pensamento" sem interferir no ciclo natural de ReAct.

A pratica de progressive disclosure se alinha perfeitamente com ReAct: o agente navega a arvore de documentacao como uma sequencia de acoes (ler arquivo) e observacoes (processar conteudo), construindo contexto incrementalmente.

### 6.6 Context Engineering como Framework Unificador

O guia de prompts identifica a transicao de prompt engineering para context engineering. No Claude Code, o CLAUDE.md e apenas uma peca de um sistema de contexto que inclui:

1. System prompt do Claude Code (fixo, nao editavel pelo usuario)
2. CLAUDE.md raiz (always-loaded, editavel)
3. Rules (condicionalmente loaded)
4. Skills (loaded on invocation)
5. Subdirectory CLAUDE.md (loaded on navigation)
6. Memoria (loaded at startup + on demand)
7. Hooks (fora do contexto, enforcement programatico)
8. Ferramentas (glob, grep, Read -- context gathering em tempo real)

O principio da Anthropic de "encontrar a solucao mais simples possivel" se aplica ao design desse sistema como um todo, nao apenas ao CLAUDE.md.

### 6.7 Self-Consistency e Revisao de Configuracao

O guia de prompts descreve Self-Consistency como amostragem de multiplos caminhos de raciocinio para a mesma tarefa. No contexto de manutencao de CLAUDE.md, isso sugere:

- Testar a mesma tarefa com e sem instrucoes especificas do CLAUDE.md
- Se o resultado e identico, a instrucao e redundante e deve ser removida
- Se o resultado varia inconsistentemente, a instrucao pode ser ambigua e precisa ser reescrita

### 6.8 Meta-Prompting e o Prompt de Refatoracao

O guia inclui um prompt pronto para refatorar CLAUDE.md inflados. Isso e uma aplicacao direta de meta-prompting -- usar o proprio LLM para otimizar as instrucoes que ele recebe. O guia de prompts documenta que meta-prompting com GPT-4 superou prompting padrao em 17.1%.

---

## 7. Correlacoes com Outros Documentos Principais

### 7.1 Evaluating-AGENTS-paper.md

O paper da ETH Zurich, embora focado em AGENTS.md, tem implicacoes diretas para CLAUDE.md:

- **Avaliacao incluiu Claude Code**: o paper testou Claude Code com Sonnet-4.5 especificamente, alimentando instrucoes via CLAUDE.md. O resultado: Claude Code foi o unico agente que **nao** melhorou com arquivos de contexto escritos por humanos (Figura 3 do paper).
- **Overviews gerados por LLM sao ineficazes**: 100% dos arquivos gerados pelo Sonnet-4.5 incluiram overviews. A propria documentacao do Claude Code "advocates for a high-level overview only and warns against listing components that are easily discoverable."
- **Custo aumentado**: arquivos de contexto aumentaram o custo do Claude Code de $1.15 para $1.30-$1.33 por instancia (13-16% de aumento).
- **Instrucoes sao seguidas**: o paper confirma que agentes seguem instrucoes do CLAUDE.md (ex: uso de `uv` quando mencionado), mas isso torna a tarefa mais dificil, com mais passos necessarios.
- **Redundancia com documentacao existente**: quando toda documentacao e removida, arquivos de contexto passam a ser uteis. Para o Claude Code, isso sugere que o CLAUDE.md agrega mais valor em projetos com pouca documentacao interna.
- **Implicacao critica**: o Claude Code ja e um agente altamente capaz de explorar repositorios com suas ferramentas nativas. CLAUDE.md excessivo pode estar adicionando "ruido" a um sistema que ja funciona bem sozinho.

### 7.2 research-llm-context-optimization.md

Este documento fornece a base cientifica e a documentacao da Anthropic que sustenta cada principio do guia:

- **Context rot**: a degradacao de performance com aumento de contexto fundamenta o minimalismo. No Claude Code, cada fonte de contexto (CLAUDE.md, rules, skills, memoria) contribui para o total de tokens. O gerenciamento deve ser holístico.
- **Lost-in-the-middle effect**: instrucoes criticas devem estar no **inicio** ou **final** do CLAUDE.md, nunca no meio. Para regras de `.claude/rules/`, o posicionamento depende de como o Claude Code as injeta no contexto (geralmente apos o CLAUDE.md raiz).
- **Instruction budget de ~200 linhas**: a recomendacao oficial da Anthropic: "Target under 200 lines per CLAUDE.md file." O guia esta totalmente alinhado.
- **Hybrid strategy**: o Claude Code implementa explicitamente o modelo hibrido: "CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time." O CLAUDE.md e a camada pre-loaded; todo o resto e on-demand.
- **Skills como progressive disclosure**: "Claude sees skill descriptions at session start, but the full content only loads when a skill is used." Isso e a implementacao tecnica do principio do guia.
- **Path-specific rules como carregamento condicional**: rules com frontmatter `paths:` "trigger only when Claude reads matching files, reducing noise and saving context."
- **Hooks como economia de contexto**: "Converting behavioral instructions to deterministic hooks removes them from the context budget entirely while guaranteeing enforcement." Esse e o principio mais impactante que o guia nao menciona explicitamente.
- **Compactacao**: o CLAUDE.md pode instruir como a compactacao deve funcionar: "When compacting, always preserve the full list of modified files." Isso e uma forma de meta-instrucao que sobrevive a compactacao.
- **Contradictions**: "If two rules contradict each other, Claude may pick one arbitrarily." Isso torna a revisao periodica de todas as fontes de instrucao (CLAUDE.md, rules, memoria) essencial.

### 7.3 claude-prompting-best-practices.md

O guia oficial de prompting da Anthropic se correlaciona de forma profunda com o CLAUDE.md:

- **"Be clear and direct"**: o principio golden rule ("Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too") se aplica diretamente a instrucoes no CLAUDE.md.
- **"Add context to improve performance"**: a descricao de uma frase funciona como contexto motivacional. O guia de prompts explica que fornecer motivacao ("Your response will be read aloud by a text-to-speech engine") e mais eficaz que proibicoes diretas ("NEVER use ellipses"). Para CLAUDE.md: "Use pnpm because we manage dependencies across packages in this monorepo" e melhor que "ALWAYS use pnpm."
- **Longform data position**: "Put longform data at the top... queries at the end can improve response quality by up to 30%." Para CLAUDE.md, a descricao do projeto (contexto) deve vir primeiro, seguida de instrucoes operacionais.
- **Anti-linguagem coercitiva**: "Claude Opus 4.5 and Claude Opus 4.6 are also more responsive to the system prompt than previous models. If your prompts were designed to reduce undertriggering on tools or skills, these models may now overtrigger." Para CLAUDE.md, instrucoes que usavam "CRITICAL" ou "MUST" em modelos anteriores devem ser suavizadas.
- **Subagent orchestration**: o Opus 4.6 orquestra subagentes nativamente. O CLAUDE.md pode guiar essa orquestracao: "Use subagents when tasks can run in parallel, require isolated context, or involve independent workstreams."
- **Overthinking**: "Claude Opus 4.6 does significantly more upfront exploration than previous models." Isso significa que CLAUDE.md nao precisa instruir o agente a ser "thorough" -- ele ja e. Instrucoes de exploracao excessiva podem causar desperdicio.
- **Multi-context window workflows**: a recomendacao de usar "a different prompt for the very first context window" e compativel com o CLAUDE.md -- instrucoes de setup podem ser diferentes de instrucoes de iteracao via skills ou conditional rules.

---

## 8. Forcas e Limitacoes

### 8.1 Forcas

1. **Principio de minimalismo validado**: a recomendacao de ~200 linhas tem respaldo tanto na documentacao da Anthropic quanto em pesquisa empirica
2. **Ecossistema rico de progressive disclosure**: o Claude Code oferece mais mecanismos de delegacao (rules, skills, hooks, memoria, @imports) do que qualquer outra ferramenta
3. **Praticabilidade**: o prompt de refatoracao oferece uma acao concreta e imediata
4. **Escalabilidade**: subdirectory CLAUDE.md e monorepo support permitem escalar para projetos grandes
5. **Versionamento**: CLAUDE.md e commited no Git, permitindo revisao, historico e rollback
6. **Merge automatico**: CLAUDE.md hierarquico com merge nativo simplifica monorepos

### 8.2 Limitacoes

1. **Nao aborda hooks**: o guia nao menciona a conversao de instrucoes para hooks, que e uma das estrategias mais impactantes para economia de contexto
2. **Nao detalha rules**: o mecanismo `.claude/rules/` e apenas uma das formas de "separate file" mencionadas, sem distincao entre rules always-loaded e path-scoped
3. **Nao aborda @imports**: o sistema de composicao via `@path/to/import` nao e mencionado
4. **Nao aborda memoria**: a interacao entre CLAUDE.md e o sistema de auto-memoria nao e discutida
5. **Foco em JavaScript/TypeScript**: exemplos predominantemente Node.js
6. **Nao aborda compactacao**: como instrucoes do CLAUDE.md se comportam durante compactacao de contexto
7. **Nao aborda a hierarquia completa**: user CLAUDE.md (`~/.claude/CLAUDE.md`), managed policy, settings hierarchy nao sao mencionados
8. **Simplificacao do minimo**: para projetos com arquitetura complexa, tres itens podem ser insuficientes, especialmente quando o Claude Code e usado para tarefas que exigem compreensao arquitetural profunda

---

## 9. Recomendacoes Praticas

### 9.1 Arquitetura de Configuracao Completa para Claude Code

Em vez de pensar apenas no CLAUDE.md, projete o sistema completo de instrucoes:

| Camada | Mecanismo | Carregamento | Enforcement | Uso ideal |
|--------|-----------|-------------|-------------|-----------|
| Core | CLAUDE.md raiz | Always | Advisory | Descricao, package manager, build commands |
| Modular | `.claude/rules/` sem paths | Always | Advisory | Regras universais modulares por topico |
| Condicional | `.claude/rules/` com paths | On file access | Advisory | Regras de dominio (API, frontend, testes) |
| Hierarquico | Subdirectory CLAUDE.md | On navigation | Advisory | Contexto de pacote/modulo |
| On-demand | Skills | On invocation | Advisory | Workflows, procedimentos, padroes |
| Isolado | Skills com `context: fork` | On invocation (isolated) | Advisory | Analise, exploracao, tarefas independentes |
| Deterministico | Hooks | Programatico | Garantido | Linting, testes, validacao, formatacao |
| Emergente | Memoria auto-gerenciada | Startup + on-demand | Advisory | Padroes descobertos, contexto inter-sessao |
| Composicao | @imports | When parent loads | Advisory | Reutilizacao de instrucoes entre projetos |

### 9.2 Para Projetos Novos

1. **Comece com tres linhas no CLAUDE.md**: descricao, package manager, build commands
2. **Crie `.claude/rules/` desde o inicio**: mesmo que com poucos arquivos, a estrutura sinaliza intencao
3. **Use path-scoping desde o primeiro dia**: regras de API em `rules/api.md` com `paths: ["src/api/**"]`
4. **Converta regras criticas em hooks imediatamente**: testes pre-commit, linting, formatacao
5. **Nao use `/init`**: escreva o CLAUDE.md manualmente com os tres itens minimos

### 9.3 Para Projetos Existentes com CLAUDE.md Inflado

1. **Audite todas as fontes de instrucao**: CLAUDE.md + rules + memoria + skills -- mapeie o total
2. **Use o prompt de refatoracao do guia**: identifique contradicoes, extraia essenciais, agrupe o resto
3. **Converta "ALWAYS"/"NEVER" em hooks**: enforcement deterministico remove do orcamento de contexto
4. **Mova regras de dominio para rules path-scoped**: TypeScript rules com `paths: ["**/*.ts"]`
5. **Encapsule workflows em skills**: deploy, migracao, geracao de codigo como skills invocaveis
6. **Remova o que o Claude ja sabe**: convencoes padrao de linguagem, boas praticas universais
7. **Teste incrementalmente**: remova uma instrucao, observe o comportamento, repita

### 9.4 Para Monorepos

1. **Root CLAUDE.md**: proposito do monorepo + ferramentas compartilhadas (3-5 linhas)
2. **Package CLAUDE.md**: proposito do pacote + stack + referencia a convencoes detalhadas
3. **`claudeMdExcludes`**: configure para evitar carregamento de CLAUDE.md de outros times
4. **Rules compartilhadas**: use symlinks em `.claude/rules/` para convencoes organizacionais
5. **Skills compartilhadas**: skills no root para workflows comuns a todos os pacotes

### 9.5 Relacao com AGENTS.md em Projetos Multi-Ferramenta

1. **AGENTS.md como fonte primaria**: se o projeto suporta multiplas ferramentas, mantenha AGENTS.md como referencia universal
2. **CLAUDE.md como extensao**: use CLAUDE.md para features Claude Code-specific (rules, skills, hooks)
3. **Symlink para conteudo comum**: `ln -s AGENTS.md CLAUDE.md` se o conteudo base e identico
4. **Ou CLAUDE.md independente**: se o Claude Code precisa de instrucoes especificas que nao se aplicam a outras ferramentas
5. **Evite duplicacao**: nao mantenha instrucoes identicas em ambos os arquivos sem symlink

### 9.6 Para Manutencao Continua

1. **Trate CLAUDE.md como codigo**: code review, historico Git, PRs para mudancas significativas
2. **Revise periodicamente**: a documentacao da Anthropic recomenda: "review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts"
3. **Sincronize com memoria**: verifique periodicamente se a auto-memoria nao contradiz o CLAUDE.md
4. **Monitore o custo**: acompanhe se mudancas no CLAUDE.md impactam o custo de tokens por sessao
5. **Documente exclusoes**: quando remover algo, registre o motivo para evitar re-adicao
6. **Use a heuristica da Anthropic**: "For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it."
