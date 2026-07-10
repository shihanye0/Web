---
title: Harness 论文答疑总览
date: 2026-07-10
tags:
  - LLM-Agent
  - Harness
  - Benchmark
  - Evaluation
  - Obsidian
status: review
related:
  - "[[Harness 模块显化、消融与诊断评估方法论]]"
  - "[[General Modular Harness 与我的评估方向关联和读后迁移]]"
  - "[[Natural-Language Agent Harnesses 论文总介绍]]"
---

# Harness 论文答疑总览

这份笔记只整理“我为什么困惑、现在怎么理解、还有哪些潜在问题”。它不是某一篇论文的摘要，而是把两篇 harness 论文读完之后，对 `harness 显化`、`模块拆分`、`消融实验`、`诊断型 benchmark` 的问题集中整理，方便复习和向老师汇报。

## 一句话总理解

我现在可以把 harness 理解为：

> 一个外部化的多轮 agent 控制系统。它不只是让模型回答当前输入，而是负责把环境状态、历史信息、反馈信号、行动约束、任务规则和反思机制组织起来，使模型能够持续地感知、记忆、判断、行动和恢复。

所以，harness 研究的重点不是“模型本身会不会推理”，而是：

> 多轮任务中，哪些外部控制结构在帮助模型表现得像 agent；这些结构能否被拆出来、替换掉、消融掉，并被稳定评估。

---

## Q1：什么叫“显化 harness”？

**短答：**  
显化 harness 就是把原来混在 prompt、controller、环境 wrapper、日志处理、动作解析、反馈处理里的隐性控制逻辑，拆成有名字、有输入输出、有可替换实现、有实验开关的模块。

**更具体地说：**

未显化时，很多能力看起来像是模型自己完成的：

```text
环境状态 -> prompt 拼接 -> LLM -> 文本动作 -> 解析执行 -> 新状态
```

但实际中间常常藏着很多控制逻辑：

- 状态如何被压缩成模型可读输入；
- 历史记录保留多少、如何摘要；
- 失败反馈如何传给模型；
- 动作是否合法、如何解析；
- 是否要求模型反思；
- 是否给模型任务规则、目标、奖励定义；
- 是否把环境反馈转写成自然语言；
- 是否把多轮轨迹整理成上下文。

显化之后，结构会变成：

```text
Environment
  -> Perception / Observation Formatter
  -> Memory / Trajectory State
  -> Reasoning / Planning / Reflection
  -> Action Grounding / Parser
  -> Feedback / Evaluation
  -> Environment
```

关键不是名字变多了，而是每一段都可以被观察、替换、关掉、比较。

---

## Q2：这么多模块，作者是怎么“精准找到”要显化的模块的？

**短答：**  
不是凭空精准找到，而是从 agent 的多轮闭环中，按功能边界和失败类型拆出来。

一般有三个来源。

第一，从 agent 循环拆：

```text
看见什么 -> 记住什么 -> 如何判断 -> 如何行动 -> 如何接收反馈 -> 如何调整
```

因此常见模块包括：

- perception：把环境状态转成模型可用输入；
- memory/context：保存历史、目标、轨迹、反馈；
- reasoning/planning：基于当前状态和历史做决策；
- action grounding：把模型输出变成环境可执行动作；
- feedback/recovery：处理错误、奖励、失败信号；
- self-evaluation/reflection：对自己的行动或策略做检查。

第二，从已有系统里找“混杂控制逻辑”。  
如果论文说 harness 隐藏在 controller 中，意思通常是：controller 里同时做了状态格式化、prompt 拼接、动作解析、错误恢复、日志记录、策略约束等事情。显化就是把这些职责从 controller 里按功能抽离出来。

第三，从失败模式倒推模块。  
如果模型失败时经常出现这些现象，就说明可能存在可评估组件：

- 看错状态：perception 问题；
- 忘记目标或历史：memory/context 问题；
- 知道状态但决策差：reasoning/planning 问题；
- 说得对但动作格式错：action grounding 问题；
- 失败后重复犯错：feedback recovery 或 reflection 问题。

所以“精准”不是一次性命名准确，而是通过：

```text
功能假设 -> 模块接口 -> 消融/替换 -> 行为日志 -> 误差归因
```

不断验证这个模块是否真有独立解释力。

---

## Q3：模块边界怎么定义？为什么一篇论文的 memory 包含 context 和 reflection，另一篇又把它们拆开？

**短答：**  
模块边界不是自然界固定存在的，而是论文作者为了某个评估问题定义出来的功能边界。不同论文拆法不同，不一定矛盾。

判断一个模块边界是否合理，可以看四个标准：

1. **输入输出是否清楚**：这个模块吃什么，产出什么？
2. **功能是否相对单一**：它主要解决哪类问题？
3. **是否可替换或可消融**：能否关掉它，或换成另一个实现？
4. **是否对应可观察失败类型**：它出问题时，日志里能否看出特定错误？

例如 memory 可以有粗粒度和细粒度两种拆法。

粗粒度拆法：

```text
Memory = 历史上下文 + 轨迹摘要 + 反思记录 + 经验保留
```

这种适合回答：

> 让 agent 拥有跨轮历史信息，整体是否有帮助？

细粒度拆法：

```text
Context Window Management
Self-Evaluation / Reflection
Long-term Memory
Episodic Trajectory
```

这种适合回答：

> 到底是上下文历史有帮助，还是反思总结有帮助，还是长期经验有帮助？

因此，一篇论文把 reflection 放进 memory，不代表 reflection 本质上必须属于 memory；另一篇把 reflection 单独拆出来，也不代表前一篇错。区别在于研究问题的粒度。

**向老师汇报时可以这样说：**

> 我理解模块不是绝对分类，而是评估假设的操作化定义。粗粒度模块适合证明某类 harness 能力整体有效，细粒度模块适合进一步做机制归因。后续如果我要做自己的评估，需要先确定研究问题粒度，再决定模块边界。

---

## Q4：传统裸模型本身不是也有感知、记忆、推理能力吗？为什么加 harness 后才说有这些模块？

**短答：**  
裸模型内部当然可能具备感知、记忆和推理能力，但这些能力是隐性的、不可控的、不可单独消融的。harness 研究的是外部显式结构，而不是模型参数内部的能力。

裸模型游戏循环通常是：

```text
当前状态 -> LLM/VLM -> 下一步动作
```

这里模型内部可能做了：

- 从文本或图像中理解状态；
- 在上下文窗口里保留一些历史；
- 进行推理；
- 生成动作。

但问题是，这些过程都包在模型内部或一次 prompt 里，研究者很难单独回答：

- 是看不懂状态，还是记不住历史？
- 是记住了但规划差，还是动作解析错？
- 加历史信息到底帮助了多少？
- 反思是有用，还是只是 prompt 变长导致的效果？

harness 的意义是把这些能力外部化：

```text
Perception module: 明确负责状态表示
Memory module: 明确负责历史保留
Reasoning module: 明确负责计划或反思
Action module: 明确负责动作约束和解析
```

这样才能做模块级对比，而不是只看最终分数。

---

## Q5：如果 LLM 可以调用 agent，那裸模型和 harness 的边界在哪里？

**短答：**  
如果 LLM 可以调用外部工具、记忆、规划器、动作解析器，那么它已经不是纯裸模型，而是在一个 agent harness 里运行。

可以这样区分：

```text
裸模型：主要是单次输入输出，控制结构不外显。
Agent：模型 + 外部状态 + 工具 + 控制循环。
Harness：支撑 agent 运行、评估和交互的外部控制系统。
```

所以问题不是“LLM 能不能调用 agent”，而是：

> 这个调用过程、状态管理、工具接口、反馈机制、动作执行逻辑是否被显式建模，并能否被评估。

---

## Q6：为什么消融时有的论文只删 perception 和 memory，没有删 reasoning？

**短答：**  
可能因为 reasoning 在该论文里不是一个可独立关闭的外部模块，而是主要由 LLM 本身或固定 prompt 承担。消融实验通常只能消融作者显式实现并可替换的部分。

reasoning 有两种情况。

一种是外部 reasoning 模块，例如明确的 planner、tree search、self-reflection、deliberation step。这种可以消融。

另一种是模型内部 reasoning，例如直接让 LLM 根据输入输出动作。这种不容易消融，因为一旦移除推理，就等于不让模型做任务。

所以如果论文没有对 reasoning 做消融，可能说明：

- reasoning 没有被实现成独立外部模块；
- reasoning 是所有实验条件共享的基础能力；
- 作者关注的是 perception/memory 这两个更可控的外部增益；
- 去掉 reasoning 会让任务定义失去意义。

这不是说 reasoning 不重要，而是说它没有被该实验设计成可单独干预的变量。

---

## Q7：prompt 模块是干什么的？为什么模块消融还要谈 prompt？

**短答：**  
prompt 是 harness 的接口层。它决定模块信息如何被模型读到，因此会显著影响实验结果。

即使 perception、memory、reasoning 模块一样，prompt 不同也可能导致模型表现差很多。例如：

```text
同样的记忆内容
Prompt A: 清楚告诉模型如何使用历史
Prompt B: 只是把历史堆在后面
```

两者性能差异可能来自 prompt，而不是 memory 模块本身。因此论文需要处理 prompt 的影响。

prompt 标准化要回答的问题是：

> 实验结果是不是被某个 prompt 模板的偶然性污染了？

如果模块有效性只在某个特殊 prompt 下成立，那结论就不稳。作者优化 prompt 的目的通常不是让某一个模型单独最好，而是找到在任务和模型集合上更稳定、更公平的模板。

---

## Q8：prompt 是如何优化和统一的？是不是选择所有模型都最好的 prompt？

**短答：**  
通常不是选择“所有模型都最好”的 prompt，因为不同模型的最优 prompt 可能不同。更合理的目标是选择一个跨模型、跨任务表现稳定、方差较小、语义一致的 prompt。

可以理解为两阶段：

第一阶段，搜索或调试多个候选 prompt。  
作者会尝试不同模板，看哪些表达能稳定让模型理解任务、规则、输出格式和模块信息。

第二阶段，固定一个标准 prompt。  
在正式评估中，所有模型尽量使用同一套或等价语义的 prompt，避免每个模型被单独调参。

这样做是在平衡两件事：

- 如果完全不优化 prompt，模型可能因为说明不清而失败；
- 如果每个模型都用专属最优 prompt，比较就不公平；
- 因此选择一个优化过但统一的 prompt，减少模板偶然性。

我的理解可以写成：

> prompt 优化是为了消除低质量提示造成的噪声；prompt 标准化是为了避免模型比较被专属提示调参污染。

---

## Q9：benchmark 是不是只是前面模块分析的总结？它是否必需？

**短答：**  
benchmark 不是简单总结，而是把模块假设放进一组可复现任务中验证。它不一定在所有研究里都“必需”，但如果目标是评估 agent 能力，benchmark 基本不可缺。

模块分析回答：

```text
我认为 agent 需要哪些组件？
每个组件可能负责什么能力？
```

benchmark 回答：

```text
这些组件在一批任务中是否真的影响行为？
不同模型、不同任务、不同模块组合下，结论是否稳定？
```

如果没有 benchmark，研究容易停留在架构描述：

```text
我设计了 perception / memory / reasoning 模块。
```

有了 benchmark，才能转向可证伪判断：

```text
去掉 memory 后，长程任务明显下降；
去掉 perception 后，状态识别错误增加；
typed feedback 对恢复失败特别有帮助。
```

所以 benchmark 不是结论的装饰，而是让模块假设接受系统检验的装置。

---

## Q10：诊断型 benchmark 和消融实验是不是重复？

**短答：**  
不重复。消融实验是诊断型 benchmark 的一种证据来源，但诊断型 benchmark 的目标更宽。

消融实验通常回答：

```text
有没有这个模块，最终分数差多少？
```

诊断型 benchmark 还想回答：

```text
模型为什么失败？
失败发生在哪个环节？
哪个模块对哪类任务帮助最大？
这种帮助是否和行为日志一致？
```

诊断型 benchmark 应该输出类似：

```text
Model A:
  Perception errors: low
  Memory errors: high in long-horizon tasks
  Action grounding errors: medium
  Feedback recovery: weak
  Best module gain: typed feedback
```

这些结果可能部分来自消融，但还需要：

- 任务分组；
- 行为轨迹日志；
- 错误类型标注；
- 模块增益对比；
- 最终分数和过程指标关联。

因此，消融是方法，诊断是目标。

---

## Q11：RQ1 里的 Runtime Charter / Runtime Skill / Harness Logic / Harness Skill 是怎么来的？

**短答：**  
这个结构来自作者对 harness 的两层拆分：一层是运行时通用规则，一层是 benchmark 专属逻辑；同时又把规则表达和实际执行技能区分开。

可以理解为一个二维表：

| 层级 | 偏规则/说明 | 偏执行/能力 |
|---|---|---|
| Runtime | Runtime Charter | Runtime Skill |
| Harness | Harness Logic | Harness Skill |

其中：

- Runtime Charter：通用运行时原则，例如如何交互、如何保持状态、如何处理多轮任务；
- Runtime Skill：实现这些通用原则的运行时能力；
- Harness Logic：某个 benchmark 或任务族的专属控制逻辑；
- Harness Skill：执行这些专属逻辑的具体能力或模块。

这不是自然产生的唯一结构，而是作者为了把“通用 agent 运行规则”和“基准专属任务逻辑”分开评估而设计的分析框架。

---

## Q12：Runtime Skill 既然是通用的，为什么还能被消融？

**短答：**  
“通用”不等于“不能关掉”。通用只说明它不绑定某一个任务，消融是为了测试它对行为有没有因果作用。

例如 Runtime Skill 可能负责：

- 维持多轮交互状态；
- 规范行动输出；
- 整理反馈；
- 保持任务约束；
- 让 agent 按某种运行协议执行。

这些能力虽然通用，但仍然可以在实验中移除或降级。目的不是说真实系统应该去掉它，而是问：

> 如果没有这层通用运行能力，模型表现是否下降？下降在哪些行为上？

所以消融的对象不是“生产系统里可随便删除的功能”，而是“研究中可干预的变量”。

---

## Q13：RQ2 消融时，Basic 本身是否还有未显化 harness 影响？实验是否不纯？

**短答：**  
有。Basic 通常仍然有最低限度的环境接口、prompt、动作解析和任务输入，所以它不是完全没有 harness 的真空状态。

这不一定是问题，因为现实中不可能让模型完全脱离输入输出接口执行任务。RQ2 的重点通常不是：

```text
完全无 harness vs 完全有 harness
```

而是：

```text
共同基础接口上，额外显化模块带来多少增量影响
```

所以应把 Basic 理解为共享底座，而不是纯裸模型。

严谨表述应该是：

> RQ2 的消融结论证明的是在共同 Basic harness 底座上，某个显式模块的增量贡献；它不能证明该模块是 agent 能力的唯一来源，也不能排除 Basic 里仍有隐式 harness 影响。

这是读这类实验时必须保留的边界。

---

## Q14：Harness 让模型更远离随机行为，这里的随机、无 harness、有 harness 怎么区分？

**短答：**

三者的区别通常是控制程度不同：

```text
Random：不理解任务，按随机策略选动作。
No Harness / Basic：模型收到当前状态和任务说明，直接输出动作。
With Harness：模型在外部感知、记忆、反馈、约束等结构帮助下行动。
```

随机策略是底线，用来表示“完全没有智能控制”的表现。  
无 harness 是模型基本能力，用来表示“模型自己读状态并行动”的表现。  
有 harness 是结构化 agent，用来表示“模型 + 外部控制系统”的表现。

如果无 harness 接近随机，说明模型没有真正形成有效策略。  
如果有 harness 明显远离随机，说明外部结构帮助模型产生了更稳定的任务行为。

---

## Q15：paired-sample t-test 中的 p 值代表什么？

**短答：**  
p 值表示：如果“两个条件其实没有真实差异”这个零假设成立，那么观察到当前差异或更极端差异的概率有多大。

在 harness 实验中，paired-sample t-test 通常比较同一组任务、同一批模型或同一批游戏回合在两个条件下的表现：

```text
With Harness vs Without Harness
Memory On vs Memory Off
Prompt A vs Prompt B
```

paired 的意思是每个样本都有配对关系，例如同一个任务在两个设置下分别跑一次。这样可以减少任务难度差异带来的噪声。

如果 p 值很小，例如 p < 0.05，通常表示：

> 在“没有真实差异”的假设下，不太可能观察到这么大的差异，因此我们倾向认为两个条件确实有统计显著差异。

但 p 值不代表效果大小，也不代表实验设计一定合理。还要看 effect size、样本量、方差、任务覆盖和实验是否有混杂变量。

---

## Q16：读完两篇 harness 论文，我和自己的评估方向有什么关联？

**短答：**  
真正有价值的迁移不是“知道了 perception/memory/reasoning 三个模块”，而是学到一种评估范式：

```text
从最终分数评价
转向
模块化机制诊断
```

以前可能只问：

```text
哪个模型分数高？
```

现在应该进一步问：

```text
它高在哪里？
是感知好，记忆好，反馈恢复好，还是动作约束好？
换任务后优势还在吗？
去掉某个模块后是否崩？
失败轨迹是否能解释分数下降？
```

这和 agent 评估方向的关系是：

- 评估对象不只是模型，而是模型 + harness + 环境接口；
- 最终分数只是结果，模块消融和行为日志才帮助解释机制；
- benchmark 不应只排榜，还应定位能力短板；
- 不同任务需要不同 harness 模块，说明评估要按任务机制设计。

---

## Q17：可否把多轮 agent 能力理解为多个模块的简单相加？

**短答：**  
不能完全理解成简单相加。模块之间有交互。

例如：

- memory 的效果依赖 perception 是否提供了正确状态；
- reasoning 的效果依赖 memory 是否提供了有用历史；
- action grounding 的效果会影响反馈是否真实；
- feedback recovery 可能反过来改变后续 reasoning。

所以更准确的理解是：

```text
agent 能力 = 模型基础能力 + harness 模块 + 模块之间的交互 + 任务环境约束
```

消融实验能说明某个模块的边际贡献，但不能自动说明所有模块独立可加。

---

## Q18：如何判断一个 benchmark 是否具有诊断能力？

**短答：**  
如果 benchmark 只能告诉我“谁分高”，它就是排行榜型；如果它还能告诉我“为什么分高/为什么失败”，它才具有诊断能力。

诊断型 benchmark 至少应该提供：

- 明确的任务能力维度；
- 可记录的中间行为轨迹；
- 可消融或可替换的 harness 模块；
- 过程错误类型，而不只有最终胜负；
- 模块增益和任务类型之间的对应关系；
- 对 prompt、随机性、模型大小等混杂因素的控制。

可以用这个问题检查：

> 如果 Model A 比 Model B 分数低，我能否知道它主要输在感知、记忆、规划、动作约束、反馈恢复，还是环境接口？

如果不能，就还不是强诊断 benchmark。

---

## Q19：这些论文对我后续做评估最重要的启发是什么？

**短答：**  
以后不要只设计一个任务集和一个总分，而要设计“任务机制 + 可观测日志 + 模块干预 + 错误归因”的完整评估框架。

可以把自己的评估问题改写成：

```text
我要评估的不是模型是否完成任务，
而是模型在某类多轮任务中，
依赖哪些外部结构完成任务，
这些结构分别影响哪类行为错误。
```

这比“做一个 benchmark 排名”更有研究价值。

---

## Q20：后续读 harness / agent benchmark 论文时，我应该固定追问哪些问题？

可以按下面清单读：

1. 这篇论文把 agent 的哪部分能力显化了？
2. 这些模块原来隐藏在哪里？
3. 每个模块的输入、输出、状态和责任是什么？
4. 模块边界是粗粒度还是细粒度？
5. 哪些模块能被消融，哪些只是共享底座？
6. baseline 是真的无 harness，还是 Basic harness？
7. prompt 是否被标准化？是否可能污染结果？
8. 消融结果看的是最终分数，还是过程错误？
9. benchmark 是排行榜型，还是诊断型？
10. 结论能否迁移到其他任务、模型和环境？
11. 是否报告了方差、显著性、effect size 或失败案例？
12. 作者有没有区分模型能力、harness 能力和环境接口能力？

---

如果迁移到我的具身评估，可以怎么做？

我可以把本文的思路迁移成一个具身 agent 消融框架。

## 1. 定义几类具身任务

```text
Search      -> 找目标物体
Manipulate  -> 开关/拿起/放下/切换状态
Transport   -> 把物体搬到容器或位置
Composite   -> 多子目标组合任务
```

每类任务都对应不同瓶颈。

## 2. 定义可消融模块

```text
Perception:
  raw image
  object list
  scene graph
  annotated image

Memory:
  no history
  last k actions
  summarized explored locations
  object-state memory

Feedback:
  no feedback
  raw error text
  typed error feedback

Reasoning / Controller:
  direct action
  plan-then-act
  reflection-after-failure
```

## 3. 定义指标

```text
Outcome:
  success rate
  task completeness

Efficiency:
  step count
  repeated search count
  invalid action count

Diagnosis:
  perception error
  memory error
  planning error
  action grounding error
  evaluator mismatch
```

## 4. 做类似本文的实验矩阵

```text
No harness
+ perception
+ memory
+ feedback
+ perception + memory
+ perception + memory + feedback
full controller
```

然后按任务类型看：

- Search 任务是否主要受益于 perception？
- Composite 任务是否主要受益于 memory？
- Manipulate 任务是否主要受益于 typed feedback？
- Transport 任务是否暴露 object-state memory 问题？
- Full harness 是否真的提升，还是只增加 token 和步骤？

这就是本文对我评估方向最大的迁移价值。


## 如何把多轮 agent 能力拆成可评估组件？

可以按下面这个流程做。

## Step 1：画运行闭环

先画清楚 agent 从任务到结果的全过程：

```text
Task instruction
  -> Observation
  -> State representation
  -> Prompt/context construction
  -> LLM/VLM call
  -> Action generation
  -> Action parsing
  -> Environment/tool execution
  -> Feedback/reward/error
  -> Memory/state update
  -> Verification/evaluator
  -> Stop or next turn
```
1. 用户说：“打开浏览器搜索天气”（Task instruction）
2. 智能体截屏看到当前桌面（Observation）
3. 提取出“桌面图标、任务栏位置”等信息（State representation）
4. 把这些信息拼成 Prompt 发给 GPT-4（Prompt construction → LLM Call）
5. GPT-4 说：“我应该点击 Chrome 图标”（Action generation）
6. 解析器把这句话翻译成：鼠标移动到 (100, 200) 点击（Action parsing）
7. 操作系统真正执行了这个点击（Environment execution）
8. 屏幕变为了浏览器界面（Feedback）
9. 智能体把“已经成功点击 Chrome”记在记忆里（Memory update）
10. 评估器检查“浏览器开了没有？”（Verification）
11. 因为还没搜索天气，所以决定进入下一轮（Next turn）
12. 新一轮：屏幕里出现了浏览器地址栏（Observation）……
这个闭环里的每个箭头都可能藏着 harness。

## Step 2：标出控制变量

问每个环节能不能被改动：

- raw observation 能否换成 structured observation？
- 是否给历史轨迹？
- 是否给错误反馈？
- 动作空间是自由文本还是有限集合？
- 是否有 verifier？
- 是否有重试？
- 是否有状态文件？
- 是否有 prompt optimization？

能被改动的就是候选变量。

## Step 3：把变量绑定到失败模式

每个模块必须回答一个失败问题：

```text
这个模块解决哪类失败？
如果拿掉它，哪类失败应该增加？
如果加上它，哪类失败应该减少？
```

如果回答不了，这个模块就只是结构装饰，不是评估模块。

## Step 4：设计最小消融矩阵

消融不是越多越好。先做能回答关键归因问题的最小矩阵。

例如具身 agent 可以这样：

```text
Base: raw image + current instruction only
+ structured perception
+ recent trajectory memory
+ typed feedback
+ constrained action parser
+ final-state verifier
Full: all modules
```

再按任务类型分组看效果。

## Step 5：记录过程指标

只看 success 不够。要记录行为机制：

- step count；
- invalid action count；
- repeated action count；
- repeated search count；
- object mismatch count；
- feedback ignored count；
- early stop count；
- verifier/evaluator mismatch；
- final state mismatch。

这些指标才能把最终分数转成行为解释。

## 如何从最终分数转向行为机制分析？

关键是不要只问：

```text
谁分数高？
```

而要问：

```text
为什么高？
高在哪里？
解决了哪类失败？
在哪类任务上有效？
代价是什么？
有没有副作用？
```

例如：

```text
Full harness success +10%
```

这只是排行榜信息。

如果进一步拆成：

```text
Search 任务 success +18%
repeated search count -35%
invalid action count 基本不变
feedback ignored count -22%
Composite 任务仍然提前终止多
```

这才是机制分析。

它说明 harness 主要改善了搜索去重和反馈利用，但还没有解决组合任务的长程规划。

## 如何把 benchmark 做成诊断工具，而不是排行榜？

排行榜 benchmark 只输出：

```text
Model A: 72
Model B: 69
Model C: 61
```

诊断型 benchmark 应该输出：

```text
Model A:
  Perception errors: low
  Memory errors: high in long-horizon tasks
  Action grounding errors: medium
  Feedback recovery: weak
  Final-state mismatch: high
  Best module gain: typed feedback
```

要做到这一点，benchmark 至少要有五个设计。

## 1. 任务按能力瓶颈分组

不要只混一个总分。要区分：

- perception-heavy；
- memory-heavy；
- planning-heavy；
- feedback-recovery-heavy；
- action-grounding-heavy；
- composite long-horizon。

General Modular Harness 选 Sokoban、Tetris、2048、Candy Crush，就是为了让不同模块的贡献有机会分化。

## 2. 每个任务保留轨迹证据

诊断必须能回看：

- observation；
- model response；
- parsed action；
- environment result；
- reward/error；
- memory update；
- final evaluator result。

没有轨迹，失败分类就是猜。

## 3. 指标不只看 outcome

至少要分三层：

| 层级 | 指标 |
|---|---|
| Outcome | success, score, task completion |
| Efficiency | steps, cost, repeated actions, time |
| Diagnosis | perception error, memory error, illegal action, evaluator mismatch |

Embodied-Reasoner 的 Success / Search Efficiency / Task Completeness 就是向这个方向迈了一步。

## 4. 模块消融要和失败类型对应

如果加 memory 后总分提升，但重复搜索没有下降、长程任务也没有提升，那 memory 的解释就站不稳。

一个好 benchmark 要能检查：

```text
模块声称解决的失败类型是否真的减少？
```

这比只看总分提升更严格。

## 5. 有代价和副作用记录

模块可能提升成功率，但增加成本或引入副作用。

例如：

- verifier 可能增加 token，但不提升最终分；
- memory 可能带来错误历史污染；
- reflection 可能让简单任务过度思考；
- multi-agent 可能增加不一致；
- prompt optimization 可能贡献性能，混淆模块归因。

诊断型 benchmark 要记录这些副作用，否则会误以为结构越多越好。


## 从其他相关笔记汇总的收获：我真正带走什么？

前面的问题解决的是“论文具体做了什么”。结合之前读的 Embodied-Reasoner、Natural-Language Agent Harnesses 和 General Modular Harness，真正可迁移的收获可以归成下面七条。

### 1. 评估对象从“模型”变成“模型 + harness + 环境接口”

多轮任务里的表现不是 base model 单独产生的。模型看到什么状态、保留什么历史、动作如何解析、失败如何反馈、最终如何验收，都会改变结果。

因此以后看到分数时，先问：

```text
这是模型能力的提升，
还是 harness、prompt、tool adapter 或 evaluator 定义改变带来的提升？
```

这不是否定模型能力，而是避免把系统层贡献误归因给模型本身。

### 2. agent 的核心评价单位是“轨迹”，不是一次输出

具身任务中的 `Observation -> Thought -> Action -> Feedback -> Next Observation`，和长程 agent 中的“状态 -> 调用 -> artifact -> 验证 -> 恢复”，本质上都是同一个闭环。

所以除了最终 success，还应该看：

- 是否重复搜索或无效循环；
- 是否遗忘已经观察到的状态；
- 是否产生非法或无法落地的动作；
- 失败反馈是否真的改变后续行为；
- 是否完成全部关键子目标，而不是只完成一部分。

这也是为什么 `efficiency`、`completeness`、错误类型和轨迹回放有价值：它们把“成功/失败”还原成行为过程。

### 3. 状态、证据和失败原因必须外部化

file-backed state 的重点不是多存几份日志，而是让关键事实可恢复、可审计、可交接。若历史只留在模型上下文中，截断、重试或复盘时都难以判断系统为何失败。

对具身或多轮 agent 评估，至少应保存：

```text
任务契约、每轮 observation、模型输入/输出、解析后的动作、环境反馈、
关键状态快照、最终结果、失败原因、指标计算依据
```

这样“memory 不足”“反馈未被利用”“动作解析失败”等结论才有证据，而不是对模型回复的主观猜测。

### 4. 中间 verifier 不能代替最终 evaluator

模型自称完成、局部动作执行成功、甚至 key action 被覆盖，都不必然代表环境最终状态满足任务。真正的成功定义必须回到任务契约指定的最终 evaluator。

这给评估设计的硬约束是：

```text
局部 verifier：帮助 agent 纠错和推进
最终 evaluator：决定 benchmark 是否成功
两者必须分别记录，也必须检查是否一致
```

如果两者不一致，不能只把它当噪声；它本身就是重要失败类型，说明 harness 的局部目标可能偏离了真实任务目标。

### 5. 模块不是越多越好，必须证明它更接近验收或降低失败率

reflection、verifier、多候选搜索、动态编排、长 CoT 都不是天然有效的模块。复杂任务上它们可能带来帮助；简单任务上也可能增加 token、步骤和干扰。

因此模块是否保留，不能只看“看起来更像 agent”，而要同时看：

```text
最终成功率是否提升？
过程效率是否恶化？
是否减少了明确的失败类型？
代价（token、步数、时间）是否值得？
```

### 6. benchmark 的价值在于形成“诊断闭环”，不只是做消融表

消融实验只回答“改动某个模块后，结果是否变化”；诊断型 benchmark 还要把这个变化和任务机制、过程日志、错误类型连接起来。

完整闭环是：

```text
任务按能力瓶颈分组
  -> 对模块实施受控干预
  -> 记录轨迹与最终验收
  -> 标注或推断错误类型
  -> 解释模块在何种任务、为何有效或无效
```

所以 benchmark 不是对前面工作的简单总结，而是让“关于 harness 的设计假设”能够被反复检验的实验装置。若目标只是部署一个能完成任务的 agent，未必必须建 benchmark；若目标是提出可比较、可迁移的研究结论，benchmark 几乎是必需的证据基础。

### 7. 我后续可以采用的最小研究模板

不必一开始就拆很多模块。可以从一个任务族、一个明确失败假设和 2-3 个可干预模块开始：

```text
任务：Search / Manipulate / Transport / Composite 中选一类或几类
假设：长程组合任务主要受状态遗忘影响
模块：memory、typed feedback、action grounding
结果：success + efficiency + completeness
诊断：memory error、feedback recovery error、action grounding error
实验：Basic、Basic + 单模块、组合模块；固定模型、任务、预算与 prompt 条件
```

这比先做一个总排行榜更容易建立因果解释，也能逐步扩展成真正的诊断型 benchmark。

---

## 向老师汇报时的简洁版本

我可以这样汇报：

> 我读完两篇 harness 论文后，最初以为核心收获只是 perception、memory、reasoning 等模块有用。但进一步梳理后，我理解它们真正的贡献是提供了一种 agent 评估方法：把原本隐藏在 controller、prompt、环境接口中的多轮控制逻辑显化为可命名、可替换、可消融、可观察的模块。这样评估就不只是比较最终分数，而是能分析模型失败来自感知、记忆、规划、动作落地还是反馈恢复。

继续说：

> 我现在也意识到模块边界不是固定的。比如 memory 在一篇论文里可能包含 context 和 reflection，在另一篇论文中又会拆成 context management 和 self-evaluation。这取决于研究问题的粒度。粗粒度模块用于证明一类能力整体有效，细粒度模块用于进一步做机制归因。

最后说：

> 所以后续如果我要做 agent 评估，不能只做排行榜式 benchmark，而应该把 benchmark 设计成诊断工具：任务要覆盖不同能力需求，运行过程要记录日志，harness 模块要能消融或替换，最终结果要能对应到具体失败机制。

---

## 仍然保留的开放问题

这些问题不是现在必须解决，但后续做研究时值得继续追：

1. 模块拆得越细，诊断越清楚，但实验成本和交互效应也越高，合理粒度如何确定？
2. 不同任务中同名模块是否真的同质？例如游戏中的 memory 和网页任务中的 memory 是否可比？
3. prompt 优化到什么程度算公平，什么时候会变成对 benchmark 的过拟合？
4. 如果 Basic baseline 已经包含隐式 harness，如何估计真正的 harness 贡献？
5. 行为错误标注是否可靠？是否需要人工标注、规则标注或模型辅助标注？
6. 模块增益是否能跨模型迁移？小模型和大模型是否依赖不同 harness？
7. 诊断型 benchmark 的结论如何转化为 agent 系统设计建议？

---

## 最后一张记忆卡片

```text
Harness 论文不是只在说：
  “感知、记忆、推理有用。”

更重要的是在说：
  “多轮 agent 的能力不能只看最终分数，
   必须把隐藏控制逻辑显化成模块，
   再通过消融、日志和任务分组，
   把 benchmark 变成诊断工具。”

我后续做评估时要关注：
  模型能力、harness 能力、环境接口能力
  这三者如何区分，以及如何被实验验证。
```
