# Analise: Research Claude Code Skills & Plugin Marketplace Format

> Analise do documento de pesquisa sobre formatos de skills, plugins e marketplaces do Claude Code.
> **Documento fonte**: `docs/skills/research-claude-code-skills-format.md`
> **Data da analise**: 2026-03-27

---

## 1. Sumario Executivo

O documento "Research: Claude Code Skills & Plugin Marketplace Format" e uma pesquisa tecnica que mapeia o ecossistema completo de extensibilidade do Claude Code em tres camadas: Skills standalone (SKILL.md seguindo o padrao Agent Skills), Plugins (pacotes que agrupam skills + agents + hooks + MCP/LSP servers) e Marketplaces (catalogos de plugins distribuidores via repositorios GitHub). A pesquisa foi realizada em marco de 2026 com fontes oficiais da Anthropic, o padrao aberto Agent Skills e repositorios da comunidade.

A contribuicao mais significativa deste documento e a clarificacao do ecossistema de distribuicao: nao existe `npx skills add` -- a instalacao ocorre via `/plugin install` dentro do Claude Code ou `claude plugin install` na CLI. Isso corrige um equivoco comum e posiciona o sistema de plugins como o mecanismo canonico de distribuicao. O documento tambem mapeia a compatibilidade cross-agent do formato SKILL.md, demonstrando que o mesmo arquivo funciona em Claude Code (`.claude/skills/`), VS Code/GitHub Copilot (`.agents/skills/`) e OpenAI Codex.

A terceira contribuicao e a documentacao da distincao entre o Agent Skills Open Standard (campos minimos: `name` e `description`) e as extensoes proprietarias do Claude Code (`disable-model-invocation`, `context`, `agent`, `hooks`, `model`, `effort`). Esta distincao e critica para autores que desejam criar skills portaveis vs skills que exploram capacidades avancadas do Claude Code.

---

## 2. Conceitos e Mecanismos Chave

### 2.1 As Tres Camadas de Extensibilidade

O documento revela uma arquitetura em tres camadas que escala de simples a complexo:

```
Camada 1: Skill (SKILL.md)
  - Unidade atomica de extensao
  - Formato: diretorio com SKILL.md + arquivos de suporte
  - Invocacao: /skill-name

Camada 2: Plugin (diretorio com .claude-plugin/)
  - Pacote de distribuicao agrupando multiplos componentes
  - Contem: skills/ + agents/ + hooks/ + .mcp.json + .lsp.json
  - Invocacao: /plugin-name:skill-name
  - Manifesto: .claude-plugin/plugin.json

Camada 3: Marketplace (repositorio com marketplace.json)
  - Catalogo de plugins para descoberta e instalacao
  - Contem: .claude-plugin/marketplace.json + plugins/
  - Instalacao: /plugin install name@marketplace
```

### 2.2 Agent Skills Open Standard vs Claude Code Extensions

**Campos do padrao aberto (agentskills.io):**

| Campo | Obrigatorio | Limite |
|-------|-------------|--------|
| `name` | Sim* | 64 chars, kebab-case |
| `description` | Sim* | 1024 chars |
| `license` | Nao | - |
| `compatibility` | Nao | 500 chars |
| `metadata` | Nao | Key-value arbitrario |
| `allowed-tools` | Nao (experimental) | Lista separada por espacos |

*No Claude Code, ambos sao tecnicamente opcionais com fallbacks: `name` usa o nome do diretorio, `description` usa o primeiro paragrafo do conteudo.

**Extensoes proprietarias do Claude Code:**

| Campo | Funcao |
|-------|--------|
| `argument-hint` | Dica de autocomplete (ex: `[issue-number]`) |
| `disable-model-invocation` | Impede invocacao automatica pelo Claude |
| `user-invocable` | Esconde do menu `/` (background knowledge) |
| `model` | Override de modelo quando skill ativa |
| `effort` | Nivel de esforco: low, medium, high, max |
| `context` | `fork` para execucao em subagente isolado |
| `agent` | Tipo de subagente (Explore, Plan, general-purpose) |
| `hooks` | Hooks scoped ao lifecycle da skill |

**Implicacao para portabilidade**: Skills que usam apenas campos do padrao aberto funcionam em Claude Code, VS Code/Copilot e OpenAI Codex. Skills com extensoes Claude Code sao especificas da plataforma.

### 2.3 Regras de Validacao de Nomes

O documento detalha regras rigorosas de validacao:

- 1-64 caracteres
- Apenas lowercase `a-z`, numeros e hifens
- NAO pode iniciar ou terminar com `-`
- NAO pode conter `--` consecutivos
- DEVE corresponder ao nome do diretorio pai
- NAO pode conter palavras reservadas: "anthropic", "claude"
- NAO pode conter tags XML

### 2.4 Variaveis de Substituicao

| Variavel | Descricao | Exemplo de uso |
|----------|-----------|----------------|
| `$ARGUMENTS` | Todos os argumentos | `Analise $ARGUMENTS` |
| `$ARGUMENTS[N]` / `$N` | Argumento por indice | `Migre $0 de $1 para $2` |
| `${CLAUDE_SESSION_ID}` | ID da sessao | Logging, correlacao |
| `${CLAUDE_SKILL_DIR}` | Diretorio da skill | Scripts bundled |

### 2.5 Injecao Dinamica de Contexto

A sintaxe `` !`<command>` `` executa comandos shell ANTES do envio ao Claude:

```markdown
- Diff: !`gh pr diff`
- Comments: !`gh pr view --comments`
```

**Mecanismo**: Pre-processamento puro. O comando executa, o output substitui o placeholder, Claude recebe apenas o resultado final. Nao e execucao pelo Claude.

### 2.6 Estrutura de Plugin Completa

```
my-plugin/
  .claude-plugin/
    plugin.json          # Manifesto (opcional - auto-discovery funciona)
  skills/                # Skills (formato Agent Skills)
  agents/                # Definicoes de subagentes
  commands/              # Comandos legacy (markdown)
  hooks/
    hooks.json           # Configuracoes de hooks
  scripts/               # Scripts para hooks e utilidades
  settings.json          # Configuracoes default
  .mcp.json              # Servidores MCP
  .lsp.json              # Servidores LSP
```

**Campo minimo do plugin.json**: Apenas `name` e obrigatorio se o manifesto existir. O manifesto em si e opcional -- Claude Code auto-descobre componentes em locais default.

**Variaveis de ambiente para plugins:**

- `${CLAUDE_PLUGIN_ROOT}` -- Path absoluto do diretorio de instalacao (muda em updates)
- `${CLAUDE_PLUGIN_DATA}` -- Diretorio de dados persistentes que sobrevive updates

### 2.7 Formato marketplace.json

```json
{
  "name": "marketplace-name",
  "owner": { "name": "Org", "email": "team@org.com" },
  "metadata": { "description": "...", "version": "1.0.0" },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "...",
      "version": "1.0.0"
    }
  ]
}
```

**Tipos de source suportados:**

- Caminho relativo: `"./plugins/my-plugin"`
- GitHub repo: `{ "source": "github", "repo": "owner/repo" }`
- Git URL: `{ "source": "url", "url": "https://..." }`
- Git subdirectory: `{ "source": "git-subdir", "url": "...", "path": "tools/plugin" }`
- npm package: `{ "source": "npm", "package": "@acme/plugin" }`

**Strict mode:**

- `true` (default): `plugin.json` e autoridade; marketplace entry apenas complementa
- `false`: Marketplace entry e a definicao completa

### 2.8 Mecanismo de Instalacao

```bash
# Adicionar marketplace
/plugin marketplace add owner/repo

# Instalar plugin
/plugin install plugin-name@marketplace-name

# CLI nao-interativa
claude plugin install formatter@my-marketplace --scope project

# Escopos de instalacao
# user (default) - pessoal, todos os projetos
# project - compartilhado via .claude/settings.json
# local - gitignored, apenas para voce neste projeto
```

### 2.9 Progressive Disclosure Model

O documento formaliza o modelo de 3 niveis:

1. **Metadados** (~100 tokens): `name` + `description` -- carregados no startup para TODAS as skills
2. **Instrucoes** (<5000 tokens recomendados): Corpo do SKILL.md -- carregado quando skill ativa
3. **Recursos** (conforme necessidade): Scripts, referencias, assets -- carregados sob demanda

---

## 3. Pontos de Atencao

### 3.1 Erros Comuns e Confusoes

1. **Confusao `npx skills add`**: NAO EXISTE. A instalacao e via `/plugin install` ou `claude plugin install`. Ferramentas comunitarias como CCPI podem oferecer alternativas, mas nao sao oficiais.

2. **Confusao `skills.json`**: NAO EXISTE manifesto de skills. O "manifesto" e o proprio SKILL.md (frontmatter). Para plugins, o manifesto e `plugin.json`. Para marketplaces, `marketplace.json`.

3. **Portabilidade assumida**: Skills com campos Claude Code (`context`, `hooks`, `agent`) NAO funcionam em VS Code/Copilot ou OpenAI Codex. Apenas campos do padrao aberto sao portaveis.

4. **Nome vs diretorio**: O campo `name` DEVE corresponder ao nome do diretorio pai. Uma skill em `my-skill/SKILL.md` deve ter `name: my-skill`.

5. **Namespace de plugins**: Skills de plugins usam `plugin-name:skill-name`. Skills de projeto/pessoal NAO tem namespace -- conflitos sao resolvidos por prioridade (enterprise > personal > project).

### 3.2 Armadilhas de Contexto

- **Descricoes de skills consomem 2% da janela de contexto**: Com muitas skills, o orcamento de descricoes pode estourar silenciosamente
- **plugins.json strict mode**: No modo strict (default), inconsistencias entre plugin.json e marketplace.json podem causar comportamento inesperado
- **Auto-discovery em monorepo**: Claude auto-descobre `.claude/skills/` em subdiretorios quando editando arquivos la. Isso pode carregar skills inesperadas.

### 3.3 Lacunas Identificadas pelo Documento

O proprio documento identifica gaps importantes:

1. **Sem `npx skills add`**: O mecanismo de distribuicao standalone de skills (sem plugin wrapper) e limitado a copia manual
2. **Sem `skills.json`**: Nao ha manifesto de colecao de skills. Cada skill e auto-contida
3. **Padrao aberto minimo**: O Agent Skills Open Standard define apenas SKILL.md com name + description. Claude Code adiciona a maioria das funcionalidades
4. **Compatibilidade cross-agent limitada**: Embora o formato seja o mesmo, funcionalidades avancadas sao especificas de cada plataforma

---

## 4. Casos de Uso e Escopo

### 4.1 Decisao de Distribuicao

| Cenario | Mecanismo Recomendado |
|---------|----------------------|
| Skill pessoal para meu workflow | `~/.claude/skills/skill-name/SKILL.md` |
| Skill compartilhada com time | `.claude/skills/skill-name/SKILL.md` (commit) |
| Colecao de skills + hooks + MCP | Plugin com `.claude-plugin/plugin.json` |
| Distribuicao publica de multiplos plugins | Marketplace com `marketplace.json` |
| Skill cross-platform (Claude + Copilot) | Manter apenas campos do padrao aberto |
| Skill com funcionalidades avancadas Claude Code | Usar extensoes proprietarias (aceitar lock-in) |

### 4.2 Quando Criar Plugin vs Skill Standalone

**Skill standalone quando:**

- Funcionalidade unica e auto-contida
- Sem necessidade de hooks, MCP ou LSP
- Distribuicao por copia/git e suficiente
- Portabilidade cross-agent e desejada

**Plugin quando:**

- Multiplas skills relacionadas
- Necessidade de hooks integrados
- Necessidade de servidores MCP/LSP
- Distribuicao via marketplace desejada
- Configuracoes default necessarias (settings.json)
- Scripts utilitarios compartilhados entre skills

### 4.3 Quando Usar Marketplace vs Distribuicao Direta

**Marketplace quando:**

- Multiplos plugins para descoberta
- Equipe/organizacao com catalogo interno
- Versionamento e atualizacao automatica desejados
- Necessidade de categorias e tags para discovery

**Distribuicao direta (GitHub repo) quando:**

- Plugin unico
- Atualizacao manual e aceitavel
- Simplicidade e prioridade

---

## 5. Aplicabilidade a Infraestrutura de Agentes

### 5.1 Skills (Design Patterns para Portabilidade)

**Padrao 1: Skill portavel (padrao aberto puro)**

```yaml
---
name: code-review-checklist
description: Checklist de revisao de codigo. Usar quando revisando PRs, fazendo code review, ou analisando qualidade de codigo.
---

# Checklist de Code Review

## Corretude
- A logica esta correta para todos os edge cases?
- Inputs sao validados adequadamente?

## Performance
- Ha queries N+1?
- Loops desnecessarios?

## Seguranca
- Inputs sao sanitizados?
- Autorizacao esta verificada?
```

Esta skill funciona identicamente em Claude Code, VS Code/Copilot e OpenAI Codex.

**Padrao 2: Skill avancada (extensoes Claude Code)**

```yaml
---
name: security-scan
description: Varredura de seguranca automatizada do codebase
context: fork
agent: Explore
disable-model-invocation: true
allowed-tools: Read, Grep, Glob
effort: high
hooks:
  PostSkillExecution:
    - command: "echo 'Scan concluido em $(date)' >> security-scan.log"
---

# Varredura de Seguranca

1. Identifique todos os pontos de entrada (endpoints HTTP, handlers)
2. Para cada ponto, verifique:
   - Validacao de input
   - Autorizacao
   - Rate limiting
3. Gere relatorio priorizado por severidade
```

Esta skill explora todo o potencial do Claude Code mas nao funciona em outras plataformas.

**Estrategia de composicao cross-platform:**

```
my-skill/
  SKILL.md              # Instrucoes usando apenas padrao aberto
  .claude-extensions.md  # Extensoes Claude Code (referenciado apenas em SKILL.md
                         # com instrucoes condicionais)
```

### 5.2 Hooks (Integracao com Plugins)

O formato de plugin permite bundling de hooks junto com skills:

```json
// hooks/hooks.json
{
  "PreToolExecution": [
    {
      "matcher": "Bash",
      "hooks": [
        { "command": "python ${CLAUDE_PLUGIN_ROOT}/scripts/validate.py" }
      ]
    }
  ]
}
```

**Padroes de integracao hook-skill:**

1. **Hook pre-skill**: Validacao de pre-condicoes antes da execucao da skill
2. **Hook pos-skill**: Logging, notificacao ou limpeza apos execucao
3. **Hook que ativa skill**: Hook detecta evento e instrui invocacao de skill
4. **Skill que configura hooks**: Skill de setup que instala hooks no projeto

### 5.3 Subagentes (Composicao via Plugins)

Plugins permitem bundling de agents customizados:

```markdown
# agents/data-analyst.md
---
skills:
  - plugin-name:bigquery-skill
  - plugin-name:visualization-skill
allowed-tools: Read, Grep, Glob, Bash(bq *)
model: claude-sonnet-4-5-20250514
---

Voce e um analista de dados especializado.
Use as skills carregadas para responder queries sobre dados.
```

**Padroes de composicao subagente-plugin:**

| Padrao | Descricao | Caso de Uso |
|--------|-----------|-------------|
| Subagente com skills pre-carregadas | Agent .md com campo `skills` | Especialista com conhecimento de dominio |
| Skill com fork para subagente | SKILL.md com `context: fork` | Tarefa isolada com resultado focado |
| Plugin como unidade de deployment | Plugin agrupa agent + skills + hooks | Pacote completo para um dominio |

### 5.4 Rules (Complemento no Plugin)

Plugins podem incluir rules via `CLAUDE.md` no diretorio do plugin (carregado quando o plugin esta ativo). Isso permite:

- Rules especificas do dominio do plugin
- Convencoes que complementam skills do plugin
- Instrucoes de integracao com o projeto host

### 5.5 Memory (Plugins com Dados Persistentes)

A variavel `${CLAUDE_PLUGIN_DATA}` aponta para um diretorio persistente que sobrevive updates do plugin:

```
~/.claude/plugins/data/{plugin-id}/
```

Isso permite:

- Cache de resultados entre sessoes
- Configuracoes persistentes do usuario
- Historico de execucoes
- Estado compartilhado entre skills do mesmo plugin

**Template de skill que usa dados persistentes:**

```yaml
---
name: project-stats
description: Estatisticas do projeto com historico
---

## Coleta de estatisticas

1. Colete metricas atuais do projeto
2. Compare com historico em ${CLAUDE_PLUGIN_DATA}/stats-history.json
3. Gere relatorio de tendencias
4. Salve metricas atuais no historico
```

---

## 6. Aplicabilidade do Guia de Engenharia de Prompts

### 6.1 CoT para Workflows Multi-Step em Plugins

Plugins que agrupam multiplas skills se beneficiam de CoT explicito para orquestracao. O guia documenta que CoT melhora raciocinio multi-passo de 17,9% para 58,1%:

```yaml
---
name: full-audit
description: Auditoria completa do projeto (seguranca + performance + qualidade)
context: fork
---

Conduza a auditoria em cadeia de raciocinio:

1. **Raciocinio**: Qual aspecto devo analisar primeiro e por que?
2. **Seguranca**: Execute analise de seguranca (patterns OWASP)
3. **Raciocinio**: Dados os achados de seguranca, que impacto em performance espero?
4. **Performance**: Analise pontos de performance
5. **Raciocinio**: Quais problemas de qualidade podem causar os problemas ja encontrados?
6. **Qualidade**: Analise de qualidade de codigo
7. **Sintese**: Consolide achados com dependencias entre categorias
```

### 6.2 ReAct para Skills com Ferramentas em Plugin

O padrao ReAct e natural para skills de plugin que integram com ferramentas externas (MCP, Bash, etc.). O guia documenta +34% de taxa de sucesso:

```yaml
---
name: data-pipeline-debug
description: Debug de pipelines de dados
allowed-tools: Bash(bq *), Read, Grep
---

Siga o loop ReAct para debugar o pipeline:

Para cada iteracao:
1. **Pensamento**: Qual parte do pipeline suspeito? Que query BQ me daria evidencia?
2. **Acao**: Execute a query ou leia o arquivo relevante
3. **Observacao**: O que os dados me dizem sobre a causa raiz?

Continue ate identificar o ponto de falha com evidencia concreta.
```

### 6.3 Tree of Thoughts para Decisoes de Arquitetura de Plugin

Quando um plugin precisa tomar decisoes complexas sobre qual abordagem seguir:

```yaml
---
name: migration-planner
description: Planejar migracoes complexas de banco de dados
context: fork
effort: high
---

Para planejar a migracao de $ARGUMENTS:

1. **Gere 3 estrategias** de migracao:
   - Migracao incremental (zero downtime)
   - Migracao big-bang (downtime planejado)
   - Migracao dual-write (paralelo temporario)

2. **Avalie cada estrategia**:
   - Risco de perda de dados (1-5)
   - Complexidade de implementacao (1-5)
   - Tempo de downtime estimado
   - Rollback capability

3. **Descarte** estrategias com risco > 3
4. **Aprofunde** nas restantes com plano detalhado
5. **Recomende** com justificativa baseada nos trade-offs
```

### 6.4 Least-to-Most para Skills de Decomposicao em Plugin

Para plugins que decompoe tarefas grandes em subtarefas progressivamente mais complexas:

```yaml
---
name: codebase-modernization
description: Modernizacao incremental de codebase legado
---

Modernize $ARGUMENTS usando decomposicao progressiva:

1. **Identifique a mudanca mais simples**: Qual e a menor melhoria que agrega valor?
   (Ex: atualizar uma dependencia, remover um deprecation warning)
2. **Implemente e valide**
3. **Identifique a proxima mudanca**: Com base no que foi feito, qual e a proxima?
4. **Repita** ate que o escopo da modernizacao esteja completo
5. **Documente** cada mudanca com motivacao e impacto
```

### 6.5 Self-Consistency para Validacao Cross-Plugin

Para garantir consistencia entre skills de um mesmo plugin:

```yaml
---
name: validate-plugin-consistency
description: Valida consistencia entre todas as skills do plugin
context: fork
agent: Explore
---

Para cada skill no plugin:
1. **Leia** o SKILL.md completo
2. **Extraia** convencoes e padroes declarados

Depois:
3. **Compare** padroes entre skills (terminologia, formato, estilo)
4. **Identifique** inconsistencias
5. **Classifique**:
   - Presente em 2+ skills: PADRAO ESTABELECIDO
   - Presente em apenas 1: POSSIVEL INCONSISTENCIA
6. **Recomende** alinhamento para inconsistencias encontradas
```

### 6.6 Reflexion para Melhoria Iterativa de Plugins

Para skills de plugin que melhoram por iteracao:

```yaml
---
name: plugin-quality-check
description: Verificacao de qualidade do plugin com ciclo de melhoria
context: fork
---

Para cada componente do plugin:
1. **Avalie**: Qualidade, completude, consistencia
2. **Critique**: O que falta? O que esta redundante?
3. **Reflita**: Como posso melhorar com minimo esforco maximo impacto?
4. **Melhore**: Aplique as melhorias identificadas
5. **Re-avalie**: A nota melhorou? Se < 8/10, repita.
```

---

## 7. Correlacoes com Documentos Principais

### 7.1 Com extend-claude-with-skills.md

O documento de research complementa a documentacao oficial com:

| Aspecto | extend-claude-with-skills | research-skills-format |
|---------|---------------------------|----------------------|
| Formato SKILL.md | Documentacao de uso | Especificacao tecnica detalhada |
| Frontmatter | Campos e exemplos | Regras de validacao rigorosas |
| Distribuicao | Mencao a plugins e managed | Detalhamento completo de plugins e marketplaces |
| Cross-platform | Mencao ao Agent Skills standard | Comparacao detalhada Claude Code vs VS Code vs Codex |
| Instalacao | Nao detalhada | `/plugin install`, `claude plugin install`, escopos |

### 7.2 Com skill-authoring-best-practices.md

O research fornece o "o que" (formatos e estruturas) enquanto best practices fornece o "como" (qualidade e eficacia):

- **Research**: Estrutura de diretorio, campos de frontmatter, regras de validacao
- **Best practices**: Como escrever descricoes eficazes, progressive disclosure, workflows
- **Complementaridade**: Research para implementacao tecnica correta, best practices para eficacia de conteudo

### 7.3 Com research-llm-context-optimization.md

| Conceito de Otimizacao | Implementacao no Ecossistema de Skills |
|------------------------|----------------------------------------|
| Context rot | Progressive disclosure em 3 niveis evita sobrecarga |
| Attention budget | Orcamento de descricoes (2% janela contexto) gerencia budget |
| Just-in-time docs | Skills carregam sob demanda; plugins usam `${CLAUDE_PLUGIN_DATA}` para persistencia |
| Isolamento de contexto | `context: fork` + `agent` type = subagente com contexto isolado |
| Hierarquia de configuracao | Enterprise > Personal > Project > Plugin |
| Hooks como enforcement | Plugin bundling de hooks + skills garante enforcement deterministico |

### 7.4 Com prompt-engineering-guide.md

| Tecnica de Prompting | Aplicacao no Ecossistema |
|---------------------|--------------------------|
| Role prompting | Agent definitions em plugins (agents/*.md) |
| Few-shot | Exemplos em supporting files de skills |
| CoT | Workflows multi-step em SKILL.md |
| ReAct | Skills com `allowed-tools` e loop iterativo |
| Structured outputs | Comunicacao entre skills e subagentes via JSON |
| Prompt chaining | Plugins que orquestram multiplas skills em sequencia |
| RAG patterns | Skills com injecao dinamica (`` !`command` ``) como RAG em tempo real |

---

## 8. Forcas e Limitacoes

### 8.1 Forcas

1. **Ecossistema completo documentado**: O documento mapeia todas as camadas de extensibilidade (skills -> plugins -> marketplaces) com estruturas e schemas
2. **Cross-platform awareness**: Documenta compatibilidade e diferencas entre Claude Code, VS Code/Copilot e OpenAI Codex
3. **Regras de validacao explicitas**: Detalhamento de regras de validacao de nomes que nao estao obvias na documentacao oficial
4. **Exemplos reais**: Referencia a repositorios reais da comunidade (davepoon/buildwithclaude, jeremylongshore/claude-code-plugins-plus-skills, etc.)
5. **Correcao de equivocos**: Clarifica que `npx skills add` nao existe, que nao ha `skills.json`, e que o padrao aberto e minimo
6. **Multiplos tipos de source**: Documenta todas as formas de referenciar plugins (relativo, GitHub, Git URL, Git subdir, npm)
7. **Strict mode explicado**: Clarifica o comportamento de strict mode no marketplace e suas implicacoes

### 8.2 Limitacoes

1. **Ponto no tempo**: Pesquisa de marco 2026 -- o ecossistema de plugins esta evoluindo rapidamente e partes podem ficar desatualizadas
2. **Sem benchmarks de performance**: Nao ha dados sobre impacto de performance de plugins vs skills standalone
3. **Sem guia de migracao**: Nao ha instrucoes para migrar de commands/ para skills/ ou de skills standalone para plugins
4. **Lacuna de marketplace privado**: Documentacao de marketplaces foca em repositorios publicos; marketplaces corporativos internos tem menos cobertura
5. **Sem analise de seguranca**: Nao discute implicacoes de seguranca de instalar plugins de terceiros (execucao de scripts, acesso a ferramentas)
6. **Comunidade vs oficial**: Alguns repositorios listados sao comunitarios e podem nao seguir as melhores praticas
7. **Validacao limitada**: O comando `/plugin validate` e mencionado mas nao detalhado em termos de o que exatamente valida

---

## 9. Recomendacoes Praticas

### 9.1 Para Autores de Skills

1. **Decida a portabilidade primeiro**: Se a skill deve funcionar em VS Code/Copilot, use APENAS campos do padrao aberto. Se e exclusiva Claude Code, use extensoes.

2. **Siga as regras de validacao de nomes rigorosamente**:
   - Apenas lowercase, numeros e hifens
   - Sem `--` consecutivos
   - Sem iniciar/terminar com `-`
   - Sem "anthropic" ou "claude"
   - Nome deve = nome do diretorio

3. **Use `${CLAUDE_SKILL_DIR}` em vez de paths hardcoded**: Garante portabilidade entre instalacoes e plataformas.

4. **Mantenha descricoes sob 200 caracteres quando possivel**: Cada caractere consome orcamento de contexto. Descricoes de 1024 chars sao o maximo, nao o ideal.

### 9.2 Para Autores de Plugins

1. **Crie plugin.json mesmo sendo opcional**: A auto-discovery funciona, mas o manifesto explicito evita ambiguidades e permite metadados adicionais.

2. **Use `${CLAUDE_PLUGIN_ROOT}` para paths de scripts**: Garante que scripts funcionem independente do diretorio de instalacao.

3. **Use `${CLAUDE_PLUGIN_DATA}` para dados persistentes**: Nao armazene dados no diretorio do plugin -- ele muda em updates.

4. **Defina escopos de instalacao claros na documentacao**: Indique se o plugin deve ser instalado no escopo user, project ou local.

5. **Template de plugin minimo:**

```
my-plugin/
  .claude-plugin/
    plugin.json
  skills/
    main-skill/
      SKILL.md
  README.md
  LICENSE
```

```json
// .claude-plugin/plugin.json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Descricao concisa do plugin",
  "author": { "name": "Autor" },
  "license": "MIT"
}
```

### 9.3 Para Autores de Marketplaces

1. **Use categorias e tags consistentes**: Facilita discovery quando o marketplace cresce.

2. **Prefira strict mode (default)**: Deixe cada plugin definir seu proprio manifesto. Use `strict: false` apenas para plugins sem manifesto.

3. **Template de marketplace minimo:**

```json
{
  "name": "my-marketplace",
  "owner": { "name": "Organizacao" },
  "plugins": [
    {
      "name": "plugin-1",
      "description": "O que faz",
      "source": "./plugins/plugin-1"
    }
  ]
}
```

### 9.4 Para Estrategia de Distribuicao

1. **Skill pessoal -> Skill de projeto -> Plugin -> Marketplace**: Evolua a distribuicao conforme o publico cresce.

2. **Comece com skills standalone**: Crie e teste skills individualmente antes de empacotar em plugin.

3. **Use namespacing de plugin para evitar conflitos**: O namespace `plugin-name:skill-name` evita conflitos com skills de projeto/pessoais.

4. **Monitore repositorios da comunidade**: Os repos listados no documento (davepoon/buildwithclaude, numman-ali/n-skills, etc.) sao fontes de inspiracao e padroes emergentes.

### 9.5 Template de SKILL.md Portavel Cross-Platform

```yaml
---
name: universal-skill
description: >
  Skill portavel que funciona em Claude Code, VS Code/Copilot e OpenAI Codex.
  Usa apenas campos do padrao aberto Agent Skills.
---

# Universal Skill

## Instrucoes
[Instrucoes que nao dependem de funcionalidades especificas de plataforma]

## Recursos
- Para detalhes: [reference.md](reference.md)
- Para exemplos: [examples.md](examples.md)
```

### 9.6 Template de SKILL.md Avancado (Claude Code)

```yaml
---
name: advanced-skill
description: >
  Skill avancada usando funcionalidades exclusivas do Claude Code.
  Executa em subagente isolado com ferramentas restritas.
context: fork
agent: Explore
disable-model-invocation: true
allowed-tools: Read, Grep, Glob
effort: high
argument-hint: "[target-path] [options]"
---

# Advanced Skill

## Contexto dinamico
- Status atual: !`git status --short`
- Branch: !`git branch --show-current`

## Instrucoes
Analise $ARGUMENTS[0] com opcoes $ARGUMENTS[1]:

1. [Passo 1 com ferramenta]
2. [Passo 2 com validacao]
3. [Passo 3 com output estruturado]
```
