# Análise Completa: Claude Hook Reference Doc

## 1. Sumário Executivo

O documento **claude-hook-reference-doc.md** é a referência técnica definitiva do sistema de hooks do Claude Code — o mecanismo que permite interceptar, validar, bloquear, modificar e estender o comportamento do agente em pontos específicos do seu ciclo de vida. Diferente do guia introdutório (`automate-workflow-with-hooks.md`), este documento especifica com precisão milimétrica cada evento, schema de entrada/saída JSON, códigos de saída, padrões de decisão e tipos de hook (command, HTTP, prompt, agent).

O sistema de hooks representa a implementação mais sofisticada do princípio de **enforcement determinístico** identificado na pesquisa de otimização de contexto: ao converter instruções comportamentais em hooks programáticos, removemos regras do budget de atenção do modelo enquanto garantimos sua aplicação 100% consistente. O documento cobre 22 eventos de lifecycle, 4 tipos de handler (command, HTTP, prompt, agent), mecanismos de decisão por evento, hooks assíncronos, e integração com skills, subagents, worktrees e MCP.

A riqueza deste documento está no nível de controle granular que ele expõe: desde a capacidade de modificar inputs de ferramentas antes da execução (`updatedInput`), injetar contexto adicional em subagents (`SubagentStart.additionalContext`), até controlar programaticamente permissões (`PermissionRequest.updatedPermissions`). Para quem constrói infraestrutura de agentes, este é o documento que transforma o Claude Code de um assistente passivo em uma plataforma programável.

## 2. Conceitos e Mecanismos-Chave

### 2.1 Arquitetura do Lifecycle de Hooks

O sistema opera em três níveis de aninhamento:

| Nível | Componente | Função |
|-------|------------|--------|
| 1 | **Hook Event** | Ponto do lifecycle (ex: `PreToolUse`, `Stop`) |
| 2 | **Matcher Group** | Filtro regex que determina quando disparar |
| 3 | **Hook Handler** | O que executar quando há match (command/http/prompt/agent) |

### 2.2 Os 22 Eventos de Lifecycle

O documento categoriza os eventos em grupos funcionais:

**Eventos de Sessão:**

- `SessionStart` — Início/resumo de sessão. Único evento com acesso a `CLAUDE_ENV_FILE` para persistir variáveis de ambiente.
- `SessionEnd` — Término de sessão. Timeout padrão de 1.5s (configurável via `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`).

**Eventos do Loop Agêntico (pré-execução):**

- `UserPromptSubmit` — Antes do Claude processar o prompt do usuário. Pode bloquear ou adicionar contexto.
- `PreToolUse` — Antes de qualquer ferramenta executar. Controle mais rico: allow/deny/ask + `updatedInput`.
- `PermissionRequest` — Quando o diálogo de permissão apareceria. Pode auto-aprovar com `updatedPermissions`.

**Eventos do Loop Agêntico (pós-execução):**

- `PostToolUse` — Após execução bem-sucedida de ferramenta. Pode fornecer feedback e até substituir output de MCP tools.
- `PostToolUseFailure` — Após falha de ferramenta. Contexto adicional para o Claude sobre a falha.

**Eventos de Subagent:**

- `SubagentStart` — Ao spawn de subagent. Pode injetar contexto no subagent.
- `SubagentStop` — Ao término de subagent. Mesmo controle que `Stop`.

**Eventos de Parada:**

- `Stop` — Quando o Claude termina de responder. Pode forçá-lo a continuar.
- `StopFailure` — Quando a resposta falha por erro de API. Sem controle de decisão.

**Eventos de Equipe:**

- `TeammateIdle` — Quando um teammate está prestes a ficar ocioso.
- `TaskCompleted` — Quando uma task é marcada como completa. Pode impedir a conclusão.

**Eventos de Configuração e Instrução:**

- `ConfigChange` — Mudança em settings. Pode bloquear (exceto `policy_settings`).
- `InstructionsLoaded` — Quando CLAUDE.md ou rules são carregados. Somente observação.

**Eventos de Compactação:**

- `PreCompact` — Antes da compactação de contexto.
- `PostCompact` — Após compactação, com acesso ao `compact_summary`.

**Eventos de Worktree:**

- `WorktreeCreate` — Substitui o comportamento padrão de `git worktree`. Deve retornar path absoluto.
- `WorktreeRemove` — Cleanup de worktrees.

**Eventos de MCP:**

- `Elicitation` — Interceptação de pedidos de input de MCP servers.
- `ElicitationResult` — Modificação de respostas a elicitações.

**Evento de Notificação:**

- `Notification` — Dispara em notificações do sistema.

### 2.3 Quatro Tipos de Hook Handler

| Tipo | Mecanismo | Eventos Suportados | Timeout Padrão |
|------|-----------|-------------------|----------------|
| `command` | Shell script via stdin/stdout | Todos os 22 eventos | 600s |
| `http` | POST para endpoint HTTP | 8 eventos do loop agêntico | 30s |
| `prompt` | LLM single-turn para decisão | 8 eventos do loop agêntico | 30s |
| `agent` | Subagent com acesso a ferramentas | 8 eventos do loop agêntico | 60s |

Os 8 eventos que suportam todos os tipos: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `TaskCompleted`.

### 2.4 Sistema de Decisão por Evento

O documento revela três padrões distintos de controle de decisão:

```
Padrão 1: Top-level decision
  → UserPromptSubmit, PostToolUse, PostToolUseFailure, Stop, SubagentStop, ConfigChange
  → { "decision": "block", "reason": "..." }

Padrão 2: hookSpecificOutput com permissionDecision
  → PreToolUse
  → { "hookSpecificOutput": { "permissionDecision": "allow|deny|ask" } }

Padrão 3: hookSpecificOutput com decision.behavior
  → PermissionRequest
  → { "hookSpecificOutput": { "decision": { "behavior": "allow|deny" } } }
```

### 2.5 Mecanismo de Exit Codes

| Exit Code | Significado | Processamento JSON |
|-----------|-------------|-------------------|
| 0 | Sucesso — ação permitida | Sim, stdout é parseado como JSON |
| 2 | Erro bloqueante — ação impedida | Não, stderr usado como mensagem |
| Outro | Erro não-bloqueante — continua | Não, stderr mostrado em modo verbose |

### 2.6 Locais de Configuração (Hierarquia de Escopo)

| Local | Escopo | Compartilhável |
|-------|--------|---------------|
| `~/.claude/settings.json` | Todos os projetos | Não |
| `.claude/settings.json` | Projeto único | Sim (versionável) |
| `.claude/settings.local.json` | Projeto único | Não (gitignored) |
| Managed policy settings | Organização | Sim (admin) |
| Plugin `hooks/hooks.json` | Plugin ativo | Sim |
| Skill/Agent YAML frontmatter | Componente ativo | Sim |

### 2.7 Hooks Assíncronos

A flag `"async": true` (apenas para `type: "command"`) permite execução em background:

- Claude continua trabalhando imediatamente
- Output entregue no próximo turno via `systemMessage` ou `additionalContext`
- Campos de decisão são ignorados (ação já procedeu)
- Sem deduplicação entre múltiplas execuções

### 2.8 Hooks em Skills e Agents

Hooks podem ser definidos diretamente no frontmatter YAML de skills e subagents:

- Escopo limitado ao lifecycle do componente
- Cleanup automático ao término
- `Stop` hooks em subagents são convertidos automaticamente para `SubagentStop`
- Suportam `"once": true` para execução única por sessão

## 3. Pontos de Atenção

### 3.1 Gotchas Críticos

| Ponto | Detalhe | Impacto |
|-------|---------|---------|
| **Loop infinito de Stop hooks** | Se um Stop hook sempre retorna `"block"`, Claude nunca para | Sessão travada; verificar `stop_hook_active` |
| **Exit code 2 ≠ block para todos** | Eventos como `PostToolUse` e `SessionStart` ignoram exit 2 como decisão | Comportamento inconsistente se não checado |
| **JSON parsing com shell profile** | Se o shell profile imprime texto no startup, interfere com parsing JSON | Hooks command falham silenciosamente |
| **Hooks HTTP não bloqueiam por status** | Non-2xx é erro não-bloqueante; para bloquear, retorne 2xx com JSON de deny | Falsa sensação de segurança |
| **policy_settings não bloqueáveis** | `ConfigChange` hooks com `"block"` são ignorados para `policy_settings` | Design intencional para enterprise |
| **SessionEnd timeout de 1.5s** | Hooks de cleanup podem não completar a tempo | Usar `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` |
| **Matchers são regex, não glob** | `Edit|Write` usa `|` como OR regex, não shell glob | Padrões inesperados se não escapados |
| **Hooks assíncronos sem decisão** | `decision`, `permissionDecision`, `continue` ignorados em async | Usar apenas para side-effects |

### 3.2 Segurança

- **Hooks command executam com permissões completas do usuário** — podem acessar, modificar ou deletar qualquer arquivo
- Variáveis de shell devem ser SEMPRE quotadas (`"$VAR"` não `$VAR`)
- Paths devem ser absolutos, usando `$CLAUDE_PROJECT_DIR`
- Inputs devem ser validados e sanitizados
- Verificar path traversal (`..` em file paths)
- Evitar processar `.env`, `.git/`, chaves privadas

### 3.3 Ordem de Execução

- Todos os hooks matching para um evento executam em paralelo
- Handlers idênticos são deduplicados (por command string ou URL)
- Hooks de múltiplas fontes (user, project, plugin, skill) se combinam
- `disableAllHooks: true` desabilita todos exceto managed hooks

## 4. Casos de Uso e Escopo

### 4.1 Quando Usar Cada Evento

| Cenário | Evento Recomendado | Tipo de Hook |
|---------|--------------------|----|
| Bloquear comandos destrutivos | `PreToolUse` matcher `Bash` | command |
| Auto-aprovar comandos seguros | `PermissionRequest` | command/prompt |
| Lint após edição de arquivo | `PostToolUse` matcher `Edit\|Write` | command (async) |
| Carregar contexto de projeto | `SessionStart` | command |
| Garantir testes passando antes de parar | `Stop` | agent |
| Logging de operações MCP | `PreToolUse` matcher `mcp__.*` | command |
| Validação de PR antes de commit | `PreToolUse` matcher `Bash` | command |
| Injetar guidelines em subagents | `SubagentStart` | command |
| Auditoria de mudanças de config | `ConfigChange` | command |
| Prevenir conclusão prematura de tasks | `TaskCompleted` | command/prompt |
| Cleanup de worktrees custom (SVN/Perforce) | `WorktreeCreate` + `WorktreeRemove` | command |
| Automação de respostas MCP | `Elicitation` | command |

### 4.2 Quando NÃO Usar Hooks

| Cenário | Alternativa Melhor | Por quê |
|---------|-------------------|---------|
| Guidance sobre estilo de código | Rules (`.claude/rules/`) | Não precisa enforcement determinístico |
| Documentação de projeto | CLAUDE.md | Hooks não adicionam contexto persistente |
| Instruções complexas multi-passo | Skills | Hooks são para ações pontuais, não workflows |
| Regras que precisam de julgamento do modelo | Rules + CoT | Hooks command são binários (allow/block) |

## 5. Aplicabilidade à Infraestrutura de Agentes

### 5.1 Skills

**Hooks como extensão de skills:**

- Skills podem definir hooks no seu frontmatter YAML, criando workflows auto-contidos
- Um skill de "database migration" pode ter um `PreToolUse` hook que valida comandos SQL antes da execução
- Flag `"once": true` é ideal para hooks de setup que devem rodar apenas na ativação do skill

**Padrão: Skill com validação por hook**

```yaml
---
name: safe-db-migration
description: Run database migrations with safety checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-sql.sh"
  Stop:
    - hooks:
        - type: agent
          prompt: "Verify migration completed successfully. Check database state."
---
```

**Ciclo de vida complementar:**

- Hook `SessionStart` pode carregar estado que skills precisam
- Hook `PostToolUse` pode validar outputs de scripts executados por skills
- Hook `Stop` (tipo agent) pode verificar se o skill completou corretamente

### 5.2 Hooks (Design Patterns)

**Padrão 1: Guardrail em Camadas**

```
PreToolUse (command) → Validação rápida e determinística
  ↓ Se "ask"
PermissionRequest (prompt) → Avaliação por LLM se ambíguo
  ↓ Se "allow"
PostToolUse (command) → Verificação de resultado
  ↓
Stop (agent) → Verificação final com acesso a ferramentas
```

**Padrão 2: Feedback Loop Assíncrono**

```
PostToolUse (async command) → Roda testes em background
  → Claude continua trabalhando
  → Resultado entregue como systemMessage no próximo turno
  → Claude corrige se testes falharam
```

**Padrão 3: Context Injection Dinâmico**

```
SessionStart → Carrega issues do GitHub, estado do CI
SubagentStart → Injeta guidelines específicas para o tipo de subagent
UserPromptSubmit → Adiciona metadata sobre o estado atual do projeto
```

**Padrão 4: Composição de Hooks de Múltiplas Fontes**

- User settings: hooks globais de segurança
- Project settings: hooks de linting e testing
- Plugin hooks: hooks de formatação
- Skill frontmatter: hooks específicos do workflow

### 5.3 Subagents

**Hooks que afetam subagents:**

- `SubagentStart` — Injetar contexto e guidelines antes do subagent começar a trabalhar
- `SubagentStop` — Validar que o subagent completou satisfatoriamente (mesmo padrão de `Stop`)
- `PreToolUse` com `agent_id` no input — Permite distinguir chamadas de subagents vs main thread
- Hooks definidos em agent frontmatter são scoped ao lifecycle do subagent

**Campo `agent_id` e `agent_type`:**
O input de hooks inclui `agent_id` e `agent_type` quando executando em contexto de subagent, permitindo lógica condicional:

```bash
AGENT_TYPE=$(echo "$INPUT" | jq -r '.agent_type // empty')
if [ "$AGENT_TYPE" = "Explore" ]; then
  # Regras diferentes para agents de exploração
fi
```

### 5.4 Rules

**Hooks vs Rules — Framework de Decisão:**

| Critério | Hook | Rule |
|----------|------|------|
| Enforcement | Determinístico (programático) | Probabilístico (via atenção do modelo) |
| Custo de contexto | Zero (fora da janela) | Consome tokens do budget |
| Flexibilidade | Binário (allow/block) ou LLM (prompt/agent) | Nuançado, contextual |
| Quando carregar | Sempre ativo (lifecycle) | Path-scoped, lazy |
| Manutenção | Scripts externos | Markdown inline |
| Verificabilidade | Testável independentemente | Depende do comportamento do modelo |

**Princípio derivado do research-llm-context-optimization:**
> "Converter instruções comportamentais que são enforced em hooks remove-as do budget de atenção enquanto garante enforcement determinístico."

**Regra prática:** Se a instrução pode ser verificada programaticamente e deve SEMPRE ser seguida, use hook. Se requer julgamento contextual, use rule.

### 5.5 Memory

**Hooks que interagem com memória:**

- `SessionStart` pode verificar se MEMORY.md existe e está atualizado
- `PostCompact` pode salvar `compact_summary` para referência futura
- `InstructionsLoaded` pode auditar quais arquivos de memória foram carregados e quando
- `ConfigChange` com matcher `skills` pode detectar quando skills que geram memória são modificados

**Padrão: Auto-cleanup de memória via PostCompact:**

```bash
#!/bin/bash
INPUT=$(cat)
SUMMARY=$(echo "$INPUT" | jq -r '.compact_summary')
echo "$SUMMARY" >> ~/.claude/projects/my-project/compaction-history.log
```

## 6. Aplicabilidade do Guia de Engenharia de Prompts

### 6.1 Técnicas Aplicáveis a Hooks

| Técnica | Tipo de Hook | Aplicação |
|---------|-------------|-----------|
| **ReAct** | `type: "agent"` | Agent hooks naturalmente implementam ReAct: raciocinam sobre o estado, usam ferramentas para investigar, decidem |
| **Chain-of-Thought** | `type: "prompt"` | Prompts de hooks podem incluir "Analise passo a passo antes de decidir" para melhor julgamento |
| **Self-Consistency** | Múltiplos hooks prompt | Rodar 2-3 prompt hooks para o mesmo evento e requerer consenso (via script wrapper) |
| **Least-to-Most** | Composição de hooks | Decompor validações complexas: hook 1 verifica sintaxe → hook 2 verifica segurança → hook 3 verifica compliance |
| **Prompt Chaining** | Pipeline de eventos | `PreToolUse` → `PostToolUse` → `Stop` formam uma chain natural de validação |

### 6.2 Exemplo: Stop Hook com CoT

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Analise passo a passo se Claude completou a tarefa. Context: $ARGUMENTS\n\n1. Quais tarefas foram solicitadas?\n2. Quais foram completadas?\n3. Há erros pendentes?\n4. Testes passaram?\n\nPasso a passo, determine se é seguro parar."
      }]
    }]
  }
}
```

### 6.3 Quando NÃO Usar Técnicas Avançadas em Hooks

- **Tree of Thoughts**: Excessivo para hooks — latência alta, custo alto
- **PAL**: Hooks command já são código; PAL é redundante
- **Few-shot CoT**: Hooks prompt devem ser concisos (timeout de 30s); exemplos longos são contra-producentes
- **Reflexion**: Hooks são stateless entre execuções; não há memória de tentativas anteriores

## 7. Correlações com Documentos Principais

### 7.1 research-llm-context-optimization.md

| Princípio de Contexto | Implementação via Hooks |
|----------------------|------------------------|
| Instruction budget (~150-200) | Hooks removem regras enforced do CLAUDE.md, liberando budget |
| Progressive disclosure | `InstructionsLoaded` rastreia carregamento lazy; `SessionStart` injeta contexto JIT |
| Context poisoning | Hooks impedem ações que poderiam poluir contexto (ex: bloquear tools desnecessários) |
| Lost-in-the-middle | Hooks com `additionalContext` injetam informação em posições privilegiadas |
| Compaction awareness | `PreCompact`/`PostCompact` permitem reagir à compactação |

### 7.2 Evaluating-AGENTS-paper.md

| Achado do Paper | Relação com Hooks |
|-----------------|-------------------|
| Arquivos gerados por LLM reduzem performance | Hooks enforcam regras sem adicionar texto ao contexto |
| "More testing" aumenta com config files | `Stop` hooks com agent type validam testes explicitamente |
| Instruções são seguidas — esse é o problema | Hooks enforcement é externo ao modelo, evitando o dilema |

### 7.3 claude-prompting-best-practices.md

| Best Practice | Aplicação em Hooks |
|---------------|-------------------|
| System prompts para constraints rígidos | Hooks implementam constraints como código, mais confiável que prompts |
| Structured output com JSON | Toda comunicação hook↔Claude usa JSON structured |
| Tool use patterns | `PreToolUse`/`PostToolUse` controlam exatamente o uso de ferramentas |

### 7.4 a-guide-to-agents.md / a-guide-to-claude.md

| Princípio do Guide | Hooks como Implementação |
|--------------------|----|
| Keep config minimal | Hooks permitem CLAUDE.md menor removendo enforcement rules |
| Progressive disclosure | Hook `InstructionsLoaded` monitora lazy loading |
| Don't auto-generate | Hooks são code, não generated text — sempre intencionais |

## 8. Framework de Decisão

### Árvore de Decisão: Hook vs Rule vs CLAUDE.md vs Skill

```
A instrução precisa ser SEMPRE seguida sem exceção?
├── SIM → Pode ser verificada programaticamente?
│   ├── SIM → Use HOOK (command type)
│   │   └── É uma regra simples (regex match)?
│   │       ├── SIM → PreToolUse/PermissionRequest com exit code
│   │       └── NÃO → PreToolUse/Stop com agent type
│   └── NÃO → Use RULE com linguagem forte ("MUST", "NEVER")
│       └── É scoped a um path específico?
│           ├── SIM → .claude/rules/ com paths: frontmatter
│           └── NÃO → CLAUDE.md principal
└── NÃO → É guidance contextual?
    ├── SIM → É específica de um workflow?
    │   ├── SIM → Use SKILL (SKILL.md)
    │   └── NÃO → Use RULE ou CLAUDE.md
    └── NÃO → Provavelmente não precisa ser documentada
```

### Matriz de Decisão Rápida

| Necessidade | Mecanismo | Exemplo |
|-------------|-----------|---------|
| Bloquear `rm -rf` | Hook command em `PreToolUse` | `block-rm.sh` |
| Rodar testes após edição | Hook async em `PostToolUse` | `run-tests-async.sh` |
| Garantir tipo commit conventional | Hook prompt em `PreToolUse[Bash]` | Prompt avaliando formato |
| Estilo de código preferido | Rule em `.claude/rules/` | `code-style.md` |
| Como rodar migrations | Skill | `db-migration/SKILL.md` |
| Arquitetura do projeto | CLAUDE.md | Seção de overview |
| Auto-aprovar `npm test` | Hook command em `PermissionRequest` | Script com `updatedPermissions` |

## 9. Recomendações Práticas

### 9.1 Padrões de Implementação Essenciais

**1. Guard Script Template (reutilizável):**

```bash
#!/bin/bash
# Template base para hooks command
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input // empty')
AGENT_TYPE=$(echo "$INPUT" | jq -r '.agent_type // empty')

# Sua lógica aqui
# exit 0 = permitir, exit 2 = bloquear (stderr), JSON stdout = controle fino
```

**2. Separação de Concerns por Configuração:**

- `~/.claude/settings.json` — Hooks de segurança global (block destructive commands)
- `.claude/settings.json` — Hooks de qualidade do projeto (lint, test, format)
- `.claude/settings.local.json` — Hooks pessoais (notificações, logging)
- Skill frontmatter — Hooks específicos de workflow

**3. Stop Hook com Proteção Anti-Loop:**

```bash
#!/bin/bash
INPUT=$(cat)
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active')
if [ "$STOP_HOOK_ACTIVE" = "true" ]; then
  exit 0  # Não entrar em loop
fi
# Verificações aqui
```

**4. Context Injection via SessionStart:**

```bash
#!/bin/bash
# Carregar contexto dinâmico no início da sessão
ISSUES=$(gh issue list --limit 5 --json title,number 2>/dev/null)
BRANCH=$(git branch --show-current 2>/dev/null)
LAST_COMMIT=$(git log --oneline -1 2>/dev/null)

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Current branch: $BRANCH\nLast commit: $LAST_COMMIT\nOpen issues: $ISSUES"
  }
}
EOF
```

### 9.2 Checklist de Implementação

- [ ] Hooks de segurança (PreToolUse para comandos destrutivos) como primeira prioridade
- [ ] Hooks de qualidade (PostToolUse async para testes) como segunda prioridade
- [ ] Stop hooks COM proteção `stop_hook_active` para evitar loops
- [ ] Usar `$CLAUDE_PROJECT_DIR` em paths de scripts
- [ ] Quotar todas as variáveis shell
- [ ] Testar com `claude --debug` para verificar matching e execução
- [ ] Verificar `/hooks` menu para confirmar configuração final
- [ ] Hooks prompt/agent apenas para os 8 eventos suportados
- [ ] Timeouts adequados: command (600s), prompt (30s), agent (60s), async (custom)
- [ ] Manter scripts hook versionados em `.claude/hooks/` com permissão executável

### 9.3 Anti-Padrões a Evitar

| Anti-Padrão | Problema | Solução |
|-------------|----------|---------|
| Hook síncrono para testes longos | Bloqueia Claude por minutos | Usar `"async": true` |
| Stop hook sem check de `stop_hook_active` | Loop infinito | Sempre verificar o campo |
| Hooks HTTP para segurança crítica | Non-2xx não bloqueia | Usar command hooks para segurança |
| Hooks agent para validações simples | Latência e custo desnecessários | Command hook com jq é suficiente |
| Mesmo hook em user + project settings | Deduplicação por string exata apenas | Consolidar em um local |
| Hooks que imprimem para stdout além do JSON | Interfere com parsing JSON | Redirecionar debug para stderr |
