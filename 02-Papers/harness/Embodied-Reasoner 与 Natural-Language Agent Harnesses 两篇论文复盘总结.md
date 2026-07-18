---
title: "Embodied-Reasoner 与 Natural-Language Agent Harnesses 两篇论文复盘总结"
date: 2026-07-09
tags: [paper-review, embodied-ai, agent-harness, evaluation, reflection, ai2thor]
status: review
related:
  - "[[Embodied-Reasoner - Synergizing Visual Search Reasoning and Action for Embodied Interactive Tasks]]"
  - "[[Natural-Language-Agent-Harnesses-与-Embodied-Reasoner-关联和心得]]"
  - "[[Natural-Language Agent Harnesses-论文总介绍]]"
---

# Embodied-Reasoner 与 Natural-Language Agent Harnesses 两篇论文复盘总结

## 一句话总收获

**Embodied-Reasoner 告诉我：具身 agent 的能力来自“观察-思考-行动-反馈”的闭环训练；Natural-Language Agent Harnesses 告诉我：多轮 agent 的可靠性来自 harness 对任务、状态、证据、验证和失败恢复的组织。**

这两篇论文不是两条无关路线，而是一上一下两层：

- **Embodied-Reasoner**：具体具身任务怎么做、怎么训练、怎么评估。
- **Natural-Language Agent Harnesses**：多轮 agent 系统应该怎么被组织、诊断、复现和消融。

我真正要吸收的不是论文表格里的分数，而是一个更稳定的读项目框架：看到一个 agent 项目时，不先被模型名字、prompt 或 CoT 文本吸引，而是先拆任务契约、runtime、环境反馈、状态产物和最终验收。

## Embodied-Reasoner 的核心价值

这篇论文不是简单说“让 VLM 多思考”，而是把具身任务重新定义为连续闭环：

```text
Observation -> Thought -> Action -> Environment Feedback -> Next Observation
```

### 1. 具身推理不是静态 VQA

普通 VQA 是看一张图回答问题；具身任务是模型在未知环境里持续搜索、记忆、修正和执行。前一步打开过什么、看过哪里、拿到了什么、失败了什么，都会改变下一步。

所以具身智能的难点不只是“看懂图像”，而是能否把视觉、历史、空间关系、任务目标和动作后果统一到同一条轨迹里。

### 2. 数据格式比模型名字更关键

Embodied-Reasoner 构造的是 9.3k 条 Observation-Thought-Action 轨迹，包含交互图像、动作、搜索过程、反思和验证，而不是只给最终答案。

以后看具身 agent 论文，要先问：

- 它训练的是最终答案，还是完整交互轨迹？
- 它有没有记录观察、动作、反馈和历史？
- 它的 thought 是否真的影响后续 action？
- 它的环境反馈是否进入下一轮决策？

### 3. 三阶段训练对应三种能力

```text
Imitation Learning        -> 学会基本交互格式
Rejection Sampling Tuning -> 学会搜索和探索
Reflection Tuning         -> 学会失败后修正
```

最值得记住的是：提升最大的是 Rejection Sampling Tuning，从 25.46% 到 65.39%。这说明具身任务的第一瓶颈往往不是“会不会推理”，而是“会不会在未知环境中有效搜索”。

Reflection Tuning 又把 65.39% 提升到 80.96%，说明反思确实有价值，但前提是它被错误动作、异常状态和纠正轨迹约束。

### 4. 反思必须绑定失败信号

Reflection Tuning 有价值，不是因为模型多写了几句“让我反思一下”，而是因为论文把异常状态、错误动作和纠正轨迹放进训练流程。

它做了两类构造：

- 在成功轨迹中插入异常状态，让模型识别 abnormal state 后重试或修正。
- 在失败轨迹中定位第一个错误动作，再接上 reflection 和后续正确轨迹。

以后看到 reflection、self-correction、self-evolution，要追问：

- 有没有真实环境反馈？
- 有没有明确失败类型？
- 反思之后动作是否真的改变？
- 训练或评估是否奖励正确纠正，而不是奖励漂亮解释？

如果没有这些约束，reflection 很可能只是形式化 chain-of-thought。

### 5. 评估不能只看 Success Rate

Embodied-Reasoner 的三个指标很关键：

```text
Success Rate       -> 最终是否完成任务
Search Efficiency  -> 是否高效，是否少走冗余步骤
Task Completeness  -> 是否覆盖关键动作链
```

这提醒我：跑具身评估时不能只盯 success。还要看轨迹质量：

- 是否重复搜索同一个位置？
- 是否打开过容器后没有更新计划？
- 是否有非法动作？
- 是否提前终止？
- 是否完成了部分子任务但漏掉关键动作？
- 是否虽然成功但路径非常低效？
##指标不只看 outcome

至少要分三层：

| 层级 | 指标 |
|---|---|
| Outcome | success, score, task completion |
| Efficiency | steps, cost, repeated actions, time |
| Diagnosis | perception error, memory error, illegal action, evaluator mismatch |

Embodied-Reasoner 的 Success / Search Efficiency / Task Completeness 就是向这个方向迈了一步。
## Natural-Language Agent Harnesses 的核心价值

NLAH 不是具身智能方法论文。它真正给我的，是一个读 agent 系统和评估代码的上层框架。

它的核心判断是：**agent 成败不只取决于 base model，还取决于 harness。**

harness 是多轮任务外面的控制系统：

```text
任务如何分解
谁负责执行
状态放在哪里
中间产物怎么保存
失败怎么恢复
验证门在哪里
什么时候停止
最终证据是什么
```

### 1. harness 要成为一等对象

很多 agent 系统表面在比模型，实际在比 controller、prompt、tool adapter、verifier、日志、状态管理和停止规则。

NLAH 的价值是把这些东西显式化，让 harness 可以被迁移、比较、消融和审计。

以后读 agent 项目时，我应该先问：

- 谁是 harness？
- 谁是 runtime？
- 哪些逻辑是任务族策略？
- 哪些逻辑是通用运行时？
- 哪些约束藏在 prompt、controller 或脚本里？

### 2. context engineering 大于 prompt engineering

长程任务不是靠一句 prompt 解决，而是靠每一步给模型什么上下文、证据、状态和约束。

NLAH 把 prompt engineering 扩展成 context engineering。它关心：

- 当前步骤应该看到哪些历史？
- 哪些状态必须外部化？
- 哪些中间产物必须保存？
- 哪些验证结果必须进入下一轮？
- 哪些失败模式应该触发修复？

这和 Embodied-Reasoner 完全对应：具身任务里每轮 observation、feedback、history 都是 context engineering。

### 3. file-backed state 是长程 agent 的关键

长程 agent 如果把状态只放在上下文里，失败后很难复盘，也容易在截断、重启和分支中丢失关键事实。

NLAH 强调 file-backed state：状态要外部化、路径可寻址、可重新打开、可审计。

迁移到 Embodied-Reasoner，就是要重视：

- `result.json`
- 轨迹图片
- `messages`
- `trajectory`
- `key_actions`
- `metrics`
- 每步 `errorInfo`

这些不是附属日志，而是判断模型为什么成功或失败的证据链。

### 4. verifier 不等于最终 evaluator

NLAH 很重要的警告是：局部 verifier 可能说 solved，但 benchmark evaluator 仍然失败。

迁移到具身任务就是：

- 模型说“任务完成”不等于环境完成。
- 中间 thought 看起来合理不等于动作正确。
- 局部反馈通过不等于最终状态满足。
- key action 覆盖也不一定完全等于物理世界最终状态正确。

真正的验收必须回到最终 evaluator。

### 5. 结构不是越多越好

NLAH 的 RQ2 不支持“结构越多越好”。verifier、多候选搜索、动态编排、file-backed state 都是工具，是否有用取决于它们是否更接近最终验收。

这也能解释 Embodied-Reasoner 的现象：复杂任务需要长思考，简单 Search 任务中过度探索反而可能伤害效率。

所以以后不要机械崇拜：

- long CoT
- reflection
- verifier
- multi-agent
- multi-candidate search
- dynamic orchestration

要问它们是否真的降低失败率、提升可诊断性，并且对齐最终 evaluator。

## 两篇论文合起来形成的项目阅读框架

以后读任何 agent 或具身项目，都按这条链拆：

```text
Task Contract
  -> Harness
  -> Runtime / Environment
  -> Model Call
  -> Action Parser
  -> Environment Feedback
  -> Trajectory Artifact
  -> Metric / Evaluator
  -> Failure Diagnosis
```

对应到 Embodied-Reasoner 项目：

```text
data/test_809.json
  -> evaluate/evaluate.py
  -> AI2-THOR Controller + RocAgent
  -> local/API VLM
  -> <DecisionMaking> parser
  -> <|feedback|> + new image
  -> result.json
  -> metric()
  -> trajectory replay
```

这条链比“模型结构在哪里”更重要，因为它决定了任务是否可执行、失败是否可诊断、指标是否可信。

## 我现在最该内化的 8 条判断

1. **具身智能不是看图回答，而是状态化交互。**
2. **agent 能力不是单点输出能力，而是轨迹质量。**
3. **搜索能力是具身任务的第一瓶颈。**
4. **反思必须绑定环境反馈，否则只是形式化 CoT。**
5. **success 只是最终结果，efficiency 和 completeness 才能解释行为质量。**
6. **harness 是 agent 系统的真实控制层。**
7. **状态、证据、日志、artifact 必须外部化，否则失败不可诊断。**
8. **verifier、reflection、多候选、长思考都只是手段，最终必须对齐 evaluator。**

## 跑 Embodied-Reasoner 评估时的检查表

每次看评估结果或失败日志，都问：

- 这个任务的真源在哪里？是 `taskquery`、`task_metadata.actions`，还是最终状态？
- 当前模型每轮看到了什么图像、历史和反馈？
- action 是怎么从自然语言解析成环境动作的？
- 非法动作如何反馈给模型？
- `success=1` 是因为最终状态真的满足，还是因为 key action 覆盖？
- efficiency 是否惩罚重复搜索？
- completeness 是否能暴露“只完成一半任务”？
- `result.json` 是否足够回放失败？
- 失败是视觉识别错、搜索错、动作错、顺序错、状态遗忘，还是提前终止？
- 模型的自我解释和环境事实是否一致？

## 读新 agent 论文时的通用问题

以后读类似论文，不先问“模型有多强”，先问：

1. 任务契约是什么？
2. 环境是否真实交互，还是离线问答？
3. 每一步是否有 observation/action/feedback？
4. 状态是否外部化？
5. 失败是否可复盘？
6. 反思是否绑定真实错误？
7. verifier 是否对齐最终 evaluator？
8. 指标能否解释过程质量，而不是只给最终分数？
9. 改进来自模型本身，还是来自 harness、数据、搜索、反馈和日志结构？
10. 如果这个系统三个月后失效，最可能是哪个环节失效？

## 自测问题与参考答案

为了确认自己真的吸收了这两篇论文，可以反复问自己：

### 1. 为什么 Embodied-Reasoner 的最大提升来自 Rejection Sampling Tuning？

因为具身任务的第一瓶颈往往不是“会不会写推理文本”，而是“会不会在未知环境中有效搜索”。第一阶段 Imitation Learning 主要让模型学会动作格式和基本交互，但它还不一定知道目标不在眼前时该如何探索。Rejection Sampling Tuning 让模型在新任务上采样多条自探索轨迹，再用数据引擎筛掉失败轨迹，保留能完成任务的成功搜索过程。

这相当于把“哪些搜索路径真的能完成任务”变成训练信号。模型学到的不只是动作标签，而是：找不到目标时要换候选位置、搜索要有优先级、探索过的地方不要机械重复、复杂任务要维持子目标顺序。所以它带来的提升最大。

### 2. 为什么 Reflection Tuning 不是普通 CoT？

普通 CoT 可以只是模型多写几句“让我想一想”，不一定改变后续行动，也不一定绑定真实错误。Reflection Tuning 的关键是它把反思放进环境反馈和纠错轨迹里。

论文里有两种构造：成功轨迹中插入异常状态，让模型识别异常后修正；失败轨迹中定位第一个错误动作，再接上反思和后续正确轨迹。训练时还会屏蔽错误部分，只对 reflection tokens 和正确后续轨迹计算 loss。也就是说，它奖励的不是“反思文本漂亮”，而是“失败后能改变计划并走向正确动作”。

### 3. Search Efficiency 和 Task Completeness 分别防止什么误判？

**Search Efficiency** 防止把“低效成功”误判成高质量成功。一个模型可能最后完成任务，但中间反复打开同一个柜子、走很多冗余步骤、绕远路找目标。只看 Success Rate 会把这种轨迹算成成功，但 Search Efficiency 会惩罚冗余动作。

**Task Completeness** 防止把“碰巧结束”或“只完成部分子任务”误判成完整能力。复杂任务通常有关键动作链，比如找到物体、拿起、导航到容器、放置、关闭或验证。Task Completeness 看预测动作覆盖了多少关键动作，可以暴露模型是否真正沿着任务结构推进。

### 4. NLAH 里的 harness 和 runtime 有什么区别？

**harness** 是任务族的控制逻辑：任务怎么分阶段、谁负责什么、需要产出哪些 artifact、验证门是什么、失败后怎么恢复、什么时候停止。它更像“这类任务应该怎么跑”的策略层。

**runtime** 是执行这些 harness 的通用底座：工具调用、沙箱、子 agent 生命周期、文件读写、权限、通用状态语义等。它更像“让 harness 能跑起来”的执行层。

一句话区分：harness 定义任务流程和验收合同，runtime 提供通用执行能力。

### 5. file-backed state 为什么对长程 agent 重要？

长程 agent 最大的问题之一是状态会丢。任务跨很多轮之后，模型可能忘记看过哪里、改过什么文件、哪个验证失败过、当前证据在哪里。如果状态只在上下文窗口里，一旦截断、重启、分支或多 agent 并行，失败就很难复盘。

file-backed state 把关键状态写成路径可寻址的文件或 artifact，让后续步骤可以重新打开同一个对象。它的价值不是“多写日志”，而是让状态可恢复、可审计、可交接。迁移到具身评估，就是 `result.json`、轨迹图片、messages、key_actions、metrics 都应该成为复盘证据链。

### 6. 为什么 verifier 通过不等于 benchmark 通过？

因为 verifier 只是局部验收器，它检查的对象可能和最终 benchmark evaluator 不完全一致。NLAH 里有案例显示，局部 verifier 认为任务 solved，但官方 evaluator 仍然失败。这说明中间验证层可能制造“局部成功”的错觉。

迁移到具身任务也是一样：模型说任务完成、局部动作成功、甚至 key action 看起来覆盖，都不一定等于 AI2-THOR 最终状态满足任务条件。最终判断必须对齐真正的 evaluator，而不是相信模型自己的解释或中间 verifier。

### 7. 如果我要读 `evaluate/` 目录，应该按什么调用链读？

不要先乱翻模型文件，应该沿着评估闭环读：

```text
data/test_809.json
  -> evaluate/evaluate.py
  -> RocAgent.exec()
  -> AI2-THOR Controller
  -> <DecisionMaking> parser
  -> <|feedback|> + image message
  -> result.json
  -> metric()
```

具体问题是：任务从哪里读入，key_actions 如何生成，模型输出如何解析成动作，动作如何进入环境，失败反馈如何拼回下一轮，轨迹如何保存，success/efficiency/completeness 如何计算。

这条链比“模型结构在哪里”更重要，因为它决定了评估是否可信、失败是否能复盘。

### 8. 如果一个模型最终成功但反复搜索同一位置，我应该如何评价它？

它应该被评价为“结果成功，但轨迹质量差”。Success Rate 可以给它 1，但 Search Efficiency 应该降低，失败分析里也要标记重复搜索或状态利用不足。

这类模型在 benchmark 表格上可能看起来成功，但在真实机器人场景中不可用：它浪费时间、消耗资源，还可能因为重复动作增加碰撞、超时或状态漂移风险。更准确的判断是：它具备一定任务完成能力，但搜索策略、记忆利用和环境反馈吸收能力不足。

## 最终消化结论

这两篇论文对我当前方向最大的价值不是“背论文贡献”，而是给我一个研究和工程统一的视角：

**Embodied-Reasoner 教我什么是具身 agent 的有效闭环；Natural-Language Agent Harnesses 教我怎么审计这个闭环是否真的可执行、可验证、可复盘。**

下一步回到项目时，我应该少问“模型结构在哪里”，多问：

```text
任务契约在哪里？
环境反馈怎么进下一轮？
轨迹证据保存在哪里？
最终验收是否对齐真实 evaluator？
失败能否沿着证据链定位？
```

这才是这两篇论文真正能迁移到我当前评估任务里的价值。
