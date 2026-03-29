# Analise: Automate Workflows with Hooks

**Documento fonte**: `docs/hooks/automate-workflow-with-hooks.md`
**Data da analise**: Março 2026
**Escopo**: Guia pratico de automação de workflows via hooks no Claude Code

---

## 1. Sumario Executivo

O documento "Automate Workflows with Hooks" serve como guia introdutorio e pratico para o sistema de hooks do Claude Code. Diferentemente do documento de referencia tecnica, este foca em **casos de uso concretos e configurações prontas para copiar**, cobrindo desde notificações de desktop ate auto-formatação de codigo e proteção de arquivos sensíveis. O documento posiciona hooks como a camada de **controle deterministico** sobre o comportamento do Claude Code — garantindo que certas ações sempre aconteçam, independentemente do julgamento do LLM.

O guia introduz quatro tipos de hooks (`command`, `http`, `prompt`, `agent`) e 22 eventos de ciclo de vida, mas concentra a maioria dos exemplos em `command` hooks por serem os mais acessíveis. A abordagem é progressiva: começa com um hook trivial de notificação, avança para formatação automatica e proteção de arquivos, e termina com hooks baseados em LLM para decisões que exigem julgamento. Esta progressão espelha a estrategia de divulgação progressiva documentada na pesquisa de otimização de contexto.

O valor central do documento para infraestrutura de agentes esta na demonstração de que **instruções comportamentais podem ser convertidas em hooks deterministicos**, removendo-as do orçamento de atenção do LLM enquanto garantem enforcement absoluto. Isto conecta diretamente com os princípios de context engineering da Anthropic sobre manter o menor conjunto possível de tokens de alto sinal.

---

## 2. Conceitos e Mecanismos Chave

### 2.1 Tipos de Hook

| Tipo | Mecanismo | Caso de Uso | Complexidade |
|------|-----------|-------------|--------------|
| `command` | Executa comando shell | Formatação, validação, notificação | Baixa |
| `http` | POST para endpoint HTTP | Auditoria centralizada, serviços externos | Media |
| `prompt` | Avaliação LLM single-turn | Decisões que exigem julgamento | Media |
| `agent` | Subagente com acesso a ferramentas | Verificação complexa contra o codebase | Alta |

### 2.2 Ciclo de Vida dos Eventos

O documento apresenta 22 eventos organizados temporalmente:

**Eventos de sessão:**

- `SessionStart` — inicio/retomada de sessão (matcher: `startup`, `resume`, `clear`, `compact`)
- `SessionEnd` — termino de sessão (matcher: `clear`, `resume`, `logout`, etc.)

**Eventos do loop agentico:**

- `UserPromptSubmit` — antes do Claude processar o prompt
- `PreToolUse` — antes da execução de ferramenta (pode bloquear)
- `PermissionRequest` — quando dialogo de permissão aparece
- `PostToolUse` — apos ferramenta executar com sucesso
- `PostToolUseFailure` — apos falha de ferramenta

**Eventos de subagentes:**

- `SubagentStart` / `SubagentStop` — spawn e termino de subagentes

**Eventos de compactação:**

- `PreCompact` / `PostCompact` — antes e apos compactação

**Eventos de controle:**

- `Stop` / `StopFailure` — quando Claude termina resposta
- `TaskCompleted` — quando tarefa é marcada como completa
- `TeammateIdle` — quando membro de equipe vai ficar idle

**Eventos de configuração:**

- `ConfigChange` — quando arquivo de configuração muda
- `InstructionsLoaded` — quando CLAUDE.md ou rules são carregados

**Eventos de worktree:**

- `WorktreeCreate` / `WorktreeRemove` — criação e remoção de worktrees

**Eventos MCP:**

- `Elicitation` / `ElicitationResult` — input de servidor MCP

### 2.3 Comunicação Hook ↔ Claude Code

```
┌──────────────┐     stdin (JSON)      ┌──────────────┐
│  Claude Code │ ─────────────────────> │  Hook Script │
│              │                        │              │
│              │ <───────────────────── │              │
│              │  stdout (JSON/texto)   │              │
│              │  stderr (mensagens)    │              │
│              │  exit code (0/2/N)     │              │
└──────────────┘                        └──────────────┘
```

**Exit codes:**

- `0` — ação prossegue; stdout é processado como JSON ou contexto
- `2` — ação bloqueada; stderr é feedback para Claude
- Qualquer outro — ação prossegue; stderr aparece em modo verbose

### 2.4 Matchers (Filtros)

Matchers são expressões regex que filtram quando hooks disparam. Cada evento filtra em campos diferentes:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "prettier --write ..." }
        ]
      }
    ]
  }
}
```

**Campos de filtragem por evento:**

- Tool events (`PreToolUse`, `PostToolUse`, etc.) → `tool_name`
- `SessionStart` → `source` (startup, resume, clear, compact)
- `SessionEnd` → `reason`
- `Notification` → `notification_type`
- `ConfigChange` → configuration source
- `SubagentStart`/`SubagentStop` → agent type

### 2.5 Escopo de Configuração

| Localização | Escopo | Compartilhavel |
|-------------|--------|----------------|
| `~/.claude/settings.json` | Todos os projetos | Nao (local) |
| `.claude/settings.json` | Projeto unico | Sim (commit) |
| `.claude/settings.local.json` | Projeto unico | Nao (gitignored) |
| Managed policy settings | Organizacional | Sim (admin) |
| Plugin `hooks/hooks.json` | Quando plugin ativo | Sim (bundled) |
| Skill/Agent frontmatter | Enquanto componente ativo | Sim (definido no arquivo) |

---

## 3. Pontos de Atenção

### 3.1 Armadilhas Comuns

**Loop infinito no Stop hook:**
O erro mais critico documentado. Se um Stop hook bloqueia Claude de parar sem verificar se ja esta em continuação, cria um loop infinito. A solução é verificar `stop_hook_active`:

```bash
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # Permite Claude parar
fi
# ... resto da logica
```

**JSON invalido por echo no shell profile:**
Quando `~/.zshrc` ou `~/.bashrc` contem `echo` incondicional, a saida contamina o stdout do hook:

```text
Shell ready on arm64        ← texto do profile
{"decision": "block"}       ← JSON do hook
```

Solução:

```bash
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

**Matcher case-sensitive:**
Matchers são regex case-sensitive. `"bash"` nao corresponde a `"Bash"`.

**PermissionRequest nao dispara em modo headless:**
Hooks `PermissionRequest` nao funcionam com `-p` (modo nao-interativo). Use `PreToolUse` como alternativa.

**PostToolUse nao pode desfazer:**
A ferramenta ja executou. O hook so pode fornecer feedback, nao reverter a ação.

### 3.2 Considerações de Segurança

- Hooks de comando executam com **permissões completas do usuario do sistema**
- Sempre validar e sanitizar inputs JSON do stdin
- Sempre usar aspas em variaveis shell (`"$VAR"` e nao `$VAR`)
- Verificar path traversal (`..` em caminhos de arquivo)
- Usar caminhos absolutos (`$CLAUDE_PROJECT_DIR`)
- Evitar processar arquivos sensiveis (`.env`, `.git/`, chaves)

### 3.3 Ordem de Execução

- Todos os hooks que correspondem a um evento rodam **em paralelo**
- Hooks identicos (mesmo comando) são **deduplicados automaticamente**
- Timeout padrao: 10 minutos (configuravel por hook)
- Hooks async nao bloqueiam execução e nao podem controlar comportamento

### 3.4 Prioridade de Deny Rules

Retornar `"allow"` em um `PreToolUse` hook **nao sobrescreve** deny rules de permissão. Regras de negação, incluindo managed settings, sempre tem prioridade sobre aprovações de hooks.

---

## 4. Casos de Uso e Escopo

### 4.1 Quando Hooks São a Ferramenta Certa

| Cenario | Hook | Rule | CLAUDE.md | Skill |
|---------|------|------|-----------|-------|
| Formatar codigo apos edição | **Hook** (determinismo) | - | - | - |
| Bloquear edição de .env | **Hook** (enforcement) | - | - | - |
| Notificar quando aguardando input | **Hook** (side-effect) | - | - | - |
| Estilo de codigo preferido | - | - | **CLAUDE.md** | - |
| Padrão de API a seguir | - | **Rule** | - | - |
| Deploy complexo | - | - | - | **Skill** |
| Verificar testes antes de parar | **Hook** (gate) | - | - | - |
| Reinjetar contexto apos compactação | **Hook** (lifecycle) | - | - | - |
| Auditoria de mudanças de config | **Hook** (observabilidade) | - | - | - |

### 4.2 Padrões Primarios Documentados

**1. Notificação (side-effect puro):**

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Precisa de atenção'"
          }
        ]
      }
    ]
  }
}
```

**2. Auto-formatação (pos-processamento):**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

**3. Proteção de arquivos (pre-validação com bloqueio):**
Script separado que verifica padrões protegidos e sai com codigo 2 para bloquear.

**4. Reinjeção de contexto apos compactação:**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Lembrete: use Bun, não npm. Execute bun test antes de commitar.'"
          }
        ]
      }
    ]
  }
}
```

**5. Auto-aprovação seletiva (controle de permissão):**

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"PermissionRequest\", \"decision\": {\"behavior\": \"allow\"}}}'"
          }
        ]
      }
    ]
  }
}
```

**6. Verificação baseada em LLM (Stop hook com prompt):**

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verifique se todas as tarefas estão completas."
          }
        ]
      }
    ]
  }
}
```

---

## 5. Aplicabilidade a Infraestrutura de Agentes

### 5.1 Skills

**Interação hooks ↔ skills:**

- Skills podem definir hooks no seu frontmatter YAML — hooks escopados ao ciclo de vida do skill
- `PostToolUse` hooks podem validar outputs de ferramentas usadas por skills
- `PreToolUse` hooks podem interceptar chamadas de ferramentas dentro de skills
- O campo `once: true` permite hooks de skill que executam apenas uma vez por sessão

**Padrão: Skill com hook de segurança integrado:**

```yaml
---
name: deploy-production
description: Deploy seguro para produção
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-deploy-command.sh"
---
```

**Hooks como alternativa a instruções em skills:**
Quando um skill tem regras de enforcement (ex: "nunca execute rm -rf"), converter essas regras em hooks `PreToolUse` remove-as do orçamento de atenção do skill e garante enforcement deterministico.

### 5.2 Hooks (Design Patterns)

**Padrão Guardião (Gate Pattern):**
Hooks `PreToolUse` e `Stop` que atuam como portões de qualidade — bloqueiam ações que nao atendem criterios.

```bash
#!/bin/bash
# gate-pattern: bloqueia commits sem testes passando
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0
fi
npm test 2>&1 > /dev/null
if [ $? -ne 0 ]; then
  echo '{"decision": "block", "reason": "Testes falhando. Corrija antes de finalizar."}'
fi
```

**Padrão Observador (Observer Pattern):**
Hooks `PostToolUse`, `Notification`, `SessionEnd` que registram eventos sem interferir no fluxo.

**Padrão Injetor de Contexto (Context Injection Pattern):**
Hooks `SessionStart` e `UserPromptSubmit` que adicionam informação ao contexto do Claude.

**Padrão Composto (Composition Pattern):**
Multiplos hooks no mesmo evento para diferentes preocupações:

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        { "type": "command", "command": "prettier --write ..." },
        { "type": "command", "command": "./lint-check.sh" }
      ]
    }
  ]
}
```

**Teste e Depuração:**

- `/hooks` para inspecionar configuração
- `Ctrl+O` (verbose mode) para ver saida de hooks no transcrito
- `claude --debug` para detalhes completos de execução
- Testar manualmente com `echo '{"tool_name":"Bash"}' | ./hook.sh; echo $?`

### 5.3 Subagentes

**Hooks em contexto de subagentes:**

- `SubagentStart` hooks podem injetar contexto adicional no subagente via `additionalContext`
- `SubagentStop` hooks podem impedir o subagente de parar (mesma semantica que `Stop`)
- Hooks de subagente definidos em frontmatter convertem `Stop` para `SubagentStop` automaticamente
- O campo `agent_id` no input distingue chamadas de subagente vs. thread principal

**Padrão: Injetar diretrizes de segurança em subagentes:**

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"SubagentStart\", \"additionalContext\": \"Siga diretrizes de segurança OWASP Top 10\"}}'"
          }
        ]
      }
    ]
  }
}
```

**Isolamento:**

- Hooks definidos em settings globais se aplicam a subagentes tambem
- Hooks definidos em frontmatter de agente são escopados ao ciclo de vida daquele agente
- `agent_type` no input permite filtrar hooks por tipo de subagente

### 5.4 Rules

**Hooks vs Rules — quando usar cada um:**

| Aspecto | Hooks | Rules (`.claude/rules/`) |
|---------|-------|--------------------------|
| Natureza | Deterministico, enforcement | Consultivo, orientação |
| Execução | Automatica, no lifecycle | Injetado no contexto |
| Impacto no contexto | Zero (executa externamente) | Consome orçamento de atenção |
| Flexibilidade | Binario (allow/block) | Nuanceado (julgamento) |
| Path-scoping | Via matcher regex | Via frontmatter `paths:` |
| Confiabilidade | 100% (se hook funciona) | Depende do LLM seguir |

**Padrão complementar:**
Rules definem o "por que" e a orientação; hooks enforcam o "o que" de forma deterministica.

Exemplo: Uma rule diz "Preferir rg sobre grep para melhor performance". Um hook `PreToolUse` intercepta chamadas Bash com `grep` e sugere `rg`:

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')
if echo "$COMMAND" | grep -q '^grep '; then
  echo '{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "Use rg ao inves de grep para melhor performance"}}'
fi
exit 0
```

### 5.5 Memory

**Hooks que gerenciam memoria:**

- `SessionStart` com matcher `compact` reinjeta contexto critico perdido durante compactação
- `PostCompact` pode salvar o `compact_summary` para persistencia externa
- `InstructionsLoaded` registra quando arquivos CLAUDE.md ou rules são carregados (auditoria)

**Hooks disparados por eventos de memoria:**

- `ConfigChange` com matcher `skills` detecta mudanças em arquivos de skill
- `InstructionsLoaded` com matcher `path_glob_match` detecta carregamento lazy de rules

**Padrão: Contexto critico resiliente a compactação:**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "cat .claude/critical-context.txt"
          }
        ]
      }
    ]
  }
}
```

O conteudo de `.claude/critical-context.txt` é adicionado automaticamente ao contexto do Claude apos cada compactação, eliminando a necessidade de manter essas informações no CLAUDE.md (que já é carregado via mecanismo proprio).

---

## 6. Aplicabilidade do Guia de Engenharia de Prompts

### 6.1 ReAct para Hooks Baseados em Agent

O padrão ReAct (Pensamento → Ação → Observação) é o loop central de hooks `type: "agent"`. O subagente spawned por um agent hook executa exatamente este ciclo:

1. **Pensamento**: analisa o prompt e contexto do hook
2. **Ação**: usa ferramentas (Read, Grep, Glob) para investigar
3. **Observação**: avalia resultados e retorna decisão `{ok: true/false}`

**Aplicação pratica**: Um hook agent que verifica se testes passam antes de permitir Claude parar usa ReAct internamente — lê arquivos de teste, executa o test suite, observa resultados, decide.

### 6.2 Prompt Chaining para Composição de Hooks

Hooks multiplos no mesmo evento implementam prompt chaining deterministico. A saida de cada hook não alimenta o proximo diretamente, mas o efeito cumulativo no Claude Code cria uma pipeline:

1. `PreToolUse` hook 1: valida segurança do comando → permite
2. `PreToolUse` hook 2: verifica patterns protegidos → permite
3. Ferramenta executa
4. `PostToolUse` hook 1: formata codigo
5. `PostToolUse` hook 2: executa linter

### 6.3 Constitutional AI para Stop Hooks

O padrão de Constitutional AI (critique → revise) se aplica diretamente a hooks `type: "prompt"` no evento `Stop`:

```json
{
  "type": "prompt",
  "prompt": "Avalie se Claude completou todas as tarefas solicitadas. Princípios: (1) Todas as funcionalidades foram implementadas (2) Testes foram escritos e passam (3) Nenhum erro pendente. Se algum principio nao foi atendido, responda {\"ok\": false, \"reason\": \"<explicação>\"}."
}
```

A "constituição" são os principios contra os quais o LLM avalia; a decisão `ok: false` com `reason` é a revisão que volta para o Claude principal.

### 6.4 Structured Output para Comunicação Hook ↔ Claude Code

Toda comunicação de hook é baseada em JSON estruturado. As recomendações do guia de engenharia de prompts se aplicam:

- Separar raciocinio de decisão (o hook raciocina internamente, retorna decisão estruturada)
- Usar campos bem definidos (`permissionDecision`, `reason`, `additionalContext`)
- Evitar misturar texto livre com JSON

### 6.5 Least-to-Most para Decomposição de Hooks Complexos

Hooks complexos devem ser decompostos em scripts menores e focados, cada um resolvendo um subproblema. Em vez de um mega-script que valida, formata e testa:

```
hooks/
├── validate-security.sh      # Subproblema 1
├── format-code.sh             # Subproblema 2
├── run-tests.sh               # Subproblema 3
└── check-protected-files.sh   # Subproblema 4
```

Cada script é simples, testavel e compostavel.

### 6.6 Role Prompting para Hooks Prompt/Agent

Em hooks `type: "prompt"` e `type: "agent"`, usar role prompting melhora a precisão da avaliação:

```json
{
  "type": "prompt",
  "prompt": "Voce é um revisor de codigo senior especializado em segurança. Avalie se o comando a seguir é seguro: $ARGUMENTS"
}
```

O papel especializado direciona a distribuição de probabilidades do modelo para decisões mais rigorosas e fundamentadas.

---

## 7. Correlações com Documentos Principais

### 7.1 Context Optimization (Otimização de Contexto)

**Conexão direta**: O documento de pesquisa de otimização de contexto afirma que "converter instruções comportamentais em hooks deterministicos remove-as do orçamento de contexto". O guia de hooks demonstra exatamente isso:

- Regra "sempre formate com Prettier" → hook `PostToolUse` com Prettier (0 tokens de contexto)
- Regra "nunca edite .env" → hook `PreToolUse` com exit 2 (0 tokens de contexto)

**Quantificação**: Cada regra convertida em hook economiza ~20-50 tokens no CLAUDE.md, que em um arquivo de 200 linhas (~3000 tokens) representa 0.7-1.7% do orçamento por regra.

### 7.2 Instruction Budget (Orçamento de Instruções)

**Conexão direta**: O principio de manter CLAUDE.md abaixo de 200 linhas é viabilizado por hooks. Regras de enforcement que antes consumiam linhas no CLAUDE.md agora vivem em hooks:

| Antes (CLAUDE.md) | Depois (Hook) | Economia |
|-------------------|---------------|----------|
| "NUNCA edite .env ou package-lock.json" | `PreToolUse` protect-files.sh | ~1 linha |
| "Sempre execute prettier apos editar" | `PostToolUse` prettier | ~1 linha |
| "Notifique quando aguardando input" | `Notification` notify-send | ~1 linha |
| "Sempre execute testes antes de commitar" | `Stop` hook com npm test | ~2 linhas |

### 7.3 Progressive Disclosure (Divulgação Progressiva)

**Conexão direta**: Hooks implementam divulgação progressiva temporal:

- `SessionStart` carrega contexto inicial
- `PreToolUse`/`PostToolUse` executam no momento exato da ação
- `InstructionsLoaded` reage ao carregamento lazy de regras
- `SessionStart` com matcher `compact` reinjeta contexto critico just-in-time

Diferente de CLAUDE.md (pre-carregado) e rules (carregadas por path), hooks operam em **pontos especificos do ciclo de vida** — a forma mais precisa de "just in time".

### 7.4 Context Poisoning (Envenenamento de Contexto)

**Conexão direta**: Hooks resolvem dois vetores de envenenamento identificados na pesquisa:

1. **Instruções desatualizadas**: Hooks executam logica programatica, nao dependem de o LLM "lembrar" a instrução
2. **Instruções contraditorias**: Hooks são deterministicos — nao ha ambiguidade sobre qual regra prevalece

O hook `SessionStart` com matcher `compact` resolve especificamente o problema de **perda de contexto critico durante compactação** — um vetor de envenenamento por omissão.

### 7.5 AGENTS Evaluation (Avaliação de Config de Agentes)

**Conexão direta**: O principio de que "arquivos de configuração funcionam melhor quando focam em orientação, nao enforcement" é implementado pela divisão hooks/rules:

- CLAUDE.md e rules: orientação, preferencias, convenções (advisory)
- Hooks: enforcement, validação, bloqueio (deterministic)

---

## 8. Framework de Decisão

### 8.1 Arvore de Decisão

```
A regra precisa ser seguida 100% das vezes?
├── SIM → A regra pode ser verificada programaticamente?
│   ├── SIM → Use um HOOK
│   │   ├── Precisa bloquear antes da ação? → PreToolUse hook
│   │   ├── Precisa processar apos a ação? → PostToolUse hook
│   │   ├── Precisa controlar quando Claude para? → Stop hook
│   │   └── Precisa reagir a eventos de ciclo de vida? → Evento apropriado
│   └── NÃO → Use um HOOK tipo prompt/agent (avaliação LLM)
├── NÃO, mas é importante → A regra é especifica a um caminho/area?
│   ├── SIM → Use uma RULE com paths: frontmatter
│   └── NÃO → A regra é universal para o projeto?
│       ├── SIM → Coloque no CLAUDE.md do projeto
│       └── NÃO → Coloque no CLAUDE.md do subdiretorio
└── É uma capacidade complexa com multiplos passos?
    └── SIM → Use um SKILL
```

### 8.2 Matriz de Decisão

| Criterio | Hook (command) | Hook (prompt/agent) | Rule | CLAUDE.md | Skill |
|----------|---------------|--------------------|----|-----------|-------|
| Enforcement 100% | Sim | ~95% | Nao | Nao | Nao |
| Zero custo de contexto | Sim | Nao (custo API) | Nao | Nao | Parcial |
| Julgamento necessario | Nao | Sim | Sim | Sim | Sim |
| Complexidade de setup | Media | Baixa | Baixa | Minima | Media-Alta |
| Auditavel | Sim (logs) | Sim (transcrito) | Nao | Nao | Nao |
| Compartilhavel via git | Sim (.claude/settings.json) | Sim | Sim | Sim | Sim |
| Escopo temporal | Ponto no lifecycle | Ponto no lifecycle | Sempre em contexto | Sempre em contexto | Sob demanda |

### 8.3 Regra de Ouro

> **Se a consequencia de violar a regra é severa (segurança, dados, compliance), use um hook.**
> **Se a consequencia é qualidade degradada mas aceitavel, use CLAUDE.md ou rules.**
> **Se a regra requer multiplos passos de execução, use um skill.**

---

## 9. Recomendações Praticas

### 9.1 Starter Kit para Projetos Novos

Configuração minima recomendada para `.claude/settings.json`:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Precisa de atenção'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null || true"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "cat \"$CLAUDE_PROJECT_DIR\"/.claude/critical-context.txt 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### 9.2 Script de Proteção de Arquivos Robusto

```bash
#!/bin/bash
# .claude/hooks/protect-files.sh
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

PROTECTED_PATTERNS=(
  ".env"
  ".env.local"
  ".env.production"
  "package-lock.json"
  "yarn.lock"
  "pnpm-lock.yaml"
  ".git/"
  "*.pem"
  "*.key"
  "credentials"
)

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Bloqueado: $FILE_PATH corresponde ao padrão protegido '$pattern'" >&2
    exit 2
  fi
done

exit 0
```

### 9.3 Stop Hook Seguro com Verificação de Testes

```bash
#!/bin/bash
# .claude/hooks/verify-before-stop.sh
INPUT=$(cat)

# Prevenir loop infinito
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0
fi

# Verificar se ha arquivos modificados que precisam de teste
MODIFIED=$(git diff --name-only 2>/dev/null | grep -E '\.(ts|js|py)$' | head -1)
if [ -z "$MODIFIED" ]; then
  exit 0  # Sem arquivos modificados, pode parar
fi

# Executar testes
if ! npm test 2>&1 > /dev/null; then
  echo '{"decision": "block", "reason": "Testes falhando. Corrija os testes antes de finalizar."}'
  exit 0
fi

exit 0
```

### 9.4 Auditoria Completa para Compliance

```json
{
  "hooks": {
    "ConfigChange": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -c '{timestamp: now | todate, event: \"config_change\", source: .source, file: .file_path}' >> ~/claude-audit.log"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -c '{timestamp: now | todate, event: \"bash_command\", command: .tool_input.command}' >> ~/claude-audit.log",
            "async": true
          }
        ]
      }
    ]
  }
}
```

### 9.5 Hook HTTP para Time Distribuido

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/tool-use",
            "headers": {
              "Authorization": "Bearer $AUDIT_TOKEN"
            },
            "allowedEnvVars": ["AUDIT_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

Para times que precisam de auditoria centralizada, um serviço HTTP local recebe todos os eventos de uso de ferramentas. O header `Authorization` usa interpolação de variavel de ambiente com `allowedEnvVars` para segurança.

### 9.6 Checklist de Implementação

1. Identificar regras de enforcement no CLAUDE.md que podem ser convertidas em hooks
2. Para cada regra, determinar o evento correto (Pre/PostToolUse, Stop, etc.)
3. Escrever o script de hook com tratamento adequado de JSON
4. Tornar o script executavel (`chmod +x`)
5. Testar manualmente com `echo '{...}' | ./hook.sh; echo $?`
6. Adicionar ao settings.json com matcher apropriado
7. Verificar com `/hooks` no Claude Code
8. Testar em cenario real e verificar com `Ctrl+O` (verbose mode)
9. Remover a regra correspondente do CLAUDE.md
10. Documentar o hook e seu proposito
