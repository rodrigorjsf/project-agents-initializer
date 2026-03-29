# Analise: A Complete Guide To AGENTS.md

## 1. Sumario Executivo

O guia "A Complete Guide To AGENTS.md" apresenta uma filosofia de configuracao minimalista para arquivos de contexto de agentes de IA em repositorios de codigo. O documento parte de uma premissa central: arquivos AGENTS.md massivos sao contraproducentes. Em vez de melhorar o comportamento do agente, eles criam um "ball of mud" que confunde o modelo, desperdicam tokens e se tornam pesadelos de manutencao. A solucao proposta e radical em sua simplicidade: manter o AGENTS.md raiz com o minimo absoluto (descricao de uma frase, gerenciador de pacotes, comandos de build) e delegar todo o restante para progressive disclosure.

O aspecto mais distintivo deste guia e sua perspectiva de **padrao aberto e cross-tool**. O AGENTS.md nao esta vinculado a nenhuma ferramenta especifica -- e suportado por multiplas plataformas de codificacao assistida por IA (Codex, Qwen Code, Aider, entre outros). Isso traz implicacoes profundas para projetos que precisam ser compativeis com diversos agentes simultaneamente. O guia reconhece explicitamente que o Claude Code nao usa AGENTS.md, sugerindo symlinks como ponte entre os dois mundos.

A articulacao entre o conceito de "instruction budget" (150-200 instrucoes maximas) e a pratica de progressive disclosure constitui a espinha dorsal do documento. Cada instrucao adicionada ao AGENTS.md consome parte de um orcamento finito de atencao, e esse orcamento e carregado em **cada requisicao**, independentemente de relevancia. O guia transforma essa restricao tecnica em principio de design: a configuracao ideal e aquela que carrega o minimo necessario e aponta para onde encontrar o restante.

---

## 2. Principais Achados e Principios

### 2.1 O Anti-Padrao do "Ball of Mud"

O guia identifica um ciclo de feedback natural que leva ao crescimento descontrolado:

> "1. The agent does something you don't like / 2. You add a rule to prevent it / 3. Repeat hundreds of times over months / 4. File becomes a 'ball of mud'"

Este padrao e agravado por dois fatores: (a) diferentes desenvolvedores adicionam opinioes conflitantes sem revisao global, e (b) scripts de auto-geracao, que o guia condena explicitamente:

> "Never use initialization scripts to auto-generate your AGENTS.md. They flood the file with things that are 'useful for most scenarios' but would be better progressively disclosed."

### 2.2 O Orcamento de Instrucoes

Referenciando o artigo de Kyle da Humanlayer, o guia estabelece:

> "Frontier thinking LLMs can follow ~ 150-200 instructions with reasonable consistency."

E acrescenta a implicacao critica: cada token no AGENTS.md e carregado em **cada requisicao**, criando um problema de orcamento rigido. O guia sintetiza isso na afirmacao: **"the ideal AGENTS.md file should be as small as possible."**

### 2.3 Documentacao Obsoleta Envenena o Contexto

O guia distingue entre o impacto de documentacao obsoleta em humanos versus agentes:

> "For human developers, stale docs are annoying, but the human usually has enough built-in memory to be skeptical about bad docs. For AI agents that read documentation on every request, stale information actively _poisons_ the context."

A recomendacao especifica e: **descrever capacidades, nao estruturas**. Em vez de mapear caminhos de arquivos (que mudam constantemente), descrever o que o projeto faz e dar dicas sobre onde as coisas podem estar. Conceitos de dominio ("organization" vs "group" vs "workspace") sao mais estaveis que caminhos de arquivo.

### 2.4 O Minimo Absoluto

O guia define tres itens como o conteudo essencial:

1. **Descricao do projeto em uma frase** -- funciona como um role-based prompt
2. **Gerenciador de pacotes** -- apenas se nao for npm
3. **Comandos de build/typecheck** -- apenas se nao forem padrao

> "That's honestly it. Everything else should go elsewhere."

### 2.5 Progressive Disclosure como Principio Arquitetural

O guia apresenta progressive disclosure em tres niveis:

1. **Referencias a arquivos separados**: `"For TypeScript conventions, see docs/TYPESCRIPT.md"` -- com "light touch", sem linguagem imperativa
2. **Aninhamento de referencias**: docs/TYPESCRIPT.md referencia docs/TESTING.md, criando uma arvore de recursos descobrivel
3. **Skills de agentes**: comandos ou workflows que o agente pode invocar para aprender algo especifico

### 2.6 AGENTS.md em Monorepos

O guia apresenta uma hierarquia de dois niveis:

| Nivel | Conteudo |
|-------|----------|
| **Root** | Proposito do monorepo, navegacao entre pacotes, ferramentas compartilhadas |
| **Package** | Proposito do pacote, tech stack especifica, convencoes do pacote |

Com a advertencia critica: **"Don't overload any level."**

---

## 3. Pontos de Atencao

### 3.1 O Perigo da Linguagem Imperativa

O guia faz uma observacao sutil mas fundamental sobre tom. O exemplo de referencia a arquivo separado usa:

> "Notice the light touch, no 'always,' no all-caps forcing. Just a conversational reference."

Isso contradiz a intuicao de muitos desenvolvedores que acreditam que instrucoes em maiusculas ou com "NEVER"/"ALWAYS" sao mais efetivas. Pesquisa documentada no guia de prompt engineering confirma que formatacao agressiva (ALL-CAPS, "NUNCA", "JAMAIS") produz resultados piores em modelos Claude recentes.

### 3.2 A Armadilha da Auto-Geracao

O guia e enfatico contra auto-geracao, mas a pratica e comum. Codex, Qwen Code e Claude Code oferecem comandos `/init` integrados. O fato de que os proprios providers recomendam auto-geracao cria uma tensao direta com o principio deste guia. O paper "Evaluating AGENTS.md" confirma empiricamente que arquivos gerados por LLM **reduzem** a taxa de sucesso em 3% na media.

### 3.3 Conceitos Estaveis vs Instancia de Codigo

A distincao entre conceitos de dominio (mais estaveis) e caminhos de arquivo (instáveis) e facil de ignorar na pratica. Muitos AGENTS.md incluem mapeamentos detalhados de diretórios como:

> "authentication logic lives in `src/auth/handlers.ts`"

O guia alerta que isso cria vulnerabilidade a renomeacoes. A alternativa proposta -- descrever capacidades e "shape of the project" -- exige mais reflexao do autor mas produz documentacao mais resiliente.

### 3.4 Quando Progressive Disclosure Falha

O guia nao aborda explicitamente cenarios onde progressive disclosure pode ser problematica: (a) agentes que nao conseguem navegar hierarquias de documentacao eficientemente, (b) projetos com modelos menores que tem capacidade limitada de navegacao, (c) tarefas que exigem contexto holístico desde o inicio.

### 3.5 O Problema da Compatibilidade Cross-Tool

O AGENTS.md e descrito como "open standard supported by many - though not all - tools." Porem, cada ferramenta interpreta o arquivo de maneira ligeiramente diferente. A necessidade de symlinks entre AGENTS.md e CLAUDE.md revela que a padronizacao ainda e incompleta. Instrucoes que funcionam bem com uma ferramenta podem nao ter o mesmo efeito em outra.

---

## 4. Casos de Uso e Escopo

### 4.1 Projetos Multi-Ferramenta

O AGENTS.md e especialmente valioso quando a equipe usa multiplas ferramentas de codificacao assistida por IA. Um unico arquivo de configuracao que funciona com Codex, Qwen Code, Aider e outros reduce duplicacao e garante consistencia. A recomendacao de symlinks (`ln -s AGENTS.md CLAUDE.md`) permite estender a compatibilidade para o Claude Code.

### 4.2 Projetos Open Source

Repositorios open source frequentemente recebem contribuicoes de desenvolvedores usando ferramentas diferentes. O AGENTS.md como padrao aberto permite que qualquer contribuidor, independentemente da ferramenta, receba orientacao consistente.

### 4.3 Monorepos

O guia apresenta suporte explicito para monorepos com AGENTS.md hierarquico. Isso e particularmente relevante para organizacoes com multiplos times trabalhando em pacotes distintos, onde cada pacote pode ter convencoes proprias.

### 4.4 Equipes em Transicao

Equipes que estao migrando entre ferramentas de codificacao assistida ou que ainda nao definiram uma ferramenta padrao se beneficiam da natureza agnóstica do AGENTS.md.

### 4.5 Cenarios Menos Apropriados

- Projetos exclusivamente vinculados ao Claude Code (onde CLAUDE.md oferece funcionalidades superiores)
- Projetos que exigem enforcement deterministico (hooks sao mais adequados)
- Equipes com necessidade de configuracao granular por desenvolvedor (AGENTS.md e focado em escopo de projeto)

---

## 5. Aplicabilidade a Infraestrutura de Agentes

### 5.1 Skills

O guia menciona agent skills como forma de progressive disclosure:

> "Many tools support 'agent skills' - commands or workflows the agent can invoke to learn how to do something specific."

**Implicacoes para design de skills:**

- Skills devem ser projetadas como unidades autocontidas de conhecimento que o agente carrega sob demanda
- A descricao da skill (visivel no inicio da sessao) funciona como o "pointer" do progressive disclosure -- deve ser concisa o suficiente para nao inflar o orcamento de instrucoes
- O conteudo completo da skill so deve ser carregado quando invocado, alinhando-se ao principio de carregar "only what it needs right now"
- Skills em contexto cross-tool devem ser projetadas com linguagem neutra, evitando dependencias de funcionalidades especificas de uma ferramenta

### 5.2 Hooks

O guia nao menciona hooks diretamente, mas a logica de minimalismo no AGENTS.md implica uma estrategia de conversao:

- Instrucoes que **devem** ser seguidas sem excecao (como "sempre executar testes antes de commit") sao candidatas a conversao para hooks
- Hooks removem essas instrucoes do orcamento de contexto -- a instrucao e enforced programaticamente, sem consumir tokens
- Para projetos cross-tool, hooks precisam ser implementados de forma ferramenta-especifica, mas o AGENTS.md pode referenciar a existencia deles: "Pre-commit hooks enforce test execution and linting"
- O principio do guia de que "everything else should go elsewhere" se aplica fortemente: o que pode ser um hook nao deve ser uma instrucao textual

### 5.3 Subagentes

O principio de minimalismo do AGENTS.md se aplica diretamente ao design de contexto de subagentes:

- Subagentes tem janelas de contexto menores e mais focadas -- o orcamento de instrucoes e ainda mais critico
- A recomendacao de "one-sentence project description" se traduz em: cada subagente deve receber apenas o contexto minimo necessario para sua tarefa especifica
- A estrategia de isolamento de contexto (cada subagente com contexto proprio) espelha a hierarquia de AGENTS.md em monorepos -- cada "pacote" de contexto e independente
- Progressive disclosure para subagentes significa: o subagente recebe instrucoes iniciais minimas e pode buscar mais contexto conforme necessario

### 5.4 Rules

O conceito de `.claude/rules/` (especifico do Claude Code) pode ser mapeado para o padrao cross-tool de AGENTS.md em monorepos:

- Rules com paths-scope sao a implementacao tecnica do principio "relevant to one domain" do guia
- Para projetos cross-tool, a mesma logica pode ser implementada via AGENTS.md em subdiretorios, que e o mecanismo nativo de progressive disclosure do padrao aberto
- A diferenca fundamental: rules sao path-triggered (carregam automaticamente quando arquivos correspondentes sao lidos), enquanto AGENTS.md em subdiretorios depende do agente navegar ate aquele diretorio
- Em projetos cross-tool, subdirectory AGENTS.md e a alternativa universal mais proxima de rules

### 5.5 Memoria

A relacao entre AGENTS.md e sistemas de memoria e de complementaridade:

- **AGENTS.md**: informacao estatica, versionada, compartilhada pela equipe -- convencoes, stack tecnica, comandos
- **Memoria**: informacao dinamica, pessoal ou emergente -- padroes descobertos durante uso, preferencias individuais, decisoes especificas de sessao
- O principio do guia de que "the agent can generate its own just-in-time documentation during planning" conecta-se diretamente ao conceito de auto-memoria
- Evitar documentar estrutura no AGENTS.md se complementa com a capacidade de memoria de gerar mapeamentos ad-hoc conforme necessario

---

## 6. Aplicabilidade do Guia de Engenharia de Prompts

### 6.1 Role Prompting na Descricao do Projeto

A "one-sentence project description" do guia funciona como role prompting:

> "This single sentence gives the agent context about _why_ they're working in this repository. It anchors every decision they make."

O guia de engenharia de prompts confirma que role prompting e o mecanismo fundamental de especializacao em arquiteturas multi-agentes. A descricao no AGENTS.md atua como um role prompt persistente -- definindo o "papel" do agente no contexto daquele repositorio. O custo e minimo (10-30 tokens adicionais) com alta relacao custo-beneficio para controle de estilo e escopo.

### 6.2 Zero-Shot vs Few-Shot na Redacao de Instrucoes

O guia de engenharia de prompts mostra que modelos modernos tem capacidades zero-shot robustas (~85% de acuracia em tarefas simples). Isso reforça a recomendacao do guia de AGENTS.md de nao documentar o que o agente ja sabe -- muitas instrucoes sao redundantes com o conhecimento parametrico do modelo.

A recomendacao de few-shot (3-5 exemplos) do guia de prompts se aplica quando o AGENTS.md precisa demonstrar padroes especificos. Porem, os exemplos devem ir em arquivos separados (progressive disclosure), nao no AGENTS.md raiz, para nao inflar o orcamento.

### 6.3 Chain-of-Thought e Planejamento

O guia de prompts mostra que CoT melhora raciocinio multi-passo, mas com custo de 35-600% mais tokens. Para AGENTS.md, isso significa:

- Instrucoes no AGENTS.md devem ser diretas (zero-shot), nao procedurais
- Se o agente precisa "pensar passo a passo" sobre algo, isso deve ser parte de uma skill invocada sob demanda, nao de uma instrucao permanente
- A tecnica de "Thread of Thought" (caminhar pelo contexto em partes gerenciaveis) e particularmente relevante para agentes navegando arvores de progressive disclosure

### 6.4 ReAct e Navegacao de Documentacao

O padrao ReAct (Pensamento -> Acao -> Observacao) e exatamente o que acontece quando um agente navega a arvore de progressive disclosure:

1. **Pensamento**: "Preciso entender as convencoes de TypeScript deste projeto"
2. **Acao**: Leitura de `docs/TYPESCRIPT.md` (referenciado no AGENTS.md)
3. **Observacao**: Obtem as convencoes e pode agir

Isso valida a eficacia do progressive disclosure -- agentes modernos sao naturalmente equipados para esse padrao de navegacao.

### 6.5 Structured Output e Formato do AGENTS.md

O guia de prompts recomenda tags XML para Claude e markdown estruturado como formato eficiente. O AGENTS.md como arquivo markdown se alinha bem com esses principios. Porem, para projetos cross-tool, evitar XML tags especificas de Claude garante compatibilidade -- markdown headers e tabelas sao mais universais.

### 6.6 Context Engineering vs Prompt Engineering

O guia de prompts identifica a transicao de prompt engineering para context engineering:

> "O LLM e uma CPU, a janela de contexto e RAM, e voce e o sistema operacional." (Andrej Karpathy)

O AGENTS.md e um artefato de context engineering -- nao e um prompt individual, mas parte de um sistema de contexto que inclui memoria, ferramentas, documentacao progressiva e orquestracao. O principio de "encontrar a solucao mais simples possivel" se aplica diretamente ao design do AGENTS.md.

---

## 7. Correlacoes com Outros Documentos Principais

### 7.1 Evaluating-AGENTS-paper.md

O paper da ETH Zurich oferece **validacao empirica direta** dos principios deste guia:

- **Arquivos gerados por LLM reduzem performance**: reducao de 3% na media na taxa de sucesso + aumento de 20% no custo. Isso confirma a advertencia do guia contra auto-geracao.
- **Arquivos escritos por humanos tem ganho marginal**: apenas +4% na media. Isso reforça que ate arquivos bem escritos tem impacto limitado, justificando o minimalismo extremo.
- **Instrucoes sao seguidas mas tornam a tarefa mais dificil**: o paper mostra que agentes seguem as instrucoes do AGENTS.md (ex: uso de `uv` quando mencionado), mas isso aumenta passos e custo. O guia esta correto ao dizer que "unnecessary requirements from context files make tasks harder."
- **Overviews de codebase nao sao eficazes**: 100% dos arquivos gerados pelo Sonnet-4.5 incluem overviews, mas eles nao reduzem o tempo para encontrar arquivos relevantes. Isso valida a recomendacao do guia de descrever capacidades, nao estrutura.
- **Redundancia com documentacao existente**: quando toda documentacao e removida, arquivos de contexto gerados por LLM passam a melhorar performance em 2.7%. Isso sugere que AGENTS.md e mais util em projetos com pouca documentacao.

### 7.2 research-llm-context-optimization.md

Este documento fornece a **base cientifica** para varias recomendacoes do guia:

- **Context rot**: a degradacao de performance com aumento de contexto (n^2 relacoes de atencao) fundamenta a recomendacao de manter o AGENTS.md pequeno.
- **Lost-in-the-middle effect**: informacoes no meio de contextos longos sao as mais ignoradas. Isso implica que, se o AGENTS.md for longo, as instrucoes do meio serao as primeiras a serem ignoradas.
- **Instruction budget de ~200 linhas**: o guia do AGENTS.md cita o artigo de Kyle da Humanlayer; a pesquisa aprofunda com recomendacao explicita da Anthropic de "target under 200 lines per CLAUDE.md file."
- **Hybrid strategy (pre-loaded + on-demand)**: exatamente o padrao que o guia propoe -- AGENTS.md carregado upfront como minimo essencial, documentacao detalhada carregada sob demanda.
- **Just-in-time documentation**: o conceito formal da Anthropic de manter "lightweight identifiers" e carregar dados dinamicamente mapeia diretamente para o progressive disclosure do guia.

### 7.3 claude-prompting-best-practices.md

O guia oficial de prompting da Anthropic se correlaciona em varios pontos:

- **"Be clear and direct"**: reforça a recomendacao de instrucoes concisas no AGENTS.md, nao vagas
- **"Add context to improve performance"**: a descricao de uma frase do projeto e exatamente isso -- contexto motivacional
- **"Put longform data at the top, queries at the end"**: para AGENTS.md, as instrucoes mais criticas devem estar no inicio do arquivo
- **Sobre formatacao agressiva**: Claude Opus 4.5/4.6 responde pior a linguagem coercitiva -- "Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'" -- validando o "light touch" recomendado pelo guia
- **Subagent orchestration**: Claude Opus 4.6 orquestra subagentes proativamente. Para projetos cross-tool, o AGENTS.md deve conter instrucoes que sejam eficazes independentemente de se um agente monolitico ou um orquestrador de subagentes as processa

---

## 8. Forcas e Limitacoes

### 8.1 Forcas

1. **Principio universal**: o minimalismo e aplicavel independentemente de ferramenta, modelo ou linguagem de programacao
2. **Base empirica**: o conceito de instruction budget tem fundamentacao em pesquisa (Humanlayer, Anthropic)
3. **Praticabilidade**: o guia oferece um prompt concreto para refatorar AGENTS.md existentes (secao "Fix A Broken AGENTS.md")
4. **Compatibilidade cross-tool**: como padrao aberto, funciona com multiplos agentes
5. **Escalabilidade**: o padrao de progressive disclosure escala naturalmente com a complexidade do projeto
6. **Decision matrix clara**: a tabela "When to use" (Root / Separate file / Nested documentation) oferece orientacao acionavel

### 8.2 Limitacoes

1. **Ausencia de metricas**: o guia nao oferece metricas quantitativas sobre o impacto do tamanho do AGENTS.md na performance. O paper da ETH Zurich preenche essa lacuna parcialmente.
2. **Foco em JavaScript/TypeScript**: os exemplos sao predominantemente do ecossistema Node.js (pnpm, npm, corepack). Projetos Python, Go, Rust etc. tem idiomas diferentes.
3. **Nao aborda enforcement deterministico**: hooks, linters, CI checks nao sao mencionados como alternativas para instrucoes criticas.
4. **Simplificacao excessiva do minimo**: projetos com arquiteturas complexas (microsservicos, event-driven, CQRS) podem precisar de mais contexto no raiz do que tres itens.
5. **Dependencia de capacidade de navegacao do agente**: o progressive disclosure assume que o agente e "fast at navigating documentation hierarchies", o que varia entre ferramentas e modelos.
6. **Nao aborda versionamento**: como o AGENTS.md deve evoluir ao longo do tempo, quem deve revisá-lo, com que frequencia.
7. **Lacuna sobre conflitos cross-tool**: nao discute como lidar quando diferentes ferramentas interpretam o mesmo AGENTS.md de formas distintas.

---

## 9. Recomendacoes Praticas

### 9.1 Para Projetos Novos

1. **Comece com tres linhas**: descricao do projeto, gerenciador de pacotes (se nao npm), comandos de build (se nao padrao)
2. **Crie a arvore de progressive disclosure desde o inicio**: mesmo que os arquivos referenciados estejam vazios, a estrutura (`docs/CONVENTIONS.md`, `docs/TESTING.md`) sinaliza intencao
3. **Use symlinks para Claude Code**: `ln -s AGENTS.md CLAUDE.md` garante compatibilidade
4. **Adicione ao .gitignore**: nao ignore o AGENTS.md -- ele deve ser compartilhado pela equipe

### 9.2 Para Projetos Existentes com AGENTS.md Inflado

1. **Use o prompt de refatoracao do guia**: copie o prompt da secao "Fix A Broken AGENTS.md" diretamente no agente
2. **Identifique contradicoes primeiro**: instrucoes conflitantes causam comportamento arbitrario
3. **Converta instrucoes deterministicas em hooks**: tudo que e "ALWAYS" ou "NEVER" provavelmente deve ser um hook, nao uma instrucao
4. **Remova o obvio**: instrucoes como "write clean code" ou "follow best practices" sao desperdiço de tokens
5. **Teste a remocao**: remova instrucoes uma por vez e observe se o comportamento muda -- se nao mudar, a instrucao era redundante

### 9.3 Para Monorepos

1. **Root AGENTS.md**: apenas proposito do monorepo, navegacao entre pacotes e ferramentas compartilhadas
2. **Package AGENTS.md**: proposito do pacote, stack especifica, referencia a convencoes detalhadas
3. **Nao duplique**: se uma instrucao se aplica a todos os pacotes, ela fica no root -- se e especifica, no pacote
4. **Use `claudeMdExcludes`** (em projetos Claude Code) para evitar que CLAUDE.md de outros times carregue desnecessariamente

### 9.4 Para Projetos Cross-Tool

1. **Mantenha o AGENTS.md como fonte primaria**: use-o como ponto de referencia para todas as ferramentas
2. **Evite features tool-specific no AGENTS.md**: nao use XML tags, `@imports`, ou path-scoped rules no AGENTS.md -- essas sao extensoes de ferramentas especificas
3. **Documente a equivalencia**: mantenha uma nota no repositorio explicando como AGENTS.md se relaciona com CLAUDE.md, .codex/configuration.md, etc.
4. **Teste com multiplos agentes**: valide que as instrucoes produzem comportamento consistente em diferentes ferramentas

### 9.5 Para Manutencao Continua

1. **Revise o AGENTS.md junto com code reviews**: trate-o como codigo -- ele merece o mesmo nivel de scrutinio
2. **Pode periodicamente**: a cada sprint ou ciclo de release, revise se as instrucoes ainda sao relevantes
3. **Meça o impacto**: se possivel, compare a taxa de sucesso do agente com e sem o AGENTS.md em tarefas representativas
4. **Documente decisoes de exclusao**: quando remover algo do AGENTS.md, registre o motivo (em commit message ou ADR) para evitar que alguem adicione de volta
