# Analise: Extend Claude with Skills

> Analise do documento oficial da Anthropic sobre o sistema de skills do Claude Code.
> **Documento fonte**: `docs/skills/extend-claude-with-skills.md`
> **Data da analise**: 2026-03-27

---

## 1. Sumario Executivo

O documento "Extend Claude with Skills" e a documentacao oficial da Anthropic que define o sistema de extensibilidade do Claude Code por meio de skills. Ele estabelece o formato SKILL.md como unidade fundamental de extensao, seguindo o padrao aberto Agent Skills (agentskills.io), e detalha toda a cadeia desde a criacao de uma skill simples ate padroes avancados como injecao dinamica de contexto e execucao em subagentes. O documento funciona como referencia canonica para qualquer pessoa que queira estender as capacidades do Claude Code.

A importancia estrategica deste documento reside em posicionar skills como o mecanismo primario de progressive disclosure do Claude Code. Diferente de CLAUDE.md (que e carregado integralmente no startup), skills carregam apenas a descricao no inicio da sessao e o conteudo completo somente sob demanda. Isso resolve diretamente o problema de "context rot" documentado pela Anthropic -- a degradacao de performance conforme o contexto cresce. Skills sao, portanto, a solucao arquitetural para o dilema entre riqueza de instrucoes e eficiencia de contexto.

O documento tambem revela a convergencia entre skills e o ecossistema mais amplo de plugins, subagentes e hooks, posicionando skills como a camada intermediaria entre instrucoes estaticas (CLAUDE.md/rules) e automacoes deterministicas (hooks). A integracao com `context: fork`, `allowed-tools` e `hooks` no frontmatter mostra que skills nao sao apenas documentos de instrucao, mas unidades de orquestracao completas.

---

## 2. Conceitos e Mecanismos Chave

### 2.1 Formato SKILL.md e Frontmatter

O formato central e um arquivo Markdown com frontmatter YAML:

```yaml
---
name: minha-skill
description: O que esta skill faz e quando usar
disable-model-invocation: true
allowed-tools: Read, Grep
context: fork
agent: Explore
---

Instrucoes em Markdown aqui...
```

**Campos do frontmatter e suas implicacoes:**

| Campo | Impacto no Contexto | Impacto Comportamental |
|-------|---------------------|------------------------|
| `name` | Minimo (~10 tokens) | Define o comando `/nome` |
| `description` | Carregado no startup (se model-invocable) | Determina auto-discovery pelo Claude |
| `disable-model-invocation` | Remove descricao do contexto | Impede invocacao automatica |
| `user-invocable` | Mantem descricao no contexto | Remove do menu `/` |
| `allowed-tools` | Nenhum | Concede permissoes durante execucao |
| `context` | Fork isola completamente | Cria subagente com contexto proprio |
| `agent` | Determina system prompt do subagente | Define ferramentas e modelo disponiveis |
| `model` | Nenhum direto | Override do modelo para a skill |
| `effort` | Nenhum direto | Controla nivel de esforco (low a max) |
| `hooks` | Nenhum | Automacoes no lifecycle da skill |

### 2.2 Modelo de Carregamento em Tres Niveis

O documento revela um modelo de progressive disclosure em tres niveis:

1. **Metadados** (~100 tokens): `name` + `description` -- carregados no startup para TODAS as skills model-invocable
2. **Instrucoes** (corpo do SKILL.md): Carregadas sob demanda quando a skill e invocada
3. **Recursos** (arquivos de suporte): Carregados sob demanda pelo Claude quando necessario

Este modelo e diretamente alinhado com o conceito de "just in time documentation" descrito no documento de context optimization.

### 2.3 Hierarquia de Localizacao e Prioridade

```
Enterprise (mais alta prioridade)
  > Personal (~/.claude/skills/)
    > Project (.claude/skills/)
      > Plugin (namespace plugin-name:skill-name)
```

**Ponto critico**: Plugins usam namespace prefixado, evitando conflitos. Porem, skills de enterprise, personal e project competem pelo mesmo namespace -- a de maior prioridade vence silenciosamente.

### 2.4 Substituicao de Variaveis

O sistema suporta substituicoes dinamicas:

- `$ARGUMENTS` / `$ARGUMENTS[N]` / `$N` -- argumentos posicionais
- `${CLAUDE_SESSION_ID}` -- identificador da sessao
- `${CLAUDE_SKILL_DIR}` -- diretorio da skill (crucial para scripts bundled)

### 2.5 Injecao Dinamica de Contexto

A sintaxe `` !`<command>` `` e um mecanismo de pre-processamento que executa comandos shell ANTES do envio ao Claude:

```yaml
---
name: pr-summary
context: fork
agent: Explore
---

- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`
```

Isso transforma skills em pipelines de dados em tempo real, nao apenas documentos estaticos.

### 2.6 Execucao em Subagente (context: fork)

Quando `context: fork` esta ativo:

1. Contexto isolado e criado (zero impacto no contexto principal)
2. O corpo do SKILL.md se torna o prompt do subagente
3. O campo `agent` define o ambiente de execucao (Explore, Plan, general-purpose, ou agente customizado)
4. Resultados sao sumarizados e retornados ao contexto principal

**Diferenca critica entre as duas direcoes:**

| Abordagem | System Prompt | Tarefa | Tambem Carrega |
|-----------|--------------|--------|----------------|
| Skill com `context: fork` | Do tipo de agente | Corpo do SKILL.md | CLAUDE.md |
| Subagente com campo `skills` | Corpo do markdown do subagente | Mensagem de delegacao | Skills pre-carregadas + CLAUDE.md |

### 2.7 Orcamento de Caracteres para Descricoes

O documento revela uma limitacao critica: descricoes de skills compartilham um orcamento de caracteres que escala a 2% da janela de contexto, com fallback de 16.000 caracteres. Isso significa que com muitas skills, algumas podem ser excluidas do contexto. O comando `/context` permite verificar warnings sobre skills excluidas, e a variavel `SLASH_COMMAND_TOOL_CHAR_BUDGET` permite override.

---

## 3. Pontos de Atencao

### 3.1 Erros Comuns na Autoria de Skills

1. **Descricoes vagas**: "Helps with files" nao ativa auto-discovery. A descricao precisa conter keywords que o usuario naturalmente diria.

2. **Skills de referencia com `context: fork`**: O documento alerta explicitamente -- skills com `context: fork` precisam de instrucoes acionaveis. Se a skill contem apenas guidelines sem tarefa, o subagente recebe as guidelines mas nao tem prompt acionavel.

3. **Confusao entre `disable-model-invocation` e `user-invocable`**: `user-invocable: false` NAO bloqueia acesso pela Skill tool -- apenas esconde do menu `/`. Para bloquear invocacao programatica, e necessario `disable-model-invocation: true`.

4. **Excesso de skills model-invocable**: Cada skill model-invocable consome orcamento de descricao. Um projeto com 50+ skills pode ultrapassar o limite de 16K caracteres.

5. **SKILL.md excessivamente longo**: O documento recomenda manter sob 500 linhas, movendo material de referencia para arquivos separados.

### 3.2 Armadilhas de Contexto

- **Descricoes sempre em contexto**: Para skills model-invocable, a descricao esta SEMPRE no contexto, consumindo budget de atencao mesmo quando a skill nao e usada.
- **context: fork carrega CLAUDE.md**: Mesmo em execucao isolada, o subagente carrega CLAUDE.md -- instrucoes conflitantes em CLAUDE.md podem afetar comportamento da skill.
- **Argumentos nao capturados**: Se `$ARGUMENTS` nao aparece no corpo, os argumentos sao ADICIONADOS ao final como `ARGUMENTS: <valor>` -- potencialmente desalinhando instrucoes.

### 3.3 Lacunas de Teste

- Nao ha mecanismo built-in de teste/validacao de skills
- Nao ha como visualizar o prompt final renderizado (apos substituicoes e injecao dinamica)
- Nao ha metricas de quantas vezes uma skill e invocada automaticamente vs manualmente
- O comportamento de auto-discovery depende da qualidade da descricao, que so pode ser testada empiricamente

---

## 4. Casos de Uso e Escopo

### 4.1 Quando Criar uma Skill vs Alternativas

| Necessidade | Mecanismo Ideal | Justificativa |
|-------------|----------------|---------------|
| Conhecimento persistente e curto (<5 linhas) | Rule (.claude/rules/) | Zero overhead, sempre no contexto |
| Conhecimento persistente e medio (5-50 linhas) | CLAUDE.md | Carregado no startup, sem invocacao |
| Conhecimento sob demanda (50-500 linhas) | **Skill** | Progressive disclosure, carregamento JIT |
| Conhecimento extenso com sub-documentos | **Skill + supporting files** | Hierarquia de disclosure em dois niveis |
| Workflow com side effects | **Skill com `disable-model-invocation`** | Controle manual de timing |
| Tarefa isolada com ferramentas especificas | **Skill com `context: fork`** | Isolamento de contexto |
| Automacao deterministica | Hook | Execucao garantida, sem LLM |
| Validacao pos-acao | Hook (post-tool) | Nao depende de atencao do modelo |

### 4.2 Exemplos de Categorias de Skills

**Skills de Referencia** (model-invocable, inline):

- Convencoes de API do projeto
- Padroes de estilo de codigo
- Conhecimento de dominio especifico

**Skills de Tarefa** (disable-model-invocation, inline ou fork):

- Deploy (`/deploy`)
- Commit formatado (`/commit`)
- Criacao de PR (`/create-pr`)

**Skills de Pesquisa** (context: fork, agent: Explore):

- Investigacao de codebase (`/deep-research`)
- Analise de PR (`/pr-summary`)
- Documentacao interativa

**Skills de Visualizacao** (inline, com scripts bundled):

- Visualizacao de codebase
- Grafos de dependencia
- Relatorios interativos em HTML

---

## 5. Aplicabilidade a Infraestrutura de Agentes

### 5.1 Skills (Design Patterns, Composicao e Evolucao)

**Padroes de design fundamentais identificados:**

1. **Skill Simples**: SKILL.md com instrucoes diretas, sem supporting files
2. **Skill com Referencia**: SKILL.md como indice + arquivos de referencia por dominio
3. **Skill com Scripts**: SKILL.md com instrucoes + scripts executaveis bundled
4. **Skill como Pipeline**: `context: fork` + injecao dinamica + agent type
5. **Skill como Orquestrador**: Instrucoes que delegam para multiplos subagentes

**Estrategias de composicao:**

- **Encadeamento manual**: Uma skill instrui o usuario a invocar outra apos conclusao
- **Delegacao a subagente com skills pre-carregadas**: Subagente definido em `.claude/agents/` com campo `skills` que pre-carrega skills relevantes
- **Skills como building blocks de plugins**: Plugin agrupa skills relacionadas com namespace compartilhado

**Estrategias de evolucao:**

- Comece com SKILL.md simples e inline
- Quando ultrapassar 200 linhas, extraia para supporting files
- Quando side effects forem criticos, adicione `disable-model-invocation: true`
- Quando contexto principal estiver saturado, migre para `context: fork`
- Quando complexidade aumentar, crie plugin com multiplas skills

**Template de skill de referencia:**

```yaml
---
name: api-conventions
description: Convencoes de API REST para este projeto. Usar quando criar ou modificar endpoints, handlers HTTP, ou rotas de API.
---

# Convencoes de API

## Padrao de resposta

Todos os endpoints retornam:
- 200: Sucesso com corpo JSON
- 400: Erro de validacao com `{ error: string, fields: Record<string, string> }`
- 500: Erro interno com `{ error: "Internal server error" }`

## Recursos adicionais

- Schemas completos: [reference/schemas.md](reference/schemas.md)
- Exemplos de endpoints: [reference/examples.md](reference/examples.md)
```

**Template de skill de tarefa com fork:**

```yaml
---
name: investigate-issue
description: Investiga um issue do GitHub em profundidade
context: fork
agent: Explore
disable-model-invocation: true
allowed-tools: Bash(gh *), Read, Grep, Glob
---

# Investigacao de Issue

Investigue o issue GitHub #$ARGUMENTS:

1. Leia o issue completo: !`gh issue view $ARGUMENTS`
2. Identifique os arquivos relevantes usando Grep e Glob
3. Analise o codigo relacionado
4. Produza um relatorio com:
   - Causa raiz provavel
   - Arquivos afetados (paths absolutos)
   - Estrategia de correcao recomendada
```

### 5.2 Hooks (Complemento a Skills)

Skills e hooks sao complementares:

- **Hooks pre-skill**: O campo `hooks` no frontmatter permite definir hooks que executam antes/depois do lifecycle da skill
- **Hooks como enforcement**: Onde CLAUDE.md/skills sao "advisory" (o modelo pode ignorar), hooks sao deterministicos
- **Conversao de instrucoes para hooks**: Conforme documentado no research de context optimization, "se Claude ja faz algo corretamente sem a instrucao, delete-a ou converta em hook"

**Exemplo de hook scoped a skill:**

```yaml
---
name: deploy
description: Deploy para producao
disable-model-invocation: true
hooks:
  PreToolExecution:
    - matcher: Bash
      hooks:
        - command: "echo 'Deploy iniciado em $(date)' >> deploy.log"
---
```

### 5.3 Subagentes (context: fork e Composicao)

O documento estabelece dois fluxos de integracao skill-subagente:

**Skill -> Subagente (context: fork):**

- A skill DEFINE a tarefa
- O agent type DEFINE o ambiente
- Ideal para tarefas auto-contidas com resultado definido

**Subagente -> Skills (preloaded skills):**

- O subagente (`.claude/agents/`) DEFINE o system prompt
- Skills pre-carregadas fornecem conhecimento de referencia
- Ideal para agentes especializados que precisam de multiplas skills

**Padroes de composicao com subagentes:**

```yaml
# Skill que usa subagente Explore para pesquisa
---
name: codebase-audit
description: Auditoria completa do codebase
context: fork
agent: Explore
---

# Auditoria de Codebase
1. Use Glob para mapear toda a estrutura
2. Use Grep para identificar padroes problematicos
3. Gere relatorio com achados priorizados
```

```markdown
# Subagente que pre-carrega skills (.claude/agents/security-reviewer.md)
---
skills:
  - owasp-security
  - api-conventions
allowed-tools: Read, Grep, Glob
---

Voce e um revisor de seguranca especializado.
Analise o codigo usando as convencoes carregadas.
```

### 5.4 Rules (Complemento e Substituicao de Skills)

**Rules que referenciam skills:**

```markdown
# .claude/rules/api-development.md
---
paths:
  - "src/api/**/*.ts"
---

Ao criar endpoints de API, invoque a skill `api-conventions` para referencia de padroes.
```

**Quando rules substituem conteudo de skills:**

- Instrucoes curtas e universais (<5 linhas) -> Rule
- Instrucoes condicionais por path -> Rule com `paths`
- Instrucoes que DEVEM ser seguidas sem excecao -> Rule (sempre no contexto quando path match)

**Quando skills substituem rules:**

- Conteudo extenso (>50 linhas) -> Skill (evita poluir contexto)
- Conteudo sob demanda -> Skill (carregamento JIT)
- Conteudo com workflows interativos -> Skill

### 5.5 Memory (Skills que Usam e Geram Memoria)

**Skills informadas por memoria:**

- Uma skill pode instruir Claude a ler `~/.claude/projects/<project>/memory/` antes de agir
- Auto-memory pode conter preferencias que influenciam comportamento de skills

**Skills que geram memoria:**

- Uma skill de workflow pode instruir Claude a registrar decisoes em auto-memory
- Skills de auditoria podem gerar achados persistentes via memoria

**Exemplo:**

```yaml
---
name: session-logger
description: Registra atividades da sessao
---

Antes de executar qualquer acao, verifique as notas anteriores em memory/:
- Se houver decisoes pendentes, liste-as para o usuario
- Apos cada acao significativa, atualize as notas

Log da sessao ${CLAUDE_SESSION_ID}: $ARGUMENTS
```

---

## 6. Aplicabilidade do Guia de Engenharia de Prompts

### 6.1 Chain-of-Thought (CoT) para Fases Multi-Step

Skills com workflows multi-etapa se beneficiam de CoT explicito. Conforme o guia, CoT melhora de 17,9% para 58,1% em tarefas de raciocinio no GSM8K. Para skills de analise:

```yaml
---
name: code-analysis
description: Analise profunda de qualidade de codigo
---

Analise o codigo em $ARGUMENTS seguindo esta cadeia de raciocinio:

1. **Compreensao**: Leia o codigo e descreva o que ele faz em uma frase
2. **Estrutura**: Identifique padroes de design e dependencias
3. **Problemas**: Para cada potencial problema, explique:
   - O que esta errado
   - Por que e problematico
   - Como corrigir
4. **Priorizacao**: Ordene problemas por severidade
5. **Recomendacao**: Sumarize as 3 acoes mais impactantes
```

### 6.2 ReAct para Skills com Ferramentas

O padrao ReAct (Pensamento -> Acao -> Observacao) e natural para skills que usam ferramentas. O guia documenta +34% de taxa de sucesso em ALFWorld com ReAct:

```yaml
---
name: debug-issue
description: Debug interativo de problemas
allowed-tools: Read, Grep, Glob, Bash(npm test *)
---

Siga o loop ReAct para debugar $ARGUMENTS:

Para cada iteracao:
1. **Pensamento**: Qual hipotese estou testando? Que evidencia preciso?
2. **Acao**: Execute uma ferramenta para coletar evidencia
3. **Observacao**: O que o resultado me diz?

Repita ate:
- Causa raiz identificada com evidencia concreta
- Correcao proposta e verificada por teste
```

### 6.3 Tree of Thoughts (ToT) para Skills de Decisao Complexa

Para skills que envolvem planejamento ou decisoes com multiplos caminhos validos, ToT oferece 18,5x de melhoria sobre CoT (Game of 24). Aplicavel a skills de arquitetura:

```yaml
---
name: architecture-decision
description: Avaliacao estruturada de decisoes arquiteturais
context: fork
---

Para a decisao arquitetural sobre $ARGUMENTS:

1. **Gere 3 alternativas** viáveis (cada uma com trade-offs explicitos)
2. **Avalie cada alternativa** nos eixos:
   - Complexidade de implementacao (1-5)
   - Manutenibilidade a longo prazo (1-5)
   - Performance esperada (1-5)
   - Alinhamento com stack atual (1-5)
3. **Elimine** alternativas com score < 12
4. **Aprofunde** nas alternativas restantes com analise de riscos
5. **Recomende** com justificativa baseada nos scores
```

### 6.4 Least-to-Most para Skills de Decomposicao

Para skills que decompoe problemas complexos em subproblemas:

```yaml
---
name: refactor-module
description: Refatoracao guiada de modulos complexos
---

Para refatorar $ARGUMENTS:

1. **Identifique o problema mais simples**: Qual e a menor mudanca que melhora o codigo?
2. **Resolva-o primeiro**: Implemente e verifique
3. **Identifique o proximo problema**: Agora que o mais simples esta resolvido, qual e o proximo?
4. **Repita** ate que o modulo esteja refatorado
5. **Verifique** que todos os testes passam apos cada mudanca
```

### 6.5 Self-Consistency para Skills de Validacao

Para skills que precisam de alta confiabilidade, Self-Consistency (+12-18% sobre CoT) pode ser simulada:

```yaml
---
name: security-audit
description: Auditoria de seguranca com validacao cruzada
context: fork
---

Para auditar $ARGUMENTS:

1. **Analise 1 (OWASP Top 10)**: Verifique cada categoria
2. **Analise 2 (Attack surface)**: Identifique pontos de entrada e fluxos de dados
3. **Analise 3 (Dependencias)**: Verifique vulnerabilidades conhecidas

4. **Consolidacao**: Compare os achados das tres analises
   - Achados presentes em 2+ analises: CONFIRMADOS
   - Achados em apenas 1 analise: REQUER INVESTIGACAO
5. **Relatorio final**: Apenas achados confirmados como criticos/altos
```

### 6.6 Reflexion para Skills de Melhoria Iterativa

Para skills que melhoram output por iteracao:

```yaml
---
name: improve-docs
description: Melhoria iterativa de documentacao
---

Para melhorar a documentacao em $ARGUMENTS:

Ciclo de melhoria (maximo 3 iteracoes):
1. **Gere**: Escreva/melhore a documentacao
2. **Critique**: Avalie contra criterios:
   - Completude (todos os parametros documentados?)
   - Clareza (um novo dev entenderia?)
   - Exemplos (ha exemplos praticos?)
3. **Reflita**: O que pode ser melhorado?
4. Se nota < 8/10, **repita** com foco nos pontos fracos
5. Se nota >= 8/10, finalize
```

---

## 7. Correlacoes com Documentos Principais

### 7.1 Com research-llm-context-optimization.md

| Conceito no Research | Implementacao em Skills |
|---------------------|------------------------|
| "Context rot" -- degradacao com mais tokens | Skills carregam conteudo JIT, minimizando tokens no contexto |
| "Attention budget" finito | `disable-model-invocation` remove descricoes do budget |
| "Lost in the middle" effect | SKILL.md e lido do inicio ao fim como unidade focada |
| Progressive disclosure em 3 niveis | Metadados -> SKILL.md -> supporting files |
| "Just in time documentation" | Skills SAO a implementacao principal deste conceito |
| Instrucoes sob 200 linhas | Recomendacao de SKILL.md sob 500 linhas (mais permissivo por ser JIT) |
| Subagentes para isolamento de contexto | `context: fork` implementa subagente com contexto isolado |
| Hooks como enforcement deterministico | Campo `hooks` no frontmatter permite hooks scoped a skills |

### 7.2 Com skill-authoring-best-practices.md

O documento de best practices detalha o "como" do que "extend-claude-with-skills" define no "o que":

- Nomenclatura: gerundio preferido (processing-pdfs vs pdf-processor)
- Descricoes: terceira pessoa, especificas, com keywords de trigger
- Progressive disclosure: SKILL.md como table of contents, referencias em um nivel de profundidade
- Workflows com checklists para skills complexas
- Feedback loops (validar -> corrigir -> repetir)

### 7.3 Com research-claude-code-skills-format.md

O documento de research complementa com:

- Formato Agent Skills Open Standard vs extensoes Claude Code
- Regras de validacao de nomes (1-64 chars, kebab-case, sem `--`)
- Estrutura de plugins e marketplaces para distribuicao
- Comparacao com VS Code/Copilot (`.agents/skills/` vs `.claude/skills/`)
- Mecanismo de instalacao via `/plugin install` (nao `npx skills add`)

### 7.4 Com prompt-engineering-guide.md

O guia de engenharia de prompts fornece o arsenal tecnico para escrita de skills eficazes:

- CoT para workflows multi-step
- ReAct para skills com ferramentas
- Structured outputs para comunicacao entre skills e subagentes
- Role prompting para especializacao de subagentes
- A recomendacao de "comecar simples, aumentar complexidade quando necessario" se aplica diretamente a evolucao de skills

---

## 8. Forcas e Limitacoes

### 8.1 Forcas

1. **Progressive disclosure nativo**: O modelo de 3 niveis (metadados -> corpo -> supporting files) e elegante e resolve o problema de context rot
2. **Flexibilidade de invocacao**: O controle fino entre user-invocable, model-invocable e ambos cobre todos os cenarios
3. **Isolamento de contexto**: `context: fork` permite skills pesadas sem impactar o contexto principal
4. **Injecao dinamica**: `` !`command` `` transforma skills em pipelines de dados em tempo real
5. **Compatibilidade cross-agent**: O padrao Agent Skills (agentskills.io) funciona em Claude Code, VS Code/Copilot e OpenAI Codex
6. **Hierarquia de escopo**: Enterprise > Personal > Project > Plugin permite governanca organizacional
7. **Bundled skills oficiais**: `/batch`, `/simplify`, `/debug` demonstram o potencial do sistema

### 8.2 Limitacoes

1. **Sem framework de testes**: Nao existe mecanismo built-in para testar skills antes do deploy. O ciclo "teste empirico" e insatisfatorio para producao.
2. **Orcamento de descricoes opaco**: O limite de 2% da janela de contexto / 16K chars nao e visivel ate que skills sejam excluidas silenciosamente.
3. **Sem versionamento**: Skills nao tem campo `version` no frontmatter Claude Code (apenas no Agent Skills spec). Nao ha mecanismo de rollback.
4. **Sem metricas de uso**: Nao ha como saber quantas vezes uma skill foi invocada, automatica vs manualmente, ou se a descricao e eficaz para auto-discovery.
5. **Dependencia de qualidade de descricao**: Auto-discovery e inteiramente dependente da descricao -- sem fallback se a descricao for inadequada.
6. **CLAUDE.md carrega em fork**: Mesmo com `context: fork`, CLAUDE.md e carregado no subagente. Instrucoes conflitantes em CLAUDE.md podem afetar a skill.
7. **Sem composicao nativa entre skills**: Nao existe mecanismo formal para uma skill invocar outra. A composicao e ad-hoc.
8. **Limite de 500 linhas**: Embora seja boa pratica, nao ha validacao automatica deste limite.

---

## 9. Recomendacoes Praticas

### 9.1 Para Autoria de Skills Individuais

1. **Comece com a descricao**: Escreva a descricao ANTES do corpo. Se nao conseguir descrever em 1024 chars quando e como usar, a skill esta mal definida.

2. **Use a regra dos 3 niveis**:
   - Nivel 1 (sempre presente): Descricao clara com keywords (~100 tokens)
   - Nivel 2 (sob demanda): SKILL.md focado, <500 linhas
   - Nivel 3 (apenas quando necessario): Supporting files com material de referencia

3. **Prefira `disable-model-invocation: true` para workflows com side effects**: Deploy, commit, envio de mensagens -- nunca deixe o Claude decidir quando executar.

4. **Use `context: fork` para tarefas pesadas**: Qualquer skill que leia muitos arquivos, execute muitos comandos, ou produza output extenso deve rodar em subagente.

5. **Referencie `${CLAUDE_SKILL_DIR}` para scripts bundled**: Em vez de paths absolutos, use a variavel para portabilidade.

### 9.2 Para Organizacao de Colecoes de Skills

1. **Monitore o orcamento de descricoes**: Use `/context` regularmente. Se skills estao sendo excluidas, considere:
   - Marcar skills menos usadas como `disable-model-invocation: true`
   - Encurtar descricoes
   - Aumentar `SLASH_COMMAND_TOOL_CHAR_BUDGET`

2. **Agrupe skills relacionadas em plugins**: Skills que compartilham dominio devem estar em um plugin com namespace proprio.

3. **Use hierarquia de prioridade conscientemente**: Skills pessoais (`~/.claude/skills/`) sobrescrevem skills de projeto. Use isso para personalizacao, nao para conflito.

### 9.3 Para Integracao com Infraestrutura de Agentes

1. **Converta instrucoes CLAUDE.md > 50 linhas em skills**: Reduz contexto sempre-presente e melhora aderencia.

2. **Use hooks para enforcement, skills para guidance**: Se uma regra DEVE ser seguida sem excecao, implemente como hook. Se e uma diretriz que admite excecoes, implemente como skill.

3. **Projete subagentes com skills pre-carregadas**: Para agentes especializados, defina em `.claude/agents/` com campo `skills` para carregar conhecimento relevante no startup do subagente.

4. **Implemente feedback loops em skills criticas**: Skills de deploy, migracao ou operacoes destrutivas devem incluir etapas de validacao explicitas (validate -> fix -> repeat).

### 9.4 Template de Skill Padrao Recomendado

```yaml
---
name: nome-da-skill
description: >
  [O que faz] e [quando usar]. Use quando [trigger keywords].
  Exemplos: [cenarios concretos que ativam a skill].
disable-model-invocation: false  # ou true para workflows com side effects
# context: fork  # descomente para tarefas pesadas
# agent: Explore  # descomente com context: fork
# allowed-tools: Read, Grep, Glob  # descomente se necessario
---

# [Nome da Skill]

## Objetivo
[Uma frase descrevendo o objetivo]

## Instrucoes
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

## Validacao
- [ ] [Criterio de sucesso 1]
- [ ] [Criterio de sucesso 2]

## Recursos adicionais
- Para detalhes de [topico]: [reference/topico.md](reference/topico.md)
```
