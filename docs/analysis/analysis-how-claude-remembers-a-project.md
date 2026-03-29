# Analise: Como o Claude Lembra de um Projeto

---

## 1. Resumo Executivo

O documento "How Claude Remembers Your Project" descreve os dois mecanismos complementares de persistencia de conhecimento cross-session do Claude Code: **CLAUDE.md files** (instrucoes escritas pelo usuario) e **Auto Memory** (notas escritas pelo Claude automaticamente). Ambos sao carregados no inicio de cada sessao como contexto -- nao como configuracao forcada -- e sua eficacia depende diretamente da especificidade, concisao e estruturacao das instrucoes.

O sistema de memoria implementa uma arquitetura hibrida de duas camadas: **always-loaded** (CLAUDE.md, primeiras 200 linhas de MEMORY.md) e **on-demand** (subdirectory CLAUDE.md, topic files de memoria, path-scoped rules). Essa arquitetura e uma implementacao direta do principio de Just-In-Time documentation descrito pela Anthropic: manter identificadores leves e carregar dados sob demanda em runtime. A hierarquia de escopo (managed policy > project > user > subdirectory) permite configuracao granular desde nivel organizacional ate area especifica do codebase.

A auto memory introduz um mecanismo elegante de documentacao emergente: o Claude decide o que vale lembrar com base em valor cross-session, armazena em MEMORY.md (index) + topic files (detalhes), e curadoria automaticamente para manter o index sob 200 linhas. Cada projeto git compartilha um unico diretorio de auto memory (todos os worktrees e subdiretorios). O sistema e machine-local, plain markdown, editavel por humanos a qualquer momento.

---

## 2. Conceitos e Mecanismos Chave

### 2.1 Dois Sistemas Complementares

| | CLAUDE.md | Auto Memory |
|---|-----------|-------------|
| **Quem escreve** | Usuario | Claude |
| **Conteudo** | Instrucoes e regras | Aprendizados e padroes |
| **Escopo** | Projeto, usuario, ou organizacao | Por working tree |
| **Carregado em** | Toda sessao (completo) | Toda sessao (primeiras 200 linhas) |
| **Usar para** | Padroes de codigo, workflows, arquitetura | Comandos de build, insights de debug, preferencias |

### 2.2 Hierarquia de CLAUDE.md

| Escopo | Localizacao | Proposito | Compartilhado com |
|--------|-------------|-----------|-------------------|
| **Managed policy** | `/etc/claude-code/CLAUDE.md` (Linux/WSL) | Instrucoes organizacionais (IT/DevOps) | Todos os usuarios |
| **Project** | `./CLAUDE.md` ou `./.claude/CLAUDE.md` | Instrucoes compartilhadas do projeto | Time via VCS |
| **User** | `~/.claude/CLAUDE.md` | Preferencias pessoais | Apenas voce |
| **Subdirectory** | `./subdir/CLAUDE.md` | Area-especifica, on-demand | Time via VCS |

- CLAUDE.md na hierarquia de diretorios acima do working directory: carregados em full no launch
- CLAUDE.md em subdiretorios: carregados on-demand quando Claude le arquivos nessas pastas
- Managed policy: NAO pode ser excluido via `claudeMdExcludes`

### 2.3 Sistema de Rules

```
.claude/
├── CLAUDE.md           # Instrucoes principais do projeto
└── rules/
    ├── code-style.md   # Diretrizes de estilo
    ├── testing.md       # Convencoes de teste
    ├── security.md      # Requisitos de seguranca
    └── frontend/
        └── react.md     # Rules especificas de frontend
```

**Rules sem `paths` frontmatter**: carregadas incondicionalmente no launch
**Rules com `paths` frontmatter**: carregadas quando Claude le arquivos correspondentes

```yaml
---
paths:
  - "src/api/**/*.ts"
---
# API Development Rules
- All API endpoints must include input validation
```

Patterns suportados:

| Pattern | Match |
|---------|-------|
| `**/*.ts` | Todos os TypeScript em qualquer diretorio |
| `src/**/*` | Todos os arquivos sob `src/` |
| `*.md` | Markdown no root do projeto |
| `src/components/*.tsx` | Components React em diretorio especifico |

### 2.4 Sistema de Imports

CLAUDE.md suporta `@path/to/import`:

- Paths relativos (relativo ao arquivo que contem o import)
- Paths absolutos
- Imports recursivos (max 5 hops)
- Imports pessoais: `@~/.claude/my-project-instructions.md`

```markdown
See @README for project overview and @package.json for available npm commands.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

### 2.5 Auto Memory

**Localizacao**: `~/.claude/projects/<project>/memory/`
**Estrutura**:

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Index conciso, carregado toda sessao
├── debugging.md       # Notas detalhadas sobre debugging
├── api-conventions.md # Decisoes de design de API
└── ...                # Outros topic files
```

- `MEMORY.md` (primeiras 200 linhas): carregado no startup
- Topic files: carregados sob demanda pelo Claude
- Compartilhado entre worktrees e subdiretorios do mesmo repo git
- Machine-local (nao compartilhado entre maquinas)
- Plain markdown editavel a qualquer momento

### 2.6 Compactacao e CLAUDE.md

CLAUDE.md **sobrevive integralmente a compactacao**. Apos `/compact`, o Claude rele CLAUDE.md do disco e re-injeta fresco na sessao. Instrucoes dadas apenas em conversacao (nao escritas em CLAUDE.md) sao perdidas apos compactacao.

### 2.7 Exclusoes para Monorepos

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

Configuravel em qualquer camada de settings. Arrays mergeiam entre camadas. Managed policy CLAUDE.md NAO pode ser excluido.

### 2.8 Diretrizes de Escrita Eficaz

- **Tamanho**: maximo 200 linhas por arquivo CLAUDE.md
- **Estrutura**: headers e bullets Markdown
- **Especificidade**: "Use 2-space indentation" ao inves de "Format code properly"
- **Consistencia**: eliminar instrucoes contraditorias entre arquivos
- **Verificabilidade**: cada instrucao deve ser concreta o suficiente para verificar

---

## 3. Pontos de Atencao

### 3.1 CLAUDE.md NAO e Configuracao Forcada

O ponto mais critico: CLAUDE.md e entregue como user message apos o system prompt, nao como parte do system prompt. O Claude le e tenta seguir, mas NAO ha garantia de compliance estrito, especialmente para instrucoes vagas ou conflitantes.

> "CLAUDE.md instructions shape Claude's behavior but are not a hard enforcement layer."

Para enforcement deterministic, use **hooks** (que executam fora do modelo) ou **permissions** (em settings.json).

### 3.2 O Limite de 200 Linhas

CLAUDE.md e carregado integralmente independentemente do tamanho. Porem, arquivos maiores que 200 linhas:

- Consomem mais contexto
- Reduzem aderencia as instrucoes
- Instrucoes importantes se perdem no ruido

O limite de 200 linhas se aplica APENAS ao MEMORY.md de auto memory (conteudo alem da linha 200 nao e carregado no startup).

### 3.3 Contradices entre Arquivos

Se dois arquivos CLAUDE.md, rules, ou combinacoes deles dao instrucoes contraditorias, o Claude pode escolher arbitrariamente. Revisao periodica e obrigatoria.

### 3.4 Auto Memory Nao e Compartilhada

Auto memory e machine-local. Worktrees do mesmo repo compartilham, mas maquinas diferentes nao. Para conhecimento compartilhado, use CLAUDE.md commitado no VCS.

### 3.5 Ordem de Carregamento Importa

CLAUDE.md na hierarquia acima do working directory: carregados no launch (completos).
Subdirectory CLAUDE.md: carregados on-demand (quando Claude le arquivos naquela pasta).
Rules sem paths: carregados no launch.
Rules com paths: carregados quando Claude trabalha com arquivos correspondentes.

O efeito "lost in the middle" implica que instrucoes no meio de arquivos longos tem menor probabilidade de serem seguidas.

### 3.6 Compactacao Preserva CLAUDE.md mas Perde Conversacao

CLAUDE.md sobrevive `/compact`. Instrucoes dadas apenas em conversacao NAO sobrevivem. Se uma instrucao e importante o suficiente para persistir, deve ser escrita em CLAUDE.md.

### 3.7 `/init` e o Modo Interativo

O comando `/init` gera um CLAUDE.md inicial analisando o codebase. Com `CLAUDE_CODE_NEW_INIT=true`, ativa um fluxo multi-fase interativo que tambem configura skills e hooks. Se CLAUDE.md ja existe, `/init` sugere melhorias ao inves de sobrescrever.

---

## 4. Casos de Uso e Escopo

### 4.1 Quando Usar CLAUDE.md vs Auto Memory vs Rules

| Cenario | Mecanismo | Justificativa |
|---------|-----------|---------------|
| Padroes de codigo do projeto | CLAUDE.md (project) | Compartilhavel via VCS, aplica-se a todos |
| Comando de build especifico | Auto Memory | Claude descobre e lembra automaticamente |
| Rules de API por diretorio | `.claude/rules/` com `paths` | Carregado apenas quando relevante |
| Preferencias pessoais de estilo | `~/.claude/CLAUDE.md` | Pessoal, cross-projeto |
| Politica de seguranca organizacional | Managed policy | Nao pode ser excluido, aplica-se a todos |
| Insights de debugging recorrentes | Auto Memory topic file | Claude carrega quando relevante |

### 4.2 Quando Converter Instrucoes em Hooks

Criterio: se enforcement deterministic e necessario e a instrucao pode ser verificada programaticamente, converta para hook.

| Instrucao em CLAUDE.md | Hook Equivalente |
|------------------------|------------------|
| "Run linter after editing" | `PostToolUse` com matcher `Edit\|Write` |
| "Never commit .env files" | `PreToolUse` com matcher `Bash` + validacao |
| "Run tests before pushing" | `PreToolUse` com matcher `Bash` + deteccao de push |

Hooks removem a instrucao do orcamento de contexto e garantem enforcement independente do modelo.

### 4.3 Organizacao para Times Grandes

1. **Managed policy**: padroes organizacionais (seguranca, compliance)
2. **Project CLAUDE.md**: arquitetura, convencoes, workflows do projeto
3. **`.claude/rules/`**: rules modulares por topico e path-scoped
4. **User CLAUDE.md**: preferencias pessoais
5. **`claudeMdExcludes`**: filtrar rules de outros times em monorepos

---

## 5. Aplicabilidade a Infraestrutura de Agentes

### 5.1 Skills

- **Skills como progressive disclosure**: Descricoes de skills sao vistas no startup; conteudo completo so carrega quando invocadas. Isso e coerente com a filosofia JIT do sistema de memoria.
- **Skills com `disable-model-invocation: true`**: Descricoes ficam completamente fora do contexto ate invocacao manual -- complementa a estrategia de manter CLAUDE.md conciso.
- **Skills vs rules**: Rules carregam toda sessao ou quando path faz match; skills carregam quando invocadas ou quando Claude determina relevancia. Para instrucoes que nao precisam estar sempre em contexto, skills sao prefereis a rules.
- **Dynamic injection em skills**: `` !`command` `` carrega dados em tempo real, implementando JIT puro.

### 5.2 Hooks

- **Hooks como alternativa a CLAUDE.md**: Instrucoes que podem ser verificadas programaticamente devem ser convertidas de CLAUDE.md para hooks. Isso remove a instrucao do orcamento de contexto e garante enforcement.
- **`InstructionsLoaded` hook**: Permite logar quais arquivos de instrucoes foram carregados, quando, e por que. Util para debugging de rules path-scoped ou lazy-loaded.
- **Hooks para higiene de memoria**: `PostToolUse` pode ser usado para atualizar auto memory apos operacoes significativas.
- **Plugin lifecycle hooks**: Hooks de plugins sao carregados na sessao normalmente e interagem com o sistema de memoria da mesma forma.

### 5.3 Subagentes

- **Memoria de subagentes**: Tres escopos (user, project, local) com mesmo mecanismo MEMORY.md + topic files
- **Subagentes e CLAUDE.md**: Subagentes carregam CLAUDE.md e project memory via fluxo normal de mensagens (NAO herdam historico de conversa)
- **Auto memory de subagentes**: Habilitavel via `memory` field no frontmatter. Cada subagente pode ter seu proprio diretorio de memoria.
- **Subagentes e rules**: Path-scoped rules sao ativadas quando o subagente le arquivos correspondentes

### 5.4 Rules

- **Rules como modularidade de CLAUDE.md**: Quando CLAUDE.md fica grande, rules permitem extrair instrucoes topicas
- **Path-scoped rules**: Implementam progressive disclosure nativo -- so carregam quando relevantes
- **Symlinks para compartilhamento**: Rules suportam symlinks, permitindo rules compartilhadas entre projetos
- **User-level rules**: `~/.claude/rules/` para preferencias pessoais cross-projeto
- **Prioridade**: user rules < project rules (project tem prioridade maior)
- **Discovery recursivo**: Rules em subdiretorios de `.claude/rules/` sao descobertas automaticamente

### 5.5 Memoria

- **Arquitetura two-tier**: MEMORY.md (index, always-loaded, 200 lines) + topic files (on-demand)
- **JIT documentation**: Implementacao direta do padrao descrito pela Anthropic em "Effective Context Engineering"
- **Auto-curadoria**: Claude move detalhes para topic files e mantem MEMORY.md conciso
- **Scope hierarquico**: Auto memory e machine-local; CLAUDE.md e compartilhavel via VCS
- **Compactacao**: CLAUDE.md sobrevive integralmente; auto memory nao e afetada (armazenada separadamente)
- **Higiene**: `/memory` para inspecionar e editar; revisao periodica recomendada
- **Worktrees**: Todos os worktrees do mesmo repo git compartilham auto memory

---

## 6. Aplicabilidade do Guia de Engenharia de Prompts

### 6.1 CoT para Cadeias de Raciocinio de Subagentes

CLAUDE.md pode incluir instrucoes de CoT que serao carregadas em toda sessao: "Antes de fazer mudancas, pense passo a passo sobre o impacto." Auto memory pode armazenar cadeias de raciocinio que funcionaram bem em sessoes anteriores, servindo como few-shot CoT emergente.

### 6.2 ReAct para Subagentes com Acesso a Ferramentas

O sistema de memoria suporta o loop ReAct indiretamente: CLAUDE.md pode definir o workflow esperado (Pensamento -> Acao -> Observacao) e auto memory pode lembrar quais ferramentas foram eficazes para quais tarefas. Path-scoped rules podem injetar instrucoes ReAct-especificas quando o Claude trabalha em areas que requerem interacao com ferramentas.

### 6.3 Tree of Thoughts para Subagentes de Exploracao

CLAUDE.md pode instruir o Claude a considerar multiplas abordagens antes de escolher. Auto memory pode armazenar hipoteses exploradas em sessoes anteriores, prevenindo re-exploracao de caminhos ja descartados.

### 6.4 Self-Consistency para Validacao entre Multiplos Subagentes

A auto memory serve como registro historico que pode ser usado para validacao de consistencia: se uma decisao em uma sessao contradiz uma decisao anterior armazenada em memoria, o Claude pode identificar e resolver a inconsistencia.

### 6.5 Reflexion para Melhoria Iterativa de Subagentes

Auto memory e o mecanismo nativo de Reflexion cross-session:

1. Claude comete um erro -> usuario corrige -> Claude armazena aprendizado em auto memory
2. Proxima sessao -> Claude consulta auto memory -> evita o mesmo erro

O `/memory` permite ao usuario auditar e refinar esse processo de reflexion.

### 6.6 Least-to-Most para Decomposicao de Tarefas entre Subagentes

CLAUDE.md pode definir a decomposicao padrao de tarefas para o projeto. Rules path-scoped podem fornecer instrucoes especificas de decomposicao por area do codebase. Auto memory pode lembrar decomposicoes que funcionaram bem anteriormente.

---

## 7. Correlacoes com os Documentos Principais

### Com "Creating Custom Subagents"

A memoria de subagentes (campo `memory` no frontmatter) e um caso especial do sistema de auto memory. Mecanismo identico (MEMORY.md + topic files, 200 linhas), mas com escopos diferentes (user/project/local no subagente vs per-working-tree na auto memory principal). CLAUDE.md e rules sao carregados normalmente por subagentes via fluxo de mensagens.

### Com "Orchestrate Teams of Claude Code Sessions"

Cada teammate em agent teams carrega CLAUDE.md e auto memory independentemente. O spawn prompt do team lead NAO e armazenado em memoria -- apenas em CLAUDE.md que os teammates carregam. Multiplos teammates escrevendo auto memory podem criar redundancia.

### Com "Research: Subagent Best Practices"

O research enfatiza que o system prompt do subagente e TUDO que ele tem (NAO recebe historico). CLAUDE.md mitiga parcialmente esse gap, fornecendo contexto persistente do projeto. A recomendacao de "Consult memory before starting" no prompt do subagente complementa o mecanismo de auto memory de subagentes.

### Com "Create Plugins"

Plugins possuem `settings.json` que pode configurar `autoMemoryEnabled` e `autoMemoryDirectory`. Skills de plugins sao progressive disclosure (descricao no startup, conteudo on-demand), alinhando com a filosofia JIT da auto memory.

### Com "Research: LLM Context Optimization"

Correlacoes mais diretas:

- **200 linhas de CLAUDE.md**: alinha com o "instruction budget" de ~2.000-4.000 tokens
- **Path-scoped rules**: implementam "progressive disclosure" formal
- **Auto memory MEMORY.md + topic files**: implementam "just-in-time documentation"
- **Compactacao**: implementa "context recycling"
- **`claudeMdExcludes`**: previne "context poisoning" por instrucoes irrelevantes
- **Lost in the middle**: justifica headers e bullets (estrutura facilita atencao)
- **Quality over quantity**: "para cada linha, pergunte se remover causaria erros"

---

## 8. Forcas e Limitacoes

### Forcas

1. **Simplicidade elegante**: Arquivos markdown editaveis, sem banco de dados ou formato proprietario
2. **Hierarquia de escopo**: Managed > project > user > subdirectory cobre todos os cenarios
3. **Progressive disclosure nativo**: Path-scoped rules + subdirectory CLAUDE.md
4. **Auto-curadoria**: Claude gerencia MEMORY.md autonomamente
5. **Sobrevive a compactacao**: CLAUDE.md e relido do disco apos compact
6. **Sistema de imports**: `@path` permite composicao flexivel
7. **Symlinks para compartilhamento**: Rules podem ser compartilhadas entre projetos
8. **`/memory` command**: Interface integrada para inspecao e edicao

### Limitacoes

1. **Nao e enforcement**: CLAUDE.md e advisory, nao deterministic -- modelo pode ignorar instrucoes
2. **Machine-local**: Auto memory nao sincroniza entre maquinas
3. **Limite de 200 linhas**: MEMORY.md alem de 200 linhas nao e carregado automaticamente
4. **Sem merge de conflitos**: Multiplos agents/worktrees escrevendo auto memory simultaneamente podem conflitar
5. **Sem versionamento**: Auto memory nao tem historico de mudancas (exceto se commitada via project scope)
6. **Contradices silenciosas**: Instrucoes conflitantes sao resolvidas arbitrariamente sem aviso
7. **Custo de contexto**: CLAUDE.md longo consome tokens do orcamento de atencao

---

## 9. Recomendacoes Praticas

### 9.1 Estrutura Recomendada de CLAUDE.md

```markdown
# Project Name

## Build & Test
- `npm install` para dependencias
- `npm test` para rodar testes
- `npm run lint` para linting

## Architecture
- API handlers: `src/api/handlers/`
- Components: `src/components/`
- Testes: `tests/`

## Code Style
- 2-space indentation
- Named exports (nao default exports)
- Async/await (nao .then chains)

## Conventions
- Commits atomicos com conventional commit format
- PRs devem ter testes para novas features
- Reviews requeridas antes de merge
```

Mantenha sob 200 linhas. Para detalhes, use `@path` imports ou `.claude/rules/`.

### 9.2 Padrao de Rules Path-Scoped

```markdown
<!-- .claude/rules/api-validation.md -->
---
paths:
  - "src/api/**/*.ts"
---

# API Validation Rules
- All endpoints must validate input with zod schemas
- Error responses follow the standard format in src/api/errors.ts
- Include rate limiting metadata in response headers
```

```markdown
<!-- .claude/rules/react-components.md -->
---
paths:
  - "src/components/**/*.tsx"
---

# React Component Rules
- Use functional components with hooks
- Props types defined with TypeScript interfaces (not type aliases)
- Extract custom hooks to src/hooks/
```

### 9.3 Estrategia de Conversao CLAUDE.md -> Hooks

Auditoria periodica:

1. Listar todas as instrucoes no CLAUDE.md
2. Para cada instrucao, perguntar: "Isso pode ser verificado programaticamente?"
3. Se SIM: converter para hook `PreToolUse` ou `PostToolUse`
4. Se NAO: manter em CLAUDE.md
5. Resultado: CLAUDE.md menor, hooks deterministic, orcamento de contexto otimizado

### 9.4 Higiene de Auto Memory

1. Executar `/memory` periodicamente para revisar o que Claude armazenou
2. Remover entradas desatualizadas ou incorretas
3. Consolidar entradas redundantes
4. Verificar que MEMORY.md esta sob 200 linhas
5. Considerar mover conhecimento valioso para CLAUDE.md (onde sera carregado integralmente)

### 9.5 Monorepo: Isolamento de Contexto

```json
// .claude/settings.local.json (nao commitado)
{
  "claudeMdExcludes": [
    "**/other-team/CLAUDE.md",
    "**/legacy-service/.claude/rules/**",
    "**/infrastructure/CLAUDE.md"
  ]
}
```

Combine com path-scoped rules para garantir que apenas instrucoes relevantes a sua area de trabalho sejam carregadas.
