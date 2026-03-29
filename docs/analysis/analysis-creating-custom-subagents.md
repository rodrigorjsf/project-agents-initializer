# Analise: Criacao de Subagentes Customizados no Claude Code

---

## 1. Resumo Executivo

O documento oficial da Anthropic sobre subagentes customizados e a referencia central para a criacao, configuracao e uso de assistentes de IA especializados dentro do Claude Code. Subagentes sao definidos como arquivos Markdown com YAML frontmatter, armazenados em diretorios `agents/` com escopo variavel (sessao via CLI, projeto, usuario, ou plugin). Cada subagente opera em sua propria janela de contexto com system prompt customizado, acesso restrito a ferramentas e permissoes independentes. Apenas dois campos sao obrigatorios: `name` e `description`.

O mecanismo fundamental e o isolamento de contexto: subagentes recebem APENAS seu system prompt (corpo do markdown) mais detalhes basicos do ambiente -- nao recebem o system prompt completo do Claude Code nem o historico da conversacao pai. Isso preserva o contexto principal enquanto permite trabalho especializado. O Claude decide automaticamente quando delegar com base no campo `description` e no contexto da conversa, mas pode ser forcado via @-mention (`@"code-reviewer (agent)"`) ou configurado como agente sessao-wide (`claude --agent code-reviewer`).

As capacidades de configuracao sao extensas: selecao de modelo (`haiku`, `sonnet`, `opus`, `inherit`), preload de skills, servidores MCP escopados, hooks de ciclo de vida, memoria persistente (user/project/local), isolamento via git worktree, limite de turnos (`maxTurns`), nivel de esforco, e execucao em foreground ou background. A restricao mais importante e que subagentes nao podem spawnar outros subagentes, prevenindo aninhamento infinito.

---

## 2. Conceitos e Mecanismos Chave

### 2.1 Subagentes Built-in

| Subagente | Modelo | Ferramentas | Proposito |
|-----------|--------|-------------|-----------|
| **Explore** | Haiku | Read-only (sem Write/Edit) | Busca e analise de codebase |
| **Plan** | Herda | Read-only (sem Write/Edit) | Pesquisa para modo planejamento |
| **general-purpose** | Herda | Todas | Pesquisa complexa, operacoes multi-passo |
| **Bash** | Herda | Comandos de terminal | Comandos em contexto separado |
| **Claude Code Guide** | Haiku | -- | Perguntas sobre features do Claude Code |

### 2.2 Hierarquia de Escopo

```
Prioridade 1 (mais alta): --agents CLI flag (sessao unica, JSON)
Prioridade 2:             .claude/agents/ (projeto, versionavel)
Prioridade 3:             ~/.claude/agents/ (usuario, todos os projetos)
Prioridade 4 (mais baixa): Plugin agents/ (onde plugin esta habilitado)
```

Quando multiplos subagentes compartilham o mesmo nome, o de maior prioridade vence.

### 2.3 Formato do Arquivo de Subagente

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

O frontmatter define metadados e configuracao. O corpo se torna o system prompt que guia o comportamento do subagente.

### 2.4 Campos de Frontmatter Suportados

| Campo | Obrigatorio | Descricao | Default |
|-------|-------------|-----------|---------|
| `name` | Sim | Identificador unico (letras minusculas e hifens) | -- |
| `description` | Sim | Quando Claude deve delegar a este subagente | -- |
| `tools` | Nao | Ferramentas permitidas (allowlist) | Herda todas |
| `disallowedTools` | Nao | Ferramentas negadas (denylist) | -- |
| `model` | Nao | Modelo: `sonnet`, `opus`, `haiku`, ID completo, ou `inherit` | `inherit` |
| `permissionMode` | Nao | Modo de permissao | `default` |
| `maxTurns` | Nao | Limite de turnos agenticos | -- |
| `skills` | Nao | Skills pre-carregadas no contexto do subagente | -- |
| `mcpServers` | Nao | Servidores MCP escopados ao subagente | -- |
| `hooks` | Nao | Hooks de ciclo de vida escopados | -- |
| `memory` | Nao | Memoria persistente: `user`, `project`, ou `local` | -- |
| `background` | Nao | `true` para executar sempre em background | `false` |
| `effort` | Nao | Nivel de esforco: `low`, `medium`, `high`, `max` | Herda da sessao |
| `isolation` | Nao | `worktree` para git worktree isolada | -- |

### 2.5 Controle de Ferramentas

**Allowlist** (apenas estas ferramentas):

```yaml
tools: Read, Grep, Glob, Bash
```

**Denylist** (todas exceto estas):

```yaml
disallowedTools: Write, Edit
```

**Restricao de subagentes spawnaveis** (apenas para `--agent` mode):

```yaml
tools: Agent(worker, researcher), Read, Bash
```

Regra de interacao: se ambos `tools` e `disallowedTools` estao definidos, `disallowedTools` e aplicado primeiro, depois `tools` e resolvido contra o pool restante.

### 2.6 Servidores MCP Escopados

```yaml
mcpServers:
  # Definicao inline: escopada apenas a este subagente
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Referencia por nome: reutiliza servidor ja configurado
  - github
```

Definicoes inline conectam no start do subagente e desconectam no finish. Isso evita que descricoes de ferramentas MCP consumam contexto na conversacao principal.

### 2.7 Memoria Persistente

```yaml
memory: project  # Armazena em .claude/agent-memory/<name>/
```

| Escopo | Localizacao | Quando Usar |
|--------|-------------|-------------|
| `user` | `~/.claude/agent-memory/<name>/` | Aprendizado cross-projeto |
| `project` | `.claude/agent-memory/<name>/` | Conhecimento especifico, versionavel |
| `local` | `.claude/agent-memory-local/<name>/` | Especifico mas nao commitavel |

Quando habilitada: system prompt inclui instrucoes de leitura/escrita, primeiras 200 linhas do `MEMORY.md` sao incluidas, e ferramentas Read/Write/Edit sao automaticamente habilitadas.

### 2.8 Hooks de Ciclo de Vida

**No frontmatter do subagente** (escopo local):

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
```

**No settings.json** (escopo do projeto):

```json
{
  "hooks": {
    "SubagentStart": [
      { "matcher": "db-agent", "hooks": [{ "type": "command", "command": "./scripts/setup-db.sh" }] }
    ],
    "SubagentStop": [
      { "hooks": [{ "type": "command", "command": "./scripts/cleanup.sh" }] }
    ]
  }
}
```

### 2.9 Modos de Execucao

| Modo | Comportamento | Permissoes |
|------|---------------|------------|
| **Foreground** | Bloqueia conversacao principal | Prompts passam para o usuario |
| **Background** | Executa concorrentemente | Pre-aprovadas; auto-nega o resto |

`Ctrl+B` para backgroundar uma tarefa em execucao.

---

## 3. Pontos de Atencao

### 3.1 O Gap de Contexto do Subagente

**O ponto mais critico.** Subagentes NAO recebem:

- O system prompt completo do Claude Code
- O historico da conversacao pai
- Skills da sessao pai (devem ser listadas explicitamente no campo `skills`)

Eles recebem APENAS:

- Seu system prompt (corpo do markdown)
- Detalhes basicos do ambiente (diretorio de trabalho)
- CLAUDE.md e memoria do projeto (via fluxo normal de mensagens)

**Implicacao**: O system prompt deve ser auto-suficiente. Todo contexto necessario deve estar no prompt ou ser reunido via ferramentas.

### 3.2 Restricao Anti-Aninhamento

Subagentes NAO podem spawnar outros subagentes. Se um workflow requer delegacao aninhada, use Skills ou chain subagentes da conversacao principal.

### 3.3 Custo de Tool Descriptions

Mesmo ferramentas nao utilizadas consomem contexto via suas descricoes. Restringir ferramentas ao minimo necessario e uma otimizacao de orcamento de atencao.

### 3.4 Permissoes de Seguranca em Plugins

Subagentes de plugins NAO suportam `hooks`, `mcpServers` ou `permissionMode`. Esses campos sao ignorados no carregamento. Para usa-los, copie o arquivo do agente para `.claude/agents/` ou `~/.claude/agents/`.

### 3.5 Auto-Compactacao

Subagentes suportam auto-compactacao a ~95% de capacidade. Configuravel via `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`. Eventos de compactacao sao logados nos transcripts: `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`.

### 3.6 Impacto do `description` na Delegacao

O campo `description` e o unico sinal de roteamento que o Claude usa para decidir quando delegar. Descricoes vagas causam delegacao inconsistente ou excessiva. Descricoes com frases como "Use proactively after..." ou "Use when encountering..." melhoram significativamente a precisao de roteamento.

---

## 4. Casos de Uso e Escopo

### 4.1 Quando Usar Subagentes

| Cenario | Recomendacao |
|---------|-------------|
| Operacoes que geram output volumoso (testes, logs) | Subagente -- isola output do contexto principal |
| Code review com restricoes de ferramenta | Subagente read-only |
| Pesquisa paralela independente | Multiplos subagentes em paralelo |
| Workflows multi-passo com validacao | Chain de subagentes |
| Dominio especializado (SQL, seguranca) | Subagente com prompt focado |
| Operacoes arriscadas (refactoring grande) | Subagente com `isolation: worktree` |

### 4.2 Quando NAO Usar Subagentes

| Cenario | Alternativa |
|---------|-------------|
| Iteracao frequente com back-and-forth | Conversacao principal |
| Fases que compartilham contexto extenso | Conversacao principal |
| Mudanca rapida e direcionada | Conversacao principal |
| Pergunta rapida sobre algo ja no contexto | `/btw` |
| Prompts reutilizaveis no contexto principal | Skills |
| Workers que precisam se comunicar | Agent Teams |

### 4.3 Criterios de Decisao para Modelo

| Tarefa | Modelo Recomendado | Justificativa |
|--------|-------------------|---------------|
| Exploracao/busca de codigo | `haiku` | Rapido, read-only, nao requer raciocinio profundo |
| Code review | `sonnet` | Equilibrio qualidade/velocidade |
| Decisoes de arquitetura | `opus` | Analise complexa de trade-offs |
| Debugging | `sonnet` | Precisa de ferramentas + raciocinio, velocidade importa |
| Operacoes de arquivo simples | `haiku` | Tarefas mecanicas e rotineiras |

---

## 5. Aplicabilidade a Infraestrutura de Agentes

### 5.1 Skills

- **Skills que delegam a subagentes**: O campo `context: fork` em skills cria um subagente isolado. O campo `agent` especifica qual configuracao de subagente usar (Explore, Plan, general-purpose, ou customizado). Isso e a ponte entre skills e subagentes.
- **Preload de skills em subagentes**: O campo `skills` no frontmatter injeta conteudo completo de skills no contexto do subagente no startup. E o inverso de `context: fork` -- aqui o subagente controla o system prompt e carrega conteudo de skills.
- **Plugin-provided skills**: Subagentes de plugins carregam skills normalmente, mas com restricoes de seguranca (sem hooks, mcpServers, permissionMode).

**Exemplo de skill que delega a subagente**:

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

**Exemplo de subagente que carrega skills**:

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

### 5.2 Hooks

- **Hooks no frontmatter**: `PreToolUse`, `PostToolUse`, `Stop` (convertido para `SubagentStop` em runtime). Executam apenas enquanto o subagente esta ativo.
- **Hooks no settings.json**: `SubagentStart` e `SubagentStop` com matchers por tipo de agente. Executam na sessao principal.
- **Tipos de hook**: `command` (shell), `http` (POST), `prompt` (avaliacao Claude), `agent` (subagente verificador)
- **Guardrails condicionais**: `PreToolUse` + scripts de validacao para controle fino (ex: permitir apenas queries SELECT)
- **Memory-triggered hooks**: Nao ha suporte direto, mas hooks `PostToolUse` no matcher "Write|Edit" podem detectar escritas em diretorios de memoria

### 5.3 Subagentes

- **Orquestracao**: Modelo hub-and-spoke -- subagentes reportam ao caller, nao entre si
- **Delegacao**: Automatica (via description) ou explicita (via @-mention ou `--agent`)
- **Sintese de resultados**: Resultado retorna ao contexto principal; Claude sintetiza
- **Execucao paralela**: Multiplos subagentes podem rodar em paralelo (foreground ou background)
- **Isolamento via worktree**: `isolation: worktree` cria copia isolada do repositorio; cleanup automatico se nenhuma mudanca
- **Retomada**: `SendMessage` com agent ID permite retomar subagentes com historico completo
- **Chaining**: Subagentes em sequencia onde cada resultado alimenta o proximo

### 5.4 Rules

- **Rules em contexto de subagentes**: `.claude/rules/` sao carregadas normalmente via CLAUDE.md
- **Path-scoped rules**: Ativadas quando o subagente le arquivos correspondentes ao pattern
- **Plugin-scoped rules**: Rules de plugins sao carregadas pelo subagente normalmente
- **Importacao `@path`**: Funciona normalmente dentro do contexto do subagente

### 5.5 Memoria

- **Memoria persistente de subagente**: Tres escopos (user, project, local) com `MEMORY.md` como index
- **Primeiras 200 linhas**: Carregadas no startup do subagente, assim como auto memory da sessao principal
- **Curadoria**: Se `MEMORY.md` excede 200 linhas, o subagente recebe instrucoes para curar
- **Cross-session**: A memoria persiste entre sessoes, construindo base de conhecimento incremental
- **Dica pratica**: Incluir instrucoes no prompt como "Consulte sua memoria antes de comecar" e "Salve o que aprendeu ao terminar"

---

## 6. Aplicabilidade do Guia de Engenharia de Prompts

### 6.1 CoT para Cadeias de Raciocinio de Subagentes

Subagentes beneficiam-se de CoT no system prompt, especialmente para tarefas de analise. O formato recomendado:

```markdown
Quando invocado:
1. Reuna contexto -- execute git diff e explore o codebase
2. Analise -- aplique o checklist de review
3. Raciocine passo a passo sobre cada issue encontrada
4. Verifique -- confirme que suas conclusoes sao suportadas por evidencia
5. Reporte -- formate findings com prioridade e exemplos de fix
```

CoT e particularmente eficaz com modelo `sonnet` para reviews e debugging. Com `haiku`, mantenha CoT minimo para nao desperdicar tokens. Com `opus`, prefira instrucoes gerais ("think thoroughly") que produzem raciocinio superior a steps prescritivos.

### 6.2 ReAct para Subagentes com Acesso a Ferramentas

Subagentes com acesso a ferramentas (Bash, Read, Grep) operam naturalmente no padrao ReAct. O system prompt deve encorajar o ciclo:

```markdown
## Processo
1. **Pense** sobre o que precisa investigar
2. **Aja** usando as ferramentas disponiveis (Read, Grep, Bash)
3. **Observe** os resultados
4. **Repita** ate ter informacao suficiente para uma conclusao fundamentada
```

### 6.3 Tree of Thoughts para Subagentes de Exploracao

Para subagentes de exploracao (`Explore` ou customizados), ToT distribudo pode ser implementado via multiplos subagentes em paralelo, cada um explorando um caminho diferente:

```text
Research the authentication, database, and API modules in parallel using separate subagents
```

O agente principal sintetiza os resultados como a etapa de avaliacao do ToT.

### 6.4 Self-Consistency para Validacao entre Multiplos Subagentes

Executar o mesmo subagente de review multiplas vezes (com temperatura >0) e comparar resultados implementa Self-Consistency. Issues reportadas por multiplas execucoes tem maior confianca. Custo: multiplicado pelo numero de execucoes.

### 6.5 Reflexion para Melhoria Iterativa de Subagentes

A combinacao de subagentes chainados implementa Reflexion:

```text
1. Use code-reviewer para encontrar issues
2. Use debugger para corrigir as issues encontradas
3. Use code-reviewer novamente para validar as correcoes
```

Hooks `PostToolUse` podem automatizar a reflexao: apos cada edicao, executar linter ou testes.

### 6.6 Least-to-Most para Decomposicao de Tarefas entre Subagentes

Decompor uma tarefa complexa em subtarefas e delegar cada uma a um subagente:

```text
Primeiro use o Explore agent para mapear a arquitetura
Depois use o planner agent para criar um plano baseado no mapeamento
Por fim use o developer agent para implementar o plano
```

Cada subagente recebe resultado do anterior, implementando decomposicao progressiva.

---

## 7. Correlacoes com os Documentos Principais

### Com "Orchestrate Teams of Claude Code Sessions"

Complementaridade direta. Subagentes operam em modelo hub-and-spoke; agent teams em modelo peer-to-peer. Subagentes sao mais baratos (resultados sumarizados de volta) mas sem comunicacao inter-worker. A decisao entre ambos depende da necessidade de comunicacao entre workers.

### Com "Research: Subagent Best Practices"

O documento de research aprofunda tudo que a documentacao oficial apresenta: patterns de ferramentas, exemplos da comunidade, anti-patterns, prompt engineering para system prompts. A informacao sobre Confidence-Based Filtering e a secao de anti-patterns sao contribuicoes unicas do research que complementam a documentacao oficial.

### Com "How Claude Remembers a Project"

A memoria de subagentes e um caso especial da auto memory: mesmo mecanismo (MEMORY.md + topic files, primeiras 200 linhas), mas com escopos especificos (user/project/local). A hierarquia CLAUDE.md funciona normalmente dentro do contexto do subagente. Path-scoped rules em `.claude/rules/` sao ativadas conforme o subagente navega pelo codebase.

### Com "Create Plugins"

Plugins podem conter agentes em `agents/`. A principal restricao e que agentes de plugin NAO suportam `hooks`, `mcpServers` ou `permissionMode` por razoes de seguranca. Para usar esses campos, o agente deve ser copiado para `.claude/agents/`. O campo `agent` no `settings.json` de plugins ativa um agente como main thread.

### Com "Research: LLM Context Optimization"

O conceito de isolamento de contexto de subagentes e uma implementacao direta da estrategia "Isolate" do LangChain (separar contextos de diferentes agentes para evitar contaminacao cruzada). A recomendacao de restringir ferramentas ao minimo necessario e uma aplicacao do principio de "attention budget" -- tool descriptions consumem contexto mesmo quando nao utilizadas.

---

## 8. Forcas e Limitacoes

### Forcas

1. **Flexibilidade de configuracao**: 14 campos de frontmatter cobrem a maioria dos cenarios
2. **Isolamento de contexto**: Protege a conversacao principal de output volumoso
3. **Hierarquia de escopo**: CLI > projeto > usuario > plugin permite override granular
4. **MCP servers escopados**: Ferramentas de plugins ficam fora do contexto principal
5. **Memoria persistente**: Conhecimento acumulado cross-session por subagente
6. **Isolamento via worktree**: Seguranca para operacoes arriscadas
7. **Multiplos metodos de invocacao**: Natural language, @-mention, --agent, settings
8. **Retomada de subagentes**: SendMessage com agent ID preserva historico completo
9. **Auto-compactacao**: Previne estouro de contexto em subagentes long-running

### Limitacoes

1. **Sem aninhamento**: Subagentes nao podem spawnar outros subagentes
2. **Gap de contexto**: Nao recebem historico da conversacao pai
3. **Skills nao herdadas**: Devem ser listadas explicitamente
4. **Restricoes de plugin**: Sem hooks, mcpServers ou permissionMode em agentes de plugin
5. **Resultado no contexto principal**: Muitos subagentes com resultados detalhados podem poluir o contexto
6. **Background auto-deny**: Subagentes em background auto-negam permissoes nao pre-aprovadas
7. **Custo de startup**: Subagentes comecam do zero, precisando tempo para reunir contexto

---

## 9. Recomendacoes Praticas

### 9.1 Template de Subagente para Projeto

```markdown
---
name: project-reviewer
description: >-
  Code review specialist for [project]. Use proactively after code changes.
  Checks quality, security, and adherence to project conventions.
tools: Read, Grep, Glob, Bash
model: sonnet
memory: project
maxTurns: 20
---

You are a senior code reviewer for [project name].

## Your Role
- Review code changes for quality, security, and maintainability
- Check adherence to project conventions documented in CLAUDE.md
- Consult your memory for patterns and issues discovered in reviews anteriores

## Process
1. **Gather context** -- Run `git diff --staged` and `git diff`
2. **Read memory** -- Check agent memory for known patterns
3. **Review** -- Apply checklist to all changed files
4. **Report** -- Format findings by priority (Critical > High > Medium)
5. **Update memory** -- Save new patterns or recurring issues

## Confidence Filter
- Report issues only if >80% confident
- Skip stylistic preferences unless they violate project conventions
- Consolidate similar issues
```

### 9.2 Padrao de Chaining para Workflows Complexos

```text
# Passo 1: Pesquisa
Use the explore subagent to analyze the authentication module architecture

# Passo 2: Planejamento
Based on the findings, use the planner subagent to create a refactoring plan

# Passo 3: Implementacao
Use the developer subagent to implement the first phase of the plan

# Passo 4: Validacao
Use the code-reviewer subagent to review the implementation
```

### 9.3 Otimizacao de Custos

1. Use `haiku` para exploracao e busca (built-in Explore ja faz isso)
2. Use `sonnet` como default para trabalho geral
3. Reserve `opus` apenas para decisoes de arquitetura complexas
4. Restrinja ferramentas ao minimo necessario (reduz token de descricoes de ferramentas)
5. Defina `maxTurns` para prevenir runaway agents
6. Use MCP servers inline para evitar descricoes de ferramentas no contexto principal

### 9.4 Seguranca

1. Use `permissionMode: plan` para subagentes que devem apenas observar
2. Use `permissionMode: dontAsk` para subagentes que devem falhar graciosamente
3. Implemente `PreToolUse` hooks para validacao de comandos arriscados
4. Use `isolation: worktree` para refactorings grandes
5. Nunca use `bypassPermissions` sem necessidade explicita e compreensao dos riscos
