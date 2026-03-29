# Análise Completa: Skill Authoring Best Practices

## 1. Sumário Executivo

O documento **skill-authoring-best-practices.md** é o guia oficial da Anthropic para autoria de skills eficazes no Claude Code. Enquanto o `extend-claude-with-skills.md` define a arquitetura e o `research-claude-code-skills-format.md` detalha o formato técnico, este documento foca no **como escrever bem** — os princípios de design, padrões de conteúdo, estratégias de teste e anti-padrões que determinam se um skill será eficaz ou desperdiçará tokens.

O documento está profundamente alinhado com os princípios de otimização de contexto identificados no `research-llm-context-optimization.md`: concisão como princípio fundamental (a janela de contexto é um "bem público"), progressive disclosure como arquitetura central (SKILL.md como índice, arquivos de referência carregados sob demanda), e graus de liberdade calibrados à fragilidade da tarefa. O mantra central é: **"Claude já é muito inteligente — adicione apenas o contexto que ele não possui."**

A contribuição mais significativa deste documento é a metodologia de **desenvolvimento iterativo com dois Claudes** (Claude A como expert que refina o skill, Claude B como agente que o utiliza), combinada com a abordagem de **evaluation-driven development** que prioriza a criação de avaliações antes da escrita de documentação extensiva. Este ciclo observe-refine-test é a implementação prática do princípio de Reflexion aplicado ao design de infraestrutura de agentes.

## 2. Conceitos e Mecanismos-Chave

### 2.1 Princípios Fundamentais

#### Concisão como Princípio Central

O documento estabelece uma hierarquia clara de custo de tokens:

| Momento | O que é carregado | Custo |
|---------|-------------------|-------|
| Startup | Apenas `name` + `description` de todos os skills | Mínimo |
| Trigger | `SKILL.md` completo do skill relevante | Moderado |
| Sob demanda | Arquivos referenciados (reference/, examples/) | Variável |

**Teste decisivo para cada informação:**

- "Claude realmente precisa desta explicação?"
- "Posso assumir que Claude já sabe isso?"
- "Este parágrafo justifica seu custo em tokens?"

**Exemplo concreto do documento:**

- Bom (~50 tokens): Código direto com `pdfplumber` sem explicação
- Ruim (~150 tokens): Explicação do que é PDF, por que usar pdfplumber, como instalar

#### Graus de Liberdade Calibrados

O documento introduz uma metáfora poderosa — Claude como robô explorando um caminho:

| Grau | Metáfora | Quando Usar | Exemplo |
|------|----------|-------------|---------|
| **Alto** | Campo aberto sem perigos | Múltiplas abordagens válidas, decisões dependem de contexto | Code review |
| **Médio** | Caminho com marcações | Padrão preferido existe mas variação é aceitável | Templates com parâmetros |
| **Baixo** | Ponte estreita com penhascos | Operações frágeis, consistência crítica | Database migrations |

**Princípio derivado:** A especificidade das instruções deve ser proporcional ao risco de erro. Quanto mais destrutiva ou irreversível a operação, mais prescritivo o skill deve ser.

#### Teste Multi-Modelo

Skills devem ser testados com todos os modelos pretendidos:

| Modelo | Consideração de Teste |
|--------|----------------------|
| **Haiku** | O skill fornece guidance suficiente? (precisa mais detalhe) |
| **Sonnet** | O skill é claro e eficiente? (equilíbrio) |
| **Opus** | O skill evita over-explaining? (pode precisar menos) |

### 2.2 Estrutura do Skill

#### Frontmatter YAML

| Campo | Requisitos | Limite |
|-------|-----------|--------|
| `name` | Lowercase, números, hífens apenas. Sem XML tags, sem palavras reservadas ("anthropic", "claude") | 64 caracteres |
| `description` | Não-vazio, sem XML tags. Deve descrever O QUE faz E QUANDO usar | 1024 caracteres |

#### Convenções de Nomenclatura

**Forma preferida — gerúndio (verb + -ing):**

- `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`

**Aceitável — frases nominais ou orientadas a ação:**

- `pdf-processing`, `process-pdfs`

**Evitar:**

- Nomes vagos: `helper`, `utils`, `tools`
- Genéricos: `documents`, `data`, `files`

#### Descrições Eficazes

**Regra crítica:** Sempre em terceira pessoa. A descrição é injetada no system prompt — POV inconsistente causa problemas de discovery.

- Bom: "Processes Excel files and generates reports"
- Ruim: "I can help you process Excel files"
- Ruim: "You can use this to process Excel files"

**Elementos de uma boa descrição:**

1. O que o skill faz (capacidades)
2. Quando usá-lo (triggers/contextos)
3. Termos-chave específicos (para matching)

### 2.3 Progressive Disclosure — Padrões

#### Padrão 1: Guia de Alto Nível com Referências

```
SKILL.md (overview + quick start)
  ├── FORMS.md (carregado se form filling necessário)
  ├── REFERENCE.md (carregado se API details necessários)
  └── EXAMPLES.md (carregado se exemplos necessários)
```

Claude carrega arquivos sob demanda. Zero custo de contexto para arquivos não acessados.

#### Padrão 2: Organização por Domínio

```
bigquery-skill/
├── SKILL.md (overview e navegação)
└── reference/
    ├── finance.md (métricas de receita)
    ├── sales.md (pipeline, oportunidades)
    ├── product.md (uso de API)
    └── marketing.md (campanhas)
```

Quando o usuário pergunta sobre vendas, Claude carrega apenas `sales.md`.

#### Padrão 3: Detalhes Condicionais

```markdown
## Creating documents
Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents
For simple edits, modify XML directly.
**For tracked changes**: See [REDLINING.md](REDLINING.md)
```

#### Regra de Profundidade: Máximo 1 Nível

**Crítico:** Referências devem ser de no máximo 1 nível de profundidade a partir de SKILL.md. Claude pode usar `head -100` para preview de arquivos referenciados por outros arquivos referenciados, resultando em informação incompleta.

- Ruim: `SKILL.md → advanced.md → details.md` (2 níveis)
- Bom: `SKILL.md → advanced.md`, `SKILL.md → reference.md` (1 nível cada)

#### Arquivos de Referência Longos: Table of Contents

Para arquivos com mais de 100 linhas, incluir TOC no topo para que Claude veja o escopo completo mesmo em leituras parciais.

### 2.4 Workflows e Feedback Loops

#### Checklists para Tarefas Complexas

O documento recomenda fornecer checklists copiáveis que Claude pode marcar durante a execução:

```markdown
Task Progress:
- [ ] Step 1: Analyze the form
- [ ] Step 2: Create field mapping
- [ ] Step 3: Validate mapping
- [ ] Step 4: Fill the form
- [ ] Step 5: Verify output
```

#### Feedback Loops (Validate → Fix → Repeat)

Padrão que melhora significativamente a qualidade:

1. Executar validador/script
2. Corrigir erros encontrados
3. Re-validar
4. Só proceder quando validação passar

Aplica-se tanto a skills com código (scripts de validação) quanto sem código (verificação contra style guides).

### 2.5 Guidelines de Conteúdo

**Evitar informação time-sensitive:**

- Ruim: "Se antes de agosto 2025, use a API antiga"
- Bom: Seção "Current method" + seção colapsável "Old patterns"

**Terminologia consistente:**

- Escolher UM termo e usar em todo o skill
- "API endpoint" sempre, não misturar com "URL", "route", "path"

### 2.6 Skills com Código Executável

#### Princípio: Solve, Don't Punt

Scripts devem tratar erros em vez de deixar Claude resolver:

- Bom: `except FileNotFoundError: create default`
- Ruim: `return open(path).read()` (falha silenciosa)

#### Constantes Documentadas (Lei de Ousterhout)

```python
# Bom: auto-documentado
REQUEST_TIMEOUT = 30  # HTTP requests typically complete within 30s
MAX_RETRIES = 3       # Most intermittent failures resolve by 2nd retry

# Ruim: magic numbers
TIMEOUT = 47  # Por quê 47?
```

#### Scripts Utilitários vs Código Gerado

| Aspecto | Script Pré-feito | Código Gerado por Claude |
|---------|-----------------|-------------------------|
| Confiabilidade | Maior (testado) | Variável |
| Custo de tokens | Baixo (apenas output) | Alto (código no contexto) |
| Tempo | Rápido (executa direto) | Lento (gera + executa) |
| Consistência | Alta | Variável |

**Distinção crítica nas instruções:**

- "Run `analyze_form.py` to extract fields" → **executar**
- "See `analyze_form.py` for the extraction algorithm" → **ler como referência**

#### Plan-Validate-Execute Pattern

Para operações complexas e destrutivas:

1. Analyze → Create plan file (`changes.json`)
2. **Validate plan** com script
3. Execute changes
4. Verify output

Quando usar: batch operations, destructive changes, complex validation, high-stakes.

### 2.7 Avaliação e Iteração

#### Evaluation-Driven Development

**Sequência recomendada:**

1. Identificar gaps (rodar Claude sem skill e documentar falhas)
2. Criar avaliações (3 cenários mínimos)
3. Estabelecer baseline (performance sem o skill)
4. Escrever instruções mínimas
5. Iterar (executar avaliações, comparar, refinar)

#### Desenvolvimento Iterativo com Dois Claudes

| Papel | Função |
|-------|--------|
| **Claude A** | Expert que ajuda a refinar o skill (design, estrutura, conteúdo) |
| **Claude B** | Agente que testa o skill em tarefas reais |
| **Você** | Observador que identifica gaps e fornece domain expertise |

**Ciclo:** Observar Claude B → Identificar problemas → Refinar com Claude A → Testar com Claude B → Repetir

#### Observar Navegação de Skills

Padrões a monitorar:

- **Caminhos inesperados**: Claude lê arquivos em ordem não antecipada → estrutura não intuitiva
- **Conexões perdidas**: Claude não segue referências → links precisam ser mais explícitos
- **Dependência excessiva**: Claude relê o mesmo arquivo repetidamente → conteúdo deveria estar no SKILL.md principal
- **Conteúdo ignorado**: Claude nunca acessa um arquivo bundled → possivelmente desnecessário

## 3. Pontos de Atenção

### 3.1 Armadilhas Comuns

| Armadilha | Problema | Solução |
|-----------|----------|---------|
| **Over-explaining para Opus** | Desperdiça tokens com informação que Opus já sabe | Testar com cada modelo; usar "escape hatches" para detalhes |
| **Under-explaining para Haiku** | Haiku precisa mais guidance que Opus | Mirar em instruções que funcionem para todos os modelos |
| **Referências de 2+ níveis** | Claude pode fazer `head -100` em vez de ler completo | Manter referências a 1 nível de SKILL.md |
| **Descrição em primeira pessoa** | Causa problemas de discovery quando injetada no system prompt | Sempre terceira pessoa |
| **SKILL.md acima de 500 linhas** | Performance degradada, competição excessiva por tokens | Split em arquivos de referência |
| **Informação time-sensitive** | Torna-se incorreta sem aviso | Usar seção "Old patterns" colapsável |
| **Múltiplas opções sem default** | Claude fica indeciso | Fornecer default claro + escape hatch |
| **Paths Windows-style** | Erros em sistemas Unix | Sempre forward slashes |
| **Assumir packages instalados** | Falha silenciosa em ambientes limpos | Listar dependências explicitamente |
| **Voodoo constants** | Claude não sabe como ajustar | Documentar justificativa de cada constante |

### 3.2 O Paradoxo da Completude

O documento revela uma tensão fundamental: skills devem ser **suficientemente completos** para guiar o Claude, mas **suficientemente concisos** para não desperdiçar o budget de contexto. A resolução está no progressive disclosure — o SKILL.md é um índice conciso, e os detalhes vivem em arquivos separados carregados sob demanda.

### 3.3 Discovery vs Execution

A `description` serve para **discovery** (Claude decidindo qual skill usar entre 100+), enquanto o corpo do SKILL.md serve para **execution** (como realizar a tarefa). Otimizar para um sem considerar o outro leva a problemas:

- Descrição vaga → skill nunca é selecionado
- Descrição boa + corpo ruim → skill é selecionado mas falha na execução

## 4. Casos de Uso e Escopo

### 4.1 Quando Criar um Skill

| Situação | Criar Skill? | Alternativa |
|----------|-------------|-------------|
| Workflow repetitivo com múltiplos passos | **Sim** | — |
| Conhecimento de domínio que Claude não tem | **Sim** | — |
| Validação/formatação com scripts específicos | **Sim** | — |
| Regra simples que deve ser sempre seguida | Não | Rule (`.claude/rules/`) |
| Enforcement determinístico de uma restrição | Não | Hook |
| Informação geral sobre o projeto | Não | CLAUDE.md |
| Contexto dinâmico de sessão | Não | Hook `SessionStart` |

### 4.2 Decisão: Grau de Liberdade

```
A operação é destrutiva ou irreversível?
├── SIM → Baixa liberdade (scripts exatos, sem variação)
│   Exemplos: migrations, deploys, file deletions
└── NÃO → Múltiplas abordagens são válidas?
    ├── SIM → Alta liberdade (instruções textuais, heurísticas)
    │   Exemplos: code review, research, documentation
    └── NÃO → Média liberdade (pseudocode/templates com parâmetros)
        Exemplos: report generation, API calls, data processing
```

### 4.3 Escopo de Aplicação por Tipo de Tarefa

| Tipo de Tarefa | Padrão Recomendado | Referências Necessárias |
|----------------|-------------------|------------------------|
| Análise de dados | Domain-specific organization | Schemas por domínio |
| Processamento de documentos | High-level guide + references | Format guides, scripts |
| Code generation | Template pattern + examples | API docs, examples |
| DevOps/CI | Workflow com checklist | Scripts, configs |
| Research/synthesis | Workflow sem código | Style guide, sources |

## 5. Aplicabilidade à Infraestrutura de Agentes

### 5.1 Skills (Design Patterns)

**Padrão de Evolução de Skills:**

```
v1: SKILL.md monolítico (< 200 linhas)
  ↓ Crescimento natural
v2: SKILL.md + 1-2 reference files (< 500 linhas total em SKILL.md)
  ↓ Mais domínios/casos
v3: SKILL.md (index) + reference/ directory (domain-specific)
  ↓ Complexidade operacional
v4: SKILL.md + reference/ + scripts/ + hooks no frontmatter
```

**Composição de Skills:**

- Skills podem referenciar outros skills indiretamente (via instruções em SKILL.md)
- Skills com `context: fork` executam em subagent isolado — zero impacto no contexto principal
- Skills com `disable-model-invocation: true` mantêm descrições fora do contexto até trigger

**Refactoring Checklist:**

1. SKILL.md acima de 500 linhas? → Split em references
2. Referências com mais de 1 nível? → Flatten para 1 nível
3. Claude ignora algum arquivo? → Remover ou melhorar sinalização
4. Claude relê repetidamente? → Mover para SKILL.md principal
5. Description suficientemente específica? → Adicionar termos-chave e triggers

### 5.2 Hooks

**Como hooks complementam skills:**

| Hook Event | Complemento ao Skill |
|-----------|---------------------|
| `PreToolUse` | Validação de segurança antes de scripts do skill executarem |
| `PostToolUse` | Verificação pós-execução (lint, format, test) |
| `Stop` (agent) | Verificação que o workflow do skill completou corretamente |
| `SessionStart` | Carregamento de estado que o skill precisa |

**Hooks no frontmatter do skill:**

```yaml
---
name: safe-deploy
description: Deploy with safety checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-deploy-cmd.sh"
  Stop:
    - hooks:
        - type: agent
          prompt: "Verify deployment completed. Check health endpoints."
---
```

**Flag `once: true`:** Para hooks de setup que devem rodar apenas uma vez na ativação do skill (ex: verificar dependências instaladas).

### 5.3 Subagents

**Skills que delegam para subagents:**

- Skill principal define workflow e delega investigação para subagents
- `context: fork` garante que o skill executa em subagent isolado
- Subagents herdam hooks definidos no skill frontmatter

**Padrão de Decomposição:**

```
Skill "research-and-implement"
  ├── Fase 1: Delega pesquisa para subagent Explore
  ├── Fase 2: Analisa resultados no contexto principal
  ├── Fase 3: Delega implementação para subagent com worktree
  └── Fase 4: Verifica resultado via hook Stop (agent type)
```

### 5.4 Rules

**Quando rules substituem conteúdo do skill:**

- Regras que se aplicam a TODOS os skills (ex: "always use TypeScript") → Rule global
- Regras específicas de paths que afetam a execução do skill → Rule com `paths:` frontmatter
- Regras que precisam enforcement mais forte → Hook no frontmatter do skill

**Rules que referenciam skills:**

```markdown
# .claude/rules/api-development.md
---
paths: ["src/api/**"]
---
When working with API endpoints, use the /api-development skill for patterns and conventions.
```

### 5.5 Memory

**Skills e o sistema de memória:**

| Interação | Exemplo |
|-----------|---------|
| Skill que consulta memória | Skill de commit verifica `feedback_commit-style.md` para preferências do usuário |
| Skill que gera memória | Skill de onboarding salva descobertas sobre o projeto em memory files |
| Memória que informa trigger | MEMORY.md registra que "usuário prefere skill X para tarefas Y" |

**Padrão: Skill Memory-Aware**

```markdown
# SKILL.md
## Before starting
Check if there are relevant memory files in the project's memory directory
that might inform this task (previous decisions, preferences, constraints).
```

## 6. Aplicabilidade do Guia de Engenharia de Prompts

### 6.1 Mapeamento Técnica → Aspecto do Skill

| Técnica | Aplicação em Skill Authoring | Onde no Skill |
|---------|------------------------------|---------------|
| **Chain-of-Thought** | Workflows multi-passo com checklists | Seções de workflow em SKILL.md |
| **Prompt Chaining** | Fases sequenciais do skill (analyze → plan → execute → verify) | Estrutura de fases do SKILL.md |
| **ReAct** | Skills que usam ferramentas (Read → Analyze → Execute → Verify) | Scripts utilitários + instruções |
| **Least-to-Most** | Decomposição de problemas complexos em sub-tarefas | Padrão de conditional workflow |
| **Self-Consistency** | Validation loops (executar → validar → corrigir → re-validar) | Feedback loops |
| **Tree of Thoughts** | Skills de decisão com múltiplos caminhos | Conditional workflow pattern |
| **Reflexion** | Desenvolvimento iterativo com dois Claudes (observe-refine-test) | Processo de avaliação |
| **Few-shot (Examples)** | Padrão de exemplos input/output no skill | Examples pattern |
| **Structured Output** | Template pattern para formatos de saída | Template pattern |
| **Zero-shot CoT** | "Analyze the code structure and organization" (alta liberdade) | Instruções textuais |

### 6.2 Técnicas por Fase do Skill

**Fase de Discovery (description):**

- Role Prompting implícito: a description define o "papel" do skill
- Zero-shot: description deve ser suficiente sem exemplos

**Fase de Execution (SKILL.md body):**

- Prompt Chaining: fases sequenciais com gates de validação
- ReAct: skills que alternam entre raciocínio e uso de ferramentas
- Least-to-Most: decomposição de tarefas complexas

**Fase de Validation (feedback loops):**

- Self-Consistency: múltiplas execuções do validador
- Reflexion: loop de melhoria iterativa

### 6.3 Quando NÃO Usar Técnicas Avançadas

| Técnica | Por que evitar em skills |
|---------|------------------------|
| Few-shot CoT extenso | Alto custo de tokens; usar referências externas |
| Tree of Thoughts | Complexidade excessiva para maioria dos skills |
| PAL | Skills já podem executar código diretamente |
| Auto-CoT | Skills são escritos manualmente, não auto-gerados |

**Princípio do documento:** "Claude já é muito inteligente." Técnicas avançadas de prompting são frequentemente desnecessárias em skills — instruções claras e concisas geralmente bastam.

## 7. Correlações com Documentos Principais

### 7.1 research-llm-context-optimization.md

| Princípio de Contexto | Implementação no Skill Authoring |
|----------------------|----------------------------------|
| Context como recurso finito | "A janela de contexto é um bem público" — cada token compete |
| Instruction budget ~150-200 | SKILL.md body < 500 linhas; split quando exceder |
| Progressive disclosure | SKILL.md como índice → references carregados sob demanda |
| Lost-in-the-middle | TOC no topo de arquivos longos garante Claude ver escopo completo |
| Context poisoning | Terminologia consistente previne contradições; evitar info time-sensitive |
| JIT documentation | Arquivos de referência carregados apenas quando relevantes |
| Hybrid strategy | Metadata sempre carregada (description) + conteúdo on-demand (SKILL.md + refs) |

### 7.2 Evaluating-AGENTS-paper.md

| Achado do Paper | Alinhamento com Best Practices |
|-----------------|-------------------------------|
| LLM-generated configs reduzem performance | Evaluation-driven development previne over-documentation |
| Mais contexto ≠ melhor performance | Concisão como princípio central; "Claude já é inteligente" |
| Overviews genéricos são ineficazes | Descriptions devem ser específicas com termos-chave |
| Instruções são seguidas literalmente | Graus de liberdade calibrados à fragilidade da tarefa |
| Repositórios nicho se beneficiam mais | Skills mais valiosos para domínios que Claude não conhece |

### 7.3 claude-prompting-best-practices.md

| Best Practice | Implementação no Skill Authoring |
|---------------|----------------------------------|
| Ser direto e específico | Descriptions específicas, sem explicações óbvias |
| Usar exemplos | Examples pattern com input/output pairs |
| Structured output | Template pattern para formatos de saída |
| Pensar passo-a-passo | Workflows com checklists sequenciais |
| Dar ao Claude um papel | Description define o papel implicitamente |

### 7.4 a-guide-to-agents.md / a-guide-to-claude.md

| Princípio dos Guides | Skill Authoring Equivalente |
|---------------------|----------------------------|
| Keep config minimal | SKILL.md < 500 linhas, split em refs |
| Progressive disclosure | 3 padrões de progressive disclosure |
| Don't auto-generate | Evaluation-driven development; iteração humana |
| Stale docs poison context | Evitar info time-sensitive; manter skills atualizados |
| Point elsewhere | SKILL.md como índice apontando para refs |

## 8. Forças e Limitações

### 8.1 Forças

| Força | Detalhe |
|-------|---------|
| **Prático e actionable** | Cada princípio acompanhado de exemplos bom/ruim concretos |
| **Metáforas eficazes** | "Ponte estreita" vs "campo aberto" para graus de liberdade |
| **Metodologia de teste** | Desenvolvimento iterativo com dois Claudes é inovador e prático |
| **Checklist final** | Lista verificável de qualidade antes de compartilhar |
| **Multi-modelo** | Reconhece que skills devem funcionar em Haiku, Sonnet e Opus |
| **Progressive disclosure nativo** | 3 padrões claros com diagramas visuais |

### 8.2 Limitações

| Limitação | Impacto |
|-----------|---------|
| **Sem métricas quantitativas** | "< 500 linhas" é regra empírica sem evidência quantitativa |
| **Foco em skills individuais** | Pouca guidance sobre composição e orquestração de múltiplos skills |
| **Avaliação manual** | "Não há forma built-in de rodar avaliações" — processo inteiramente manual |
| **Sem guidance sobre versionamento** | Como evoluir skills sem quebrar usuários existentes |
| **Coding-centric** | Exemplos majoritariamente de processamento de PDF/dados; pouca cobertura de skills de análise, research, ou criação |
| **Sem integração com hooks** | Menciona hooks no frontmatter mas não explora padrões avançados |
| **Sem métricas de discovery** | Como saber se a description está funcionando (taxa de trigger correto) |

## 9. Recomendações Práticas

### 9.1 Checklist Estendido para Criação de Skills

**Pré-criação:**

- [ ] Executar a tarefa sem skill; documentar onde Claude falha
- [ ] Criar 3+ cenários de avaliação
- [ ] Medir baseline (performance sem skill)
- [ ] Identificar se domínio requer knowledge que Claude não tem

**Estrutura:**

- [ ] `name` em gerúndio, lowercase com hífens, < 64 chars
- [ ] `description` em terceira pessoa, específica, com triggers, < 1024 chars
- [ ] SKILL.md body < 500 linhas
- [ ] Referências a 1 nível de profundidade apenas
- [ ] TOC em arquivos de referência > 100 linhas
- [ ] Organização por domínio para skills multi-domínio

**Conteúdo:**

- [ ] Sem explicações que Claude já sabe
- [ ] Grau de liberdade calibrado à fragilidade
- [ ] Terminologia consistente em todo o skill
- [ ] Sem informação time-sensitive (ou em seção "Old patterns")
- [ ] Exemplos concretos (não abstratos)
- [ ] Workflows com checklists copiáveis
- [ ] Feedback loops para qualidade crítica

**Código (se aplicável):**

- [ ] Scripts que tratam erros (não "punt to Claude")
- [ ] Constantes documentadas (sem magic numbers)
- [ ] Dependências listadas explicitamente
- [ ] Distinção clara entre executar vs ler como referência
- [ ] Plan-validate-execute para operações destrutivas
- [ ] Forward slashes em todos os paths
- [ ] Scripts com mensagens de erro verbose e específicas

**Teste e Iteração:**

- [ ] Testado com Haiku, Sonnet E Opus
- [ ] Testado com cenários reais (não apenas test cases)
- [ ] Observado como Claude navega o skill
- [ ] Iterado com base em observação (não suposições)
- [ ] Feedback de equipe incorporado (se aplicável)

### 9.2 Templates Reutilizáveis

**Template: Skill Simples (sem código)**

```markdown
---
name: reviewing-pull-requests
description: Reviews pull requests for code quality, security, and conventions. Use when the user asks to review a PR, check code changes, or evaluate merge readiness.
---

# Pull Request Review

## Process
1. Read the diff completely before commenting
2. Check for security issues (OWASP Top 10)
3. Verify adherence to project conventions
4. Assess test coverage for changed code
5. Provide actionable feedback with specific suggestions

## Conventions
See [conventions.md](conventions.md) for project-specific rules.

## Common Issues
See [common-issues.md](common-issues.md) for frequently caught problems.
```

**Template: Skill com Scripts**

```markdown
---
name: processing-data-exports
description: Processes and validates data exports from the analytics pipeline. Use when working with CSV/JSON export files or when the user mentions data validation, export processing, or pipeline output.
---

# Data Export Processing

## Quick start
Run the validation script on any export file:
```bash
python scripts/validate_export.py input.csv
```

## Workflow

- [ ] Step 1: Validate format (`validate_export.py`)
- [ ] Step 2: Check data quality (`check_quality.py`)
- [ ] Step 3: Transform if needed (`transform.py`)
- [ ] Step 4: Generate report (`report.py`)

## Schemas

See [reference/schemas.md](reference/schemas.md) for expected data formats.

## Error handling

See [reference/errors.md](reference/errors.md) for common validation errors and fixes.

```

**Template: Skill com Hooks**

```yaml
---
name: deploying-services
description: Deploys services with safety checks and rollback capability. Use when deploying, releasing, or pushing to production environments.
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-deploy-command.sh"
  Stop:
    - hooks:
        - type: agent
          prompt: "Verify deployment health. Check endpoints respond correctly. $ARGUMENTS"
          timeout: 120
---
```

### 9.3 Padrão de Evolução Recomendado

```
Semana 1: Criar skill mínimo + 3 avaliações
  ↓ Testar com Claude B, observar
Semana 2: Refinar com Claude A baseado em observações
  ↓ Adicionar referências onde Claude falhou
Semana 3: Adicionar scripts para operações repetitivas
  ↓ Adicionar feedback loops para qualidade
Semana 4: Adicionar hooks no frontmatter para enforcement
  ↓ Compartilhar com equipe, coletar feedback
Semana 5+: Iteração contínua baseada em uso real
```
