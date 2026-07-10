---
title: "General Modular Harness 与我的评估方向关联和读后迁移"
date: 2026-07-09
tags: [paper-reflection, agent-evaluation, embodied-ai, agent-harness, modular-agent, failure-analysis]
status: review
source:
  - "[[General Modular Harness for LLM Agents in Multi-Turn Gaming Environments]]"
related:
  - "[[Natural-Language Agent Harnesses 论文总介绍]]"
  - "[[Natural-Language Agent Harnesses 与 Embodied-Reasoner 的关联和阅读心得]]"
  - "[[Embodied-Reasoner - Synergizing Visual Search Reasoning and Action for Embodied Interactive Tasks]]"
---

# General Modular Harness 与我的评估方向关联和读后迁移

## 先纠正我现在的浅层理解

我读完这篇论文后，最直接的感受是：

> 作者把 agent 外部 harness 显化成 perception、memory、reasoning 三个模块，然后证明这些模块对 agent 有帮助，而且不同任务依赖不同模块。

这个理解没错，但还停留在论文表层。

更深一层看，这篇论文对我的评估方向真正有价值的地方不是“知道感知、记忆、推理有用”，而是它提供了一种 **agent 评估实验设计方法**：

> 不要只评估模型最终得分，而要把 agent 的外部支架、输入表示、历史记忆、动作决策、任务类型和奖励指标拆成可控制变量，再通过消融实验判断每个变量对不同任务的贡献。

所以这篇论文不是简单教我“三个模块的作用”，而是教我：

- 如何把多轮 agent 能力拆成可评估组件；
- 如何用任务类型解释模块收益；
- 如何避免把模型能力、prompt、环境接口、记忆机制混在一起；
- 如何从最终分数转向行为机制分析；
- 如何把 benchmark 做成诊断工具，而不是排行榜。

## 它和我的评估方向到底有什么关系？

我的方向不是“做一个会玩游戏的 agent”，而是理解和设计 **agent / 具身智能评估**。从这个角度看，本文的价值主要有五个。

## 1. 它把评估对象从“模型”扩展到“模型 + harness”

传统评估容易问：

```text
哪个模型分数更高？
```

这篇论文提醒我，agent 评估应该问：

```text
模型在什么 harness 下分数更高？
这个 harness 给了什么状态表示？
有没有历史记忆？
有没有反思反馈？
动作选择流程是什么？
这些外部结构分别贡献了多少？
```

这很关键。因为多轮 agent 的表现并不只取决于 base model，还取决于外部系统如何组织输入、状态、反馈和动作。

比如同一个 GPT-4o：

- 直接看当前截图行动，可能接近 random；
- 加结构化 perception 后，空间任务可能明显变好；
- 加 memory 后，长程任务可能更稳；
- 加两者后，才暴露出更真实的决策能力。

所以以后看任何 agent benchmark，我都不能只问“用了哪个模型”，还要问：

- 它的 harness 是什么？
- 它给模型什么 observation？
- 它是否记录 trajectory？
- 它是否把失败反馈传回下一轮？
- 它是否允许模型从历史中纠正策略？

这和我的评估方向高度相关，因为评估的对象不再是单个模型，而是完整 agent system。

## 2. 它给了我一种“能力拆解”的评估范式

这篇论文最值得迁移的是模块消融思维。

不是只看：

```text
Full agent score = 多少
```

而是拆成：

```text
No harness
+ Perception only
+ Memory only
+ Both
```

这种设计能回答“为什么有效”，而不是只回答“有没有效”。

对我的评估方向来说，这相当于一个模板。以后我评估具身 agent 或多轮 agent，可以类似拆：

| 能力维度 | 可消融变量                                                | 想回答的问题           |
| ---- | ---------------------------------------------------- | ---------------- |
| 视觉感知 | raw image vs structured scene graph vs object list   | 失败来自看不懂，还是不会计划？  |
| 历史记忆 | no history vs recent trajectory vs summarized memory | 失败来自遗忘，还是动作选择错误？ |
| 环境反馈 | no feedback vs raw feedback vs typed error feedback  | 模型能否根据失败修正？      |
| 动作空间 | free-form action vs constrained action set           | 失败来自动作格式，还是策略？   |
| 反思机制 | no reflection vs failure-bound reflection            | 反思是否真的改变后续动作？    |
| 最终验收 | key action coverage vs final state check             | 指标是否真的对齐任务完成？    |

这比“模型 A 比模型 B 高 5 分”有用得多，因为它能定位能力瓶颈。

## 3. 它说明评估任务必须按“瓶颈类型”分类

我以前可能会笼统地说：

```text
这个任务需要感知、记忆、推理。
```

但这篇论文更细：不同任务的主瓶颈不同。

| 任务类型 | 主要瓶颈 | 对应模块 |
|---|---|---|
| Sokoban | 空间布局、死锁、对象位置 | perception + planning |
| Tetris | 几何形状、放置位置、局部空间结构 | perception |
| 2048 | 长期策略、避免破坏结构、合并路径 | memory |
| Candy Crush | 连锁反应、延迟奖励、步数管理 | memory + perception |

这对我的评估方向很重要，因为好的评估不是把所有任务混成一个平均分，而是要知道每类任务在测什么。

迁移到具身智能，可以这样看：

| 具身任务 | 可能主瓶颈 | 应该重点看什么 |
|---|---|---|
| 找物体 Search | 视觉识别、探索策略、历史去重 | 是否重复搜索、是否漏看区域 |
| 操作 Manipulate | 物体状态、动作前置条件 | 是否知道 open/pickup/toggle 的条件 |
| 搬运 Transport | 目标保持、路径和容器关系 | 是否拿起后还记得放到哪里 |
| 组合 Composite | 子目标顺序、状态更新、长程规划 | 是否完成前置子任务、是否提前终止 |

因此本文给我的不是“感知和记忆都重要”这种常识，而是：

> 评估任务要按瓶颈设计；模块收益要按任务类型解释。

## 4. 它提醒我：benchmark 要有诊断能力，而不是只排榜

如果一个 benchmark 只输出总分，我最多知道哪个模型强。但我不知道：

- 模型是看错了；
- 还是忘了历史；
- 还是动作格式错；
- 还是重复无效行动；
- 还是最终验收不对齐；
- 还是 prompt 模板偶然影响。

本文用模块消融和游戏分类，让 benchmark 变成诊断工具。

例如：

- Sokoban 加 perception 提升大，说明空间状态表示是关键瓶颈；
- 2048 加 memory 提升大，说明长程策略和历史状态是关键瓶颈；
- Candy Crush +Both 提升大，说明复杂任务需要多模块协同；
- 某些强模型在 +Both 条件下才拉开差距，说明零样本分数可能掩盖真实能力差异。

迁移到我的评估方向，我应该追求的不是：

```text
给出一个总分
```

而是：

```text
给出总分 + 失败类型 + 任务瓶颈 + 模块贡献 + 轨迹证据
```

这才是对 agent evaluation 有用的结果。

## 5. 它把 prompt、harness、model 的关系暴露出来

本文有一节 prompt standardization，看起来和三模块关系不大，但其实对评估很重要。

因为在 agent 评估里，prompt 不是中性背景。prompt 会影响：

- 模型是否遵守动作格式；
- 是否利用历史；
- 是否反思失败；
- 是否偏向某种策略；
- 是否输出冗余解释；
- 是否提前终止。

如果不控制 prompt，那么所谓 memory module 的收益，可能其实来自“memory 条件下 prompt 写得更强”。

所以本文用 DSPy/SIMBA 选跨模型平均表现最稳的 prompt。它的启发是：

> 做 agent 评估时，prompt 也是实验变量，不能假装它不存在。

这对我的方向很重要。以后我看论文或项目实验，要检查：

- prompt 是否对所有模型一致；
- prompt 是否针对某个模型调过；
- memory/perception 条件的 prompt 是否公平；
- prompt 是否泄露策略；
- prompt optimization 是否也贡献了性能；
- 作者是否把 prompt 方差当作风险处理。

## 我真正应该带走的评估方法论

## 方法论 1：评估的是 agent system，不只是 base model

多轮任务里，模型只是系统的一部分。

```text
Agent performance =
  base model
  + observation representation
  + memory design
  + action interface
  + prompt/controller
  + environment feedback
  + evaluator
```

如果不拆这些因素，就很容易把 harness 的收益误认为模型能力，或者把 prompt 的收益误认为模块能力。

## 方法论 2：每个模块必须绑定可观察失败模式

不要泛泛说“加 memory 有帮助”。要问：

```text
memory 解决了哪类失败？
```

在本文中：

- perception 主要解决空间状态理解和视觉/棋盘表示问题；
- memory 主要解决重复无效动作、长期策略不稳定、延迟奖励难追踪问题；
- reasoning/controller 主要负责把状态和历史转成动作，但没有被严格独立消融。

迁移到我的方向，每个模块都应该对应失败模式：

| 模块 | 对应失败 |
|---|---|
| perception | 看错物体、漏掉目标、空间关系错 |
| memory | 重复搜索、忘记已操作对象、子目标丢失 |
| feedback | 动作失败后继续重复、无法纠错 |
| action parser | 输出非法动作、对象名不匹配 |
| evaluator | 模型自称完成但环境未完成 |

## 方法论 3：消融实验要回答“归因”问题

一个好的评估不是只给 full system 分数，而是能归因：

```text
Full system 提升来自哪里？
```

本文的归因链是：

```text
Harness overall > No harness
Perception helps spatial games
Memory helps long-horizon games
Both exposes higher-resolution model differences
Prompt standardization reduces template noise
```

我以后设计或阅读实验，也应该找类似的归因链。

## 方法论 4：任务集要覆盖不同瓶颈

如果一个 benchmark 里所有任务都测同一种能力，它就不能诊断 agent 的模块结构。

本文选 Sokoban、Tetris、2048、Candy Crush 的价值在于，它们不是同一种游戏换皮，而是有不同瓶颈：

- 空间布局；
- 长期规划；
- 延迟奖励；
- 低容错；
- 连锁反应；
- 部分可观测。

这提醒我，具身评估任务也要覆盖不同瓶颈。否则最后只能得到一个平均分，看不出模型到底缺什么。

## 方法论 5：最终指标要和轨迹证据结合

本文看的是游戏分数，但真正有解释力的是结合模块条件和任务类型看。

迁移到具身任务，最终 success 也不够。我要结合：

- 每步 observation；
- thought / action；
- 环境反馈；
- legal / illegal action；
- 关键动作覆盖；
- 最终状态；
- 轨迹长度；
- 重复行为；
- 失败类型。

这和我之前读 Natural-Language Agent Harnesses 得到的 file-backed state 思想一致：评估结果必须能被轨迹证据解释。

## 和我之前读的两篇论文如何连起来

现在三篇论文可以形成一条线：

| 论文 | 给我的核心收获 | 在评估方向里的位置 |
|---|---|---|
| Embodied-Reasoner | 具身任务是 Observation-Thought-Action 闭环，指标要看 success、efficiency、completeness | 具体具身评估对象和指标 |
| Natural-Language Agent Harnesses | agent 成败受 harness、state、runtime、verification 影响 | 上层 agent 评估基础设施 |
| General Modular Harness | 用可消融模块和多任务环境诊断 perception/memory/reasoning 的贡献 | 模块化评估实验范式 |

这篇 General Modular Harness 正好补在两者中间：

- 它不像 Embodied-Reasoner 那样训练一个具身模型；
- 也不像 NLAH 那样研究自然语言 runtime；
- 它更像是在说：**如何把 agent harness 拆成模块，然后用多轮环境评估模块贡献。**

所以它对我不是“直接教我一个新指标”，而是教我怎么设计评估实验。

## 如果迁移到我的具身评估，可以怎么做？

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

## 我现在对这篇论文的最终定位

这篇论文不是我的方向里的“核心具身评估指标论文”，但它是很好的 **agent 评估方法论论文**。

它让我意识到：

1. agent evaluation 不能只比模型；
2. harness 本身是评估对象；
3. 模块必须可消融；
4. 任务必须按瓶颈分类；
5. prompt 必须作为实验变量控制；
6. 最终分数必须结合轨迹证据解释；
7. 不同模块适配不同任务，这件事应该通过实验矩阵证明，而不是靠直觉。

所以我不应该把收获停在“知道三个模块有作用”。更应该把它转化成一个问题清单：

> 当我看到一个 agent 评估系统时，我能不能说清楚：它在测哪个模块？这个模块解决哪类失败？任务瓶颈是什么？有没有消融？prompt 是否公平？最终指标是否能被轨迹证据解释？

如果能，这篇论文就真正被我吸收了。

## 后续阅读和实践建议

下一步最值得做的不是再背论文结论，而是把它变成评估分析模板。

可以建立一个自己的 agent evaluation 表格：

| 论文/项目 | 环境 | 任务类型 | harness 模块 | 消融变量 | 指标 | 可诊断失败 | 局限 |
|---|---|---|---|---|---|---|---|
| General Modular Harness | Gym games | Sokoban/Tetris/2048/Candy Crush | perception/memory/reasoning | ZS/+Memory/+Perception/+Both | game score, t-test, Glass's delta | 空间/长程/随机基线 | reasoning 未独立消融 |
| Embodied-Reasoner | AI2-THOR | Search/Manipulate/Transport/Composite | OTA trajectory + reflection | IL/RST/RT | SR/SE/TC | 搜索/操作/组合失败 | 需看最终状态验收 |
| NLAH | SWE/OS tasks | coding/desktop tasks | runtime/state/verifier | module ablation | success + process metrics | harness/evaluator mismatch | 不直接给具身指标 |

这个表格会比单篇论文摘要更有价值，因为它能帮助我建立自己的评估框架。

