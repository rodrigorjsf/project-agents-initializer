# Analise: Pesquisa de Melhores Praticas para Subagentes

---

## 1. Resumo Executivo

O documento de pesquisa sobre melhores praticas de subagentes e o mais abrangente dos cinco documentos analisados, compilando informacoes de documentacao oficial da Anthropic, repositorios da comunidade (97k+ stars no everything-claude-code), guias de prompt engineering e padroes emergentes do ecossistema. Ele sintetiza 17 secoes cobrindo desde a especificacao oficial ate templates completos de definicao de agentes, com foco pratico em anti-patterns a evitar e padroes de sucesso comprovados.

As descobertas mais valiosas incluem: (1) a importancia critica do campo `description` como unico sinal de roteamento para delegacao automatica; (2) o padrao de "Confidence-Based Filtering" que reduz ruido nas saidas de subagentes; (3) a observacao de que agentes read-only dominam nos repositorios da comunidade; (4) a estrutura eficaz de system prompt (Role -> Process -> Checklist -> Output Format -> Approval Criteria); e (5) os 10 anti-patterns documentados que representam as falhas mais comuns. O documento tambem mapeia a relacao bidirecional entre skills e subagentes (`context: fork` em skills vs campo `skills` em subagentes) e fornece analise de selecao de modelo com justificativa por tipo de tarefa.

A contribuicao unica deste documento em relacao a documentacao oficial e a compilacao de padroes da comunidade, a analise de anti-patterns, e a ponte explicita entre subagentes e tecnicas de prompt engineering aplicaveis a system prompts de agentes.

---

## 2. Conceitos e Mecanismos Chave

### 2.1 Delegacao Automatica

O Claude decide quando delegar com base em tres fatores:

1. Descricao da tarefa na solicitacao do usuario
2. Campo `description` nas configuracoes de subagentes
3. Contexto atual da conversa

Para encorajar delegacao proativa, incluir frases como **"use proactively"** no campo description.

### 2.2 Relacao Bidirecional Skills ↔ Subagentes

| Abordagem | System Prompt | Tarefa | Tambem Carrega |
|-----------|---------------|--------|----------------|
| Skill com `context: fork` | Do tipo de agente (Explore, Plan, etc.) | Conteudo do SKILL.md | CLAUDE.md |
| Subagente com campo `skills` | Corpo markdown do subagente | Mensagem de delegacao do Claude | Skills pre-carregadas + CLAUDE.md |

**Skill que roda em subagente**:

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---
Research $ARGUMENTS thoroughly...
```

**Subagente que carrega skills**:

```yaml
---
name: api-developer
description: Implement API endpoints
skills:
  - api-conventions
  - error-handling-patterns
---
```

### 2.3 Injecao Dinamica de Contexto

A sintaxe `` !`<command>` `` em skills executa comandos shell antes do conteudo ser enviado ao Claude:

```yaml
---
name: pr-summary
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---
## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`

## Your task
Summarize this pull request...
```

Comandos executam imediatamente (pre-processamento); output substitui o placeholder.

### 2.4 Estrutura Eficaz de System Prompt

Baseado na analise de exemplos oficiais e padroes da comunidade:

```
1. Role Definition -- "You are a [specific role] specializing in [domain]"
2. Responsibilities -- Bullets claros do que o agente faz
3. Process Steps -- Numerados: gather context -> analyze -> act -> verify -> report
4. Checklist/Criteria -- Categorizado por severidade (CRITICAL -> LOW)
5. Output Format -- Formato exato esperado
6. Approval/Success Criteria -- Quando aprovar vs quando sinalizar
```

### 2.5 Selecao de Modelo

| Alias | Mapeia Para | Melhor Para |
|-------|-------------|-------------|
| `haiku` | Claude Haiku 4.5 | Tarefas rapidas, exploracao, analise simples |
| `sonnet` | Claude Sonnet 4.6 | Tarefas padrao, reviews, trabalho diario |
| `opus` | Claude Opus 4.6 | Raciocinio complexo, arquitetura, planejamento |
| `inherit` | Mesmo da conversacao principal | Comportamento default |
| `sonnet[1m]` | Sonnet com contexto 1M | Sessoes longas com codebases grandes |
| `opus[1m]` | Opus com contexto 1M | Sessoes longas com raciocinio complexo |

**Principio**: Opus para arquitetura, Sonnet para tudo mais. Haiku apenas para tarefas mecanicas e de exploracao.

### 2.6 Niveis de Esforco

| Nivel | Comportamento | Melhor Para |
|-------|---------------|-------------|
| `low` | Thinking minimo, respostas rapidas | Tarefas simples, mecanicas |
| `medium` | Thinking equilibrado | Tarefas padrao |
| `high` | Thinking profundo | Problemas complexos |
| `max` | Sem restricao de tokens de thinking (Opus 4.6 only) | Problemas mais dificeis |

### 2.7 Padroes da Comunidade (everything-claude-code, 97k+ stars)

| Agente | Modelo | Ferramentas | Padrao |
|--------|--------|-------------|--------|
| `code-reviewer` | sonnet | Read, Grep, Glob, Bash | Read-only com confidence filtering |
| `architect` | opus | Read, Grep, Glob | Read-only com analise de trade-offs |
| `security-reviewer` | sonnet | Read, Write, Edit, Bash, Grep, Glob | Auditoria de seguranca full-capability |
| `debugger` | inherit | Read, Edit, Bash, Grep, Glob | Workflow analise + fix |
| `typescript-reviewer` | implied | Read, Grep, Glob, Bash | Review language-specific |

**Padroes observados**:

1. Agentes read-only dominam (maioria restringe a Read, Grep, Glob, Bash)
2. Reviewers language-specific com checklists por tecnologia
3. Opus reservado para `architect`; Sonnet para todo o resto
4. Checklists detalhados com prioridade (CRITICAL -> LOW)
5. Formato de output estruturado com tabelas e sumarios

### 2.8 Confidence-Based Filtering

```markdown
## Confidence-Based Filtering

**IMPORTANT**: Do not flood the review with noise. Apply these filters:

- **Report** if you are >80% confident it is a real issue
- **Skip** stylistic preferences unless they violate project conventions
- **Skip** issues in unchanged code unless they are CRITICAL security issues
- **Consolidate** similar issues
- **Prioritize** issues that could cause bugs, security vulnerabilities, or data loss
```

Este padrao reduz significativamente o ruido e torna a saida do agente acionavel.

---

## 3. Pontos de Atencao

### 3.1 Os 10 Anti-Patterns Documentados

| # | Anti-Pattern | Consequencia | Mitigacao |
|---|-------------|--------------|-----------|
| 1 | Prompts de delegacao agressivos ("CRITICAL: You MUST...") | Overtriggering com Opus 4.6 | Usar linguagem normal ("Use this tool when...") |
| 2 | Muitas skills/agentes | Excedem orcamento de contexto (2% por skill description) | Monitorar via `/context` |
| 3 | Subagentes para operacoes grep simples | Desperdicio de tokens e latencia | Orientar para uso direto da ferramenta |
| 4 | Nao restringir ferramentas | Modificacoes nao intencionais, contexto desperdicado | Allowlist minimo necessario |
| 5 | Descricoes vagas | Delegacao inconsistente ou ausente | "Use proactively when [trigger]" |
| 6 | God agents (faz tudo) | Perde proposito de especializacao | Um dominio por agente |
| 7 | Sem especificacao de formato de output | Resultados inconsistentes e dificieis de usar | Especificar formato exato no prompt |
| 8 | Ignorar gap de contexto do pai | Agente nao tem informacao necessaria | Tudo no system prompt ou via ferramentas |
| 9 | Sem etapa de coleta de contexto | Analise sem fundamentacao | Sempre comecar com "gather context" |
| 10 | Sem `maxTurns` | Agentes rodam indefinidamente consumindo tokens | Definir limite razoavel (10-30) |

### 3.2 Custo de Tool Descriptions no Contexto

Skill descriptions ocupam ~2% da janela de contexto. Com muitos agentes e skills registrados, esse custo acumula. Use `/context` para verificar warnings sobre excesso.

### 3.3 Claude Opus 4.6 e Responsividade Excessiva

Opus 4.6 e mais responsivo a system prompts, o que significa que linguagem agressiva ("CRITICAL", "YOU MUST", "NEVER") causa overtriggering. A recomendacao e usar linguagem normal e confiar na capacidade do modelo de interpretar instrucoes sem enfase artificial.

### 3.4 Orquestracao Nativa vs Prescritiva

Os modelos mais recentes do Claude possuem orquestracao nativa de subagentes. A recomendacao da Anthropic e: "Prefer general instructions over prescriptive steps" -- "think thoroughly" frequentemente produz raciocinio melhor que planos step-by-step escritos manualmente.

### 3.5 Seguranca de Plugins

Agentes de plugins NAO podem usar `hooks`, `mcpServers` ou `permissionMode`. Campos suportados: `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `isolation`.

---

## 4. Casos de Uso e Escopo

### 4.1 Perfis de Ferramentas por Tipo de Agente

| Tipo de Agente | Ferramentas Recomendadas | Justificativa |
|----------------|-------------------------|---------------|
| Read-only reviewer | Read, Grep, Glob, Bash | Inspeciona sem modificar |
| Code modifier | Read, Edit, Bash, Grep, Glob | Analisa e corrige |
| Explorer/researcher | Read, Grep, Glob | Exploracao pura, sem efeitos colaterais |
| Full-capability | Herda todas | Operacoes complexas multi-passo |

### 4.2 Quando Usar `context: fork` em Skills

- Tarefas orientadas a resultado que devem rodar em isolamento
- Pesquisa profunda que geraria muito output no contexto principal
- Tarefas que se beneficiam de subagente especifico (ex: Explore para read-only)

### 4.3 Quando Usar Preload de Skills em Subagentes

- Subagentes que precisam de conhecimento de dominio especifico
- Convencoes de API, padroes de error handling, guias de estilo
- Quando o conhecimento deve estar no contexto desde o inicio (nao descoberto sob demanda)

---

## 5. Aplicabilidade a Infraestrutura de Agentes

### 5.1 Skills

- **Relacao bidirecional**: Skills podem rodar em subagentes (`context: fork`) E subagentes podem carregar skills (`skills` field)
- **Injecao dinamica**: `` !`command` `` permite dados em tempo real no skill content
- **Descricoes como custo**: Cada skill description consome ~2% do orcamento de contexto
- **Disable-model-invocation**: `true` mantem descricoes fora do contexto ate invocacao manual
- **Plugin skills**: Skills de plugins sao invocaveis por subagentes com namespace `plugin-name:skill-name`

### 5.2 Hooks

- **PreToolUse para guardrails**: Validacao de comandos antes da execucao (ex: bloquear SQL write)
- **PostToolUse para qualidade**: Linter apos edicoes, testes apos mudancas
- **Stop -> SubagentStop**: Conversao automatica no runtime
- **SubagentStart/SubagentStop**: Hooks de ciclo de vida no settings.json para setup/cleanup
- **Quatro tipos**: `command` (shell), `http` (POST), `prompt` (avaliacao Claude), `agent` (subagente verificador)
- **Exit codes**: 0 = permite, 2 = bloqueia (stderr vira feedback para o Claude)

### 5.3 Subagentes

- **Anti-aninhamento**: Subagentes nao podem spawnar outros subagentes
- **Hub-and-spoke**: Resultados retornam apenas ao caller
- **Retomada**: SendMessage com agent ID preserva historico
- **Isolamento**: worktree para operacoes arriscadas, cleanup automatico
- **Delegacao**: description e o sinal de roteamento; "use proactively" melhora delegacao
- **Agent(type)**: Restringe quais subagentes podem ser spawnados no modo `--agent`
- **CLI-defined**: JSON via `--agents` para sessoes temporarias e automacao

### 5.4 Rules

- **Em contexto de subagente**: `.claude/rules/` carregadas normalmente
- **Path-scoped**: Ativadas conforme subagente le arquivos correspondentes
- **Plugin-scoped**: Carregadas pelo subagente junto com o plugin
- **Conflitos**: Se rules contradizem o system prompt do subagente, o system prompt prevalece
- **Hierarquia**: Managed > project > user, mesma ordem dentro do subagente

### 5.5 Memoria

- **Tres escopos**: user (cross-projeto), project (versionavel), local (nao commitavel)
- **MEMORY.md index**: Primeiras 200 linhas no startup
- **Topic files**: Carregados sob demanda
- **Instrucoes no prompt**: "Read memory before starting, update after finishing"
- **Curadoria automatica**: Subagente instruidoa a curar MEMORY.md se exceder 200 linhas
- **Auto-enable**: Read, Write, Edit habilitados automaticamente quando memory esta ativo

---

## 6. Aplicabilidade do Guia de Engenharia de Prompts

### 6.1 CoT para Cadeias de Raciocinio de Subagentes

O documento enfatiza que o system prompt do subagente e TUDO que ele tem. CoT no system prompt melhora a qualidade de raciocinio, especialmente para reviews e debugging. A estrutura recomendada:

```markdown
When invoked:
1. Gather context -- understand what you're working with
2. Analyze -- apply criteria systematically
3. Reason step by step about each finding
4. Verify -- confirm conclusions with evidence
5. Report -- structured output
```

**Alerta**: Com Opus 4.6, "think thoroughly" frequentemente supera steps prescritivos de CoT. CoT explicito e mais eficaz com Sonnet e Haiku.

### 6.2 ReAct para Subagentes com Acesso a Ferramentas

O padrao ReAct e o loop fundamental de cada subagente com ferramentas. Os melhores exemplos da comunidade (code-reviewer, debugger) implementam ReAct implicitamente:

1. **Pensamento**: "Preciso entender as mudancas recentes"
2. **Acao**: `git diff --staged`
3. **Observacao**: Analise do output
4. **Repeticao**: Proxima ferramenta ou conclusao

O system prompt deve estruturar o workflow para encorajar esse ciclo naturalmente.

### 6.3 Tree of Thoughts para Subagentes de Exploracao

Multiplos subagentes em paralelo implementam ToT distribuido:

- Cada subagente explora um ramo (hipotese, modulo, abordagem)
- O agente principal avalia e sintetiza os resultados
- Implementacao natural via: "Research authentication, database, and API modules in parallel using separate subagents"

### 6.4 Self-Consistency para Validacao entre Multiplos Subagentes

O padrao Confidence-Based Filtering e uma forma de Self-Consistency interna ao subagente. Para Self-Consistency entre subagentes:

- Executar multiplos subagentes de review no mesmo codigo
- Comparar findings: issues reportadas por multiplas execucoes tem maior confianca
- Custo multiplicado pelo numero de execucoes

### 6.5 Reflexion para Melhoria Iterativa de Subagentes

A memoria persistente implementa Reflexion cross-session:

- Subagente aprende com reviews anteriores (armazenados em MEMORY.md)
- Padroes recorrentes sao documentados e consultados
- Cada sessao melhora a base de conhecimento

Dentro de uma sessao, chaining de subagentes implementa Reflexion:

```
reviewer -> fixer -> reviewer (validacao)
```

### 6.6 Least-to-Most para Decomposicao de Tarefas entre Subagentes

O padrao "Explore -> Plan -> Code -> Verify" e uma implementacao de Least-to-Most:

1. Subagente Explore (tarefa mais simples: mapear)
2. Subagente Plan (intermediario: planejar)
3. Subagente general-purpose (mais complexo: implementar)
4. Subagente reviewer (validacao final)

---

## 7. Correlacoes com os Documentos Principais

### Com "Creating Custom Subagents"

Este documento de research e o complemento pratico direto da documentacao oficial. Onde a doc oficial apresenta campos e opcoes, o research fornece:

- Exemplos concretos da comunidade (27+ agentes do everything-claude-code)
- Anti-patterns que a doc oficial nao cobre
- Padroes de prompt engineering especificos para system prompts de agentes
- Analise de custo por modelo com justificativa

### Com "Orchestrate Teams of Claude Code Sessions"

A secao 15 (Agent Teams vs Subagents) fornece a tabela comparativa que ajuda na decisao. O ponto-chave que nao esta na doc de teams: subagentes sao para tarefas focadas com resultado sumarizado; teams sao para trabalho complexo com debate.

### Com "How Claude Remembers a Project"

A secao 11 (Persistent Memory) aplica os mecanismos de memoria do CLAUDE.md/auto memory especificamente para subagentes. A recomendacao de `memory: project` como default alinha com a filosofia de versionamento da doc de memoria. O limite de 200 linhas do MEMORY.md e consistente entre as duas documentacoes.

### Com "Create Plugins"

A secao 16 (Plugin-Shipped Agents) documenta as restricoes de seguranca de agentes em plugins. A estrutura de diretorio (`agents/` no plugin root) e consistente com a arquitetura de plugins. A limitacao de campos suportados e uma informacao unica deste documento.

### Com "Research: LLM Context Optimization"

As recomendacoes de "attention budget" mapeiam diretamente para:

- Anti-pattern #2 (muitas skills/agentes consomem orcamento de contexto)
- Anti-pattern #4 (tool descriptions de ferramentas nao utilizadas)
- Principio de selecao de modelo (haiku para tarefas simples = menos custo de tokens)
- Confidence-Based Filtering (reduz tokens de output desperdicados)

O principio "lost in the middle" implica que a estrutura do system prompt importa: informacoes criticas no inicio e no fim.

---

## 8. Forcas e Limitacoes

### Forcas

1. **Abrangencia**: 17 secoes cobrindo da especificacao oficial a padroes da comunidade
2. **Praticidade**: Anti-patterns concretos com mitigacoes
3. **Template completo**: Apendice A com template de definicao de agente pronto para uso
4. **Dados da comunidade**: 97k+ stars do everything-claude-code validam os padroes
5. **Ponte skills-subagentes**: Documentacao clara da relacao bidirecional
6. **Tabela de selecao de modelo**: Justificativa por tipo de tarefa
7. **Confidence-Based Filtering**: Padrao replicavel para qualquer agente de review
8. **Prompt engineering para agentes**: Secao dedicada com principios da Anthropic

### Limitacoes

1. **Datacao**: Data de marco 2026 -- features experimentais podem ter mudado
2. **Sem benchmarks quantitativos**: Nao ha metricas de performance comparativa entre padroes
3. **Foco em review/analise**: A maioria dos exemplos e para agentes de review, com menos cobertura de agentes de implementacao
4. **Ausencia de testing**: Nao ha secao sobre como testar subagentes de forma sistematica
5. **Comunidade como fonte**: Padroes da comunidade podem nao refletir melhores praticas oficiais
6. **Sem analise de custo real**: Recomendacoes de modelo sao qualitativas, sem dados de custo por tarefa

---

## 9. Recomendacoes Praticas

### 9.1 Checklist para Criacao de Subagente

```
[ ] name: identificador unico, lowercase com hifens
[ ] description: inclui "Use proactively when..." ou "Use after..."
[ ] tools: minimo necessario (preferir Read, Grep, Glob, Bash para read-only)
[ ] model: sonnet como default, haiku para exploracao, opus para arquitetura
[ ] maxTurns: definido (10-30 para a maioria dos cenarios)
[ ] System prompt: segue Role -> Process -> Checklist -> Output Format
[ ] Confidence filter: incluido para agentes de review
[ ] Memory: definida se aprendizado cross-session e valioso
[ ] Testado: invocado manualmente e verificado output
```

### 9.2 Padrao de Review Agent com Confidence Filtering

```markdown
---
name: domain-reviewer
description: >-
  [Domain] review specialist. Use proactively after changes to [scope].
tools: Read, Grep, Glob, Bash
model: sonnet
memory: project
maxTurns: 20
---

You are a [domain] specialist reviewing code for [criteria].

## Process
1. Run `git diff --staged` to see changes
2. Read agent memory for known patterns
3. Review each file against checklist
4. Apply confidence filter
5. Report findings in structured format
6. Update memory with new patterns

## Checklist
### Critical
- [Must-flag items]

### High
- [Should-flag items]

## Confidence Filter
- Report only if >80% confident
- Skip stylistic preferences unless violating conventions
- Consolidate similar issues
- Prioritize bugs, security, data loss

## Output Format
[SEVERITY] Issue title
File: path/to/file:line
Issue: Description
Fix: Suggested fix
```

### 9.3 Estrategia de Selecao de Modelo para o Projeto

```
Regra simples:
- Exploracao, busca, tarefas mecanicas -> haiku
- Reviews, debugging, implementacao -> sonnet
- Arquitetura, planejamento complexo -> opus
- Em duvida -> sonnet (melhor custo/qualidade)
```

### 9.4 Migrar de Plugin Agent para Project Agent

Quando um agente de plugin precisa de `hooks`, `mcpServers` ou `permissionMode`:

```bash
# Copiar do diretorio do plugin para o projeto
cp path/to/plugin/agents/reviewer.md .claude/agents/reviewer.md

# Adicionar campos restritos no frontmatter
# hooks:, mcpServers:, permissionMode: agora funcionam
```

### 9.5 Automatizar Verificacao de Orcamento de Contexto

Executar periodicamente `/context` para verificar se skills e agentes estao consumindo orcamento excessivo. Se warnings aparecerem:

1. Reduzir numero de agentes registrados
2. Usar `disable-model-invocation: true` em skills nao essenciais
3. Mover skills raramente usadas para invocacao manual
4. Consolidar agentes com dominios sobrepostos
