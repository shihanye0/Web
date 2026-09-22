---
title: "Natural-Language Agent Harnesses 论文总介绍"
date: 2026-07-08
tags: [paper, agent-harness, ai-agent, evaluation, codex, claude-code]
status: done
source:
  - "/home/user/Downloads/paper/Natural-Language Agent Harnesses-dual.pdf"
related:
  - "[[Natural-Language Agent Harnesses-]]"
  - "[[Natural-Language-Agent-Harnesses-4plus-integrated-notes]]"
  - "[[Natural-Language Agent Harnesses-图表解读]]"
  - "[[Natural-Language-Agent-Harnesses-与-Embodied-Reasoner-关联和心得]]"
---

# Natural-Language Agent Harnesses 论文总介绍

## 先回答最关键的问题

这篇论文 **不是提出一个新模型**，也不是像 Transformer、MoE、VLM 那样提出一种新的神经网络结构。

它提出的是一种 **agent 系统层面的新表示方式和执行框架**：

- **NLAH（Natural-Language Agent Harness）**：用结构化自然语言表达 agent 的高层控制逻辑。
- **IHR（Intelligent Harness Runtime）**：一个共享运行时，用来解释并执行这些自然语言 harness。

所以如果要在“新模型 / 新架构 / 新方法”里归类，它更接近：

> **新 agent 架构思想 + 新 harness 表示方式 + 新运行时框架。**

但要注意，这里的“架构”不是模型内部架构，而是 **agent 外部控制架构**。它关心的不是模型参数怎么设计，而是模型之外那套控制系统怎么组织。

一句话概括：

> 本文想把原本埋在代码里的 agent 控制逻辑，抽出来变成可读、可执行、可迁移、可比较、可消融的自然语言构件。

## 它到底研究的是什么对象

论文研究的对象叫 **harness**。

在 agent 系统里，harness 可以理解为“控制 agent 如何运行的一整套外部逻辑”。它包括：

- 任务如何分阶段；
- 什么时候调用模型；
- 什么时候调用工具；
- 如何记录状态；
- 如何委派子 agent；
- 如何验证输出；
- 失败后如何重试；
- 什么时候停止；
- 最终产物放在哪里；
- 如何判断任务完成。

这和模型本身不同。

模型是“会思考/生成文本/调用工具的核心能力”；harness 是“让这个能力按照某种流程持续工作”的控制系统。

可以这样类比：

| 概念 | 类比 |
|---|---|
| LLM | 发动机 |
| Tool / API | 车轮、刹车、传感器 |
| Harness | 驾驶系统和行车规则 |
| Runtime | 真正执行规则的车载系统 |
| NLAH | 用自然语言写出来的驾驶流程说明 |

论文真正想说的是：过去大家太关注发动机，也就是模型本身，但越来越多 agent 的成败其实取决于驾驶系统，也就是 harness。

## 它不是在做什么

读这篇论文时，容易误解为它在做下面几件事，但其实不是。

### 1. 它不是提出新大模型

论文没有训练一个新的 LLM，也没有提出新的模型参数结构。实验里使用的是现成模型和 Codex 后端。模型只是执行系统的一部分，不是本文的主要贡献。

### 2. 它不是提出一个新的 agent 算法

它没有发明新的 ReAct、RAG、Reflection、多智能体算法。相反，它把这些已有 agent control pattern 视为 harness pattern，研究如何把它们显式表示和执行。

### 3. 它不是说自然语言可以替代代码

这是很重要的点。论文明确不是主张用自然语言取代代码。

它的分工是：

- 自然语言负责表达高层控制逻辑；
- 代码、脚本、工具负责确定性操作；
- runtime 负责解释自然语言逻辑并调用工具执行。

也就是说，NLAH 不是“用自然语言写 Python”，而是“用自然语言写 agent 的控制协议”。

### 4. 它不是证明流程越复杂越好

论文结果反而证明：更多 verifier、多候选搜索、多 agent 编排不一定提升结果。结构只有在对齐最终验收目标时才有价值。

## 它提出了什么

## 1. Natural-Language Agent Harness（NLAH）

NLAH 是一种结构化自然语言表示，用来描述 agent harness 的高层逻辑。

一份 NLAH 里应该明确：

- **Contracts**：输入输出要求、格式约束、权限边界、停止条件。
- **Roles**：planner、solver、verifier、debugger 等角色。
- **Stage structure**：plan -> execute -> verify -> repair 这样的阶段结构。
- **Adapters and scripts**：哪些确定性操作交给工具或脚本。
- **State semantics**：哪些状态要跨步骤保留，如何重新打开。
- **Failure taxonomy**：失败类型和恢复策略。

这相当于把 agent 的“工作流程、职责划分、验收标准、失败恢复”都写成一个可执行说明书。

这里的关键不是“自然语言”本身，而是 **自然语言承载的是结构化控制逻辑**。

## 2. Intelligent Harness Runtime（IHR）

IHR 是执行 NLAH 的运行时。

因为 NLAH 是自然语言，所以不能像普通代码一样直接运行。IHR 的做法是在运行循环里放一个 LLM，让它每一步读取：

- 当前 NLAH；
- 当前任务状态；
- 当前环境和文件；
- runtime charter；
- 预算和契约约束；

然后决定下一步该做什么。

IHR 包含三部分：

- **In-loop LLM**：解释 harness 逻辑并选择下一步行动。
- **Backend**：提供工具调用、终端、文件、子 agent 能力。
- **Runtime Charter**：定义契约、状态、编排、子 agent 生命周期等通用语义。

这就把“任务专属逻辑”和“通用运行时”分开了。

## 3. File-backed state

这是整篇论文最实用的机制之一。

作者认为长任务失败的重要原因是：状态只存在模型上下文窗口里，容易被截断、遗忘、压缩、混淆。

所以他们让状态写入文件系统：

- `TASK.md` 保存任务说明；
- `RESPONSE.md` 保存标准化结果；
- `state/task_history.jsonl` 保存子任务和状态提升历史；
- `children/*/TASK.md` 保存子 agent 任务包；
- `children/*/RESPONSE.md` 保存子 agent 返回；
- `artifacts/` 保存最终可评判产物。

这样状态变成：

- path-addressable：可以通过路径重新打开；
- durable：不会随上下文窗口消失；
- compaction-stable：上下文压缩后仍然可恢复；
- auditable：可以回看任务过程和证据链。

这也是本文对我使用 Codex / Claude Code 最有启发的部分。

## 作者到底想表达什么

这篇论文的核心表达可以拆成四层。

## 第一层：Agent 成败越来越依赖模型外部控制层

传统观点容易把 agent 能力归因于模型本身。模型越强，agent 越强。

但作者认为，这已经不够了。现代 agent 往往不是一次模型调用，而是长期运行、多轮交互、工具调用、状态积累、失败恢复的系统。

在这种系统里，真正影响结果的常常是：

- 上下文如何组织；
- 是否有记忆；
- 是否有验证；
- 是否有反思；
- 是否能调用工具；
- 是否能委派子 agent；
- 是否能保存中间产物；
- 是否能从失败中恢复。

这些都属于 harness。

所以作者想把 harness 从“胶水代码”提升为“值得研究的一等系统对象”。

## 第二层：现在的 harness 太隐式，导致不可迁移、不可比较、不可消融

现有 agent harness 通常散落在：

- controller code；
- prompt template；
- framework defaults；
- tool adapters；
- verifier scripts；
- runtime assumptions；
- shell 脚本；
- 文件路径约定。

这会带来几个问题：

- 换框架就要重写；
- 换任务就要重写；
- 不同系统难以公平比较；
- 很难单独消融某个模块；
- 不知道性能变化来自模型、prompt、工具、状态还是验证逻辑。

作者认为，这会让 agent 研究停留在“比较整个 controller bundle”，而不是比较可解释的模块。

## 第三层：NLAH + IHR 让 harness 成为可执行、可迁移、可比较对象

作者的解决方案是：

```text
高层控制逻辑 -> 写成 NLAH
通用执行语义 -> 放到 IHR
确定性操作 -> 交给工具、脚本、backend
状态和产物 -> 文件化保存
```

这样同一份 harness 可以：

- 被人读懂；
- 被 runtime 执行；
- 被迁移到不同任务或后端；
- 被分模块消融；
- 被系统比较；
- 被后续自动搜索或优化。

论文真正想推动的是一种新研究方向：

> harness representation science

也就是研究“agent 控制逻辑如何表示、组合、迁移、评估”。

## 第四层：更多结构不等于更好，关键是对齐最终验收

这篇论文很重要的一点是，它没有把 NLAH/IHR 包装成“性能全面提升”的故事。

实验结果反而说明：

- Full IHR 明显改变 agent 行为；
- 但不一定提高最终分数；
- self-evolution 有明显帮助；
- file-backed state 有帮助；
- verifier 可能有害；
- multi-candidate search 可能成本高但效果差；
- 结构化流程可能偏离最终 evaluator。

所以作者真正表达的是：

> Harness 是强控制变量，但这个变量必须被设计、验证和消融，不能盲目增加结构。

这和我使用 AI 编程工具的经验非常一致。让 Codex / Claude Code 多开几个 agent、多跑几个 verifier、多写几份计划，不一定更好。只有当这些结构帮助我更接近最终验收，它才有价值。

## 实验到底证明了什么

论文实验围绕三个问题。

## RQ1：Harness 是否真的影响行为

作者比较 Full IHR、去掉 runtime skill、去掉 harness skill。

结果说明：

- 最终分数变化不一定大；
- 但 token、工具调用、LLM 调用、运行时间变化很大；
- 大量工作转移到 child agents；
- 说明 harness 不是 prompt 装饰，而是真实改变系统行为。

这个实验回答的是：

> Harness 会不会真的改变 agent？

答案是：会，而且改变很大。

## RQ2：Harness 模块能不能消融

作者逐个添加模块：

- file-backed state；
- evidence-backed answering；
- verifier；
- self-evolution；
- multi-candidate search；
- dynamic orchestration。

结果说明：

- self-evolution 在 SWE 上提升明显；
- file-backed state 在 OSWorld 上提升明显；
- verifier 和 multi-candidate search 不一定有效；
- 模块效果集中在边界样本，而不是整体均匀提升。

这个实验回答的是：

> 显式化后的 harness 能不能像模块一样比较？

答案是：可以。但比较结果说明结构有好有坏。

## RQ3：代码 harness 能不能迁移成自然语言 harness

作者把 OS-Symphony 的原生代码 harness 迁移成 NLAH。

结果说明：

- NLAH 版本得分更高；
- 行为机制从 GUI 局部修复转向 file-backed state 和 artifact-backed verification；
- 重点不是复现完全相同内部轨迹，而是保持任务级可比较行为。

这个实验回答的是：

> 原本写在代码里的 harness 高层逻辑，能不能迁移到自然语言表示？

答案是：在一定范围内可以，而且迁移后可能带来更好的状态管理和验证闭环。

## 它和“模型架构”的区别

如果把 AI 系统分层，可以这样看：

```text
模型层: LLM / VLM / 多模态模型
能力层: 推理、生成、视觉理解、代码生成
工具层: shell、浏览器、文件、API、数据库
Harness 层: 任务分解、状态、验证、重试、委派、停止
Runtime 层: 执行 harness 的通用规则和后端接口
评估层: benchmark、日志、指标、官方 evaluator
```

这篇论文主要在 **Harness 层 + Runtime 层**。

它不是改模型内部结构，而是改 agent 外部控制结构的表示和执行方式。

所以它对模型研究者的意义是：不要只看 base model，要控制 scaffold / harness 变量。

对工程使用者的意义是：不要只写 prompt，要设计任务契约、状态、验证和失败恢复。

## 它和 Embodied-Reasoner 的关系

Embodied-Reasoner 是一个具体具身 agent 方法。它关注模型如何在 AI2-THOR 中观察、思考、行动、搜索、操作和完成任务。

Natural-Language Agent Harnesses 更上层。它不关心某个具身任务怎么做，而关心：

- 多轮 agent 的任务如何定义；
- 状态如何保存；
- 工具如何接入；
- 轨迹如何记录；
- 验证如何对齐最终 evaluator；
- harness 模块如何消融。

可以这样理解：

| 维度 | Embodied-Reasoner | Natural-Language Agent Harnesses |
|---|---|---|
| 研究对象 | 具身任务 agent | agent harness 表示和运行时 |
| 核心轨迹 | Observation-Thought-Action | Agent call / artifact / child workspace |
| 主要贡献 | 具身搜索、反思、训练流程 | NLAH、IHR、file-backed state |
| 评估关注 | Success、Efficiency、Completeness | 行为变化、模块消融、迁移保真 |
| 对我的帮助 | 理解具身任务怎么评估 | 理解 agent 评估系统怎么组织 |

所以 NLAH 对具身方向的价值是间接的：它帮我理解评估系统和轨迹组织，而不是直接提供具身智能方法。

## 对我使用 Codex / Claude Code 的启发

这篇论文对 AI 编程工具的启发非常直接。

过去容易把 Codex / Claude Code 当成“会写代码的聊天框”。但从这篇论文看，更好的理解是：

> Codex / Claude Code 是一个需要 harness 管住的多轮 agent。

也就是说，工具效果不只取决于模型，还取决于我如何设计使用流程。

对应到实际使用：

## 1. 任务要有契约

不要只说“帮我修一下”。应该明确：

- 目标是什么；
- 不改什么；
- 验收命令是什么；
- 失败后怎么停手；
- 输出需要包含哪些证据。

## 2. 状态要外部化

长任务不能只靠聊天上下文。应该让 agent 写：

- 当前目标；
- 已改文件；
- 验收命令；
- 失败日志；
- 未闭合风险；
- 下一步动作。

这就是 file-backed state 在编程工具中的落地。

## 3. 验证要对齐最终目标

agent 自己说“已解决”不算。局部 verifier 说通过也不一定算。

真正的验收是：

- 测试通过；
- 构建通过；
- 页面真实渲染正常；
- API 返回正确；
- 数据库状态正确；
- benchmark evaluator 通过。

## 4. 多 agent 和 verifier 不要滥用

论文结果说明，更多结构不一定更好。

小 bug 应该小闭环解决。只有当任务真的需要并行覆盖、独立审查、跨模块搜索时，才值得使用多 agent 或 Codex second opinion。

## 5. 反思必须绑定失败信号

让 agent “反思一下”没有意义。有效的是：

```text
失败日志 -> 可证伪假设 -> 最小修改 -> 重跑同一验收
```

这就是 self-evolution 真正有价值的地方。

## 我对这篇论文的最终理解

这篇论文想表达的不是“自然语言比代码好”，也不是“提出了一个更强 agent 模型”。

它真正想表达的是：

> Agent 系统的核心竞争力正在从单次模型调用，转向长任务中的控制逻辑、状态管理、验证闭环和失败恢复。为了研究和复用这些能力，我们需要把 harness 从代码胶水里抽出来，变成可执行、可迁移、可比较的对象。

更短一点：

> 它提出的不是新模型，而是一种让 agent 控制逻辑成为一等公民的新系统框架。

如果只把它当成一篇 benchmark 提分论文，会读偏。它更像一篇 **agent 工程范式论文**：告诉我未来评价 agent，不能只问模型多强，还要问 harness 怎么设计、状态怎么保存、验证怎么对齐、失败怎么恢复。

## 读完后我应该记住什么

1. **它不是新模型，是新 harness 表示和运行时框架。**
2. **NLAH 负责表达高层控制逻辑，IHR 负责解释执行。**
3. **代码没有被取代，确定性操作仍然靠工具和脚本。**
4. **file-backed state 是长任务可靠性的关键机制。**
5. **更多结构不等于更好，结构必须对齐最终验收。**
6. **实验贡献主要是证明 harness 可执行、可消融、可迁移。**
7. **对我使用 Codex / Claude Code 的启发是：要设计自己的 AI 编程 harness。**

