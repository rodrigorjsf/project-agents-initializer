# Analise: Orquestracao de Times de Agentes no Claude Code

---

## 1. Resumo Executivo

O documento sobre orquestracao de times de agentes (Agent Teams) descreve um mecanismo experimental do Claude Code (v2.1.32+) que permite coordenar multiplas instancias do Claude Code trabalhando em paralelo. Diferentemente dos subagentes tradicionais -- que operam em modelo hub-and-spoke reportando resultados apenas ao agente principal -- os agent teams implementam comunicacao peer-to-peer entre teammates, com lista de tarefas compartilhada e auto-coordenacao. A arquitetura consiste em um team lead (sessao principal), teammates (instancias independentes), task list (lista compartilhada com estados pending/in-progress/completed e dependencias) e mailbox (sistema de mensagens entre agentes).

O custo de tokens escala linearmente com o numero de teammates, pois cada um possui sua propria janela de contexto. A Anthropic recomenda iniciar com 3-5 teammates e 5-6 tarefas por teammate. Os melhores casos de uso incluem pesquisa paralela, features independentes, debugging com hipoteses concorrentes e coordenacao cross-layer (frontend/backend/testes). O mecanismo introduz hooks especificos (`TeammateIdle`, `TaskCompleted`) que permitem quality gates automatizados.

A principal implicacao arquitetural e que agent teams resolvem o problema de comunicacao entre workers que subagentes nao conseguem resolver, ao custo de maior complexidade e consumo de tokens. A decisao entre subagentes e agent teams deve ser guiada pela necessidade de comunicacao inter-worker: se os workers precisam apenas reportar resultados, subagentes bastam; se precisam debater, desafiar e coordenar entre si, agent teams sao a escolha correta.

---

## 2. Conceitos e Mecanismos Chave

### 2.1 Arquitetura do Time

| Componente | Funcao | Analogia |
|------------|--------|----------|
| **Team Lead** | Sessao principal que cria o time, spawna teammates e coordena trabalho | Gerente de projeto |
| **Teammates** | Instancias independentes do Claude Code com contexto proprio | Desenvolvedores especializados |
| **Task List** | Lista compartilhada com estados e dependencias | Board do Kanban |
| **Mailbox** | Sistema de mensagens inter-agentes | Slack do time |

### 2.2 Ciclo de Vida do Time

```
1. Usuario solicita criacao do time com descricao da tarefa
2. Lead analisa e cria task list com dependencias
3. Lead spawna teammates com prompts especificos
4. Teammates auto-claimam tarefas (file locking previne race conditions)
5. Teammates comunicam-se diretamente via mensagens
6. Lead sintetiza resultados
7. Lead solicita shutdown dos teammates
8. Lead executa cleanup dos recursos compartilhados
```

### 2.3 Modos de Exibicao

- **In-process**: todos os teammates rodam no mesmo terminal; `Shift+Down` para navegar
- **Split panes**: cada teammate em painel separado via tmux ou iTerm2

### 2.4 Coordenacao de Tarefas

As tarefas possuem tres estados (pending, in progress, completed) e suportam dependencias. O sistema desbloqueia tarefas automaticamente quando dependencias sao completadas. O file locking previne que multiplos teammates tentem clamar a mesma tarefa simultaneamente.

### 2.5 Controle de Qualidade via Hooks

```json
{
  "hooks": {
    "TeammateIdle": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/check-teammate-output.sh" }
        ]
      }
    ],
    "TaskCompleted": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/validate-task-quality.sh" }
        ]
      }
    ]
  }
}
```

- `TeammateIdle`: executa quando teammate vai ficar idle; exit code 2 envia feedback e mantem o teammate trabalhando
- `TaskCompleted`: executa quando tarefa sera marcada como completa; exit code 2 previne a conclusao

### 2.6 Plan Approval

Para tarefas criticas, e possivel exigir que teammates planejem antes de implementar:

```text
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

O lead aprova ou rejeita o plano autonomamente com base em criterios fornecidos pelo usuario.

---

## 3. Pontos de Atencao

### 3.1 Custo de Tokens

**O maior risco operacional.** Cada teammate consome tokens independentemente. Com 5 teammates, o custo pode ser 5-6x maior que uma sessao unica (overhead de coordenacao incluso). Nao ha mecanismo de compactacao inter-times -- cada janela e independente.

### 3.2 Conflitos de Arquivo

Dois teammates editando o mesmo arquivo gera sobrescrita. A documentacao e explicita: "Break the work so each teammate owns a different set of files." Nao ha merge automatico ou deteccao de conflitos.

### 3.3 Limitacoes Experimentais Criticas

- **Sem resumo de sessao**: `/resume` e `/rewind` nao restauram teammates in-process
- **Status de tarefas pode ficar desatualizado**: teammates as vezes nao marcam tarefas como completas
- **Um time por sessao**: nao e possivel gerenciar multiplos times simultaneamente
- **Sem times aninhados**: teammates nao podem spawnar seus proprios times
- **Lead e fixo**: nao e possivel transferir lideranca
- **Shutdown pode ser lento**: teammates terminam a requisicao atual antes de parar
- **Split panes nao funcionam no VS Code terminal, Windows Terminal ou Ghostty**

### 3.4 Armadilha do Lead que Implementa

O lead pode comecar a implementar tarefas ao inves de delegar. Mitigacao: "Wait for your teammates to complete their tasks before proceeding."

### 3.5 Orcamento de Contexto

Cada teammate carrega CLAUDE.md, MCP servers e skills no startup -- mas NAO herda o historico de conversacao do lead. O spawn prompt deve conter todo o contexto necessario para a tarefa.

---

## 4. Casos de Uso e Escopo

### 4.1 Quando Usar Agent Teams

| Cenario | Adequacao | Justificativa |
|---------|-----------|---------------|
| Code review paralelo (seguranca + performance + testes) | Alta | Lentes independentes, sintese valiosa |
| Debugging com hipoteses concorrentes | Alta | Debate ativo previne anchoring bias |
| Features independentes em modulos distintos | Alta | Cada teammate possui arquivos distintos |
| Coordenacao frontend/backend/testes | Alta | Cross-layer com dependencias gerenciaveis |
| Tarefas sequenciais com dependencias fortes | Baixa | Overhead de coordenacao supera beneficio |
| Edicoes no mesmo arquivo | Baixa | Conflitos de sobrescrita |
| Tarefas simples e rapidas | Baixa | Custo de tokens desproporcional |

### 4.2 Criterios de Decisao: Subagentes vs Agent Teams

```
Pergunta 1: Os workers precisam se comunicar entre si?
  NAO -> Subagentes
  SIM -> Pergunta 2

Pergunta 2: O trabalho envolve debater/desafiar descobertas?
  NAO -> Subagentes com sintese pelo main agent
  SIM -> Agent Teams

Pergunta 3: O custo de tokens e aceitavel (5-6x)?
  NAO -> Subagentes com execucao sequencial
  SIM -> Agent Teams
```

---

## 5. Aplicabilidade a Infraestrutura de Agentes

### 5.1 Skills

- **Skills que delegam a subagentes**: Agent teams sao uma alternativa quando a skill requer multiplas perspectivas coordenadas (ex: skill de design review que spawna architect + UX + devil's advocate)
- **Plugin-provided skills**: Skills de plugins podem iniciar agent teams se o plugin for habilitado e a flag experimental estiver ativa
- **Memory-informed skills**: Cada teammate carrega CLAUDE.md e auto memory independentemente, permitindo que skills baseadas em memoria funcionem em cada contexto separadamente

### 5.2 Hooks

- **Hooks em contexto de agent teams**: `TeammateIdle` e `TaskCompleted` sao hooks exclusivos de agent teams, sem equivalente em subagentes
- **Memory-triggered hooks**: Nao ha suporte direto, mas `PostToolUse` pode ser usado para acionar atualizacoes de memoria quando teammates completam tarefas
- **Plugin lifecycle hooks**: Hooks de plugins sao carregados por cada teammate da mesma forma que em sessoes normais

### 5.3 Subagentes

- **Padrao de orquestracao**: Agent teams implementam o padrao Orchestrator-Workers da Anthropic com comunicacao peer-to-peer adicionada
- **Delegacao**: O lead delega via task list (nao via Agent tool como subagentes); teammates auto-claimam
- **Sintese de resultados**: O lead sintetiza findings de multiplos teammates -- diferente de subagentes onde cada resultado volta individualmente
- **Execucao paralela**: Agent teams sao nativamente paralelos com coordenacao; subagentes podem rodar em paralelo mas sem comunicacao
- **Isolamento via worktree**: Cada teammate pode operar em worktree separada, mas a feature nao e explicitamente documentada para teams (apenas subagentes possuem `isolation: worktree`)

### 5.4 Rules

- **Rules em contexto de teammates**: Cada teammate carrega `.claude/rules/` como uma sessao normal
- **Plugin-scoped rules**: Rules de plugins sao carregadas normalmente por cada teammate
- **Memory-informed rules**: Rules path-scoped sao ativadas independentemente por cada teammate conforme trabalham em arquivos diferentes

### 5.5 Memoria

- **Arquitetura de memoria**: Cada teammate possui sua propria janela de contexto e carrega auto memory independentemente
- **Indexacao**: MEMORY.md (primeiras 200 linhas) e carregado no startup de cada teammate
- **On-demand loading**: Topic files de memoria sao carregados sob demanda por cada teammate
- **Persistencia cross-session**: Limitada -- `/resume` nao restaura teammates; porem, auto memory persiste entre sessoes
- **Higiene de memoria**: Com multiplos teammates escrevendo em auto memory simultaneamente, ha risco de conflitos ou redundancia

---

## 6. Aplicabilidade do Guia de Engenharia de Prompts

### 6.1 CoT para Cadeias de Raciocinio de Subagentes

Agent teams beneficiam-se de CoT no spawn prompt de cada teammate: "Caminhe pelo problema passo a passo antes de propor solucoes." O CoT ajuda teammates a fundamentar seu raciocinio antes de comunicar findings ao time, reduzindo ruido na comunicacao inter-agentes.

### 6.2 ReAct para Subagentes com Acesso a Ferramentas

Cada teammate opera num loop ReAct nativo (Pensamento -> Acao -> Observacao). O spawn prompt deve encorajar o ciclo explicito: "Primeiro explore os arquivos relevantes, analise os padroes, e so entao proponha mudancas." Isso e especialmente importante porque teammates nao herdam contexto do lead.

### 6.3 Tree of Thoughts para Subagentes de Exploracao

O caso de uso "debugging com hipoteses concorrentes" e uma implementacao natural de Tree of Thoughts distribuida: cada teammate explora um ramo da arvore de hipoteses. O debate entre teammates funciona como o mecanismo de avaliacao e backtracking do ToT.

**Exemplo pratico**:

```text
Spawn 5 teammates to investigate different hypotheses about the crash.
Have them talk to each other to try to disprove each other's theories.
```

Cada teammate e um no da arvore; a comunicacao peer-to-peer implementa a avaliacao cruzada.

### 6.4 Self-Consistency para Validacao entre Multiplos Subagentes

Agent teams implementam Self-Consistency de forma natural quando multiplos teammates investigam o mesmo problema e convergem (ou divergem). O lead pode sintetizar via votacao majoritaria: se 3 de 5 teammates apontam a mesma causa raiz, a confianca na conclusao aumenta.

### 6.5 Reflexion para Melhoria Iterativa de Subagentes

Os hooks `TaskCompleted` e `TeammateIdle` implementam parcialmente Reflexion: o hook pode rejeitar a conclusao (exit code 2), forcando o teammate a refletir e iterar. Combinado com plan approval, cria um loop gerar -> avaliar -> refinar.

### 6.6 Least-to-Most para Decomposicao de Tarefas entre Subagentes

A task list com dependencias implementa Least-to-Most naturalmente: tarefas simples sao completadas primeiro, desbloqueando tarefas mais complexas que dependem delas. O lead pode decompor um problema complexo em subtarefas ordenadas por dependencia.

---

## 7. Correlacoes com os Documentos Principais

### Com "Creating Custom Subagents"

A relacao e de complementaridade direta. Subagentes sao para tarefas focadas com resultado reportado ao caller; agent teams sao para trabalho complexo com comunicacao. A tabela comparativa do documento e essencial para a tomada de decisao. Subagentes individuais dentro de agent teams herdam o mesmo modelo de contexto isolado dos subagentes customizados.

### Com "Research: Subagent Best Practices"

O documento de best practices enfatiza que subagentes nao podem spawnar outros subagentes. Agent teams superam essa limitacao permitindo comunicacao direta entre teammates, mas com custo maior. Os anti-patterns documentados (god agents, descricoes vagas) aplicam-se igualmente ao spawn de teammates.

### Com "How Claude Remembers a Project"

Agent teams carregam CLAUDE.md e auto memory da mesma forma que sessoes normais. A limitacao critica e que teammates nao herdam o historico do lead, exigindo que o spawn prompt contenha todo o contexto necessario. A auto memory pode ser atualizada por multiplos teammates, criando risco de conflito.

### Com "Create Plugins"

Plugins sao carregados normalmente por cada teammate. Skills de plugins podem ser invocadas em contexto de teams. Hooks de plugins (`TeammateIdle`, `TaskCompleted`) oferecem extensibilidade especifica para agent teams.

### Com "Research: LLM Context Optimization"

A relacao mais critica e com o conceito de "context rot". Cada teammate inicia com contexto limpo (prevenindo context rot), mas o custo e linear. O conceito de "attention budget" da Anthropic implica que o custo de atencao total de um time e a soma dos orcamentos individuais, sem compartilhamento eficiente.

---

## 8. Forcas e Limitacoes

### Forcas

1. **Comunicacao peer-to-peer** resolve problemas que subagentes hub-and-spoke nao conseguem
2. **Task list compartilhada** com dependencias e auto-claiming oferece coordenacao robusta
3. **File locking** previne race conditions no claiming de tarefas
4. **Hooks dedicados** (TeammateIdle, TaskCompleted) permitem quality gates automatizados
5. **Plan approval** oferece checkpoint humano-no-loop antes de implementacao
6. **Contexto limpo por teammate** previne context rot
7. **Debate adversarial** entre teammates combate anchoring bias em debugging

### Limitacoes

1. **Status experimental** com limitacoes significativas (sem resume, um time por sessao)
2. **Custo de tokens linear** com numero de teammates (5x para 5 teammates)
3. **Sem merge automatico** de conflitos de arquivo
4. **Lead fixo** sem possibilidade de transferencia
5. **Sem teams aninhados** (teammates nao podem criar sub-times)
6. **Compatibilidade limitada** de split panes (nao funciona em VS Code, Windows Terminal)
7. **Risco de task status desatualizado** quando teammates nao marcam tarefas como completas

---

## 9. Recomendacoes Praticas

### 9.1 Para Iniciar com Agent Teams

1. **Comece com pesquisa e review** (sem escrita de codigo) para entender a dinamica
2. **Use 3 teammates** na primeira experiencia; escale apenas quando o valor for demonstrado
3. **Defina spawn prompts detalhados** incluindo arquivos relevantes, criterios e formato esperado
4. **Monitore ativamente** -- cheque progresso dos teammates regularmente

### 9.2 Para Prevenir Conflitos

```text
# Bom: cada teammate possui modulos distintos
Teammate A: src/auth/ (todos os arquivos)
Teammate B: src/api/ (todos os arquivos)
Teammate C: tests/ (todos os arquivos)

# Ruim: multiplos teammates no mesmo diretorio
Teammate A: src/auth/login.ts
Teammate B: src/auth/session.ts  # risco se tocarem no mesmo arquivo
```

### 9.3 Para Controle de Qualidade

Implemente hooks `TaskCompleted` com scripts de validacao:

```bash
#!/bin/bash
# validate-task-quality.sh
INPUT=$(cat)
TASK_NAME=$(echo "$INPUT" | jq -r '.task_name // empty')

# Executar testes relevantes
npm test -- --related 2>&1
if [ $? -ne 0 ]; then
  echo "Testes falharam para a tarefa: $TASK_NAME" >&2
  exit 2  # Bloqueia conclusao da tarefa
fi
exit 0
```

### 9.4 Para Otimizacao de Custos

- Use `sonnet` como modelo padrao para teammates (nao `opus`)
- Limite o numero de tarefas por teammate a 5-6
- Prefira subagentes quando comunicacao inter-worker nao e necessaria
- Considere agent teams apenas quando o beneficio de paralelismo + debate justifica o custo

### 9.5 Para Integracao com a Infraestrutura Existente

- Adicione instrucoes especificas para teams no `CLAUDE.md` do projeto
- Crie skills que encapsulam padroes comuns de criacao de times
- Use hooks `SubagentStart`/`SubagentStop` no `settings.json` para logging e metricas
- Documente na auto memory os padroes de team que funcionaram bem para o projeto
