---
title: "Harness 模块显化、消融与诊断评估方法论"
date: 2026-07-10
tags: [agent-harness, agent-evaluation, benchmark-design, ablation, failure-analysis, embodied-ai]
status: review
related:
  - "[[Natural-Language Agent Harnesses 论文总介绍]]"
  - "[[General Modular Harness 与我的评估方向关联和读后迁移]]"
  - "[[General Modular Harness for LLM Agents in Multi-Turn Gaming Environments]]"
  - "[[Embodied-Reasoner - Synergizing Visual Search Reasoning and Action for Embodied Interactive Tasks]]"
---

# Harness 模块显化、消融与诊断评估方法论

## 我真正卡住的问题

我已经读完两篇 harness 论文，但还有一个更底层的问题没有想明白：

> 既然 harness 原本隐藏在 controller、prompt、tool adapter、状态管理、验证脚本和运行时默认行为里，研究者到底是怎么把它“精确显化”成模块的？这些模块是怎么找出来、怎么抽离、怎么消融、怎么证明它们有作用的？

这个问题很关键。否则我只会得到一个表层结论：

> 感知、记忆、推理这些模块对 agent 有帮助。

但这还不是研究能力。真正要学会的是：

> 如何把一个多轮 agent 系统拆成可观察、可干预、可消融、可诊断的组件。

这份笔记专门回答这个问题。

## 先给结论

Harness 模块不是凭空“发现”的，也不是作者随便给几个名字。

它们通常来自四条线索：

1. **信息从哪里来**：observation 如何进入模型。
2. **状态如何保留**：历史、记忆、轨迹、文件、反馈如何跨轮保留。
3. **动作如何产生和执行**：模型输出如何变成合法动作或工具调用。
4. **结果如何验证和修复**：失败如何检测、解释、重试、停止。

换句话说，显化 harness 的第一步不是起模块名，而是画出 agent 的运行闭环：

```text
Environment / Task
  -> Observation Representation
  -> Context Construction
  -> Model Call
  -> Reasoning / Controller
  -> Action Parser / Tool Adapter
  -> Environment Feedback
  -> Memory / State Update
  -> Verification / Evaluator
  -> Next Turn or Stop
```

任何能影响这条链路、又能被单独替换或关闭的部分，都可能成为一个 harness 模块。

所以模块显化的核心是：

> 从 agent 的信息流、状态流、动作流、反馈流中找到稳定边界，把原本隐式耦合的控制逻辑变成显式接口。

## 为什么 harness 原本难以抽离？

因为实际 agent 系统里的控制逻辑通常不是干净分层的。

它可能散落在：

- prompt 里的一句话；
- controller 里的 if/else；
- tool adapter 的默认参数；
- action parser 的容错逻辑；
- message history 的拼接方式；
- verifier 的局部判断；
- 重试策略；
- 文件路径和日志约定；
- framework runtime 的默认行为。

例如一个网页 agent 失败后能继续尝试，可能不是模型本身更聪明，而是 controller 在背后做了：

```text
检测动作失败
  -> 追加错误消息
  -> 重新截图
  -> 把上一步动作写入历史
  -> 限制下一步动作集合
  -> 再调用模型
```

如果这些逻辑全藏在 controller 里，论文或 benchmark 只报告“模型 A 成功率更高”，我根本不知道提升来自哪里。

这就是两篇 harness 论文共同反对的东西：

> 不要把整个 controller bundle 当成黑盒来比较。

要把 bundle 里的关键控制变量拆出来。

## 模块是怎么“精确找到”的？

严格说，模块不是一次性精确找到的，而是通过三步逐渐稳定下来。

## 第一步：按 agent 闭环拆职责

先不问“有什么模块”，先问每一轮 agent 到底做了什么。

一个多轮 agent 至少有这些职责：

| 职责 | 问题 | 可能显化成的模块 |
|---|---|---|
| 观察输入 | agent 看到了什么？输入是什么格式？ | perception / observation adapter |
| 上下文组织 | 哪些信息被送进模型？ | prompt/context builder |
| 历史保留 | 过去动作和反馈怎么保存？ | memory / file-backed state |
| 决策控制 | 谁决定下一步动作？ | reasoning / planner / controller |
| 动作落地 | 文本输出如何变成环境动作？ | action parser / tool adapter |
| 反馈回流 | 失败和奖励如何进入下一轮？ | feedback module |
| 验证停止 | 怎么知道任务完成？ | verifier / evaluator / stopping rule |

这一步得到的是“候选模块”。

注意：候选模块不是论文作者脑补出来的，而是从 agent 运行闭环的必要职责中拆出来的。

## 第二步：找可干预边界

不是所有职责都能成为好模块。一个模块要能研究，必须满足至少三个条件：

1. **可替换**：能换成另一种实现。
2. **可关闭**：能拿掉或降级成 baseline。
3. **可观测**：拿掉后行为变化能被指标或日志捕捉。

例如 General Modular Harness 里的 perception 很适合做模块，因为它可以有几种形态：

```text
raw image
text grid from backend ### 后端文本网格）
image with coordinate overlay ### （带坐标叠加的图像）
text + image combined ### 文本+图像组合）
```

memory 也适合做模块，因为它可以开关：

```text
no history
recent N states/actions
recent trajectory + reward
reflection summary
```

reasoning 在那篇论文里就没那么好消融，因为它本质上是默认 controller/action selector。如果完全关掉 reasoning，agent 就不再是同一个 agent，只剩随机动作或固定规则。因此它虽然被命名为模块，但没有像 perception/memory 那样形成严格独立消融。

这说明一个重要原则：

> 能命名不等于能消融；能消融才是真正稳定的评估模块。

## 第三步：用失败模式反推模块

模块不是只从系统结构里拆，也可以从失败现象里反推。

例如多轮 agent 常见失败：

| 失败现象 | 可能缺的模块 |
|---|---|
| 看错对象、漏掉目标、空间位置错 | perception |
| 重复访问同一区域、忘记已操作对象 | memory |
| 知道目标但输出非法动作 | action parser / constrained action |
| 动作失败后继续重复同一错误 | feedback / reflection |
| 自称完成但环境状态不满足 | evaluator / verifier alignment |
| 子任务顺序错、提前终止 | planning / controller |

这一步非常适合我的评估方向。

如果我想把 benchmark 做成诊断工具，就不能只看最终 success，而要把失败归类为：

```text
perception error
memory error
planning error
action grounding error
feedback use error
evaluator mismatch
```

然后再设计对应模块，看这些模块是否能降低对应失败。

## “显化”到底是什么意思？

显化不是把代码改得更复杂，也不是把每个功能都包一层类。

显化的意思是让模块具备清晰接口：

```text
输入是什么
输出是什么
保存什么状态
改变什么上下文
影响什么动作
用什么指标验证
关闭后会退化成什么 baseline
```

例如一个 memory module 不能只叫 memory，它要有接口定义：

```text
Input:
  current state, previous action, reward/error feedback

State:
  last N states/actions
  failed actions
  explored objects/locations

Output:
  memory summary inserted into next prompt

Ablation:
  remove memory summary and previous trajectory

Expected effect:
  repeated actions increase, long-horizon performance drops
```

这才叫显化。

如果只是 prompt 里写一句“remember previous actions”，但没有状态结构、没有开关、没有对照，那还不是一个可研究模块。

## 两篇 harness 论文分别如何显化模块？

## 1. Natural-Language Agent Harnesses 的做法

NLAH 处理的是更复杂的 agent workflow。它面对的问题是：原本 harness 散落在代码和运行时里。

它的显化方式是把高层控制逻辑写成自然语言 harness，并交给共享 runtime 执行。

它显化的不是 perception/memory 这种认知模块，而是 workflow 模块：

- task contract；
- roles；
- stage structure；
- file-backed state；
- evidence-backed answering；
- verifier；
- self-evolution；
- multi-candidate search；
- dynamic orchestration。

它的关键是把这些逻辑从 controller code 里提出来，变成可读、可迁移、可消融的 harness section。

例如 file-backed state 的显化方式不是“模型记住历史”，而是明确写入：

```text
TASK.md
RESPONSE.md
state/task_history.jsonl
children/*/TASK.md
children/*/RESPONSE.md
artifacts/
```

这样它就变成了可观察、可删除、可比较的模块。

## 2. General Modular Harness 的做法

General Modular Harness 处理的是游戏 agent。它面对的问题更干净：每个游戏都有状态、动作、奖励和多轮交互。

它的显化方式是把 agent 每轮输入输出拆成：

- perception：把游戏 UI / 棋盘 / 图像转成模型可用状态表示；
- memory：保存最近轨迹、奖励、反思摘要；
- reasoning/controller：读取状态和记忆，输出下一步动作。

然后用不同游戏测试模块作用：

```text
ZS
+ Memory Only
+ Perception Only
+ Both
```

这里真正被严格消融的是 perception 和 memory。reasoning 更像默认控制器，没有被完全独立消融。

这也给我一个提醒：

> 论文说“模块化”时，我要检查它的模块是否真的都有可关闭对照。

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

## NLAH 中 Runtime Skill / Harness Skill 与 RQ1 / RQ2 的分层答疑

读 Natural-Language Agent Harnesses 时，我容易把几个层次混在一起：Runtime Charter、Runtime Skill、Harness Logic、Harness Skill、RQ1、RQ2。这里单独整理。

## 1. Runtime Charter / Runtime Skill / Harness Logic / Harness Skill 是什么关系？

这个结构不是四个同级模块，而是两组“抽象规则 -> 可执行载体”的映射。

| 概念层 | 实现载体层 | 含义 |
|---|---|---|
| Runtime Charter / Policy | Runtime Skill | 通用运行时纪律如何被写成可执行文本 |
| Harness Logic | Harness Skill | 某个 benchmark / 任务族的专属控制逻辑如何被写成可执行文本 |

更具体地说：

```text
Runtime Charter
  = 所有 agent 运行都应该遵守的通用规则
  = 例如：如何创建子 agent、如何保存状态、如何交接 artifact、如何完成任务

Runtime Skill
  = 把这些通用规则包装成 skill 文本，注入 agent 上下文，让 agent 按这些规则运行

Harness Logic
  = 某个任务族自己的高层流程
  = 例如 SWE-bench 怎么修 bug，OSWorld 怎么操作桌面，什么时候验证，输出什么 artifact

Harness Skill
  = 把这个任务族逻辑包装成 skill 文本，注入 agent 上下文
```

所以 Runtime Skill 和 Harness Skill 都处在 **agent harness 层 / prompt-context 层 / skill 注入层**。它们不是模型内部，也不是底层工具本身。

更完整的层级是：

```text
Backend / Tools / Sandbox
  提供真实执行能力，比如文件、shell、浏览器、子 agent

Base Agent
  负责读上下文、调用工具、生成动作

Runtime Skill
  注入通用运行纪律
  对应 Runtime Charter / Policy

Harness Skill
  注入 benchmark 专属工作流
  对应 Harness Logic

Task Instance
  当前这道题、这个 issue、这个桌面任务
```

## 2. Runtime Skill 不是通用的吗，为什么还能被消融？

“通用”不等于“不能被拿掉”。

这里的“通用”意思是：Runtime Skill 不属于某一个 benchmark，而是多个 harness 都可以复用的共享运行时规则。

但在实验里，作者要问：

> 这层共享运行时规则到底有没有改变 agent 行为？

所以他们故意做了 `w/o RTS`，也就是去掉 Runtime Skill，看 agent 在没有这层通用运行纪律时会怎样。

RQ1 的三个条件可以理解为：

```text
Full IHR:
  base agent + runtime skill + harness skill

w/o RTS:
  base agent + harness skill
  去掉共享运行时纪律

w/o HS:
  base agent + runtime skill
  去掉 benchmark 专属 harness logic
```

这个消融不是说真实系统应该随便删除 runtime，而是为了实验因果判断：

> 如果我移除 Runtime Skill，行为指标、工具调用、token、成功样本集合是否变化？

结果是会变化，而且过程指标变化很大。这说明 Runtime Skill 不是装饰性 prompt，而是真实控制了 agent 行为。

## 3. RQ1 和 RQ2 的实验对象不是同一层级

RQ1 是粗粒度消融：

```text
Full IHR
w/o Runtime Skill
w/o Harness Skill
```

它想回答：

> 共享 runtime 和 benchmark-specific harness logic 是否真的改变 agent 行为？

所以 RQ1 看的是大块结构的行为效应。

RQ2 是细粒度模块消融：

```text
Basic
+ file-backed state
+ evidence-backed answering
+ verifier
+ self-evolution
+ multi-candidate search
+ dynamic orchestration
```

它想回答：

> 当 harness pattern 被显化以后，具体模块能不能像组件一样添加、移除、比较？

所以 RQ2 不是继续消融 Runtime Skill / Harness Skill，而是在一个 benchmark-specific Basic 起点上叠加具体模块。

## 4. RQ2 的 Basic 里还有没有未显化的 harness 影响？

有。这个判断必须保留。

任何 agent benchmark 都不可能完全没有 harness。即使叫 Basic，它仍然至少有：

- base agent 的默认循环；
- 工具调用机制；
- benchmark runner；
- prompt 基础格式；
- action / output parser；
- 官方 evaluator；
- backend 和 sandbox 约束。

所以 RQ2 不是在比较“纯模型 vs 纯模块”，而是在比较：

```text
在同一个基础运行底座上，
额外显化模块带来的边际效果。
```

更准确地说：

> RQ2 的结论是“这些显式模块在当前 Basic harness substrate 上的增量影响”，不是“这些模块在绝对真空中的纯效果”。

这也是读论文时要警惕的点：作者说模块提升，不等于所有隐式 harness 都被完全剥离了。实验只能控制一部分变量。

但这不让实验无效。只要每个条件共享同一个 Basic substrate，差异主要来自新增模块，就可以研究相对贡献。

## 5. 既然还有隐式 harness，显化有什么意义？

意义在于把一部分原本混在 bundle 里的变量拿出来单独研究。

目标不是：

```text
彻底消灭所有隐式 harness
```

而是：

```text
把关键控制结构从黑盒里提出来，
让它至少部分可见、可替换、可消融。
```

这是渐进式显化，不是一次性完全透明。

可以这样理解：

```text
原来:
  controller bundle = prompt + memory + verifier + retry + state + adapter + evaluator glue

显化后:
  Basic substrate 固定
  单独研究 file-backed state / verifier / self-evolution 等模块
```

这已经比只比较整个 controller bundle 好很多。

## 6. 诊断型 benchmark 和消融实验是不是重复？

不重复，但它们有关联。

消融实验是 **产生诊断证据的一种方法**。

诊断型 benchmark 是 **最终希望 benchmark 输出的信息形态**。

也就是说：

```text
消融实验 = 怎么获得证据
诊断型 benchmark = 证据最后如何组织和解释
```

例如这个输出：

```text
Model A:
  Perception errors: low
  Memory errors: high in long-horizon tasks
  Action grounding errors: medium
  Feedback recovery: weak
  Final-state mismatch: high
  Best module gain: typed feedback
```

它确实可以部分来自消融实验，但不只来自消融实验。它通常来自四类证据：

```text
1. 任务分组结果
   memory-heavy tasks 上差 -> 可能 memory 弱

2. 过程日志指标
   repeated search 多、重复打开同一位置 -> memory / state tracking 弱

3. 模块消融增益
   +memory 提升大 -> 说明 memory 是瓶颈之一

4. 失败标注 / evaluator 对齐检查
   自称完成但 final state 不满足 -> final-state mismatch 高
```

所以“诊断型 benchmark”不是在重复说“做消融”，而是在说：

> benchmark 不应该只输出一个总分，而应该把任务分组、过程日志、消融增益、失败类型整合成可解释画像。

## 7. 为什么还要单独强调诊断型 benchmark？

因为很多论文即使做了消融，最后仍然只把它当成表格：

```text
Full: 80
w/o memory: 72
w/o perception: 75
```

这只是消融表。

诊断型 benchmark 要进一步回答：

```text
为什么 w/o memory 掉分？
掉在哪些任务？
对应哪些失败行为？
是否出现重复探索？
是否忘记子目标？
memory 是否也带来副作用？
```

也就是说，消融表只告诉我“模块有影响”；诊断 benchmark 要告诉我“模块影响了哪类行为机制”。

一个简单例子：

```text
+memory 后成功率 +8%
```

这是消融结论。

进一步诊断是：

```text
+memory 后：
  repeated search count -35%
  long-horizon task success +18%
  invalid action count 基本不变
  simple search tasks step count 增加
```

这就不是重复了。它告诉我：

- memory 主要解决重复搜索和长程状态保持；
- 它不解决动作合法性；
- 它可能让简单任务变慢。

这才叫 benchmark 从排行榜变成诊断工具。

## 8. 最终层级图

```text
NLAH / IHR 论文分层：

Backend / base agent
  固定底座，提供工具和模型调用能力
        |
Runtime Skill
  通用运行纪律，来自 Runtime Charter
  RQ1 可移除，测试它是否改变行为
        |
Harness Skill
  benchmark-specific harness logic
  RQ1 可移除，测试任务族逻辑是否改变行为
        |
Basic benchmark-specific substrate
  RQ2 的起点，仍然有最小 harness
        |
显式模块
  file-backed state
  verifier
  self-evolution
  multi-candidate search
  dynamic orchestration
        |
RQ2
  测这些模块在 Basic 上的边际影响
```

最短记忆：

> RQ1 测“大层级”：Runtime Skill 和 Harness Skill 是否真实改变行为。  
> RQ2 测“小模块”：显式 harness pattern 在固定 Basic 底座上的增量作用。  
> 诊断型 benchmark 不是消融实验本身，而是把消融、任务分组、过程日志和失败类型整合成行为解释。

## 一个可迁移到我方向的分析模板

以后我看任何 agent / 具身评估论文，可以填这个表。

| 问题 | 要查什么 |
|---|---|
| 评估对象是什么？ | base model 还是 model + harness？ |
| harness 藏在哪里？ | prompt、controller、adapter、memory、verifier、runtime？ |
| 模块怎么显化？ | 是否有明确输入、输出、状态、接口？ |
| 模块能否消融？ | 是否有关闭/替换/降级 baseline？ |
| 模块对应哪类失败？ | perception、memory、planning、action、feedback、evaluator？ |
| 任务是否按瓶颈分组？ | 不同任务是否能拉开模块差异？ |
| 指标是否可诊断？ | 是否有过程指标和失败类型？ |
| prompt 是否受控？ | 是否统一、优化、或对模型特调？ |
| 最终验收是否可靠？ | 模型自称完成是否等于环境完成？ |
| 代价是否记录？ | token、步数、时间、调用次数、复杂度？ |

这个模板比单纯记论文结论更重要。

## 我现在应该形成的理解

两篇 harness 论文真正想教我的不是“模块有用”，而是：

> 多轮 agent 的能力不是一个整体黑盒，而是由 observation、context、memory、controller、action、feedback、verification 这些环节共同产生的。要研究 agent，就必须把这些环节显化成可干预模块，并用消融和轨迹证据解释最终分数。

更短一点：

> Harness 显化 = 把隐式控制逻辑变成可观察接口；模块消融 = 判断哪个接口真的影响行为；诊断 benchmark = 把总分拆成失败机制。

## 最终记忆卡片

> [!summary] 一句话
> Harness 模块不是随便命名出来的，而是从 agent 的信息流、状态流、动作流和验证流中找到可替换、可关闭、可观测的控制边界；只有这些边界能通过消融解释具体失败类型时，benchmark 才从排行榜变成诊断工具。

> [!tip] 判断一个模块是否真实
> 一个模块必须说清楚：输入是什么、输出是什么、保存什么状态、解决哪类失败、关闭后退化成什么 baseline、用什么指标验证。如果这些说不清，它就只是概念标签，不是可评估组件。
