# Engenharia de prompts: guia técnico completo das técnicas de 2022 a 2026

A engenharia de prompts evoluiu de uma arte informal para uma disciplina técnica rigorosa com **mais de 58 técnicas documentadas** e impacto direto na qualidade, custo e confiabilidade de sistemas de IA. Este relatório cobre as principais técnicas — desde as fundacionais (zero-shot, few-shot) até as de fronteira (agentic patterns, DSPy, Graph of Thoughts) — com análise comparativa de performance, custo de tokens e aplicabilidade em arquiteturas multi-agentes. A descoberta mais importante dos últimos dois anos é a inversão de paradigma: **modelos de raciocínio avançados (o1, R1, GPT-5) frequentemente performam pior com técnicas clássicas como few-shot e CoT explícito**, exigindo que engenheiros reavaliem premissas consolidadas. O campo está em transição acelerada de "prompt engineering" para "context engineering" — o gerenciamento holístico de todo o contexto que alimenta o modelo a cada passo.

---

## Técnicas fundamentais: a base de toda engenharia de prompts

### Role Prompting (atribuição de papéis)

**Definição e funcionamento.** Role prompting instrui o modelo a adotar uma persona, identidade profissional ou padrão comportamental antes de executar uma tarefa. Ao atribuir um papel, o modelo ajusta sua distribuição de probabilidades para gerar texto no estilo, vocabulário e profundidade típicos daquela persona. A implementação é simples: `"Você é um cardiologista experiente"` antes da pergunta muda drasticamente o registro, a terminologia e o foco da resposta.

**Melhores casos de uso.** Controle de tom e estilo (formal, técnico, casual); especialização de domínio (jurídico, médico, financeiro); criação de agentes conversacionais com identidade definida; escrita criativa com voz específica.

**Quando NÃO usar.** Pesquisa de Schulhoff et al. (2024, "The Prompt Report") testou 12 role prompts em 2.000 questões MMLU com GPT-4-turbo e demonstrou que **2-shot CoT supera role prompts consistentemente em tarefas de raciocínio**. Role prompting não melhora acurácia factual em modelos de ponta — seu valor está no estilo, não na precisão.

**Custo de tokens.** Mínimo: 10-30 tokens adicionais. Melhor relação custo-benefício entre todas as técnicas para controle de estilo.

**Impacto em multi-agentes.** Role prompting é o mecanismo fundamental de especialização em arquiteturas multi-agentes. No sistema de pesquisa da Anthropic, cada subagente recebe um papel especializado via system prompt. LangChain e CrewAI usam role prompting como base para definir comportamentos de agentes.

### Zero-Shot Prompting (sem exemplos)

**Definição e funcionamento.** O modelo recebe apenas a instrução da tarefa, sem exemplos demonstrativos. Depende inteiramente do conhecimento adquirido durante o treinamento. Para tarefas comuns (classificação, tradução, sumarização), modelos modernos como GPT-4o e Claude Sonnet 4.5 têm capacidades zero-shot robustas.

**Melhores casos de uso.** Chatbots de propósito geral; classificação e tradução simples; brainstorming rápido; quando eficiência de tokens é prioridade.

**Quando NÃO usar.** Raciocínio multi-passo complexo; tarefas exigindo formato de saída específico; classificações ambíguas com sarcasmo ou negação; tarefas fora dos padrões comuns de treinamento.

**Custo e performance.** **Menor custo de tokens** entre todas as técnicas. Modelos modernos alcançam **~85% de acurácia** em tarefas simples em zero-shot. A variante **zero-shot CoT** ("Vamos pensar passo a passo") frequentemente supera few-shot em tarefas de raciocínio com modelos de ponta (Kojima et al., 2022).

### Few-Shot Prompting (poucos exemplos)

**Definição e funcionamento.** Fornece 2-5+ exemplos de pares entrada-saída no prompt, funcionando como um "mini conjunto de treinamento" para aprendizado em contexto (in-context learning). Demonstrado extensivamente por Brown et al. (2020) com GPT-3. O modelo identifica o mapeamento entre entradas e saídas e generaliza para novas entradas.

**Práticas recomendadas.** A Anthropic recomenda **3-5 exemplos diversos e relevantes**, encapsulados em tags XML (`<example>`, `</example>`). Pesquisa de Min et al. (2022) revelou que **o espaço de labels e a distribuição dos inputs importam mais que a correção dos labels** — até labels aleatórios superam zero-shot. A **ordem dos exemplos importa significativamente** (Lu et al., 2021), recomendando-se testar múltiplas ordenações.

**Quando NÃO usar.** Com **modelos de raciocínio avançados** (o1, R1, GPT-5): exemplos podem **prejudicar a performance** ao restringir o processo de raciocínio. Após ~5-10 exemplos, retornos são decrescentes. Few-shot padrão não ajuda em raciocínio multi-passo complexo — para isso, use CoT.

**Custo de tokens.** Moderado a alto: cada exemplo adiciona 50-200+ tokens. Em sistemas multi-agentes, exemplos competem com o orçamento limitado da janela de contexto de subagentes.

**Combinações eficazes.** Few-shot + CoT (a combinação mais poderosa — base do paper de Wei et al., 2022); few-shot + XML tags (recomendação da Anthropic); few-shot + role prompting para estilo + formato.

### System Prompts versus User Prompts

O **system prompt** define o framework comportamental persistente do modelo — identidade, restrições, regras de formato, guardrails de segurança. O **user prompt** carrega a tarefa dinâmica específica — dados, perguntas, exemplos contextuais.

**Melhores práticas em produção.** Colocar role e restrições no system prompt (persistência entre turnos), exemplos few-shot no user prompt (flexibilidade por tarefa), e queries ao **final** do prompt após documentos/contexto — testes da Anthropic mostram **melhoria de até 30% na qualidade** quando a pergunta está no final. **Prompt caching** (disponível na Anthropic e OpenAI) reduz dramaticamente o custo de system prompts repetidos.

**Em arquiteturas multi-agentes**, system prompts são **críticos**: definem completamente o comportamento de cada subagente (stateless por natureza). Conforme o blog de engenharia da Anthropic: *"Como cada agente é dirigido por um prompt, prompt engineering foi nossa principal alavanca para melhorar comportamentos... prompts precisam ser mais explícitos, detalhados e intencionais."*

---

## Técnicas de raciocínio: quando o modelo precisa "pensar"

### Chain-of-Thought (CoT): o raciocínio passo a passo

**Definição e funcionamento.** Introduzido por Wei et al. (2022), CoT encoraja o modelo a gerar passos intermediários de raciocínio antes da resposta final. Três variantes: **Few-Shot CoT** (exemplos manuais com raciocínio explícito), **Zero-Shot CoT** (adicionar "Vamos pensar passo a passo"), e **Auto-CoT** (Zhang et al., 2022 — geração automática de cadeias diversas).

**Benchmarks quantitativos.** No GSM8K, PaLM 540B saltou de **17,9% para 58,1%** com CoT (>3x de melhoria). Com Self-Consistency: **74%**. Flan-PaLM com CoT+SC: **83,9%**. Modelos modernos com 8-shot CoT: Llama 3.1 405B alcança **96,8%**, GPT-4o **96,1%**, Claude 3.5 Sonnet **96,4%**.

**Quando NÃO usar.** Modelos pequenos (<100B parâmetros) produzem cadeias "fluentes mas ilógicas" que **prejudicam** a acurácia. Em **modelos de raciocínio** (o1, R1), um estudo da Wharton (2025) encontrou apenas **2-3% de melhoria marginal** com aumento de **20-80% no tempo de resposta**. Um estudo do NeurIPS 2024 ("Chain of Thoughtlessness") demonstrou que CoT só ajuda quando exemplos anotados correspondem de perto à query — conforme problemas se generalizam, a acurácia cai para níveis de prompting padrão. **Tarefas simples de um passo** ganham pouco ou nada.

**Custo de tokens.** Requisições CoT levam **35-600% mais tempo** que requisições diretas. A alternativa **Chain of Draft (CoD)** iguala a acurácia usando apenas **~7,6% dos tokens**. A Anthropic recomenda usar tags XML (`<thinking>`, `<answer>`) para separação estruturada e sempre permitir que o modelo externalize seu raciocínio.

### Tree of Thoughts (ToT): exploração e backtracking

**Definição.** Introduzido por Yao et al. (2023, NeurIPS), ToT generaliza CoT ao permitir exploração de múltiplos caminhos de raciocínio organizados em árvore, com autoavaliação e backtracking. Quatro módulos: decomposição de pensamentos, geração de candidatos, avaliação de estados (o LLM classifica como "certo/talvez/impossível"), e algoritmo de busca (BFS/DFS).

**Benchmarks surpreendentes.** No Game of 24: GPT-4 com CoT alcançou **4%** de sucesso; com ToT, **74%** — melhoria de **18,5x**. Descrito como **~10x mais preciso que CoT** em benchmarks de planejamento e busca.

**Quando NÃO usar.** Problemas simples e lineares (overkill massivo); aplicações sensíveis a latência; ambientes com restrição de tokens — ToT requer **5-20x mais chamadas de API** que CoT. Cada avaliação requer múltiplas amostras do LLM.

**Combinações.** CoT é um caso especial de ToT (árvore de profundidade 1, largura 1). **Graph of Thoughts (GoT)** estende ToT permitindo múltiplos nós-pai e operações de agregação — obteve **62% de melhoria** sobre ToT em tarefas de ordenação com **>31% de redução de custo**.

### ReAct: raciocínio + ação com ferramentas

**Definição.** Introduzido por Yao et al. (2022, ICLR 2023), ReAct sincroniza raciocínio verbal e ações no ambiente externo em um loop iterativo **Pensamento → Ação → Observação**. O modelo raciocina sobre o estado atual, executa uma ferramenta (busca, calculadora, API), recebe o resultado, e repete.

**Performance.** No ALFWorld (tomada de decisão interativa), ReAct superou métodos de imitação e RL por **34% absolutos** de taxa de sucesso com apenas 1-2 exemplos. No Fever (verificação de fatos), **supera CoT** ao reduzir alucinações via recuperação de informação fundamentada. Os melhores resultados gerais vêm de **ReAct + CoT-SC combinados**.

**Quando NÃO usar.** Tarefas de raciocínio puro sem necessidade de dados externos (CoT basta); quando nenhuma ferramenta está disponível (ReAct perde metade do valor); tarefas de perguntas factuais simples; quando resultados de busca são provavelmente ruins. À medida que o número de ferramentas cresce, modelos cometem mais erros.

**Importância em multi-agentes.** **ReAct é O padrão fundamental para agentes de IA modernos.** LangChain (`create_react_agent`), CrewAI, LangGraph e AutoGen implementam ReAct como seu loop central de agente. Google Cloud recomenda começar com ReAct antes de escalar para multi-agentes.

### Self-Consistency: votação majoritária sobre múltiplos caminhos

**Definição.** Proposto por Wang et al. (2022, ICLR 2023), substitui a decodificação greedy no CoT: amostra **N caminhos de raciocínio diversos** (temperatura >0) para o mesmo problema e seleciona a resposta mais frequente por votação majoritária.

**Resultados.** Sobre CoT no GSM8K: **+17,9%**; SVAMP: **+11%**; AQuA: **+12,2%**. Tão poucas quanto **3 amostras** já melhoram sobre CoT greedy. Completamente não-supervisionado — sem treinamento, anotação ou fine-tuning adicional.

**Quando NÃO usar.** Geração aberta/criativa (sem resposta "correta" para votar); aplicações sensíveis a latência; custo restrito — **multiplica o custo de tokens pelo número de amostras** (5-30x). Retornos decrescentes após 20-30 caminhos. **Universal Self-Consistency (USC)** é uma variante onde o próprio LLM escolhe a melhor resposta, eliminando a necessidade de votação externa.

---

## Técnicas avançadas e estruturais para sistemas de produção

### Prompt Chaining: decomposição em pipeline

Prompt chaining quebra tarefas complexas em subtarefas sequenciais, onde a saída de uma alimenta a entrada da próxima. Tipos: **sequencial** (linear), **condicional** (ramificação if/else baseada na saída do LLM), **iterativo** (loops gerar → criticar → refinar), e **paralelo** (subtarefas independentes simultâneas).

**Caso prático típico.** Análise de documentos: extrair citações relevantes → sintetizar resposta → auto-revisão de acurácia. Cada passo usa um prompt focado com objetivo único. Frameworks como LangChain (operador pipe `|` do LCEL), LangGraph (grafos com ciclos e edges condicionais), e Vellum (construtor visual) implementam chaining nativamente.

**Trade-offs.** Custo tipicamente **2-5x** maior que prompt único. Latência aditiva — cada elo adiciona uma ida-e-volta completa à API. Compensa com maior qualidade, controlabilidade e debuggabilidade. Conforme a documentação mais recente da Anthropic: *"Com pensamento adaptativo e orquestração de subagentes, Claude lida internamente com a maioria do raciocínio multi-passo. Prompt chaining explícito ainda é útil quando você precisa inspecionar saídas intermediárias ou impor uma estrutura de pipeline específica."*

### Meta-Prompting: prompts que geram prompts

Meta-prompting tem três acepções na literatura. **Scaffolding (Suzgun & Kalai, 2024):** transforma um LM em "condutor" que orquestra múltiplas instâncias "especialistas" com contexto fresco ("Fresh Eyes"). **Otimização prática (OpenAI Cookbook):** usar um modelo forte (o1-preview) para gerar/otimizar prompts para um modelo mais barato (GPT-4o). **Estrutural (Zhang et al., 2023):** formaliza a estrutura de tarefas usando teoria de categorias.

**Resultados.** Suzgun & Kalai: meta-prompting com GPT-4 superou prompting padrão em **17,1%**, expert prompting em **17,3%**, e multipersona em **15,2%** (média em Game of 24, Checkmate-in-One, Python Programming Puzzles). Zhang et al.: Qwen-72B com meta-prompt zero-shot alcançou **46,3% no MATH** e **83,5% no GSM8K**.

**Ferramentas.** O gerador de prompts da Anthropic, DSPy (Stanford NLP, 30k+ stars no GitHub — otimiza pipelines de prompts com Signatures, Modules e Optimizers), e TEXTGRAD (feedback em linguagem natural como "gradientes textuais").

### Structured Output: saídas em JSON, XML e schemas

Técnicas para forçar saídas de LLMs em formatos legíveis por máquina. Três níveis de rigor: **prompt engineering** (instruir em texto — ~35% de conformidade), **JSON mode da API** (garante JSON válido mas não schema), e **structured outputs com constrained decoding** (100% de conformidade de schema via máquinas de estados finitos que mascaram tokens inválidos durante a geração).

**Descoberta crítica sobre raciocínio.** Forçar JSON durante raciocínio **degrada a acurácia em 10-15%** (estudo "Let Me Speak Freely?", EMNLP 2024). A prática recomendada é usar **duas etapas**: raciocínio livre primeiro, formatação estruturada depois — acurácia salta de **48% para 61%** em tarefas de agregação. Colocar campos de raciocínio **antes** dos campos de resposta no schema permite que o modelo "pense" dentro do formato estruturado.

**Comparação de formatos.** JSON minificado é mais eficiente em tokens e tem **78,5% de acurácia** de compreensão pelo LLM. XML é **14% menos eficiente** mas a Anthropic treinou Claude especificamente para reconhecer XML, gerando **15-20% de boost de performance**. YAML é bom para configuração humana. TOON (formato tabular) usa **40% menos tokens** para dados tabulares.

**Ferramentas modernas.** OpenAI Structured Outputs (API nativa com `strict: true`); Anthropic Structured Outputs (beta desde novembro 2025, constrained decoding); Outlines (open-source); XGrammar (overhead próximo de zero — ~50μs por token); Instructor (biblioteca de alto nível para Pydantic).

### RAG Prompting Patterns: contexto externo fundamentado

RAG (Retrieval-Augmented Generation) combina recuperação de documentos externos com geração do LLM. Os padrões de prompt para RAG são o que determina a qualidade das respostas.

**Padrões essenciais.** **(1) Context Injection básico:** system prompt com regras de grounding + contexto recuperado no user prompt. **(2) Dual Prompt Structure:** separar camadas — system prompt persistente com papel e regras, user prompt dinâmico com contexto e pergunta. Regra-chave: *"Nunca misture estas camadas — a maioria da instabilidade em RAG vem de mesclá-las"* (StackAI, 2026). **(3) N-Shot RAG:** incluir exemplos demonstrando como respostas devem ser derivadas do contexto. **(4) CoT RAG:** guiar raciocínio sobre conteúdo recuperado passo a passo. **(5) Agentic RAG:** o LLM decide quando recuperar usando tool calls.

**Evolução.** Naive RAG (simples index → retrieve → generate) → Advanced RAG (reranking, filtragem, otimização de pré-recuperação) → **Modular RAG** (componentes plugáveis, reescrita de query, recuperação multi-hop, orquestração por agentes) — o padrão de produção em 2025-2026.

**Custo.** Busca vetorial adiciona **50-200ms** de latência. Chunks recuperados consomem **1-4K tokens** por query. Prompt caching e estratégias "just in time" de contexto mitigam custos.

---

## Técnicas de fronteira: inovações de 2022 a 2026

### Constitutional AI e Self-Critique

Metodologia de alinhamento da Anthropic (Bai et al., 2022) que treina modelos usando princípios escritos (uma "constituição") ao invés de feedback humano extensivo. Duas fases: **supervisionada** (modelo critica e revisa suas próprias respostas contra princípios constitucionais) e **RL** (RLAIF — RL from AI Feedback). Como **técnica de prompting**, implementa loops critique → revision explícitos no prompt.

**Aplicabilidade.** Produção-ready — core dos modelos Claude. Elimina necessidade de labels humanos de harmfulness. Modelos CAI igualam ou superam RLHF em harmlessness mantendo helpfulness. Custo: **2-3x** por resposta devido aos ciclos de crítica-revisão. Modelos pequenos (7-9B) mostram capacidade limitada de auto-crítica.

### Automatic Prompt Engineering (APE)

APE (Zhou et al., 2022) enquadra geração de instruções como otimização black-box: LLMs geram candidatos de prompt, executam cada um, e selecionam o melhor por score de avaliação. Alcançou performance de nível humano em **24/24** tarefas de Instruction Induction. Descobriu prompts melhores que os humanos, como *"Let's work this out in a step by step way to be sure we have the right answer"* — que melhorou MultiArith de 78,7 para 82,0.

**OPRO (Google DeepMind):** usa LLMs como otimizadores via meta-prompt com pares instrução-score anteriores. Superou prompts humanos em **até 8%** no GSM8K e **até 50%** em Big-Bench Hard. Descobriu: *"Take a deep breath and work on this problem step-by-step."*

**DSPy (Stanford NLP):** framework que substitui prompt engineering manual por pipelines otimizáveis com Signatures, Modules e Optimizers (MIPROv2, COPRO, SIMBA, GEPA). Acurácia de avaliação de prompts: **46,2% → 64,0%** com otimização. 30k+ stars no GitHub, amplamente adotado em produção.

### Directional Stimulus Prompting (DSP)

Li et al. (2023, NeurIPS) usa um pequeno modelo de política treinável (T5) para gerar estímulos direcionais — dicas, keywords, cues — específicos por instância que guiam um LLM frozen black-box. **41,4% de melhoria** no ChatGPT para diálogo (MultiWOZ com apenas 80 exemplos). Custo mínimo por query (apenas tokens do estímulo), mas requer treinar o modelo de política.

### Skeleton-of-Thought (SoT)

Ning et al. (Microsoft Research, ICLR 2024) reduz latência de geração: primeiro gera um esqueleto (outline com 3-5 palavras por ponto), depois expande cada ponto em **paralelo**. **≥2x de speedup** em 8/12 modelos testados. Qualidade comparável ou melhor em **60%** dos casos. Até **3,72x de speedup** no LLaMA-2. Não usar para: matemática, código, raciocínio sequencial.

### Emotion Prompting

Li et al. (2023, Microsoft Research) demonstra que adicionar estímulos emocionais (*"Isto é muito importante para minha carreira"*, *"Estou contando com você!"*) melhora performance em **>10%** em 45 tarefas. Custo zero de implementação. Mais eficaz para tarefas criativas e abertas.

### Step-Back Prompting (Google DeepMind)

Zheng et al. (2023) instrui o LLM a primeiro responder uma questão de abstração mais alta antes de enfrentar a query específica. Melhoria de **7-27%** sobre CoT dependendo da tarefa. Exemplo: em vez de resolver diretamente a questão sobre gases ideais, primeiro perguntar "Qual é a lei dos gases ideais?" → PV = nRT → aplicar ao problema.

### Rephrase and Respond (RaR)

Deng et al. (2024) instrui o LLM a reformular a pergunta antes de responder. Pode ser one-step (*"Reformule e expanda a pergunta, e responda"*) ou two-step (reformulação separada da resposta). Eficaz em QA e raciocínio simbólico. Combina bem com CoT. Zero overhead de implementação.

### Thread of Thought (ThoT)

Substitui "Vamos pensar passo a passo" por: *"Caminhe por este contexto em partes gerenciáveis passo a passo, resumindo e analisando conforme avançamos."* Superior para tarefas de compreensão de contexto longo e análise documental. Drop-in replacement para zero-shot CoT.

### Multimodal CoT e prompts visuais

**Multimodal CoT** (Meta/AWS, ICLR 2024): framework de dois estágios separando geração de justificativa (texto+imagens) de inferência de resposta. Modelo sub-1B parâmetros alcançou SOTA no ScienceQA. **Compositional CoT (CCoT)** (CVPR 2024): gera grafos de cena como passos intermediários para raciocínio visual. **Interleaved-Modal CoT (ICoT)** (CVPR 2025): intercala justificativas visuais e textuais.

---

## Análise comparativa e matriz de decisão

### Performance por técnica e benchmark

| Técnica | GSM8K (impacto) | Custo tokens | Latência | Melhores cenários |
|---------|-----------------|-------------|----------|-------------------|
| Zero-shot | Baseline (~85% tarefas simples) | Mínimo | Mínima | Classificação, tradução, QA simples |
| Few-shot (3-5) | +25-40% vs zero-shot | Moderado | Baixa | Formato, padrão, extração |
| Chain-of-Thought | +30-50% raciocínio | 2-3x | Média | Matemática, lógica, análise |
| Self-Consistency | +12-18% sobre CoT | 5-30x | Alta (paralelizável) | Aritmética, raciocínio crítico |
| Tree of Thoughts | 18,5x sobre CoT (Game of 24) | 5-20x chamadas | Muito alta | Puzzles, planejamento, exploração |
| ReAct | +34% abs. em ALFWorld | 2-5x por loop | Média-alta | Tool use, QA fundamentado |
| Prompt Chaining | N/A (qualitativo) | 2-5x | Aditiva por elo | Pipelines, documentos, workflows |
| Structured Output | N/A | +10-20% (JSON) | Similar | APIs, extração, inter-agentes |
| Meta-Prompting | +17,1% vs padrão | Alto (otimização) | Alta | Multi-domínio, otimização |
| Step-Back | +7-27% vs CoT | ~2x | Dupla | Raciocínio abstrato, física |
| SoT | Qualidade ≈ | Maior | **≥2x mais rápido** | QA, conselhos, paralelizável |

### Matriz de decisão por tipo de tarefa

Para **classificação e extração simples**, começar com zero-shot — se insuficiente, adicionar 2-3 exemplos few-shot com tags XML. Para **raciocínio multi-passo**, usar CoT (few-shot para modelos padrão, zero-shot para modelos de raciocínio). Para **tarefas de alta confiabilidade**, adicionar Self-Consistency (aceitar custo 5-10x). Para **problemas de exploração e planejamento**, ToT. Para **tarefas com ferramentas e dados em tempo real**, ReAct. Para **workflows complexos multi-etapa**, prompt chaining. Para **saídas consumidas por sistemas**, structured outputs com constrained decoding.

### Matriz por tier de modelo

A descoberta mais contra-intuitiva de 2025-2026: **a técnica ótima depende do modelo**. Kusano et al. (2025) testaram 23 tipos de prompt em 12 LLMs com resultados radicalmente diferentes.

- **Modelos de raciocínio** (o1, o3, R1, GPT-5): zero-shot, sem exemplos, sem "pense passo a passo" — essas instruções **prejudicam** a performance.
- **Modelos frontier padrão** (GPT-4o, Claude Sonnet 4.5, Gemini 1.5 Pro): few-shot CoT, XML tags para Claude, templates estruturados para GPT.
- **Modelos mid-tier** (GPT-4o-mini, Claude Haiku, Llama 3 8B): prompting complexo com mais exemplos e CoT explícito — **beneficiam-se mais** de engenharia de prompts.
- **Modelos pequenos** (<10B params): few-shot extensivo, instruções detalhadas. CoT só funciona com modelos de **100B+** parâmetros.

### Restrições de custo e otimização

Pesquisa de Levy, Jacoby & Goldberg (2024) encontrou que **performance de raciocínio começa a degradar em torno de 3.000 tokens**. O sweet spot prático para a maioria das tarefas: **150-300 palavras** de prompt. **TALE-EP** (ACL 2025) reduz tokens de CoT em **67%** com **59% de redução de custo** mantendo performance competitiva. Prompt otimizado versus naive pode significar **$706/dia versus $3.000/dia** em 100K chamadas — **70% de redução de tokens** com qualidade idêntica ou superior.

---

## Impacto em arquiteturas multi-agentes e subagentes

### De prompts para context engineering

O campo evoluiu de otimizar prompts individuais para gerenciar **todo o contexto** que alimenta o modelo. Na formulação de Andrej Karpathy (junho 2025): *"O LLM é uma CPU, a janela de contexto é RAM, e você é o sistema operacional."* Context engineering inclui instruções, definições de ferramentas, memória, resultados de ferramentas anteriores e saídas estruturadas.

### Os cinco padrões de workflow da Anthropic

O guia "Building Effective Agents" da Anthropic (dezembro 2024) define cinco padrões composíveis que representam o estado da arte:

- **Prompt Chaining:** saída de uma chamada LLM alimenta a próxima; cada passo pode incluir verificações programáticas
- **Routing:** classificar input e direcionar para prompts/agentes especializados
- **Paralelização:** múltiplas chamadas LLM simultâneas
- **Orchestrator-Worker:** LLM central decompõe tarefas dinamicamente e delega a workers
- **Evaluator-Optimizer:** um LLM gera, outro avalia; refinamento iterativo

O princípio dominante é **"encontrar a solução mais simples possível, só aumentando complexidade quando necessário"**. Começar com prompts simples → otimizar com avaliação → adicionar sistemas agentic apenas quando soluções mais simples falham.

### Como técnicas de prompting se aplicam em multi-agentes

**Role prompting** é o mecanismo de especialização — cada agente recebe persona com metas, heurísticas de decisão e políticas de interação. No sistema EvoMAC (ICLR 2025), prompts de agentes são **iterativamente evoluídos** durante teste, superando sistemas estáticos humanos em **26,48%** em Website Basic e **34,78%** em Game Basic.

**Prompt chaining** é a espinha dorsal de workflows — a saída de um agente alimenta o próximo. **ReAct** é o loop central de cada agente individual (Pensamento → Ação → Observação). **Structured outputs** garantem comunicação confiável entre agentes via JSON/schemas. **RAG** integra-se como estratégia de contexto "just in time" — recuperar apenas quando necessário, em vez de pré-carregar todo o contexto.

As **quatro estratégias de contexto do LangChain** para multi-agentes são fundamentais: **Write** (persistir contexto externamente), **Select** (recuperar via RAG), **Compress** (sumarizar e compactar), **Isolate** (separar contextos de diferentes agentes para evitar contaminação cruzada).

### Frameworks de multi-agentes em produção

**CrewAI** adota uma metáfora de equipe com roles, backstory e metas por agente — ideal para prototipagem rápida e pipelines de conteúdo. **LangGraph** oferece grafos de estado com checkpointing e execução durável — ideal para produção com requisitos de auditabilidade e compliance. **AutoGen** (Microsoft, 54,7k+ stars) usa conversação multi-agente com execução de código — ideal para debate, refinamento iterativo e geração de código. **OpenAI Agents SDK** implementa dois padrões: agents-as-tools (hub-and-spoke) e handoffs (peer-to-peer com transferência de controle). O Gartner projeta que **40% das aplicações enterprise** terão agentes de IA integrados até o final de 2026.

---

## Combinações sinérgicas e conflitos entre técnicas

### Combinações que amplificam resultados

**CoT + Self-Consistency** produz os maiores ganhos quantitativos em raciocínio: +12-18% de acurácia sobre CoT sozinho. **ReAct + CoT-SC** é a combinação com melhor performance geral segundo o paper original — combina raciocínio interno com ações externas e votação por consistência. **Few-shot + Structured Output** é o padrão de produção para extração de dados: exemplos ensinam o formato, constrained decoding garante conformidade. **Role + CoT + Restrições de formato** cria "layered prompting" que reduz ambiguidade e melhora acurácia e consistência simultaneamente. **RAG + Prompt Chaining** fundamenta cada etapa em conhecimento recuperado — o padrão dominante em sistemas de pesquisa.

### Combinações que prejudicam ou são redundantes

**Few-shot + modelos de raciocínio** (o1, R1): exemplos restringem o processo de raciocínio e **reduzem** performance. **CoT explícito + modelos de raciocínio**: redundante — esses modelos já raciocinam internamente; instruções de CoT são contraproducentes. **Self-Consistency + tarefas simples**: custo massivo (5-30x) com benefício mínimo. **ToT + raciocínio simples**: over-engineering onde CoT basta. **Formatação agressiva (ALL-CAPS, "NUNCA", "JAMAIS") + modelos Claude recentes**: produz resultados piores. **Contexto longo + raciocínio complexo**: performance degrada após ~3.000 tokens.

### A estratégia de stacking em 6 camadas

Baseado na síntese de 1.500 papers por Gupta (2025): **(1)** Definir objetivos de negócio claros. **(2)** Escolher técnicas específicas por tarefa (CoT para raciocínio, Chain-of-Table para dados, instruções diretas para a maioria). **(3)** Otimizar para o modelo específico (XML para Claude, templates para GPT, zero-shot para modelos de raciocínio). **(4)** Implementar testes automatizados — **otimização automática de prompts supera otimização manual por margem significativa**. **(5)** Monitorar e iterar (modelos mudam, distribuições de dados mudam). **(6)** Balancear custo total e qualidade.

---

## Conclusão: o que muda agora e para onde caminha o campo

A engenharia de prompts em 2026 não é mais sobre encontrar as "palavras mágicas" — é sobre **arquitetar o contexto certo para o modelo certo no momento certo**. Três insights transformam a prática atual. Primeiro, a descoberta de que modelos de raciocínio avançados **performam pior** com técnicas clássicas como few-shot e CoT explícito inverte a sabedoria convencional e exige que engenheiros testem antes de assumir. Segundo, a automação de prompt engineering (APE, OPRO, DSPy) está tornando a otimização manual progressivamente obsoleta — sistemas automatizados criam prompts melhores em 10 minutos do que especialistas humanos em 20 horas. Terceiro, a transição para context engineering em arquiteturas multi-agentes significa que o prompt individual é apenas uma peça de um sistema complexo onde memória, ferramentas, recuperação de contexto e orquestração de subagentes devem funcionar em harmonia.

A recomendação mais consistente de Anthropic e OpenAI permanece deceptivamente simples: **comece com a solução mais simples possível e só aumente a complexidade quando demonstravelmente necessário**. Em um campo onde novas técnicas surgem semanalmente, a disciplina de medir, testar e simplificar é o diferencial entre engenharia eficaz e complexidade desnecessária.

# Fontes de Referência — Engenharia de Prompts (2022–2026)

> Curadoria de links oficiais, papers acadêmicos e documentações técnicas consultados para o relatório de técnicas de prompt engineering.
> Última atualização: Março/2026

---

## 1. Documentação Oficial dos Providers

### Anthropic (Claude)

- [Multishot Prompting — Claude API Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting)
- [Chain of Thought Prompting — Claude API Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought)
- [Let Claude Think (Extended Thinking)](https://docs.anthropic.com/en/docs/let-claude-think)
- [Chain Complex Prompts (Prompt Chaining) — Claude API Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts)
- [Long Context Prompting Tips — Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)
- [Prompt Generator — Claude API Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-generator)
- [Console Prompting Tools (Prompt Improver)](https://console.anthropic.com/docs/en/build-with-claude/prompt-engineering/prompt-improver)
- [Effective Context Engineering for AI Agents — Anthropic Engineering Blog](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [How We Built Our Multi-Agent Research System — Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)

### OpenAI

- [Reasoning Best Practices — OpenAI API Docs](https://platform.openai.com/docs/guides/reasoning-best-practices)
- [Structured Model Outputs — OpenAI API Docs](https://platform.openai.com/docs/guides/structured-outputs)
- [Enhance Your Prompts with Meta Prompting — OpenAI Cookbook](https://developers.openai.com/cookbook/examples/enhance_your_prompts_with_meta_prompting)

### Google Cloud / DeepMind

- [Choose a Design Pattern for Your Agentic AI System — Google Cloud Architecture](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)
- [What is RAG? — Google Cloud](https://cloud.google.com/use-cases/retrieval-augmented-generation)

### LangChain

- [Subagents — LangChain Docs](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents)
- [Build a RAG Agent with LangChain](https://docs.langchain.com/oss/python/langchain/rag)

### DSPy (Stanford NLP)

- [Optimizers — DSPy Docs](https://dspy.ai/learn/optimization/optimizers/)

---

## 2. Papers Acadêmicos (arXiv e Conferências)

### Surveys e Meta-Análises

- [The Prompt Report: A Systematic Survey of Prompt Engineering Techniques (Schulhoff et al., 2024)](https://arxiv.org/abs/2406.06608)
- [Unleashing the Potential of Prompt Engineering for LLMs — ScienceDirect (2025)](https://www.sciencedirect.com/science/article/pii/S2666389925001084)
- [Smarter AI Through Prompt Engineering: Insights and Case Studies (2025)](https://arxiv.org/pdf/2602.00337)

### Chain-of-Thought e Variantes

- [Chain-of-Thought Prompting Elicits Reasoning in LLMs (Wei et al., 2022) — JMLR](https://jmlr.org/papers/volume25/23-0870/23-0870.pdf)
- [Chain of Thoughtlessness? An Analysis of CoT in Planning — NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/3365d974ce309623bd8151082d78206c-Paper-Conference.pdf)
- [The Decreasing Value of Chain of Thought in Prompting — Wharton Generative AI Labs](https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/)

### Tree of Thoughts / Graph of Thoughts

- [Tree of Thoughts: Deliberate Problem Solving with LLMs (Yao et al., 2023)](https://arxiv.org/pdf/2305.10601)
- [Graph of Thoughts: Solving Elaborate Problems with LLMs (Besta et al., 2023)](https://arxiv.org/abs/2308.09687)
- [Graph of Thoughts — AAAI 2024 Proceedings](https://dl.acm.org/doi/10.1609/aaai.v38i16.29720)

### ReAct

- [ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022)](https://arxiv.org/abs/2210.03629)
- [ReAct Paper — Full PDF](https://arxiv.org/pdf/2210.03629)

### Constitutional AI

- [Constitutional AI: Harmlessness from AI Feedback (Bai et al., 2022)](https://arxiv.org/abs/2212.08073)
- [Constitutional AI — Full Paper PDF](https://arxiv.org/pdf/2212.08073)
- [How Effective Is Constitutional AI in Small LLMs? (2025)](https://arxiv.org/html/2503.17365v1)

### Automatic Prompt Engineering e Otimização

- [APE: Automatic Prompt Engineer — Project Page](https://sites.google.com/view/automatic-prompt-engineer)
- [OPRO: Large Language Models as Optimizers (Yang et al., 2023)](https://arxiv.org/abs/2309.03409)
- [OPRO — OpenReview](https://openreview.net/forum?id=Bb4VGOWELI)
- [Is It Time To Treat Prompts As Code? Multi-Use Case Study for DSPy (2025)](https://arxiv.org/html/2507.03620)

### Directional Stimulus Prompting

- [Guiding LLMs via Directional Stimulus Prompting (Li et al., 2023)](https://arxiv.org/abs/2302.11520)

### Skeleton-of-Thought

- [Skeleton-of-Thought: Prompting LLMs for Efficient Parallel Generation (Ning et al., 2023)](https://arxiv.org/abs/2307.15337)
- [Skeleton-of-Thought — Project Page (Microsoft Research)](https://sites.google.com/view/sot-llm)
- [Skeleton-of-Thought — Microsoft Research Blog](https://www.microsoft.com/en-us/research/blog/skeleton-of-thought-parallel-decoding-speeds-up-and-improves-llm-output/)

### Multimodal CoT

- [Multimodal Chain-of-Thought Reasoning in Language Models — OpenReview](https://openreview.net/forum?id=gDlsMWost9)
- [Compositional Chain-of-Thought Prompting for Large Multimodal Models — CVPR 2024](https://openaccess.thecvf.com/content/CVPR2024/papers/Mitra_Compositional_Chain-of-Thought_Prompting_for_Large_Multimodal_Models_CVPR_2024_paper.pdf)
- [CCoT — GitHub (Official Code)](https://github.com/chancharikmitra/CCoT)

### Meta-Prompting

- [Meta-Prompting: Enhancing Language Models with Task-Agnostic Scaffolding (Suzgun & Kalai, 2024)](https://github.com/suzgunmirac/meta-prompting)
- [Meta Prompting for AI Systems — Official Implementation](https://github.com/meta-prompting/meta-prompting)

---

## 3. Guias Técnicos e Referências Educacionais de Alta Qualidade

### Prompt Engineering Guide (DAIR.AI)

- [Basics of Prompting](https://www.promptingguide.ai/introduction/basics)
- [Zero-Shot Prompting](https://www.promptingguide.ai/techniques/zeroshot)
- [Few-Shot Prompting](https://www.promptingguide.ai/techniques/fewshot)
- [Chain-of-Thought Prompting](https://www.promptingguide.ai/techniques/cot)
- [Tree of Thoughts (ToT)](https://www.promptingguide.ai/techniques/tot)
- [ReAct Prompting](https://www.promptingguide.ai/techniques/react)
- [Prompt Chaining](https://www.promptingguide.ai/techniques/prompt_chaining)
- [Automatic Prompt Engineer (APE)](https://www.promptingguide.ai/techniques/ape)
- [Retrieval Augmented Generation (RAG)](https://www.promptingguide.ai/techniques/rag)
- [RAG for LLMs — Research Section](https://www.promptingguide.ai/research/rag)

### Learn Prompting

- [Shot-Based Prompting: Zero-Shot, One-Shot, and Few-Shot](https://learnprompting.org/docs/basics/few_shot)
- [Chain-of-Thought Prompting](https://learnprompting.org/docs/intermediate/chain_of_thought)
- [Is Role Prompting Effective?](https://learnprompting.org/blog/role_prompting)
- [The Prompt Report: Insights from the Most Comprehensive Study](https://learnprompting.org/blog/the_prompt_report)
- [Step-Back Prompting](https://learnprompting.org/docs/advanced/thought_generation/step_back_prompting)
- [Rephrase and Respond (RaR) Prompting](https://learnprompting.org/docs/advanced/zero_shot/rephrase_and_respond)
- [Skeleton-of-Thought Prompting](https://learnprompting.org/docs/advanced/decomposition/skeleton_of_thoughts)

### Lil'Log (Lilian Weng / OpenAI)

- [Prompt Engineering — Comprehensive Overview](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)

---

## 4. Blogs Técnicos de Empresas e Pesquisadores

### IBM

- [Prompt Engineering Techniques](https://www.ibm.com/think/topics/prompt-engineering-techniques)
- [What is a ReAct Agent?](https://www.ibm.com/think/topics/react-agent)
- [Directional Stimulus Prompting](https://www.ibm.com/think/topics/directional-stimulus-prompting)
- [Prompt Chaining with LangChain](https://www.ibm.com/think/tutorials/prompt-chaining-langchain)

### AWS

- [Enhance Performance with Self-Consistency Prompting on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/enhance-performance-of-generative-language-models-with-self-consistency-prompting-on-amazon-bedrock/)

### ByteByteGo

- [How Anthropic Built a Multi-Agent Research System](https://blog.bytebytego.com/p/how-anthropic-built-a-multi-agent)

### Hugging Face

- [Prompt Engineering in Multi-Agent Systems with KaibanJS](https://huggingface.co/blog/darielnoel/llm-prompt-engineering-kaibanjs)

### DataCamp

- [CrewAI vs LangGraph vs AutoGen: Choosing the Right Multi-Agent Framework](https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen)
- [Prompt Chaining Tutorial: What Is Prompt Chaining and How to Use It](https://www.datacamp.com/tutorial/prompt-chaining-llm)

### Towards Data Science

- [Systematic LLM Prompt Engineering Using DSPy Optimization](https://towardsdatascience.com/systematic-llm-prompt-engineering-using-dspy-optimization/)

### Neptune.ai

- [Strategies for Effective Prompt Engineering](https://neptune.ai/blog/prompt-engineering-strategies)

### Mercity Research

- [Comprehensive Guide to Chain-of-Thought Prompting](https://www.mercity.ai/blog-post/guide-to-chain-of-thought-prompting/)
- [Advanced Prompt Engineering Techniques](https://www.mercity.ai/blog-post/advanced-prompt-engineering-techniques/)
- [Comprehensive Guide to ReAct Prompting and Agentic Systems](https://www.mercity.ai/blog-post/react-prompting-and-react-based-agentic-systems/)

### PromptHub

- [Prompt Engineering for AI Agents](https://www.prompthub.us/blog/prompt-engineering-for-ai-agents)
- [A Complete Guide to Meta Prompting](https://www.prompthub.us/blog/a-complete-guide-to-meta-prompting)

### Vellum

- [Zero-Shot vs Few-Shot Prompting: A Guide with Examples](https://vellum.ai/blog/zero-shot-vs-few-shot-prompting-a-guide-with-examples)
- [Learn Prompt Chaining: Simple Explanations and Examples](https://www.vellum.ai/blog/what-is-prompt-chaining)

### Outros

- [Prompt Engineering Best Practices 2026 — Thomas Wiegold](https://thomas-wiegold.com/blog/prompt-engineering-best-practices-2026/)
- [A Practitioner's Guide to Prompt Engineering in 2025 — Maxim](https://www.getmaxim.ai/articles/a-practitioners-guide-to-prompt-engineering-in-2025/)
- [Prompt Engineering Statistics 2025 — SQ Magazine](https://sqmagazine.co.uk/prompt-engineering-statistics/)
- [Reduce LLM Costs: Token Optimization Strategies — Rost Glukhov](https://www.glukhov.org/post/2025/11/cost-effective-llm-applications)
- [Prompt Engineering Techniques: Top 6 for 2026 — K2view](https://www.k2view.com/blog/prompt-engineering-techniques/)
- [The Ultimate Prompt Engineering Guide for 2026 — Sariful Islam](https://sarifulislam.com/blog/prompt-engineering-2026/)
- [Chain-of-Thought (CoT): Prompting and LLM Reasoning Explained — AltexSoft](https://www.altexsoft.com/blog/chain-of-thought-prompting/)
- [CoT Prompting: Complete Overview 2025 — SuperAnnotate](https://www.superannotate.com/blog/chain-of-thought-cot-prompting)
- [Tree-of-Thought Prompting: Key Techniques and Use Cases — Helicone](https://www.helicone.ai/blog/tree-of-thought-prompting)
- [Tree of Thoughts Prompting — Cameron R. Wolfe, Ph.D.](https://cameronrwolfe.substack.com/p/tree-of-thoughts-prompting)
- [Advanced Prompt Engineering: Tree-of-Thoughts — Deepgram](https://deepgram.com/learn/tree-of-thoughts-prompting)
- [Optimize Token Efficiency When Prompting — Portkey](https://portkey.ai/blog/optimize-token-efficiency-in-prompts/)
- [Accelerating LLMs with Skeleton-of-Thought Prompting — Portkey](https://portkey.ai/blog/skeleton-of-thought-prompting/)
- [3 Research-Driven Advanced Prompting Techniques — KDnuggets](https://www.kdnuggets.com/3-research-driven-advanced-prompting-techniques-for-llm-efficiency-and-speed-optimization)
- [Optimize Your ChatGPT Prompts with DeepMind's OPRO — TechTalks](https://bdtechtalks.com/2023/11/20/deepmind-opro-llm-optimization/)
- [I Spent a Month Reading 1,500+ Research Papers on Prompt Engineering — Aakash Gupta](https://aakashgupta.medium.com/i-spent-a-month-reading-1-500-research-papers-on-prompt-engineering-7236e7a80595)

---

## 5. Structured Output e Formatos

- [Structured Model Outputs — OpenAI API Docs](https://platform.openai.com/docs/guides/structured-outputs)
- [Taming LLM Outputs: Guide to Structured Text Generation — Dataiku](https://www.dataiku.com/stories/blog/your-guide-to-structured-text-generation)
- [How Structured Outputs and Constrained Decoding Work — Let's Data Science](https://www.letsdatascience.com/blog/structured-outputs-making-llms-return-reliable-json)
- [LLM Structured Output: JSON, YAML, XML & TOON — Michael Hannecke](https://medium.com/@michael.hannecke/beyond-json-picking-the-right-format-for-llm-pipelines-b65f15f77f7d)

---

## 6. RAG (Retrieval-Augmented Generation) — Guias Especializados

- [Prompt Engineering for RAG Pipelines: Complete Guide 2026 — StackAI](https://www.stackai.com/blog/prompt-engineering-for-rag-pipelines-the-complete-guide-to-prompt-engineering-for-retrieval-augmented-generation)
- [RAG — Prompt Engineering Guide](https://www.promptingguide.ai/techniques/rag)
- [RAG for LLMs — Research Section](https://www.promptingguide.ai/research/rag)
- [Build a RAG Agent — LangChain Docs](https://docs.langchain.com/oss/python/langchain/rag)
- [What is RAG? — Google Cloud](https://cloud.google.com/use-cases/retrieval-augmented-generation)

---

## 7. System Prompts, Role Prompting e Fundamentos

- [LLM System Prompt vs. User Prompt — Nebuly](https://www.nebuly.com/blog/llm-system-prompt-vs-user-prompt)
- [What Should Go in System Prompt vs User Prompt — Hamel Husain](https://hamel.dev/blog/posts/evals-faq/what-should-go-in-the-system-prompt-vs-the-user-prompt.html)
- [What is Role Prompting? — PromptLayer](https://www.promptlayer.com/glossary/role-prompting/)
- [Role Prompting: How to Steer LLMs with Persona-Based Instructions — WaterCrawl](https://watercrawl.dev/blog/Role-Prompting)
- [Role-Based Prompting — GeeksforGeeks](https://www.geeksforgeeks.org/artificial-intelligence/role-based-prompting/)

---

## 8. Referência Enciclopédica

- [Prompt Engineering — Wikipedia](https://en.wikipedia.org/wiki/Prompt_engineering)