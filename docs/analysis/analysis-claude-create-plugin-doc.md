# Analise: Criacao de Plugins para o Claude Code

---

## 1. Resumo Executivo

O documento "Create Plugins" e o guia oficial da Anthropic para criacao de extensoes customizadas do Claude Code. Plugins sao pacotes distribuiveis que agrupam skills, agents, hooks, MCP servers, LSP servers e settings em uma unica unidade com namespace, versionamento e metadata. A distincao fundamental em relacao a configuracao standalone (`.claude/`) e a distribuibilidade: plugins podem ser compartilhados via marketplaces, instalados com `/plugin install`, e versionados com semantic versioning.

A arquitetura de plugins e baseada em um manifesto (`plugin.json` dentro de `.claude-plugin/`), com componentes organizados em diretorios no root do plugin: `commands/`, `agents/`, `skills/`, `hooks/`, `.mcp.json`, `.lsp.json`, e `settings.json`. O namespacing e obrigatorio -- skills de plugins sao acessadas como `/plugin-name:skill-name`, prevenindo conflitos entre plugins. O campo `settings.json` no root do plugin pode ativar um agent customizado como main thread, mudando fundamentalmente como o Claude Code se comporta quando o plugin esta habilitado.

A Anthropic recomenda comecar com configuracao standalone em `.claude/` para iteracao rapida e converter para plugin quando pronto para compartilhar. O teste local via `--plugin-dir` permite desenvolvimento sem instalacao, e `/reload-plugins` atualiza componentes sem reiniciar. A conversao de configuracao existente para plugin e um processo estruturado de migrar arquivos de `.claude/` para a estrutura do plugin.

---

## 2. Conceitos e Mecanismos Chave

### 2.1 Standalone vs Plugin

| Aspecto | Standalone (`.claude/`) | Plugin |
|---------|------------------------|--------|
| Nomes de skill | `/hello` | `/plugin-name:hello` |
| Melhor para | Pessoal, projeto-especifico, experimentacao | Compartilhamento, distribuicao, reutilizacao |
| Versionamento | Manual | Semantic versioning no manifest |
| Instalacao | Copiar arquivos | `/plugin install` |
| Conflitos de nome | Possivel com multiplos projetos | Prevenido por namespacing |

### 2.2 Estrutura do Plugin

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Manifesto (APENAS plugin.json aqui)
├── commands/                  # Skills como Markdown (invocaveis pelo usuario)
├── agents/                    # Definicoes de agentes customizados
├── skills/                    # Agent Skills com SKILL.md
│   └── code-review/
│       └── SKILL.md
├── hooks/
│   └── hooks.json             # Event handlers
├── .mcp.json                  # Configuracoes de MCP servers
├── .lsp.json                  # Configuracoes de LSP servers
└── settings.json              # Settings default do plugin
```

**ALERTA CRITICO**: NAO colocar `commands/`, `agents/`, `skills/` ou `hooks/` dentro de `.claude-plugin/`. Apenas `plugin.json` vai dentro de `.claude-plugin/`. Todos os outros diretorios ficam no root do plugin.

### 2.3 Manifesto do Plugin

```json
{
  "name": "my-plugin",
  "description": "A greeting plugin to learn the basics",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

| Campo | Proposito |
|-------|-----------|
| `name` | Identificador unico e namespace de skills |
| `description` | Exibido no plugin manager |
| `version` | Semantic versioning para releases |
| `author` | Atribuicao (opcional) |

Campos adicionais: `homepage`, `repository`, `license`.

### 2.4 Skills em Plugins

```yaml
---
name: code-review
description: Reviews code for best practices and potential issues.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

Skills em plugins possuem frontmatter com `name` e `description`, seguido de instrucoes. O Claude as invoca automaticamente baseado na descricao ou o usuario via `/plugin-name:skill-name`.

### 2.5 LSP Servers em Plugins

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

Fornece code intelligence em tempo real. Usuarios precisam ter o binario do language server instalado.

### 2.6 Settings Default do Plugin

```json
{
  "agent": "security-reviewer"
}
```

O campo `agent` ativa um dos agentes customizados do plugin como main thread, aplicando seu system prompt, restricoes de ferramentas e modelo. Atualmente apenas o campo `agent` e suportado em `settings.json` de plugins.

### 2.7 Argumentos Dinamicos

O placeholder `$ARGUMENTS` captura texto apos o nome do skill:

```markdown
---
description: Greet the user with a personalized message
---
# Hello Skill
Greet the user named "$ARGUMENTS" warmly.
```

Invocacao: `/my-plugin:hello Alex`

### 2.8 Desenvolvimento e Teste

- **`--plugin-dir ./my-plugin`**: Carrega plugin localmente sem instalacao
- **`/reload-plugins`**: Atualiza componentes sem reiniciar a sessao
- **Multiplos plugins**: `claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two`
- **Override**: Plugin local com mesmo nome que marketplace plugin tem precedencia (exceto managed)
- **Validacao**: Verificar estrutura, testar cada componente individualmente

### 2.9 Migracao de Standalone para Plugin

```bash
# 1. Criar estrutura
mkdir -p my-plugin/.claude-plugin

# 2. Criar manifesto
echo '{"name":"my-plugin","description":"Migrated","version":"1.0.0"}' > my-plugin/.claude-plugin/plugin.json

# 3. Copiar componentes
cp -r .claude/commands my-plugin/
cp -r .claude/agents my-plugin/
cp -r .claude/skills my-plugin/

# 4. Migrar hooks (de settings.json para hooks/hooks.json)
mkdir my-plugin/hooks
# Copiar objeto "hooks" do settings.json para hooks/hooks.json

# 5. Testar
claude --plugin-dir ./my-plugin
```

---

## 3. Pontos de Atencao

### 3.1 Erro Comum de Estrutura

O erro mais documentado: colocar diretorios de componentes dentro de `.claude-plugin/`. A documentacao enfatiza com um warning explicito:

> "Don't put `commands/`, `agents/`, `skills/`, or `hooks/` inside the `.claude-plugin/` directory."

### 3.2 Restricoes de Seguranca em Agentes de Plugin

Agentes definidos em plugins NAO suportam:

- `hooks` (sem lifecycle hooks)
- `mcpServers` (sem definicoes de MCP server)
- `permissionMode` (sem override de permissoes)

Esses campos sao silenciosamente ignorados. Para usa-los, copie o agente para `.claude/agents/` ou `~/.claude/agents/`.

### 3.3 Namespacing Obrigatorio

Skills de plugins SEMPRE sao prefixadas: `/plugin-name:skill-name`. Nao e possivel ter skills de plugin com nomes curtos como `/deploy`. Para nomes curtos, use configuracao standalone.

### 3.4 Custo de Contexto de Skills

Descricoes de skills consomem ~2% da janela de contexto. Plugins com muitas skills podem acumular custo significativo. Monitorar via `/context`.

### 3.5 Settings Limitados

Atualmente apenas `agent` e suportado no `settings.json` do plugin. Chaves desconhecidas sao silenciosamente ignoradas.

### 3.6 Managed Plugins NAO Podem Ser Overridden

Marketplace plugins force-enabled por managed settings NAO podem ser overridden pelo `--plugin-dir` local.

### 3.7 Dependencia de Binarios para LSP

Plugins com `.lsp.json` requerem que o usuario tenha o binario do language server instalado. Nao ha mecanismo de instalacao automatica.

---

## 4. Casos de Uso e Escopo

### 4.1 Quando Usar Plugins

| Cenario | Recomendacao |
|---------|-------------|
| Compartilhar skills/agents com o time | Plugin (versionavel, instalavel) |
| Distribuir para a comunidade | Plugin (marketplace) |
| Mesmas skills em multiplos projetos | Plugin (instala uma vez, usa em todos) |
| Iteracao rapida pessoal | Standalone primeiro, plugin depois |
| Skills com nomes curtos | Standalone (sem namespace) |
| Experimentacao com hooks | Standalone (sem restricoes de seguranca) |

### 4.2 Tipos de Plugin por Funcionalidade

| Tipo | Componentes Principais | Exemplo |
|------|----------------------|---------|
| **Code quality** | agents (reviewer), hooks (PostToolUse linter), skills | Plugin de review com code-reviewer agent |
| **Language support** | LSP server, agents (language-reviewer), rules | Plugin de TypeScript com gopls LSP |
| **Workflow automation** | skills, hooks, agents | Plugin de deploy com skill + validacao |
| **Domain knowledge** | skills (reference material), agents | Plugin de API conventions |
| **Testing** | agents (tester), hooks (PreToolUse validation) | Plugin de TDD com test-runner agent |

### 4.3 Fluxo de Desenvolvimento Recomendado

```
1. Prototipar em .claude/ (standalone)
   -> Iterar rapidamente, testar, refinar

2. Converter para plugin quando estavel
   -> Criar manifesto, copiar componentes, migrar hooks

3. Testar localmente com --plugin-dir
   -> Verificar cada componente, /reload-plugins

4. Versionar e documentar
   -> Semantic versioning, README.md

5. Distribuir
   -> Marketplace ou repositorio git
```

---

## 5. Aplicabilidade a Infraestrutura de Agentes

### 5.1 Skills

- **Skills como componente central**: Plugins permitem empacotar e distribuir skills reutilizaveis com namespace
- **Agent Skills vs Commands**: `skills/` contem SKILL.md com frontmatter (model-invoked); `commands/` contem Markdown simples (user-invoked)
- **$ARGUMENTS para parametrizacao**: Placeholder captura input dinamico do usuario
- **Progressive disclosure mantido**: Descricoes no startup, conteudo carregado sob demanda, mesmo em plugins
- **Frontmatter de skills em plugins**: Suporta `name`, `description`, `argument-hint`, `disable-model-invocation`, `context`, `agent`, `hooks`, `allowed-tools`, `model`, `effort`
- **Injecao dinamica**: `` !`command` `` funciona normalmente em skills de plugins

### 5.2 Hooks

- **`hooks/hooks.json` no plugin**: Formato identico ao de `settings.json`, com array de hooks por evento
- **Todos os eventos suportados**: `PreToolUse`, `PostToolUse`, `Stop`, etc.
- **JSON on stdin**: Comandos de hooks recebem input como JSON; `jq` para extração
- **Restricao em agentes de plugin**: Agentes definidos em plugins NAO podem ter hooks no frontmatter
- **Hooks no root do plugin**: `hooks/hooks.json` funciona normalmente (a restricao e apenas no frontmatter de agentes)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }]
      }
    ]
  }
}
```

### 5.3 Subagentes

- **Agentes em plugins**: Definidos em `agents/` no root do plugin, aparecem como `<plugin-name>:<agent-name>`
- **Invocacao**: `claude --agent <plugin-name>:<agent-name>` ou @-mention
- **Restricoes de seguranca**: Sem `hooks`, `mcpServers`, `permissionMode` em agentes de plugin
- **Campos suportados**: `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `isolation`
- **Settings.json do plugin**: Campo `agent` ativa um agente como main thread -- muda comportamento default do Claude Code
- **Precedencia**: `settings.json` do plugin tem prioridade sobre `settings` em `plugin.json`

### 5.4 Rules

- **Rules em plugins**: Nao ha diretorio `rules/` explicitamente documentado na estrutura de plugins
- **CLAUDE.md de plugins**: Nao documentado diretamente, mas plugins carregam contexto do projeto normalmente
- **Path-scoped rules**: Devem ser mantidas no projeto (`.claude/rules/`), nao no plugin
- **Settings como rules**: `settings.json` do plugin pode influenciar comportamento via campo `agent`
- **Alternativa**: Skills de plugins servem como meio de injetar instrucoes contextuais

### 5.5 Memoria

- **Agentes de plugin com memoria**: Campo `memory` suportado (user, project, local)
- **Memoria compartilhada**: Agentes de plugin podem usar `memory: project` para construir conhecimento versionavel
- **Auto memory**: Carregada normalmente em sessoes com plugins habilitados
- **CLAUDE.md do projeto**: Carregado junto com o plugin, fornecendo contexto persistente
- **Cross-plugin**: Nao ha mecanismo de memoria compartilhada entre plugins

---

## 6. Aplicabilidade do Guia de Engenharia de Prompts

### 6.1 CoT para Cadeias de Raciocinio de Subagentes

Skills de plugins podem incluir instrucoes de CoT no SKILL.md. Agentes de plugins podem ter CoT no system prompt (corpo do markdown). O CoT e particularmente valioso em skills complexas que requerem raciocinio multi-passo:

```yaml
---
name: architecture-review
description: Review architecture decisions for the project
context: fork
agent: general-purpose
---

## Process
Think step by step:
1. What is the current architecture?
2. What are the proposed changes?
3. What are the trade-offs?
4. What are the risks?
5. Recommendation with justification
```

### 6.2 ReAct para Subagentes com Acesso a Ferramentas

Agentes de plugins com acesso a ferramentas operam no loop ReAct. O system prompt deve encorajar o ciclo Pensamento -> Acao -> Observacao. Skills com `context: fork` e `agent: general-purpose` herdam ferramentas completas para ReAct.

### 6.3 Tree of Thoughts para Subagentes de Exploracao

Plugins podem incluir skills que spawnaam multiplos subagentes em paralelo (via `context: fork` com `agent: Explore`), cada um explorando um aspecto diferente. O plugin de code review poderia ter skills separadas para seguranca, performance e testes, invocaveis em paralelo.

### 6.4 Self-Consistency para Validacao entre Multiplos Subagentes

Plugins de review podem implementar Self-Consistency executando o mesmo agent de review multiplas vezes e comparando resultados. O hook `PostToolUse` pode acionar validacao cruzada.

### 6.5 Reflexion para Melhoria Iterativa de Subagentes

Agentes de plugin com `memory: project` implementam Reflexion cross-session:

- Agente aprende padroes em cada review
- Proxima invocacao consulta memoria
- Feedback incorporado incrementalmente

A combinacao agente + memoria + hooks cria um loop de melhoria continua.

### 6.6 Least-to-Most para Decomposicao de Tarefas entre Subagentes

Plugins podem definir workflows multi-passo com skills encadeadas:

1. Skill de exploracao (Explore agent)
2. Skill de planejamento (Plan agent)
3. Skill de implementacao (general-purpose agent)
4. Skill de validacao (review agent)

Cada skill pode ser invocada sequencialmente ou automaticamente pelo Claude baseado na descricao.

---

## 7. Correlacoes com os Documentos Principais

### Com "Creating Custom Subagents"

Plugins sao o mecanismo de distribuicao para subagentes. Agentes em `.claude/agents/` podem ser empacotados em plugins para compartilhamento. A restricao de seguranca (sem hooks/mcpServers/permissionMode em agentes de plugin) e documentada em ambos. O `settings.json` do plugin com campo `agent` e uma forma de tornar um subagente o default da sessao.

### Com "Orchestrate Teams of Claude Code Sessions"

Nao ha integracao direta documentada entre plugins e agent teams. Plugins sao carregados normalmente por cada teammate, e skills de plugins podem ser invocadas em contexto de teams. A principal conexao e que plugins podem fornecer hooks `TeammateIdle`/`TaskCompleted` via `hooks/hooks.json`.

### Com "How Claude Remembers a Project"

Plugins interagem com o sistema de memoria de duas formas:

1. Agentes de plugin podem ter `memory` field (user/project/local)
2. CLAUDE.md do projeto e carregado junto com o plugin

A filosofia de progressive disclosure se mantem: descricoes de skills de plugins no startup, conteudo completo on-demand.

### Com "Research: Subagent Best Practices"

A secao 16 do research (Plugin-Shipped Agents) documenta:

- Estrutura de diretorio para agentes em plugins
- Campos suportados vs restricoes de seguranca
- Naming convention `<plugin-name>:<agent-name>`

O research complementa a doc de plugins com exemplos da comunidade e anti-patterns aplicaveis a plugins.

### Com "Research: LLM Context Optimization"

Plugins implementam progressive disclosure (skills description no startup, conteudo on-demand). O custo de ~2% de contexto por skill description acumula com multiplos plugins. A estrategia "hybrid pre-loaded + on-demand" e mantida em plugins. O principio de "quality over quantity" aplica-se a quantidade de skills/agents registrados por plugin.

---

## 8. Forcas e Limitacoes

### Forcas

1. **Distribuibilidade**: Marketplaces, `/plugin install`, semantic versioning
2. **Namespacing**: Previne conflitos entre plugins
3. **Composicao rica**: Skills + agents + hooks + MCP + LSP + settings em um pacote
4. **Teste local**: `--plugin-dir` + `/reload-plugins` para desenvolvimento rapido
5. **Migracao facil**: Processo estruturado de standalone para plugin
6. **Settings default**: Campo `agent` pode transformar comportamento do Claude Code
7. **Override local**: Plugin local tem precedencia sobre marketplace (exceto managed)
8. **Multiplos plugins**: `--plugin-dir` aceita multiplos plugins simultaneamente

### Limitacoes

1. **Restricoes de seguranca em agentes**: Sem hooks, mcpServers, permissionMode
2. **Settings limitados**: Apenas campo `agent` suportado em settings.json de plugins
3. **Namespacing obrigatorio**: Skills sempre prefixadas (nao possivel ter `/deploy` via plugin)
4. **Dependencia de binarios LSP**: Sem instalacao automatica
5. **Sem rules nativo**: Nao ha diretorio `rules/` na estrutura de plugins
6. **Custo de contexto acumulado**: Muitos plugins = muitas descricoes de skills = orcamento consumido
7. **Managed plugins imutaveis**: Force-enabled pelo IT nao podem ser overridden localmente
8. **Sem memoria cross-plugin**: Nao ha compartilhamento de memoria entre plugins

---

## 9. Recomendacoes Praticas

### 9.1 Template de Plugin Minimo

```bash
mkdir -p my-plugin/.claude-plugin my-plugin/skills/main my-plugin/agents

# Manifesto
cat > my-plugin/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "description": "Description of what this plugin does",
  "version": "1.0.0",
  "author": { "name": "Your Name" }
}
EOF

# Skill principal
cat > my-plugin/skills/main/SKILL.md << 'EOF'
---
name: main
description: Primary skill of the plugin. Use when [trigger].
---

Instructions for the skill...
EOF

# Agente principal
cat > my-plugin/agents/reviewer.md << 'EOF'
---
name: reviewer
description: Review specialist. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
memory: project
---

You are a reviewer specializing in [domain]...
EOF
```

### 9.2 Padrao de Plugin de Code Quality

```
quality-plugin/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── code-reviewer.md      # Review agent (read-only)
│   ├── security-reviewer.md   # Security specialist
│   └── performance-reviewer.md # Performance analyst
├── skills/
│   └── full-review/
│       └── SKILL.md           # Spawna os 3 reviewers em paralelo
├── hooks/
│   └── hooks.json             # PostToolUse: lint after edits
└── settings.json              # Default agent: code-reviewer
```

### 9.3 Checklist de Publicacao

```
[ ] plugin.json com name, description, version, author
[ ] Estrutura correta (nada dentro de .claude-plugin/ exceto plugin.json)
[ ] Todas as skills testadas via /reload-plugins
[ ] Agentes testados via /agents
[ ] Hooks testados via operacoes reais
[ ] README.md com instalacao e uso
[ ] Semantic versioning aplicado
[ ] Testado com --plugin-dir em projeto limpo
[ ] Verificado via /context que custo de skills e aceitavel
```

### 9.4 Estrategia de Migracao Gradual

1. **Semana 1**: Prototipar em `.claude/` -- skills, agents, hooks individuais
2. **Semana 2**: Testar com o time via `.claude/` commitado no VCS
3. **Semana 3**: Converter para plugin, testar com `--plugin-dir`
4. **Semana 4**: Publicar no marketplace ou repo git da equipe

### 9.5 Otimizacao de Custo de Contexto

Para plugins com muitas skills:

1. Usar `disable-model-invocation: true` em skills raramente usadas pelo modelo
2. Consolidar skills semelhantes em uma unica skill com `$ARGUMENTS`
3. Monitorar orcamento via `/context`
4. Preferir menos skills mais poderosas a muitas skills especificas
5. Usar descricoes concisas (cada descricao consome tokens no startup)
