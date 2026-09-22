---
title: "General Modular Harness for LLM Agents in Multi-Turn Gaming Environments"
date: 2026-07-09
tags: [paper, agent-harness, llm-agent, gaming, evaluation, modular-agent, memory, perception, reasoning]
aliases: [General Modular Harness, Modular Harness for Gaming Agents, 多轮游戏智能体模块化 Harness]
status: read
source:
  - "/home/user/Downloads/paper/General Modular Harness for LLM Agents in Multi-Turn Gaming Environments-dual.pdf"
related:
  - "[[Natural-Language Agent Harnesses 论文总介绍]]"
  - "[[Embodied-Reasoner - Synergizing Visual Search Reasoning and Action for Embodied Interactive Tasks]]"
---

# General Modular Harness for LLM Agents in Multi-Turn Gaming Environments

> [!info] 论文信息
> - **标题**: General Modular Harness for LLM Agents in Multi-Turn Gaming Environments
> - **作者**: Yuxuan Zhang, Haoyang Yu, Lanxiang Hu, Haojian Jin, Hao Zhang
> - **会议**: ICML 2025
> - **arXiv**: 2507.11633v1
> - **本地 PDF**: `/home/user/Downloads/paper/General Modular Harness for LLM Agents in Multi-Turn Gaming Environments-dual.pdf`
> - **阅读状态**: 已读完，但需要反复消化
> - **关键词**: LLM agent、modular harness、perception、memory、reasoning、multi-turn games、Gymnasium、ablation

## 先回答你最困惑的问题

你说自己只看到了 **感知、记忆、推理** 三个模块的重要作用，但没理解本文到底讲了什么。这个判断很正常，因为论文表面上确实围绕这三个模块展开，但它真正提出的不是“三个模块很重要”这么简单。

这篇论文真正做的是：

> **提出一个通用的、可开关的、可消融的 agent harness，用同一套外部控制框架把不同 LLM/VLM 放进多轮游戏环境里，然后系统测量感知、记忆、推理这些模块分别带来什么收益。**

也就是说，论文的重点不是发明一个新模型，也不是训练一个专门会玩游戏的模型，而是搭建一套 **模型外部的 agent 控制框架**。这个框架像一个实验平台：同一个模型，可以在没有 harness、只有 memory、只有 perception、memory + perception 等条件下运行；同一套接口，可以接入 Sokoban、Tetris、2048、Candy Crush 等不同游戏；最后通过分数、统计检验和消融实验来回答：

- 模型裸跑时到底有多弱？
- 加上结构化 perception 后，空间类游戏是否更好？
- 加上 memory 后，长程规划类游戏是否更稳？
- 两个模块一起用时，是否能产生叠加收益？
- 游戏成绩是否能反映更一般的模型能力？

所以这篇论文的核心不是“模块很重要”，而是：

> **把 agent 的外部支架模块化，然后用游戏作为统一实验场，定量分析每个模块对多轮决策能力的贡献。**

## 一句话概括

本文提出一个用于多轮游戏环境的 **General Modular Harness**：它把 LLM/VLM agent 拆成 perception、memory、reasoning 三个可插拔模块，并用 Sokoban、Tetris、2048、Candy Crush 这类 Gym-compatible 游戏作为低门槛、高多样性的实验场，证明模块化 harness 通常能显著提升 agent 表现，并揭示不同游戏依赖不同模块。

## 它不是在做什么

读这篇论文时，先排除几个误解。

### 1. 它不是提出一个新大模型

论文没有训练新的 LLM，也没有改变模型内部结构。实验对象是 Claude、Gemini、GPT、o 系列、Llama、DeepSeek、Grok 等现成模型。

作者真正关心的是：**同一个模型外面套上不同 harness 后，行为会不会变好。**

### 2. 它不是只做 game benchmark

如果只是比较谁玩游戏分数高，那就是普通游戏榜单。本文更想用游戏作为 **agent 设计实验室**。

游戏的好处是：

- 规则清楚；
- 奖励信号明确；
- 可以多轮交互；
- 不需要办公软件、网页、系统操作这类专业背景；
- 可以用 Gymnasium / Stable Retro 统一接口接入；
- 可以观察模型在空间推理、长期规划、视觉识别、重复错误纠正上的差异。

所以游戏不是目的，而是一个干净、可复现、可扩展的 agent 评测环境。

### 3. 它不是说 perception、memory、reasoning 是新概念

这三个概念当然不是作者发明的。作者的贡献在于把它们做成 **可插拔、可开关、可消融的 harness 模块**，再放进统一环境里比较。

这和只在 prompt 里写一句“请记住历史、仔细观察、认真推理”完全不同。本文的模块有明确的输入、输出、开关方式和实验条件。

### 4. 它不是证明模块越多越好

表 2 里可以看到，有些模型在某些游戏上加 memory 或 perception 并不一定提升，甚至可能下降。作者的结论更细：

- 空间结构强的任务更依赖 perception；
- 长程依赖和延迟奖励任务更依赖 memory；
- 两者结合通常更强，但不保证每个模型、每个游戏都单调提升。

## 本文提出了什么

## 1. General Modular Harness

论文提出一个通用模块化 harness。这里的 harness 可以理解为 **包在模型外面的 agent 运行支架**。

裸模型玩游戏时，通常是：

```text
当前游戏状态 -> LLM/VLM -> 下一步动作
```

本文的 harness 让流程变成：

```text
游戏环境
  -> perception 模块把观察转换成结构化状态
  -> memory 模块保存近期轨迹并生成反思摘要
  -> reasoning 模块综合当前状态、历史、反思，输出动作
  -> 环境执行动作并返回新状态/奖励
  -> 进入下一轮
```

关键是这个 harness 是 **通用的**：不是给 Sokoban 手写一套，给 2048 再手写一套，而是通过 Gymnasium 风格接口尽量统一。

## 2. 三个可插拔模块

论文把 agent 拆成三块。

### Perception Module

perception 的职责是把游戏界面转换成模型更容易理解的输入。

作者实现了三种 perception 方式：

| 模式 | 做什么 | 作用 |
|---|---|---|
| text mode | 从游戏后端直接抽取网格、坐标、对象属性 | 降低视觉误识别 |
| vision mode | 把渲染图像交给 VLM 描述 | 更贴近真实视觉输入 |
| combined mode | 同时给图像和后端结构化文本 | 输入更丰富、更稳 |

例子：Sokoban 里可以把图像转换成“Box at (2,3), Wall at (4,5), Target at ...”这样的结构化描述。

这不是普通截图理解，而是把环境状态变成适合推理的 **state representation**。

### Memory Module

memory 的职责是让模型不要只看当前一步，而是看到近期轨迹，并对上一步行动做自我评估。

它包含两部分：

- 保存最近 N 步的状态、动作、奖励；
- 比较当前状态和过去状态，生成反思摘要。

论文里的 prompt 结构大致是：

```text
[过去 N 步 trajectory, 上一步 reflection, 当前 state]
```

这和 Reflexion 思路接近：模型不只是记录“发生过什么”，还要判断“刚才那步是不是有效、有没有重复、有没有陷入无效动作”。

memory 对 2048 和 Candy Crush 特别重要，因为这类任务有长期依赖、延迟奖励和策略稳定性要求。

### Reasoning Module

reasoning 是最终控制器。它综合 perception 和 memory 的输出，决定下一步 action。

它还有一个实验上的重要作用：**允许研究者打开或关闭不同模块**。例如：

- Zero-shot：没有 memory，没有 perception；
- +Memory Only；
- +Perception Only；
- +Both。

这让论文能做表 2 那样的模块消融，而不是只说“我们整体系统比较好”。

## 3. 游戏中心的评测方法

作者选了四个游戏：

| 游戏 | 主要考察能力 | 为什么有代表性 |
|---|---|---|
| Sokoban | 空间推理、长程规划、低容错 | 一步错可能死锁 |
| Tetris | 视觉模式识别、空间放置、局部规划 | 几何结构明显 |
| 2048 | 数值格局管理、策略稳定、长期规划 | 错误会逐步累积 |
| Candy Crush | 视觉识别、连锁反应、延迟奖励 | 有复杂时间依赖 |

这四个游戏覆盖了不同类型的多轮交互问题。它们都不是简单问答，而是每一步动作都会改变后续状态。

## 4. Prompt Standardization

论文还有一个容易被忽略的贡献：作者不只手写 prompt，还用 DSPy + SIMBA 做 prompt optimization。

目的不是追求“最会写 prompt”，而是降低 prompt 差异带来的实验噪声。否则不同 prompt 模板可能导致很大方差，模块效果就说不清。

流程大致是：

1. 先用经验方法设计 baseline prompt；
2. 用 DSPy/SIMBA 以累计奖励为目标迭代优化 prompt；
3. 用多个 optimizer model 引导优化；
4. 在多个 target model 上看平均表现，选最稳定的 prompt。

表 5 显示，在 2048 上，DSPy 优化能降低不同 prompt 对之间的性能差异。这个点说明：作者不只是在比较模型，也在努力让评测协议更稳定。

## 方法主线

整篇论文的方法可以压成一个闭环：

```text
选择统一环境接口
  -> 接入多个游戏
  -> 为每个游戏定义奖励/分数
  -> 构建 perception / memory / reasoning harness
  -> 让多个 LLM/VLM 在有无 harness 条件下玩游戏
  -> 做整体性能比较
  -> 做模块消融
  -> 做 prompt 标准化
  -> 做与其他 benchmark 的相关性分析
```

这条主线比“感知、记忆、推理很重要”更完整。

## 关键实验结果

## 1. Harness 整体有效

表 1 比较了多种模型在有 harness 和无 harness 下的表现。整体结论是：**完整模块化 harness 在四个游戏上普遍提升平均表现**。

比较典型的例子：

| 模型 | 游戏 | No Harness | Harness | 变化 |
|---|---|---:|---:|---:|
| Claude-3.5 Sonnet | 2048 | 57.8 | 108.2 | 大幅提升 |
| Claude-3.7 Sonnet thinking | Candy Crush | 126.3 | 484.0 | 大幅提升 |
| Gemini-2.5 Pro | Sokoban | 1.0 | 4.3 | 提升 |
| o3 | Candy Crush | 106.0 | 647.0 | 大幅提升 |
| o4-mini | Sokoban | 1.3 | 5.3 | 提升 |

统计上，作者做了 paired-sample t-test，报告四个游戏都有显著提升：

| 游戏 | 平均提升 | p 值 |
|---|---:|---:|
| Candy Crush | +217.50 | 0.0022 |
| Sokoban | +1.97 | 0.0144 |
| 2048 | +17.81 | 0.0424 |
| Tetris | +5.60 | 0.0490 |

要注意：样本规模不大，每个模型每个游戏主要是 3 次运行，部分高成本模型只有 1 次。因此结论可以说“有力但初步”，不能当成最终定论。

## 2. Harness 让模型更远离随机行为

作者用 Glass's delta 衡量模型表现相对 random baseline 的距离。

结果：

- 30 个 harnessed 条件里有 29 个 delta 为正；
- 30 个 unharnessed 条件里只有 17 个 delta 为正；
- harnessed 在 23/30 个 case 中优于 unharnessed；
- 平均效应量差异约为 2.748。

这说明 harness 不只是让分数偶尔涨一点，而是让模型行为更稳定地偏离随机策略。

## 3. 模块消融揭示了不同模块的分工

表 2 是理解本文最重要的表。

它比较四种条件：

| 条件 | 含义 |
|---|---|
| ZS | zero-shot，没有模块支持 |
| +Memory Only | 只加记忆 |
| +Perception Only | 只加感知 |
| +Both | 同时加记忆和感知 |

### Sokoban / Tetris 更依赖 perception

Sokoban 和 Tetris 都是空间结构很强的游戏。模型需要知道墙、箱子、目标、方块形状、放置位置等。

例子：

- o4-mini 在 Sokoban 从 1.3 提升到 +Perception 5.3；
- Gemini 在 Sokoban 从 1.0 提升到 +Perception 6.0；
- o4-mini 在 Tetris 从 15.0 提升到 +Perception 38.0。

这说明很多时候模型不是不会规划，而是输入状态太乱，导致规划能力发挥不出来。perception 把环境变成结构化状态后，模型潜在的规划能力被释放。

### 2048 / Candy Crush 更依赖 memory

2048 和 Candy Crush 的困难不是单步看不懂，而是策略要连续、不能重复犯错，还要处理延迟收益。

例子：

- Llama-4 在 2048 从 44.6 提升到 +Memory 98.1；
- Claude-3.5 在 2048 从 57.8 提升到 +Memory 102.5；
- Claude-3.5 在 Candy Crush 从 17.0 提升到 +Memory 120.3。

memory 的价值不是“把历史塞进上下文”这么简单，而是让模型知道：

- 上一步是否无效；
- 当前状态有没有变好；
- 是否在重复同一类动作；
- 长期策略是否被破坏。

### Both 通常最强，但不是绝对单调

同时加 memory 和 perception 通常更强，尤其是 Candy Crush：

- o4-mini: 110.7 -> +Both 487.3；
- Gemini: 177.3 -> +Both 416.3；
- Claude-3.7: 126.3 -> +Both 484.0；
- GPT-4o: 59.0 -> +Both 147.3。

但不是所有 case 都单调提升。比如 Gemini 在 2048 的 ZS 已经很高，加模块后略降；Tetris 里某些模型的 memory only 也可能下降。

这说明 harness 是工具，不是魔法。模块必须和任务瓶颈匹配。

## 4. 游戏表现和其他 benchmark 有相关性

作者还比较了 8 个模型在 20 个常见 benchmark 上的排名，并计算和游戏表现的 Spearman correlation。

大致发现：

- Sokoban 和数学、代码 benchmark 相关较强；
- Tetris 和 2048 更接近模式识别任务；
- Candy Crush 和 coding 相关明显，可能因为它需要算法式搜索和延迟收益规划。

这个实验的目的不是说“游戏可以替代所有 benchmark”，而是说明：游戏环境可能是观察通用 agent 能力的一个有用代理指标。

## 我真正应该记住的核心洞见

## 1. Harness 是模型外部能力放大器

强模型裸跑不一定能做好多轮任务，因为它可能看错状态、忘记历史、重复无效动作、无法从奖励中修正策略。

harness 的作用是把环境、历史、反馈组织成模型更能使用的形式。

这和真实 agent 工程非常接近：不是只换更强模型，而是要设计更好的状态表示、记忆机制、反馈机制和动作控制协议。

## 2. Perception 的本质是状态表示

在这篇论文里，perception 不是“让模型看见图片”这么简单，而是 **把环境转换成可推理的 state**。

如果状态表示错了，后面的 reasoning 再强也没用。Sokoban 和 Tetris 的结果说明，空间任务里很多失败来自输入表征不清楚，而不是模型完全没有推理能力。

## 3. Memory 的本质是跨步一致性

memory 不是无限上下文，也不是简单聊天记录。它服务于多轮决策中的几个问题：

- 防止重复无效动作；
- 记录策略承诺；
- 判断行动是否带来奖励；
- 支持长程规划；
- 在失败后改变策略。

这解释了为什么 memory 对 2048 和 Candy Crush 这类长程任务更有价值。

## 4. Reasoning 是整合器，不是孤立模块

论文里的 reasoning 不只是 chain-of-thought，而是一个 controller：它读取 perception 和 memory，输出动作，并支持模块开关。

因此 reasoning 的质量依赖前两个模块。如果 perception 给错状态，memory 给乱历史，reasoning 会在错误材料上认真推理。

## 5. 消融比总分更重要

如果只看表 1，你只能知道 harness 有用。如果看表 2，才知道为什么有用：

- 哪类任务靠 perception；
- 哪类任务靠 memory；
- 哪些模型本身已经强，模块收益小；
- 哪些模型裸跑弱，但 harness 后提升大；
- 哪些模块组合可能产生叠加效果。

这就是本文比普通 benchmark 更有价值的地方。

## 和 Natural-Language Agent Harnesses 的关系

这篇论文和 [[Natural-Language Agent Harnesses 论文总介绍]] 都在讲 harness，但侧重点不同。

| 论文 | 关心的问题 | Harness 的角色 |
|---|---|---|
| Natural-Language Agent Harnesses | 如何用自然语言表达和执行 agent 控制逻辑 | agent workflow 的可读、可迁移、可执行表示 |
| General Modular Harness | 如何用模块化支架提升并分析多轮游戏 agent | perception/memory/reasoning 的实验支架 |

共同点：

- 都把重点放在模型外部的控制层；
- 都认为 agent 能力不只来自模型参数；
- 都强调状态、模块、流程、验收的重要性；
- 都关心 harness 能否迁移和比较。

差异：

- NLAH 更偏 agent runtime / workflow 表示；
- 本文更偏 benchmark / module ablation / gaming environment；
- NLAH 的对象是自然语言控制协议；
- 本文的对象是多轮游戏中的感知、记忆、推理模块。

可以把两者合起来理解：

> NLAH 研究“怎么描述和执行 agent harness”；本文研究“一个模块化 harness 在多轮游戏里到底能带来什么、每个模块贡献多少”。

## 和 Embodied-Reasoner 的关系

这篇论文也和 [[Embodied-Reasoner - Synergizing Visual Search Reasoning and Action for Embodied Interactive Tasks]] 很相关。

| 论文 | 环境 | 核心闭环 | 主要方法 |
|---|---|---|---|
| Embodied-Reasoner | AI2-THOR 室内具身环境 | Observation-Thought-Action | 训练一个专门具身模型 |
| General Modular Harness | Gym / Retro 游戏环境 | Perception-Memory-Reasoning-Action | 给现成模型加外部 harness |

两者都说明：多轮 agent 不是一次性问答，而是 **带状态的连续决策过程**。

差异在于：

- Embodied-Reasoner 更像“训练模型学会具身交互”；
- 本文更像“用外部模块支架让现成模型更会交互，并分析每个模块作用”。

对我的启发是：如果不想训练模型，可以先通过 harness 提升 agent；如果要让能力内化，则需要像 Embodied-Reasoner 那样构造轨迹数据和训练流程。

## 局限与我需要保持怀疑的地方

## 1. 实验规模偏小

论文自己也承认，由于最新模型运行成本高，每个模型每个游戏主要是 3 次运行，部分模型甚至只有 1 次。这会影响统计稳健性。

所以结论应该理解为：当前证据显示模块化 harness 有明显趋势，而不是已经完全证明所有模型、所有游戏、所有设置都成立。

## 2. 游戏虽干净，但不等于真实世界

游戏有明确规则、明确动作空间、明确 reward。真实网页、机器人、软件操作环境更混乱：

- observation 可能不完整；
- action 可能失败；
- reward 不一定即时可见；
- 状态空间更开放；
- 任务目标更模糊；
- 安全和权限边界更复杂。

因此本文更适合作为 agent harness 研究平台，而不是直接证明真实世界 agent 已解决。

## 3. Perception 里使用后端结构化状态，可能降低真实视觉难度

text mode 从游戏后端抽取坐标和对象属性，这对分析模块很有帮助，但也会让 perception 比真实视觉问题更简单。

这不是错误，因为作者的目的之一是隔离模块贡献。但如果要迁移到真实 UI 或机器人，不能默认拿得到完美后端状态。

## 4. Prompt optimization 可能也在贡献性能

作者用 DSPy/SIMBA 标准化 prompt，这有助于降低方差，但也意味着最终效果不完全来自 perception/memory 模块本身，还包含 prompt 优化带来的收益。

好处是评测更稳定；风险是模块贡献和 prompt 工程贡献之间仍可能有耦合。

## 5. Reasoning 模块定义相对宽

论文中 reasoning 更像 controller 和 action selector，并不像 perception、memory 那样有清晰可见的独立机制。因此“reasoning 模块贡献”不如 perception/memory 那么容易独立量化。

如果后续复现或扩展，我会特别关注 reasoning 的具体 prompt、动作格式和错误处理逻辑。

## 我的理解版总结

我可以这样重新理解这篇论文：

> 作者发现现代 LLM/VLM agent 的失败不只是模型不够聪明，而是外部工作流太定制、太混乱、不可比较。于是他们选择游戏作为统一实验场，把 agent 外部控制层拆成 perception、memory、reasoning 三个模块，并让不同模型在同一批游戏中运行。通过打开/关闭模块，他们证明完整 harness 通常提升表现，同时发现不同任务依赖不同模块：空间任务靠 perception，长程任务靠 memory，组合模块能暴露更细的模型差异。

这篇论文最重要的不是告诉我“感知、记忆、推理重要”，而是教我一种研究 agent 的方法：

1. 不要只看最终模型分数；
2. 要把 agent 控制系统拆成模块；
3. 每个模块都要能开关；
4. 每个任务都要有明确 reward；
5. 用消融实验而不是直觉判断模块价值；
6. 用统一接口减少环境差异；
7. 用 prompt 标准化减少模板噪声；
8. 最后再讨论这些游戏结果能否代理更一般能力。

## 复习问题

下次复习时，可以用下面几个问题检查自己是否真的懂了。

1. 本文的 harness 和 LLM 本身有什么区别？
2. 为什么作者选择游戏，而不是 WebArena 或 OSWorld？
3. Perception module 为什么不是简单“看图”？
4. Memory module 和普通上下文历史有什么区别？
5. Reasoning module 在本文中更像“推理能力”还是“控制器”？
6. 表 1 和表 2 分别回答什么问题？
7. 为什么 Sokoban/Tetris 更吃 perception，而 2048/Candy Crush 更吃 memory？
8. 为什么 +Both 通常更强，但不是每个 case 都单调提升？
9. Prompt standardization 为什么是必要的？
10. 如果把这套 harness 迁移到真实网页或机器人，最大的风险是什么？

## 追加答疑：我最容易卡住的 6 个问题

## 1. 论文说三模块，为什么消融只看到感知和记忆？

这是一个真实问题，不是你看漏了。

论文在方法部分把 harness 说成三块：perception、memory、reasoning。但到表 2 的模块消融时，实验条件主要是：

| 条件 | 实际含义 |
|---|---|
| ZS | zero-shot，裸提示/无额外模块支持 |
| +Memory Only | 加 memory，不加 perception |
| +Perception Only | 加 perception，不加 memory |
| +Both | 同时加 memory 和 perception |

这里没有一个清晰的 “no reasoning” 或 “reasoning only removed” 条件。

原因在于：本文里的 **reasoning module 更像默认 controller / action selector**，不是一个和 perception、memory 同级可拆卸的独立算法模块。论文原文说 reasoning module 负责整合 perception 和 memory 的信息，决定最终动作，并允许激活或停用特定模块。也就是说，它更像总控入口。

如果把 reasoning 也关掉，agent 就没有“根据状态选择动作”的核心环节了，只剩随机动作或固定规则，那就不再是同一个 LLM agent。作者真正能方便消融的是：

- perception 输入给不给；
- memory 历史和反思给不给；
- 两者是否同时给。

所以更准确的理解是：

> 本文声称是 perception / memory / reasoning 三模块 harness，但实验中被清楚消融的是 perception 和 memory；reasoning 是默认动作决策器，没有被作为独立变量严格消融。

这也是论文的一个局限。标题和叙述会让人以为三模块都做了对称消融，但实验没有完全做到。

## 2. 裸 LLM/VLM 本身不也有感知、记忆、推理吗？为什么用了 harness 才有这些模块？

要区分 **模型内部能力** 和 **agent 外部模块**。

裸模型当然可能具备某些能力：

- VLM 能看图，这是内部视觉感知能力；
- LLM 上下文窗口能读历史，这是临时记忆能力；
- LLM 能生成分析和动作，这是推理能力。

但裸模型的流程通常是：

```text
当前 observation + prompt -> LLM/VLM -> action
```

这里的“感知、记忆、推理”是混在一次模型调用里的隐式能力，没有清晰边界，也不容易控制。

harness 做的是把这些能力外部化、结构化：

| 层面 | 裸模型 | Harness 后 |
|---|---|---|
| 感知 | 直接看截图/文本，模型自己理解 | 外部 perception 模块先把状态整理成坐标、对象、棋盘特征 |
| 记忆 | 上下文里可能有历史，但无固定结构 | memory 模块维护最近 N 步状态、动作、奖励和 reflection |
| 推理 | 模型直接输出动作 | reasoning/controller 读取结构化 state + memory，再输出动作 |

所以不是“LLM 不能有这三个能力”，而是：

> 裸模型的能力是隐式的、耦合的、难以消融；harness 把它们变成显式的、可控的、可比较的外部 agent 组件。

至于“LLM 能不能调用 agent”，这个说法要反过来理解：LLM 通常是 agent 的核心模型，agent/harness 是包在 LLM 外面的运行系统。不是 LLM 调用 agent，而是 agent runtime 调用 LLM，并给它提供状态、工具、记忆、动作接口。

## 3. Prompt standardization 是干嘛的？为什么做模块消融还要涉及提示词？

因为在 LLM agent 里，prompt 本身就是控制逻辑的一部分。即使 perception 和 memory 完全相同，不同 prompt 也可能导致完全不同的动作选择。

如果不控制 prompt，实验会变成：

```text
模块差异 + prompt 差异 + 模型差异 + 随机性
```

这样就很难说性能提升到底来自 memory/perception，还是来自某个 prompt 写得更好。

你问“统一 prompt 不就可以了吗？”理论上可以，但问题是：统一成哪一个？

如果只人工写一个统一 prompt，会有两个风险：

- 它可能偏向某个模型；
- 它可能在某个游戏上特别好或特别差；
- 它可能方差很大，导致实验不稳定。

所以作者做了两阶段：

1. **经验 prompt engineering**：先用人类经验写出合理模板，保证任务说明、动作空间、输出格式、策略提示都完整。
2. **DSPy/SIMBA optimization**：再用累计奖励作为目标，在训练环境上迭代优化 prompt，并在多个 target model 上选择平均表现更好的模板。

这一步的目的不是证明“三模块之一叫 prompt”，而是降低实验噪声，让后面的模块比较更稳定。

但是这里也有一个值得怀疑的地方：

> Prompt optimization 本身也可能贡献性能，因此最终效果不完全来自 perception/memory。作者把它叫 standardization，但它同时也是一种性能优化。

所以更稳妥的说法是：prompt standardization 是实验控制和性能稳定化手段，但它会和模块效果产生一定耦合。

### 3.1 Prompt 到底是怎么优化和统一的？

论文里的 prompt optimization 不是“给每个模型分别找自己的最优 prompt”。如果那样做，比较就不公平了，因为 Claude 用 Claude 最优 prompt，Gemini 用 Gemini 最优 prompt，o4-mini 用 o4-mini 最优 prompt，最后就分不清是模型强、模块强，还是 prompt 给某个模型开了小灶。

它更接近下面这个流程：

```text
先写一个基础 prompt P
  -> 用多个 optimizer models 生成/改写候选 prompt
  -> 候选 prompt 在训练环境里用累计 reward 优化
  -> 把候选 prompt 放到多个 target LMs 上评估
  -> 计算这些 target LMs 的平均 dev score
  -> 选择平均分最高的 prompt P*
  -> 后续实验统一使用 P*
```

论文算法 1 里的关键是：

```text
savg = sum(Evaluate(candidate_prompt, target_model_i)) / number_of_target_models
if savg > sbest:
    P* = candidate_prompt
```

所以它选择的是 **跨目标模型平均表现最好的 prompt**，不是所有模型各自最好的 prompt。

可以这样理解：

| 做法 | 是否公平 | 问题 |
|---|---|---|
| 每个模型用自己的最优 prompt | 不太公平 | prompt 变成模型专属调参 |
| 所有模型用人工写的同一个 prompt | 公平但可能不稳 | 可能偶然偏向某个模型或某个游戏 |
| 所有模型用跨模型平均表现最好的 optimized prompt | 相对公平且更稳 | 仍然可能引入 prompt optimization 的性能贡献 |

作者采用的是第三种。

这里的 “optimizer model” 和 “target model” 要分清：

- **optimizer model**：帮助搜索/改写 prompt 的模型，例如 Claude-3.7、Gemini-2.5、o3、DeepSeek-R1、Grok-3-mini。
- **target model**：真正被评测的模型。候选 prompt 要在这些模型上跑，按平均表现选出统一模板。

所以 prompt optimization 的目标不是让某一个模型最好，而是找一个对多模型、多环境都比较稳的通用模板。

### 3.2 “避免 prompt 偶然性污染实验结果”到底是什么意思？

假设我们想比较 memory 有没有用。理想情况下，两个条件唯一差异应该是：

```text
无 memory：当前状态 -> 模型 -> 动作
有 memory：当前状态 + 历史轨迹 + 反思摘要 -> 模型 -> 动作
```

但如果两个条件的 prompt 写法差异很大，例如：

```text
无 memory prompt：
  "Play the game. Choose an action."

有 memory prompt：
  "You are an expert game-playing agent. Review previous failures,
   avoid repeated invalid moves, plan 3 steps ahead, then choose action."
```

那最后有 memory 条件表现更好，未必是 memory 真的有效，也可能是第二个 prompt 本身写得更强。这个就是 prompt 污染。

再比如，在同一个 harness 下，prompt A 和 prompt B 都是人工写的合理模板，但分数差了一个标准差以上。那说明实验对 prompt 很敏感。此时如果论文只报告 prompt A 的结果，读者会怀疑：

> 你的模块真的有效吗？还是刚好选了一个对这个模块有利的 prompt？

因此 prompt standardization 要解决的是两个问题：

1. **减少任意人工模板选择带来的偶然性**：不是作者随便挑一个看起来效果好的 prompt。
2. **降低不同 prompt 之间的表现差异**：让实验结果更不依赖某个模板措辞。

表 5 的意思正是这个。作者在 2048 上比较两组 prompt：

| 类型 | 比较什么 | 观察点 |
|---|---|---|
| Empirical P1 vs Empirical P2 | 两个人工经验 prompt 的差异 | 差异较大 |
| DSPy P1 vs DSPy P2 | 两个优化后 prompt 的差异 | 差异变小 |

论文报告优化流程能把两个候选 prompt 的表现差异降低约 33.8% 到 63.5%。这说明优化后 prompt 之间没那么“看运气”，实验更稳。

但这不等于 prompt 影响完全消失。更准确地说：

> prompt standardization 不是把 prompt 变量彻底消灭，而是把 prompt 从“随意人工选择”变成“按统一搜索和平均评估规则选择”，从而降低 prompt 对模块消融结论的干扰。

我后续读这部分时要记住一个边界：prompt optimization 增强了实验稳定性，但也让系统多了一个优化环节，所以不能把最终提升全部归因给 perception 或 memory。

## 4. 为什么方法主线最后还有 prompt 标准化和 benchmark 相关性分析？

这两步回答的是不同层级的问题。

前面的步骤回答：

> 这个 harness 在游戏里有没有用？哪些模块有用？

prompt 标准化回答：

> 这个实验结果是不是被 prompt 模板偶然性污染了？

如果不同 prompt 带来超过一个标准差的性能波动，那么“模块有效”就可能只是 prompt 巧合。因此作者要证明优化后的 prompt 更稳定，减少模板选择对结果的影响。

benchmark 相关性分析回答：

> 游戏成绩有没有可能反映更一般的模型能力？

如果游戏表现和数学、代码、视觉推理、模式识别 benchmark 完全无关，那这套游戏环境可能只是玩具。作者做相关性分析，是为了说明这些游戏不是随便选的小游戏，而可能对应一些更通用的能力维度：

- Sokoban 和数学/代码相关，可能因为需要规划和搜索；
- Tetris、2048 和模式识别相关；
- Candy Crush 和 coding 相关，可能因为需要算法式规划和延迟收益处理。

所以后两步的意义是：

- prompt 标准化：保护实验内部有效性；
- benchmark 相关性：证明评测外部意义。

## 5. Paired-sample t-test 里的 p 值代表什么？

paired-sample t-test 用来比较同一批对象在两个条件下的差异。这里的配对对象可以理解为同一模型在同一游戏上的两个条件：

```text
同一个模型/游戏：
  no harness 分数
  harness 分数
```

它检验的问题是：

> 如果 harness 其实没有真实效果，那么我们现在看到的平均提升，有多大概率只是随机波动造成的？

p 值就是这个概率意义上的量。

简单说：

- p 越小，说明“只是随机波动”的解释越不可信；
- 常见阈值是 p < 0.05；
- p < 0.05 通常表示差异具有统计显著性。

论文报告：

| 游戏 | 平均提升 | p 值 | 怎么读 |
|---|---:|---:|---|
| Candy Crush | +217.50 | 0.0022 | 很显著 |
| Sokoban | +1.97 | 0.0144 | 显著 |
| 2048 | +17.81 | 0.0424 | 刚过 0.05 |
| Tetris | +5.60 | 0.0490 | 非常接近阈值 |

但要小心：p 值不是“harness 有 95% 概率有效”，也不是“效果大小”。它只是在特定统计假设下，衡量观察到这种差异由随机噪声产生的可能性。

此外，本文每个模型/游戏运行次数不多，所以 p 值只能作为初步证据，不能过度解读。

## 6. 随机、无 harness、有 harness 三者到底怎么区分？

三者的区别是 action 怎么产生。

| 条件 | 谁选择动作 | 是否用 LLM/VLM | 是否有外部模块 |
|---|---|---|---|
| Random | 随机策略从合法动作里选 | 否 | 否 |
| No Harness | 裸 LLM/VLM 根据当前状态和基础 prompt 选动作 | 是 | 基本没有 perception/memory 支架 |
| Harness | LLM/VLM 在 perception + memory + reasoning/controller 支架下选动作 | 是 | 是 |

random baseline 的作用是给一个“完全不会玩，只是乱动”的底线。无 harness 则是“模型自己看当前状态直接行动”的能力。

所以比较逻辑是三层：

```text
Random:
  没有智能，只是环境中的随机动作底线

No Harness:
  有 LLM/VLM，但缺少结构化状态、历史记忆、反思支架

Harness:
  有 LLM/VLM，并且有外部模块帮助它理解状态、利用历史、输出动作
```

Glass's delta 实验问的是：

> 模型表现离 random baseline 有多远？

如果 no harness 离 random 很近，说明裸模型虽然在输出动作，但实际行为质量接近乱玩。若 harness 离 random 更远，说明结构化支架确实让模型产生了更有策略性的行为。

这就是“harness 让模型更远离随机行为”的含义。它不是说 random 和 no harness 一样，而是说 no harness 有时并没有比 random 好太多，尤其在长程或空间复杂游戏里。

## 最短记忆卡片

> [!summary] 一句话记忆
> 本文提出一个通用模块化 agent harness，把 perception、memory、reasoning 做成可插拔支架，用多轮游戏作为统一实验场，证明外部控制层能显著改善 LLM/VLM agent，并通过消融说明空间任务主要受益于 perception，长程任务主要受益于 memory。

> [!tip] 最关键表格
> - **表 1**: 有 harness vs 无 harness，证明整体有效。
> - **表 2**: ZS / +Memory / +Perception / +Both，证明不同模块的贡献。
> - **表 5**: empirical prompt vs DSPy prompt，说明 prompt 标准化能降低方差。

## 引用

> [!cite]
> Zhang, Y., Yu, H., Hu, L., Jin, H., & Zhang, H. (2025). *General Modular Harness for LLM Agents in Multi-Turn Gaming Environments*. Proceedings of the 42nd International Conference on Machine Learning, PMLR 267. arXiv:2507.11633v1.
