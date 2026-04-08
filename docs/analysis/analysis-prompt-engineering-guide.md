# Análise: Engenharia de Prompts — Guia Técnico Completo (2022-2026)

**Documento analisado**: `docs/prompt-engineering-guide.md`
**Data da análise**: 27 de março de 2026
**Tipo**: Documento transversal — referenciado por todos os 5 documentos principais do projeto

---

## 1. Sumário Executivo

O `prompt-engineering-guide.md` é o documento mais extenso e denso do projeto, catalogando mais de 58 técnicas de engenharia de prompts com benchmarks quantitativos, custos de tokens e aplicabilidade em arquiteturas multi-agentes. Sua importância para a infraestrutura de agentes é direta: cada SKILL.md, cada prompt de subagente, cada regra em `.claude/rules/`, cada hook e cada entrada de memória é, em última instância, um prompt — e a eficácia desses artefatos depende da aplicação correta (ou incorreta) das técnicas catalogadas neste guia.

A descoberta mais relevante para o projeto é a **inversão de paradigma**: modelos de raciocínio avançados (o1, R1, Claude com extended thinking) performam pior com técnicas clássicas como few-shot e CoT explícito. Isso impacta diretamente a escrita de skills e prompts de subagentes — técnicas que funcionam em prompts conversacionais podem ser contraproducentes em contextos agentic. O guia também documenta a transição de "prompt engineering" para "context engineering", alinhando-se perfeitamente com o `research-llm-context-optimization.md` e validando a abordagem de progressive disclosure defendida em `a-guide-to-agents.md`.

Para o `agent-engineering-toolkit`, este documento serve como a **base técnica de referência** para todas as decisões de prompting nos dois conjuntos de skills (plugin e standalone). Cada técnica catalogada aqui tem aplicação direta em pelo menos um dos artefatos que as skills geram: AGENTS.md, CLAUDE.md, SKILL.md, rules, hooks ou prompts de subagentes.

---

## 2. Análise Técnica por Técnica

### 2.1 Role Prompting (Atribuição de Papéis)

**O que é e como funciona.** Instrui o modelo a adotar uma persona profissional antes de executar a tarefa. Ajusta distribuição de probabilidades para vocabulário, profundidade e estilo típicos da persona. Custo mínimo: 10-30 tokens. Melhor relação custo-benefício para controle de estilo entre todas as técnicas.

**Quando usar.** Controle de tom e estilo; especialização de domínio; criação de agentes com identidade definida. Em multi-agentes, é o mecanismo fundamental de especialização — cada subagente recebe papel via system prompt.

**Quando NÃO usar.** Role prompting não melhora acurácia factual em modelos de ponta. Para tarefas de raciocínio, 2-shot CoT supera role prompts consistentemente (Schulhoff et al., 2024). Não usar como substituto de instruções específicas.

**Aplicação em skills (SKILL.md).** Definir o papel do agente executor logo na primeira linha do SKILL.md. Exemplo: "Você é um analista de arquitetura de software especializado em repositórios TypeScript." Manter em 1-2 frases — brevidade é essencial dado o orçamento de atenção.

```markdown
# Exemplo em SKILL.md — Role Prompting
Você é um engenheiro de configuração especializado em infraestrutura de agentes de IA.
Sua tarefa é analisar o repositório e gerar um AGENTS.md otimizado.
```

**Aplicação em hooks (pre/post prompts).** Hooks são curtos por natureza. Role prompting em hooks deve ser implícito, não explícito — o contexto da ação já define o papel. Exemplo de hook de pre-commit: "Verifique se as alterações seguem as convenções do projeto" (papel de revisor está implícito). Evitar gastar tokens com "Você é um revisor de código experiente..." em hooks de 2-3 linhas.

**Aplicação em subagentes.** Este é o caso de uso mais forte de role prompting. Cada subagente recebe uma persona especializada que direciona seu comportamento. Conforme o guia: "No sistema de pesquisa da Anthropic, cada subagente recebe um papel especializado via system prompt."

```markdown
# Exemplo de delegação a subagente
Delegue ao subagente com o seguinte papel:
"Você é um analista de dependências. Examine package.json, go.mod ou
Cargo.toml e retorne: linguagem principal, framework, gerenciador de pacotes,
e dependências críticas em formato JSON."
```

**Aplicação em rules (.claude/rules/).** Rules não devem usar role prompting. São instruções diretas e factuais — adicionar persona desperdiça tokens e não agrega valor em regras de escopo limitado.

**Aplicação em memória.** Entradas de memória são factuais e descritivas. Role prompting é irrelevante para memória — nunca usar.

---

### 2.2 Zero-Shot Prompting

**O que é e como funciona.** O modelo recebe apenas a instrução, sem exemplos. Depende do conhecimento pré-treinado. Modelos modernos alcançam ~85% de acurácia em tarefas simples. Menor custo de tokens entre todas as técnicas.

**Quando usar.** Tarefas que o modelo já faz bem nativamente: classificação simples, tradução, sumarização, brainstorming. Quando eficiência de tokens é prioridade (hooks, rules, memória).

**Quando NÃO usar.** Raciocínio multi-passo complexo; tarefas exigindo formato de saída muito específico; classificações ambíguas; tarefas fora dos padrões comuns de treinamento.

**Aplicação em skills.** A maioria das instruções de fase em SKILL.md deve ser zero-shot. Skills bem escritas fornecem contexto suficiente para que o modelo execute sem exemplos. Reservar few-shot apenas para fases com formato de saída crítico.

```markdown
# Exemplo zero-shot em fase de skill
## Fase 2: Análise de Estrutura
Examine a estrutura de diretórios do repositório.
Identifique: linguagens usadas, frameworks, padrões arquiteturais.
Retorne os achados em formato bullet list.
```

**Aplicação em hooks.** Hooks devem ser predominantemente zero-shot. São curtos, executam tarefas específicas, e tokens são preciosos. "Verifique se o commit message segue o formato conventional commits" é suficiente — não precisa de exemplos.

**Aplicação em subagentes.** Subagentes com tarefas simples e bem definidas podem operar em zero-shot. Para tarefas complexas ou com formato de saída específico, considerar few-shot.

**Aplicação em rules.** Rules são zero-shot por definição. São instruções diretas: "Use 2-space indentation", "API handlers live in src/api/handlers/". Não incluir exemplos em rules — desperdiça tokens carregados em toda sessão.

**Aplicação em memória.** Entradas de memória são zero-shot — são fatos, não instruções com exemplos.

---

### 2.3 Few-Shot Prompting

**O que é e como funciona.** Fornece 2-5+ pares entrada-saída como "mini conjunto de treinamento". O modelo identifica o mapeamento e generaliza. A Anthropic recomenda 3-5 exemplos diversos encapsulados em tags XML. A ordem dos exemplos importa significativamente.

**Quando usar.** Formato de saída específico e crítico; extração de dados estruturados; padrões que o modelo não infere corretamente em zero-shot; calibração de tom/estilo que role prompting sozinho não resolve.

**Quando NÃO usar.** Com modelos de raciocínio avançados (o1, R1) — exemplos prejudicam a performance. Após 5-10 exemplos, retornos são decrescentes. Em artefatos de contexto sempre-carregado (rules, CLAUDE.md root) — custo fixo em toda requisição.

**Aplicação em skills.** Few-shot é valioso em fases que geram artefatos com formato específico. Usar na fase de geração de output, não nas fases de análise. Encapsular exemplos em tags XML conforme recomendação da Anthropic.

```markdown
## Fase 4: Geração do AGENTS.md
Gere o arquivo seguindo este formato. Exemplos:

<example>
<input>Projeto React com TypeScript, usando pnpm workspaces</input>
<output>
# Project
React component library for accessible data visualization.
Uses pnpm workspaces.

## Conventions
For TypeScript conventions, see docs/TYPESCRIPT.md
</output>
</example>

<example>
<input>API Go com PostgreSQL, usando make</input>
<output>
# Project
REST API for inventory management built with Go and PostgreSQL.

## Build
Run `make build` to compile. Run `make test` for all tests.
</output>
</example>
```

**Aplicação em hooks.** Raramente necessário. Se o hook precisa validar formato, um único exemplo pode ser mais eficiente que uma descrição textual longa. Manter no máximo 1 exemplo.

**Aplicação em subagentes.** Útil quando o subagente precisa retornar dados em formato estruturado específico. Incluir 1-2 exemplos no prompt de delegação. Lembrar que exemplos competem com o orçamento limitado da janela de contexto de subagentes.

**Aplicação em rules.** Evitar. Rules são carregadas em toda sessão. Cada exemplo adiciona 50-200+ tokens de custo fixo. Se uma rule precisa de exemplo, considerar converter em skill (carregamento on-demand).

**Aplicação em memória.** Não aplicável. Memória armazena fatos, não exemplos demonstrativos.

---

### 2.4 System Prompts vs User Prompts

**O que é e como funciona.** System prompt define framework comportamental persistente (identidade, restrições, regras). User prompt carrega a tarefa dinâmica (dados, perguntas, exemplos contextuais). Queries ao final do prompt melhoram qualidade em até 30%.

**Quando usar.** Sempre — é a estrutura fundamental de todo prompt de produção.

**Quando NÃO usar.** Não é uma técnica opcional, mas sim uma decisão de arquitetura sobre onde colocar cada informação.

**Aplicação em skills.** SKILL.md funciona como system prompt para a execução da skill. As fases são o "user prompt" progressivo. Manter o papel e restrições no topo do SKILL.md, dados contextuais e instruções específicas nas fases.

**Aplicação em hooks.** Hooks são essencialmente user prompts curtos que operam sob o system prompt da sessão. Não tentar redefinir o system prompt dentro de um hook.

**Aplicação em subagentes.** A separação system/user é crítica para subagentes. O prompt de delegação deve definir claramente: (1) papel e restrições (system-like), (2) tarefa específica e dados (user-like).

```markdown
# Prompt de subagente com separação clara
## Contexto (system-like)
Você é um analista de testes. Examine apenas arquivos de teste.
Nunca modifique código — apenas analise e reporte.

## Tarefa (user-like)
Analise os padrões de teste em `tests/` e retorne:
- Framework de testes usado
- Padrão de nomeação de arquivos de teste
- Cobertura aproximada por área do código
```

**Aplicação em rules.** Rules são injetadas no system prompt pelo Claude Code. Cada rule deve ser escrita como uma instrução de system prompt — direta, factual, sem conversação.

**Aplicação em memória.** Memória é injetada como contexto adicional no system prompt. Deve conter fatos e decisões, não instruções de tarefa.

---

### 2.5 Chain-of-Thought (CoT)

**O que é e como funciona.** Encoraja o modelo a gerar passos intermediários de raciocínio antes da resposta final. Três variantes: Few-Shot CoT (exemplos com raciocínio), Zero-Shot CoT ("Vamos pensar passo a passo"), Auto-CoT. No GSM8K, PaLM 540B saltou de 17,9% para 58,1% com CoT.

**Quando usar.** Raciocínio multi-passo; análise complexa de código; decisões arquiteturais que requerem ponderação de trade-offs; depuração de problemas.

**Quando NÃO usar.** Modelos de raciocínio avançados (o1, R1) — apenas 2-3% de melhoria marginal com 20-80% mais tempo. Modelos pequenos (<100B) — cadeias "fluentes mas ilógicas". Tarefas simples de um passo. Em artefatos de contexto limitado (rules, hooks).

**Aplicação em skills.** Usar CoT implícito em fases de análise — instruir o modelo a "analisar cada aspecto antes de concluir". Usar tags XML `<thinking>` e `<answer>` para separação estruturada quando a fase requer raciocínio complexo.

```markdown
## Fase 3: Análise de Convenções
Para cada convenção encontrada no repositório:
<thinking>
1. Identifique a evidência (arquivo, padrão, configuração)
2. Avalie se é uma convenção explícita ou inferida
3. Determine se é relevante para o AGENTS.md ou melhor em progressive disclosure
</thinking>
<answer>
Liste apenas as convenções que passaram no filtro de relevância.
</answer>
```

**Aplicação em hooks.** Não usar CoT em hooks. Hooks devem ser rápidos e diretos. Se um hook precisa de raciocínio complexo, ele deveria ser uma skill ou um subagente.

**Aplicação em subagentes.** CoT é valioso em subagentes de análise. O subagente pode raciocinar extensivamente sem impactar o contexto principal (context: fork). Permitir que o subagente "pense" livremente antes de retornar o resultado sintetizado.

**Aplicação em rules.** Nunca usar CoT em rules. Rules são instruções diretas, não prompts de raciocínio.

**Aplicação em memória.** A memória pode registrar a conclusão de um raciocínio CoT, mas não o processo. Armazenar "Decidimos usar PostgreSQL porque..." (resultado), não os passos de análise.

---

### 2.6 Tree of Thoughts (ToT)

**O que é e como funciona.** Generaliza CoT permitindo exploração de múltiplos caminhos de raciocínio em árvore, com autoavaliação e backtracking. No Game of 24: 4% (CoT) vs 74% (ToT) — melhoria de 18,5x. Requer 5-20x mais chamadas de API.

**Quando usar.** Problemas de planejamento complexo; decisões arquiteturais com múltiplos caminhos viáveis; exploração de alternativas onde backtracking é valioso.

**Quando NÃO usar.** A grande maioria das tarefas de infraestrutura de agentes. Custo proibitivo para uso rotineiro. Problemas lineares onde CoT basta.

**Aplicação em skills.** Raramente diretamente. Pode ser implementado indiretamente via skills multi-fase que exploram alternativas e depois convergem. Exemplo: Fase 3a gera opção A, Fase 3b gera opção B, Fase 4 avalia e escolhe.

**Aplicação em hooks.** Nunca. Custo e latência incompatíveis com hooks.

**Aplicação em subagentes.** Pode ser implementado como padrão orchestrator-workers: um agente orquestrador delega exploração de N caminhos a N subagentes, depois sintetiza. O custo é aceitável quando a decisão é de alto impacto.

**Aplicação em rules.** Irrelevante para rules.

**Aplicação em memória.** Irrelevante para memória.

---

### 2.7 ReAct (Raciocínio + Ação)

**O que é e como funciona.** Loop iterativo Pensamento-Acao-Observacao. O modelo raciocina sobre o estado, executa uma ferramenta, recebe o resultado, e repete. Superou métodos baseline por 34% absolutos em ALFWorld.

**Quando usar.** Tarefas com ferramentas e dados em tempo real; verificação de fatos; exploração de repositórios; qualquer tarefa que se beneficie de interação com o ambiente.

**Quando NÃO usar.** Raciocínio puro sem dados externos; quando nenhuma ferramenta está disponível; tarefas factuais simples.

**Aplicação em skills.** ReAct é o padrão natural para skills de análise de repositório. Cada fase de exploração é implicitamente um ciclo ReAct: ler arquivos, raciocinar sobre o conteúdo, decidir próxima ação. Skills devem facilitar isso fornecendo orientação sobre quais ferramentas usar e quais arquivos examinar.

```markdown
## Fase 2: Exploração do Repositório
Use as seguintes ferramentas para investigar:
- `glob` para encontrar arquivos por padrão
- `grep` para buscar padrões de código
- `read` para examinar conteúdo de arquivos

Para cada achado, raciocine sobre sua relevância antes de prosseguir.
```

**Aplicação em hooks.** Hooks podem implementar mini-ciclos ReAct: verificar → avaliar → reportar. Exemplo: hook post-commit que verifica se testes passam, avalia resultado, reporta.

**Aplicação em subagentes.** Subagentes de exploração são fundamentalmente agentes ReAct. O prompt de delegação deve listar as ferramentas disponíveis e orientar o ciclo de exploração.

**Aplicação em rules.** Irrelevante. Rules são estáticas, não interativas.

**Aplicação em memória.** O resultado de ciclos ReAct pode ser armazenado em memória para evitar re-exploração. Exemplo: "O projeto usa Jest com configuração em jest.config.ts" — resultado de exploração prévia.

---

### 2.8 Self-Consistency (Votação Majoritária)

**O que é e como funciona.** Amostra N caminhos de raciocínio diversos para o mesmo problema e seleciona a resposta mais frequente por votação majoritária. +17,9% sobre CoT no GSM8K com tão poucas quanto 3 amostras.

**Quando usar.** Decisões de alta confiabilidade onde erro é custoso; classificações ambíguas.

**Quando NÃO usar.** Geração aberta/criativa; aplicações sensíveis a latência; custo restrito (5-30x o custo normal).

**Aplicação em skills.** Pode ser implementado em fases críticas de decisão: gerar análise N vezes e convergir. Na prática, raramente justificável para geração de AGENTS.md/CLAUDE.md, mas pode ser valioso em skills de auditoria.

**Aplicação em hooks.** Nunca. Custo proibitivo para hooks.

**Aplicação em subagentes.** Pode ser implementado despachando o mesmo prompt a 3 subagentes e sintetizando as respostas. Útil para análise de segurança ou revisão de código de alta criticidade.

**Aplicação em rules.** Irrelevante.

**Aplicação em memória.** Irrelevante.

---

### 2.9 Prompt Chaining (Decomposição em Pipeline)

**O que é e como funciona.** Quebra tarefas complexas em subtarefas sequenciais. Cada passo usa um prompt focado com objetivo único. Custo 2-5x maior que prompt único, mas com maior qualidade e debuggabilidade.

**Quando usar.** Workflows complexos multi-etapa; quando inspecionar saídas intermediárias é necessário; quando qualidade por etapa importa mais que velocidade.

**Quando NÃO usar.** Tarefas simples; quando latência aditiva é inaceitável; quando o modelo lida bem com a tarefa em um único prompt.

**Aplicação em skills.** Skills são fundamentalmente prompt chains. Cada fase é um elo da cadeia: Explorar → Analisar → Planejar → Gerar → Validar. A saída de cada fase alimenta a entrada da próxima. Este é o padrão mais importante para o projeto.

```markdown
# Estrutura de SKILL.md como Prompt Chain
## Fase 1: Exploração (saída: inventário de arquivos relevantes)
## Fase 2: Análise (entrada: inventário; saída: achados estruturados)
## Fase 3: Planejamento (entrada: achados; saída: plano de conteúdo)
## Fase 4: Geração (entrada: plano; saída: artefato final)
## Fase 5: Validação (entrada: artefato; saída: relatório de conformidade)
```

**Aplicação em hooks.** Hooks podem implementar mini-chains de 2-3 passos: verificar → decidir → agir.

**Aplicação em subagentes.** O padrão orchestrator-workers é prompt chaining distribuído. O orquestrador decompõe, delega aos workers, e sintetiza resultados.

**Aplicação em rules.** Rules podem referenciar outras rules ou docs criando uma cadeia de resolução, mas não são chains no sentido técnico.

**Aplicação em memória.** Irrelevante diretamente, mas memória pode armazenar resultados intermediários de chains longas para recuperação em sessões futuras.

---

### 2.10 Structured Output (JSON, XML, Schemas)

**O que é e como funciona.** Técnicas para forçar saídas em formatos legíveis por máquina. Descoberta crítica: forçar JSON durante raciocínio degrada acurácia em 10-15%. A prática recomendada é raciocínio livre primeiro, formatação depois. XML tem 15-20% de boost de performance no Claude por treinamento específico.

**Quando usar.** Saídas consumidas por sistemas; comunicação entre agentes; extração de dados; quando conformidade de formato é obrigatória.

**Quando NÃO usar.** Durante raciocínio (degrada acurácia). Para saídas que humanos lerão diretamente (Markdown é melhor).

**Aplicação em skills.** Usar structured output para comunicação entre fases e entre skills. Dentro da skill, separar raciocínio de formatação: primeiro analisar livremente, depois formatar em JSON/YAML.

```markdown
## Fase 2: Análise
Analise livremente as convenções encontradas. Depois, estruture os achados:

<analysis_output>
{
  "language": "TypeScript",
  "framework": "Next.js",
  "package_manager": "pnpm",
  "conventions": [
    {"rule": "2-space indentation", "evidence": "prettier.config.js", "confidence": "high"}
  ]
}
</analysis_output>
```

**Aplicação em hooks.** Hooks de validação podem exigir saída estruturada para processamento programático (ex: lista de violações em JSON).

**Aplicação em subagentes.** Crítico. Subagentes devem retornar resultados em formato estruturado para que o orquestrador possa sintetizar. JSON é preferido por ser menos propenso a modificação indevida pelo modelo. Conforme o guia de long-running agents: "Feature list em JSON (não Markdown) — modelo é menos propenso a modificar JSON inapropriadamente."

**Aplicação em rules.** Rules podem especificar formatos de saída esperados: "Sempre retorne erros de linting em formato JSON com campos: file, line, rule, message."

**Aplicação em memória.** Memória usa Markdown por design (legibilidade humana). Não usar JSON para memória.

---

### 2.11 RAG Prompting Patterns

**O que é e como funciona.** Combina recuperação de documentos externos com geração. Padrões: context injection, dual prompt structure, N-shot RAG, CoT RAG, agentic RAG.

**Quando usar.** Quando o modelo precisa de informação que não está no treinamento; fundamentação factual; documentação específica do projeto.

**Quando NÃO usar.** Quando a informação é comum e o modelo já sabe; quando resultados de busca serão ruins; tarefas puramente generativas.

**Aplicação em skills.** Skills implementam RAG implicitamente: as fases de exploração recuperam contexto (leem arquivos, buscam padrões) que alimentam as fases de geração. A seção `references/` de cada skill é essencialmente um corpus RAG pré-curado.

```markdown
## Fase 1: Recuperação de Contexto
Leia os seguintes arquivos de referência para orientar sua análise:
- references/evidence-based-conventions.md
- references/progressive-disclosure-patterns.md

Depois, examine o repositório para coletar evidências específicas.
```

**Aplicação em hooks.** Hooks podem implementar agentic RAG: decidir se precisam buscar contexto antes de agir.

**Aplicação em subagentes.** Subagentes de pesquisa são agentes RAG por natureza: recuperam, analisam, sintetizam.

**Aplicação em rules.** Rules podem orientar o modelo a buscar contexto antes de agir: "Antes de modificar arquivos em src/api/, leia docs/API_CONVENTIONS.md."

**Aplicação em memória.** Auto memory do Claude Code é um sistema RAG: MEMORY.md como índice, topic files como corpus, carregamento on-demand como recuperação.

---

### 2.12 Meta-Prompting

**O que é e como funciona.** Prompts que geram prompts. Três acepções: scaffolding (LLM como condutor de especialistas), otimização prática (modelo forte gera prompts para modelo barato), estrutural (formalização via teoria de categorias). +17,1% vs prompting padrão.

**Quando usar.** Otimização de prompts existentes; geração de prompts especializados para múltiplos domínios; quando prompts manuais atingem plateau de qualidade.

**Quando NÃO usar.** Para tarefas simples; quando custo de otimização não se justifica; prompts de uso único.

**Aplicação em skills.** Meta-prompting é a essência de skills de inicialização. A skill que gera AGENTS.md é um meta-prompt: um prompt que analisa o repositório e gera instruções (prompts) para futuros agentes.

```markdown
# A skill de inicialização é fundamentalmente meta-prompting:
# Prompt (SKILL.md) → analisa repo → gera AGENTS.md → que será prompt para agentes futuros
```

**Aplicação em hooks.** Hooks de otimização de prompts podem usar meta-prompting: hook que revisa e sugere melhorias em prompts antes de commit.

**Aplicação em subagentes.** O padrão orchestrator-workers é meta-prompting: o orquestrador gera prompts específicos para cada worker dinamicamente.

**Aplicação em rules.** Irrelevante diretamente.

**Aplicação em memória.** Irrelevante diretamente.

---

### 2.13 Técnicas de Fronteira Relevantes

#### Constitutional AI e Self-Critique

**Aplicação em skills.** Fases de validação implementam self-critique: o modelo revisa sua própria saída contra princípios. Usar "constituição" explícita na fase de validação.

```markdown
## Fase 5: Validação
Revise o AGENTS.md gerado contra estes princípios:
- Cada instrução é específica e verificável?
- O arquivo está sob 200 linhas?
- Informações voláteis foram excluídas?
- Progressive disclosure foi aplicado corretamente?
Se qualquer princípio foi violado, revise o artefato.
```

#### Step-Back Prompting

**Aplicação em skills.** Útil em fases de análise: antes de examinar detalhes do repositório, fazer uma pergunta de abstração mais alta. "Qual é o propósito geral deste repositório?" antes de "Quais são as convenções de código?"

#### Rephrase and Respond (RaR)

**Aplicação em skills.** Útil quando o prompt de fase é complexo: instruir o modelo a reformular a tarefa antes de executar garante compreensão correta.

#### Skeleton-of-Thought (SoT)

**Aplicação em skills.** Adequado para fases de geração de documentos longos: gerar outline primeiro, expandir depois. Alinha-se naturalmente com o padrão Planejar → Gerar das skills.

---

## 3. Pontos de Atenção

### 3.1 Misaplicações Comuns

| Erro | Consequência | Correção |
|------|-------------|----------|
| Few-shot em rules | Custo fixo de 50-200+ tokens por exemplo em toda sessão | Mover exemplos para skills ou docs de referência |
| CoT explícito em hooks | Latência desnecessária em operações que devem ser rápidas | Hooks devem ser zero-shot e diretos |
| Role prompting em rules | Tokens desperdiçados sem ganho de acurácia | Rules são instruções, não personas |
| Structured output durante raciocínio | Degradação de 10-15% na acurácia | Separar raciocínio livre de formatação |
| Técnicas complexas (ToT, SC) em tarefas simples | Custo 5-30x sem benefício proporcional | Começar com a técnica mais simples |
| CoT explícito com modelos de raciocínio | Performance pior que zero-shot | Testar antes de assumir que CoT ajuda |
| Formatação agressiva (ALL-CAPS, "NUNCA") | Resultados piores em modelos Claude recentes | Tom direto sem ênfase excessiva |

### 3.2 Quando Mais Simples é Melhor

O guia enfatiza repetidamente: **"Comece com a solução mais simples possível e só aumente a complexidade quando demonstravelmente necessário."** Para infraestrutura de agentes, isso significa:

1. **Rules**: sempre zero-shot, sempre diretas, sem exemplos
2. **Hooks**: zero-shot, 1-3 frases, sem raciocínio elaborado
3. **Memória**: fatos brutos, sem técnicas de prompting
4. **Skills**: prompt chaining (multi-fase) com zero-shot por padrão, few-shot apenas quando formato é crítico
5. **Subagentes**: role + zero-shot por padrão, few-shot para formato de retorno específico

### 3.3 O Paradoxo do Over-Engineering

Quanto mais técnicas de prompting se empilham em um artefato de infraestrutura, mais tokens são consumidos, mais o orçamento de atenção é diluído, e mais o modelo tende a ignorar instruções. O `a-guide-to-agents.md` e o `research-llm-context-optimization.md` convergem neste ponto: o "ideal AGENTS.md é pequeno, focado, e aponta para outros recursos". Técnicas sofisticadas de prompting devem ser usadas cirurgicamente, não por padrão.

---

## 4. Matriz de Aplicabilidade entre Documentos

Esta matriz mapeia cada técnica principal do guia de engenharia de prompts aos princípios de cada um dos 5 documentos do projeto.

### 4.1 Mapeamento Técnica → Documento

| Técnica | Evaluating-AGENTS-paper | research-llm-context-optimization | claude-prompting-best-practices | a-guide-to-agents | a-guide-to-claude |
|---------|------------------------|-----------------------------------|-------------------------------|-------------------|-------------------|
| **Role Prompting** | Confirma que role prompting em AGENTS.md define escopo eficazmente | Consome mínimo do orçamento de atenção (10-30 tokens) | Recomendado no system prompt para persistência entre turnos | One-liner de projeto é role prompting implícito | CLAUDE.md pode definir persona do projeto |
| **Zero-Shot** | Maioria das instruções eficazes em AGENTS.md são zero-shot | Maximiza eficiência do orçamento de atenção | Recomendado como ponto de partida antes de complexificar | "AGENTS.md ideal deve ser o menor possível" — zero-shot é o caminho | Rules e CLAUDE.md devem ser zero-shot |
| **Few-Shot** | Exemplos em AGENTS.md custam tokens fixos; evitar | Cada exemplo consome 50-200+ tokens do orçamento limitado | Recomenda 3-5 exemplos em tags XML para tarefas de formato | "Mova rules específicas para arquivos separados" — evitar exemplos no root | Skills podem usar few-shot; CLAUDE.md não deve |
| **System vs User** | AGENTS.md é fundamentalmente system prompt | Posicionamento de instruções afeta aderência (lost-in-middle) | Coloque role no system, exemplos no user, queries no final | Hierarquia root/package é hierarquia system/user | Hierarquia CLAUDE.md/rules/skills espelha system/user |
| **Chain-of-Thought** | Não documentado em AGENTS.md configs | CoT consome tokens significativos; usar apenas quando necessário | Recomenda tags `<thinking>` e `<answer>` para Claude | Não relevante para AGENTS.md estático | Skills de análise podem usar CoT em fases de exploração |
| **ReAct** | Loop de exploração é implícito na avaliação de AGENTS.md | Ciclos ReAct consomem contexto progressivamente | Base do loop agentic do Claude Code | Agentes "são rápidos em navegar hierarquias de documentação" — ReAct | Claude Code opera em loop ReAct nativo |
| **Prompt Chaining** | Avaliação multi-critério é chain implícita | Cada elo da chain é uma oportunidade de compaction | "Chaining explícito útil quando precisa inspecionar intermediários" | Progressive disclosure é chain de resolução | Skills multi-fase são prompt chains |
| **Structured Output** | Métricas em formato estruturado para avaliação | JSON é preferido para estado entre agentes (menos propenso a modificação) | XML tem 15-20% boost no Claude; JSON para inter-sistema | AGENTS.md é Markdown; saídas intermediárias podem ser JSON | Rules podem especificar formatos; memória usa Markdown |
| **RAG Patterns** | AGENTS.md como "contexto pré-carregado" é RAG estático | Progressive disclosure + JIT = RAG agentic | "Agentic RAG: LLM decide quando recuperar" | "Deixe o agente gerar documentação JIT" — agentic RAG | Skills com `references/` são RAG pré-curado |
| **Meta-Prompting** | Meta-análise de eficácia de AGENTS.md | Otimização automática supera manual significativamente | Prompt generator da Anthropic é meta-prompting | Prompt de refactoring de AGENTS.md é meta-prompt | Skill de inicialização gera prompts para agentes futuros |
| **Self-Critique** | Validação de qualidade de AGENTS.md | Ciclos critique-revision custam 2-3x por resposta | Loop evaluate → revise é padrão recomendado | "Encontrar contradições" no prompt de refactoring | Fase de validação em skills é self-critique |
| **Step-Back** | Perguntar "Para que serve este repo?" antes de analisar | Abstração reduz tokens gastos em exploração irrelevante | Melhoria de 7-27% sobre CoT | One-liner de projeto é um step-back implícito | Antes de gerar CLAUDE.md, entender o propósito do projeto |

### 4.2 Princípios Convergentes

Cinco princípios emergem da convergência entre todos os documentos:

1. **Minimalismo agressivo**: Todos os documentos concordam que menos é mais. O guia de prompts confirma que técnicas simples são suficientes para a maioria das tarefas, e técnicas complexas têm retornos decrescentes.

2. **Progressive disclosure como arquitetura**: O padrão de carregar contexto on-demand aparece como RAG agentic no guia de prompts, como JIT documentation no research, como skills no Claude Code, e como hierarquia de arquivos no AGENTS.md.

3. **Separação de raciocínio e formatação**: O guia de prompts documenta a degradação de 10-15% ao forçar formato durante raciocínio. Isso valida a abordagem de fases em skills: explorar livremente, depois formatar.

4. **Começar simples, complexificar com evidência**: O guia de prompts, a Anthropic, e o AGENTS.md guide convergem: zero-shot primeiro, técnicas avançadas apenas com evidência de necessidade.

5. **Contexto é recurso finito**: O orçamento de atenção do research, o instruction budget do AGENTS.md guide, e o custo de tokens por técnica no guia de prompts são facetas do mesmo princípio.

---

## 5. Implicações de Context Engineering

### 5.1 Orçamento de Atenção e Técnicas de Prompting

O `research-llm-context-optimization.md` estabelece que o orçamento prático de instrução por arquivo é ~200 linhas (~2.000-4.000 tokens). O guia de engenharia de prompts adiciona custos específicos por técnica:

| Técnica | Custo de Tokens | Impacto no Orçamento |
|---------|----------------|---------------------|
| Role prompting | 10-30 tokens | Negligível — usar livremente |
| Zero-shot | 0 tokens extras | Nenhum — preferir sempre |
| Few-shot (3 exemplos) | 150-600 tokens | 4-15% do orçamento de um CLAUDE.md |
| CoT explícito | 2-3x do prompt base | Significativo — usar apenas em skills |
| Self-Consistency | 5-30x do custo base | Proibitivo para artefatos estáticos |
| Structured output | +10-20% (JSON) | Moderado — aceitável para inter-agentes |

**Implicação prática**: Em artefatos sempre-carregados (CLAUDE.md, rules sem path-scope), cada token importa. Técnicas que adicionam tokens (few-shot, CoT) devem ser reservadas para artefatos on-demand (skills, subagentes).

### 5.2 Lost-in-the-Middle e Posicionamento de Técnicas

O research documenta que performance é maior quando informação relevante está no início ou fim do contexto. O guia de prompts confirma que "queries ao final do prompt melhoram qualidade em até 30%".

**Implicações para infraestrutura de agentes:**

- **SKILL.md**: Papel e restrições no topo (início do contexto). Fase de geração final no fim. Fases intermediárias de análise no meio (menos críticas).
- **Rules**: Instruções mais críticas primeiro. Se uma rule tem múltiplas instruções, a mais importante deve abrir o arquivo.
- **CLAUDE.md**: Convenções fundamentais no topo. Instruções secundárias no meio. Instruções de ambiente/setup no final.
- **Prompts de subagente**: Papel no topo, ferramentas no meio, tarefa específica no final.

### 5.3 Progressive Disclosure como Mitigação de Custo

O guia de prompts documenta que técnicas avançadas custam 2-30x mais tokens. O research documenta que context rot degrada performance com mais tokens. A solução convergente é progressive disclosure:

```
Sempre-carregado (CLAUDE.md, rules globais):
→ Zero-shot, role implícito, sem exemplos
→ Orçamento: ~200 linhas, ~3.000 tokens

On-demand (skills, rules com path-scope):
→ Zero-shot + few-shot seletivo + CoT em fases de análise
→ Orçamento: mais generoso (contexto isolado ou temporário)

Isolado (subagentes com context: fork):
→ Todas as técnicas disponíveis
→ Orçamento: janela de contexto completa do subagente
→ Nenhum impacto no contexto principal
```

### 5.4 Compaction e Técnicas de Prompting

Quando o contexto é compactado, detalhes de técnicas elaboradas (cadeias CoT, exemplos few-shot) são naturalmente descartados. Isso significa que:

- Informações críticas devem estar em artefatos estáticos (não dependentes de compaction)
- Técnicas elaboradas devem ser usadas em contextos que não serão compactados (subagentes com context: fork)
- Se uma instrução é importante o suficiente para sobreviver a compaction, deve ser um fato simples, não um exemplo elaborado

---

## 6. Receitas Práticas

### 6.1 Receita: Escrevendo uma Nova Skill

```markdown
# SKILL.md — Template Baseado em Técnicas de Prompting

# Nome da Skill
[Role prompting: 1 frase definindo quem o agente é]
[Step-back: 1 frase sobre o propósito geral]

## Fase 1: Exploração [ReAct]
[Zero-shot: instruções diretas sobre o que explorar]
[Liste ferramentas disponíveis: glob, grep, read]
[Orientação sobre ciclo: observar → raciocinar → próxima ação]

## Fase 2: Análise [CoT implícito]
[Zero-shot: instruções de análise]
[Separação de raciocínio e formatação]
<thinking>
[Orientação sobre aspectos a analisar]
</thinking>
<findings>
[Formato estruturado para achados]
</findings>

## Fase 3: Planejamento [Prompt chaining — recebe saída da Fase 2]
[Zero-shot: instruções de planejamento]
[Referência a docs/references/ para critérios — RAG]

## Fase 4: Geração [Few-shot se formato é crítico]
[1-2 exemplos em tags XML se necessário]
[Template de saída]

## Fase 5: Validação [Self-critique / Constitutional AI]
[Lista de princípios para autoavaliação]
[Instruções de revisão se princípios forem violados]
```

**Técnicas usadas**: Role prompting (topo), ReAct (exploração), CoT (análise), Prompt chaining (multi-fase), Few-shot (geração, se necessário), Self-critique (validação), Step-back (contextualização), Structured output (entre fases).

### 6.2 Receita: Prompt de Delegação a Subagente

```markdown
# Template de Delegação a Subagente

## Papel [Role prompting]
Você é um [especialização]. Seu objetivo é [resultado esperado].

## Restrições [System prompt behavior]
- Nunca modifique arquivos — apenas analise e reporte
- Limite sua análise a [escopo]
- Retorne resultados em formato JSON

## Ferramentas Disponíveis [ReAct enablement]
- `glob`: encontrar arquivos por padrão
- `grep`: buscar conteúdo em arquivos
- `read`: ler conteúdo de arquivo

## Tarefa [User prompt — no final para boost de 30%]
Analise [alvo] e retorne:
[Lista de campos esperados]

## Formato de Retorno [Structured output]
<result>
{
  "campo1": "...",
  "campo2": ["..."],
  "confidence": "high|medium|low"
}
</result>
```

**Princípios aplicados**: Papel no topo (role prompting no início do contexto), restrições como system prompt, ferramentas listadas para ReAct, tarefa no final (lost-in-the-middle), saída estruturada em JSON (inter-agente).

### 6.3 Receita: Rule com Path-Scope

```markdown
# Template de Rule — .claude/rules/[topic].md

---
paths:
  - "[glob pattern]"
---

# [Tópico] — Rules

[Zero-shot: instruções diretas, sem exemplos]

- [Instrução mais crítica primeiro — posicionamento primacy]
- [Instrução secundária]
- [Instrução terciária]

[Se referência externa é necessária — RAG pointer]
Para detalhes, consulte docs/[reference].md
```

**Princípios aplicados**: Zero-shot exclusivo (sem exemplos para economizar tokens), instrução mais importante primeiro (lost-in-the-middle), path-scope para progressive disclosure, referência a docs para JIT loading.

**Exemplo concreto:**

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- Todos os endpoints devem incluir validação de input com Zod schemas
- Respostas de erro seguem o formato RFC 7807 (Problem Details)
- Handlers vivem em src/api/handlers/, validators em src/api/validators/
- Para padrões de autenticação, consulte docs/auth-patterns.md
```

### 6.4 Receita: Entrada de Memória

```markdown
# Template de Entrada de Memória

## [Tópico] — [Data]

[Fato direto, sem técnicas de prompting]
[Decisão tomada + justificativa em 1 frase]
[Referência a arquivo/doc se relevante]
```

**Princípios aplicados**: Zero-shot puro (memória é fato, não prompt), minimalismo agressivo (cada token conta no orçamento de 200 linhas do MEMORY.md), informação factual que sobrevive a compaction.

**Exemplo concreto:**

```markdown
## Arquitetura de Testes — 2026-03-15

- Framework: Jest com ts-jest para TypeScript
- Padrão de nomeação: `[module].test.ts` co-localizado com o código
- Fixtures compartilhadas em `tests/fixtures/`
- Comando principal: `pnpm test` (roda todos), `pnpm test:watch` (modo watch)
- Decisão: mocks externos isolados em `tests/__mocks__/` por requisito de determinismo
```

### 6.5 Receita: Prompt de Hook

```markdown
# Template de Hook Prompt

[Zero-shot: 1-3 frases descrevendo a verificação]
[Critério de sucesso/falha]
[Ação em caso de falha — se aplicável]
```

**Princípios aplicados**: Zero-shot exclusivo (hooks devem ser rápidos), minimalismo extremo (cada token de hook é custo em toda execução), sem role prompting (papel é implícito no contexto da ação).

**Exemplo concreto para hook pre-commit:**

```markdown
Verifique se o commit message segue o formato conventional commits:
{type}({scope}): {description}

Tipos válidos: feat, fix, docs, chore, refactor, test, perf, ci.
Se o formato estiver incorreto, rejeite o commit e sugira correção.
```

---

## 7. Forças e Limitações

### 7.1 Forças do Guia

1. **Cobertura abrangente**: 58+ técnicas documentadas com benchmarks quantitativos, não apenas descrições qualitativas. Permite decisões informadas sobre custo-benefício de cada técnica.

2. **Descoberta contra-intuitiva documentada**: A inversão de paradigma com modelos de raciocínio (técnicas clássicas prejudicam) é essencial para evitar over-engineering em skills e subagentes. Sem essa informação, a tendência natural seria adicionar CoT e few-shot em todo lugar.

3. **Custos de tokens quantificados**: Saber que few-shot custa 50-200+ tokens por exemplo ou que Self-Consistency multiplica custo por 5-30x permite planejar o orçamento de atenção concretamente.

4. **Matrizes de decisão**: As tabelas comparativas por tipo de tarefa e por tier de modelo são ferramentas de referência práticas para escolha de técnicas.

5. **Seção de multi-agentes**: A análise de como técnicas se aplicam em arquiteturas multi-agentes é diretamente relevante para o projeto, que gera infraestrutura para agentes.

6. **Combinações sinérgicas e conflitantes**: Saber que "Few-shot + modelos de raciocínio" prejudica ou que "CoT + Self-Consistency" amplifica é conhecimento crítico para design de prompts.

### 7.2 Limitações do Guia

1. **Foco em prompts de API, não em infraestrutura de agentes**: O guia cobre técnicas para prompts diretos ao modelo, mas não mapeia sistematicamente como cada técnica se traduz para artefatos de infraestrutura (AGENTS.md, rules, hooks, skills). Esta análise preenche essa lacuna.

2. **Ausência de exemplos de infraestrutura de agentes**: Todos os exemplos são de prompts conversacionais ou de API. Faltam exemplos de como aplicar role prompting em um SKILL.md ou CoT em uma fase de skill.

3. **Benchmarks de domínio acadêmico**: GSM8K, Game of 24, ALFWorld — benchmarks relevantes para validade acadêmica, mas distantes das tarefas práticas de geração de AGENTS.md ou análise de repositório.

4. **Evolução rápida**: Muitos benchmarks são de 2022-2024. Modelos de 2026 podem ter características diferentes, especialmente modelos de raciocínio que mudam a dinâmica de técnicas clássicas.

5. **Ausência de guidance sobre combinação para infraestrutura**: O guia lista combinações sinérgicas e conflitantes, mas não orienta sobre qual combinação usar para "gerar um AGENTS.md" ou "delegar análise a subagente".

6. **Custo computacional não mapeado para contexto de agentes**: Os custos de tokens são apresentados em termos absolutos, mas não em termos do orçamento de atenção de 200 linhas de um CLAUDE.md ou do contexto limitado de um subagente.

---

## 8. Recomendações

### 8.1 Técnicas Prioritárias para Infraestrutura de Agentes

Ordenadas por impacto e relação custo-benefício para o projeto:

**Tier 1 — Usar sempre:**

| Técnica | Onde | Justificativa |
|---------|------|---------------|
| **Zero-shot** | Rules, hooks, memória, fases simples de skills | Custo mínimo, eficácia comprovada para instruções diretas |
| **Role prompting** | Topo de SKILL.md, prompts de subagente | 10-30 tokens para especialização completa do agente |
| **Prompt chaining** | Estrutura de skills multi-fase | Padrão fundamental de decomposição — a skill inteira é uma chain |
| **System vs User separation** | Prompts de subagente, estrutura de SKILL.md | Organização básica que melhora aderência |

**Tier 2 — Usar quando necessário:**

| Técnica | Onde | Justificativa |
|---------|------|---------------|
| **Few-shot** (1-2 exemplos) | Fases de geração com formato crítico | Quando o formato de saída não pode ser inferido por zero-shot |
| **CoT** (implícito) | Fases de análise em skills, subagentes de análise | Quando raciocínio multi-passo é necessário; nunca em rules/hooks |
| **Structured output** | Comunicação entre fases, retorno de subagentes | JSON para inter-agente, XML para Claude, Markdown para humanos |
| **ReAct** (orientação) | Fases de exploração em skills | Listar ferramentas disponíveis e orientar ciclo de exploração |
| **Self-critique** | Fases de validação em skills | Loop de revisão contra princípios explícitos |
| **Step-back** | Início de skills de análise | Contextualizar antes de detalhar — custo mínimo, ganho significativo |

**Tier 3 — Usar excepcionalmente:**

| Técnica | Onde | Justificativa |
|---------|------|---------------|
| **Meta-prompting** | Skills que geram prompts/configs para outros agentes | A skill de inicialização já é meta-prompting por natureza |
| **Self-Consistency** | Decisões de alta criticidade via múltiplos subagentes | Custo 5-30x — justificável apenas para decisões irreversíveis |
| **Tree of Thoughts** | Exploração de alternativas arquiteturais | Implementável via orchestrator-workers, não via prompt direto |
| **RAG patterns** | Skills com `references/` como corpus | Já implementado implicitamente na estrutura de referências |

**Tier 4 — Evitar em infraestrutura de agentes:**

| Técnica | Razão |
|---------|-------|
| **Emotion prompting** | Irrelevante para artefatos técnicos de configuração |
| **Multimodal CoT** | Infraestrutura de agentes é textual |
| **Directional Stimulus** | Requer modelo de política treinado — overhead injustificado |
| **Skeleton-of-Thought** | Otimização de latência irrelevante para geração de configs |

### 8.2 Regras de Ouro Derivadas

1. **Em artefatos sempre-carregados (CLAUDE.md root, rules globais), usar exclusivamente zero-shot.** Cada token extra é custo em toda requisição. Few-shot e CoT pertencem a artefatos on-demand.

2. **Em skills, usar prompt chaining como estrutura e zero-shot como padrão de fase.** Adicionar few-shot apenas em fases de geração com formato crítico. Adicionar CoT apenas em fases de análise complexa.

3. **Em subagentes, investir em role prompting e structured output de retorno.** O papel define o comportamento, o formato de retorno garante integração. Tarefa sempre no final do prompt.

4. **Nunca usar técnicas que custem 5x+ em artefatos que não sejam isolados (context: fork).** Self-Consistency e ToT só fazem sentido em contextos isolados de subagentes.

5. **Testar antes de assumir.** A descoberta de que modelos de raciocínio performam pior com técnicas clássicas invalida pressupostos. Medir, não presumir.

6. **Tratar cada técnica como investimento de tokens.** Calcular o custo marginal (tokens extras) contra o benefício marginal (melhoria mensurável) antes de adicionar complexidade.

---

## Referências Cruzadas

- `docs/prompt-engineering-guide.md` — Documento analisado
- `docs/research-llm-context-optimization.md` — Context engineering, orçamento de atenção, progressive disclosure
- `docs/a-guide-to-agents.md` — AGENTS.md minimalismo, progressive disclosure, instruction budget
- `docs/analysis/` — Diretório de análises do projeto
