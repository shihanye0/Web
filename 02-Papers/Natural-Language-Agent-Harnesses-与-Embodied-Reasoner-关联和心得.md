---
title: "Natural-Language Agent Harnesses 与 Embodied-Reasoner 的关联和阅读心得"
date: 2026-07-07
tags: [paper, embodied-ai, evaluation, agent-harness, reading-reflection]
status: read
related:
  - "[[Natural-Language-Agent-Harnesses-4plus-integrated-notes]]"
  - "[[Embodied-Reasoner - Synergizing Visual Search Reasoning and Action for Embodied Interactive Tasks]]"
  - "[[2026-07-06-具身智能评估方向论文阅读顺序]]"
---

# Natural-Language Agent Harnesses 与 Embodied-Reasoner 的关联和阅读心得

## 先纠正一个判断

我之前把 **Natural-Language Agent Harnesses** 放在“具身智能评估方向”的第一篇，容易让人误以为它是一篇直接讲具身智能评估指标的论文。这个表述不够准确。

更准确地说：这篇论文不是“具身评估指标论文”，而是 **agent harness / 评估基础设施论文**。它不直接回答 Embodied-Reasoner 里的 Success Rate、Search Efficiency、Task Completeness 怎么定义，也不专门分析 AI2-THOR 里的搜索、操作、搬运、组合任务。它真正有价值的地方是帮我理解：一个多轮 agent 的任务、环境、模型、轨迹、状态、工具调用、验证门控和最终指标，应该怎样被组织成一个可重复、可比较、可诊断的评估系统。

所以，如果我带着“我要找具身评估指标”的预期去读，会觉得它没有讲到点上；但如果我带着“我要理解 agent 评估框架和 harness 结构”的问题去读，它就很有价值。

## 这篇论文哪里有“评估”

它的评估不在具身任务指标层，而在 harness 层。

它评估的是：

- 共享运行时和 harness logic 是否真的改变 agent 行为；
- harness 模块能不能被单独添加、移除和比较；
- 代码 harness 迁移成自然语言 harness 后，是否还能保持任务级可比较行为；
- 只看最终成功率是否会掩盖过程差异；
- verifier、多候选搜索、文件化状态、证据产物等控制结构是否真的帮助最终验收。

这对应论文的三个 RQ：

1. **RQ1：Behavioral Effect**  
   Full IHR、w/o runtime skill、w/o harness skill 之间的成功率差异不大，但 token、工具调用、LLM 调用、运行时间、子 agent 占比都明显变化。说明 harness 不是 prompt 装饰，而是真实改变轨迹的控制变量。

2. **RQ2：Module Ablation**  
   file-backed state、evidence-backed answering、verifier、self-evolution、multi-candidate search、dynamic orchestration 被逐个消融。结果不是“模块越多越好”，而是看模块是否对齐最终 evaluator。

3. **RQ3：Code-to-text Migration**  
   OS-Symphony 从原生代码 harness 迁移到 NLAH 后，可靠性机制从 GUI 局部修复转向 file-backed state 和 artifact-backed verification。这里的重点是评估迁移后的行为是否仍然可比较、可诊断。

因此，这篇论文的“评估”是 **评估 agent harness 本身**，不是评估某个具身模型的视觉、导航或操作能力。

## 它和 Embodied-Reasoner 的关系

Embodied-Reasoner 是一个具体的具身 agent 方法论文。它关心的是：

- 模型如何在 AI2-THOR 中完成任务；
- Observation-Thought-Action 轨迹怎么生成；
- 搜索、操作、搬运、组合任务怎么评估；
- 训练流程如何从 imitation learning 到 rejection sampling，再到 reflection tuning；
- 最终用 Success Rate、Search Efficiency、Task Completeness 衡量行为质量。

Natural-Language Agent Harnesses 是更上层的框架论文。它关心的是：

- 一个多轮 agent 的运行逻辑如何被外部化；
- 状态、产物、日志、验证门控如何从上下文窗口中拿出来；
- harness 模块如何被消融；
- 运行时和任务逻辑如何分离；
- 为什么最终指标之外，还要看轨迹、调用成本、失败类型和局部验收是否对齐。

二者的关系可以这样理解：

| 维度 | Embodied-Reasoner | Natural-Language Agent Harnesses |
|---|---|---|
| 层级 | 具体具身任务方法 | agent harness / evaluation infrastructure |
| 环境 | AI2-THOR 室内交互 | SWE-bench、OSWorld 等多轮 agent 基准 |
| 轨迹 | Observation-Thought-Action | agent call、child agent、artifact、ledger |
| 指标 | Success、Efficiency、Completeness | outcome + process metrics + ablation flips |
| 关注点 | 模型是否会搜索、推理、行动 | harness 是否可执行、可迁移、可消融 |
| 对我的作用 | 看懂具身任务怎么完成 | 看懂评估系统怎么组织和诊断 |

一句话：**Embodied-Reasoner 是被评估的具身 agent；NLAH 帮我理解评估这类 agent 时，harness、状态、轨迹、验证和指标应该怎么拆开看。**

## 对我当前有什么帮助

### 1. 帮我不要只盯 Success Rate

Embodied-Reasoner 的 Success Rate 很重要，但 NLAH 提醒我：最终成功率只是结果，不是全部证据。

我还应该看：

- 轨迹长度是否异常；
- 是否重复搜索同一个位置；
- 是否有非法动作；
- 是否提前终止；
- 是否在局部 verifier 或环境反馈上“自以为成功”；
- 是否虽然完成了任务，但用了过多冗余步骤；
- 是否有关键状态没有被记录，导致失败不可诊断。

这正好对应 Embodied-Reasoner 的 Search Efficiency 和 Task Completeness。

### 2. 帮我理解 evaluate 目录应该看什么

我现在跑 `/home/user/github-product/embodied_reasoner` 项目的评估任务时，不应该只找“分数在哪里算”。更应该看：

- task 是如何定义的；
- observation、thought、action、feedback 是否完整记录；
- success 判断依赖最终状态还是动作序列；
- efficiency 是否惩罚重复探索；
- completeness 是否检查关键动作覆盖；
- 失败日志能否定位到搜索失败、操作失败、顺序错误、状态遗忘、提前终止；
- 评估器的验收目标和模型自己的终止理由是否一致。

NLAH 的 RQ2 对我尤其有提醒：**局部验证通过不等于 benchmark 通过**。在 Embodied-Reasoner 里，如果模型说“任务完成”，但 AI2-THOR 最终状态不满足任务条件，那就是 harness/evaluator 对齐失败。

### 3. 帮我理解“反思”什么时候有用

Embodied-Reasoner 的 Reflection Tuning 有明显收益。NLAH 里的 self-evolution 也有明显正向效果。但两篇论文共同说明：反思有用，不是因为模型多写了几句思考，而是因为它被真实失败信号和明确验收门约束。

有效反思应该满足：

- 有真实环境反馈；
- 有明确失败类型；
- 下一次行动真的根据失败信号改变；
- 最终以任务验收条件为准，而不是以自我解释为准。

这对我读具身 agent 论文很重要。以后看到 reflection、self-correction、self-evolution，不能只看名字，要看它是否绑定了环境反馈和评估门。

### 4. 帮我警惕“结构越多越好”的误区

Embodied-Reasoner 里也有类似问题：复杂任务需要长思考，但简单 Search 任务上过度探索可能反而低效。NLAH 的 RQ2 更直接说明：verifier、多候选搜索、动态编排都可能让过程更有组织，但不一定提高最终结果。

所以我后面分析具身智能评估时，要区分：

- 必要结构：帮助状态记录、失败恢复、任务验收；
- 多余结构：增加 token 和步骤，但没有更接近最终目标；
- 有害结构：让模型相信局部成功，却偏离真实 evaluator。

## 我目前的收获

第一，**我对“评估”的理解从指标层上升到了 harness 层**。以前我容易把评估理解成最终表格里的 Success Rate、Efficiency、Completeness。但现在更清楚：这些指标背后必须有任务定义、环境状态、动作记录、日志格式、验证门控和失败分类。没有这些基础设施，指标只是一个数字，无法解释模型为什么成功或失败。

第二，**多轮 agent 的核心不是一次输出，而是轨迹质量**。Embodied-Reasoner 的 Observation-Thought-Action 和 NLAH 的 agent call / artifact / ledger，本质都在强调同一件事：agent 的能力体现在连续交互轨迹中。一个模型如果最终成功，但过程中大量重复搜索、状态遗忘、错误自信，那么它的真实能力仍然不稳。

第三，**具身智能评估需要把“环境验收”放在最高优先级**。模型自己的 thought、verifier 的局部判断、甚至中间工具输出，都不能替代环境最终状态。NLAH 里 verifier 与 benchmark evaluator 不一致的案例，对 Embodied-Reasoner 很有警示意义：具身任务最终必须回到 AI2-THOR 状态是否满足任务条件。

第四，**file-backed state 这个思想可以迁移到具身评估日志分析中**。具身任务中很多失败都和状态有关：看过哪里、打开过什么、拿到了什么、目标是否可见、容器是否已检查。如果这些状态只存在模型上下文里，评估后很难复盘。更好的做法是把轨迹、关键状态、失败原因、最终产物分层记录，形成可回放、可审计的日志。

第五，**NLAH 对我不是直接提供具身方法，而是提供读项目代码的框架**。读 Embodied-Reasoner 项目时，我应该问：谁是 harness？谁是 runtime？任务契约在哪里？环境反馈如何进入下一轮？最终验收条件在哪里？失败时有没有证据链？这些问题比单纯找模型结构更接近我当前跑评估任务的需求。

## 我的判断

这篇论文对我当前方向的价值是“间接但重要”。它不是具身智能评估指标论文，所以不能替代 Embodied-Reasoner、OSWorld、AI2-THOR 这类直接评估论文。但它提供了一个上层视角：多轮 agent 评估不能只看最终得分，必须看 harness 如何组织任务、状态、轨迹、验证和产物。

如果我的目标是马上理解 Embodied-Reasoner 的论文指标，那 NLAH 不是最短路径；如果我的目标是理解项目里的 evaluate 目录、失败日志、轨迹诊断和评估系统设计，那 NLAH 是有帮助的。

因此，这篇论文应该放在阅读顺序里的位置是：**作为 Embodied-Reasoner 之后的评估框架补充，而不是具身评估指标主文献。**



对我使用codex,claude code这些ai编程工具有什么帮助
NLAH 这篇论文对我用 Codex、Claude Code 的核心提醒是：不要把 AI 编程工具当成“会写代码的聊天框”，要把它当成一个可被 harness 管住的多轮 agent。也就是说，效果不只取决于模型聪不聪明，还取决于怎么组织任务、状态、验证、失败恢复和交接。

  对你最有用的几点：

  1. 任务要写成契约，不要只写成愿望

  差的提法：

  > 帮我改一下这个 bug。

  更好的提法：

  > 目标：修复 X bug。
  > 边界：不要重构无关模块。
  > 验收：必须跑 pytest ...，如果跑不了说明原因。
  > 输出：说明改了哪些文件、验证结果、剩余风险。
  > 禁止：不要改生成文件，不要覆盖我已有改动。

  这就是论文里的 contract-first 思维。

  2. 让 AI 先定位 owner，再写代码 NLAH 强调 harness 要区分 runtime、task logic、adapter、artifact。对应到代码项目里，就是
  先问：

  - 这个概念谁创建？
  - 谁消费？
  - 真源在哪里？
  - 是核心逻辑、adapter、UI、CLI，还是测试层？
  - 有没有已有模块负责这件事？

  你用 Codex/Claude Code 时，可以要求：

  > 先只读审计，找出这个功能的 owner、调用链、测试入口，再给判断；不要先改代码。

  这能减少 AI “看见哪里顺手改哪里”的问题。

  3. 不要只让 AI 自称修好了，要让它产出证据

  论文里很重要的一点是：局部 verifier 说 solved，不等于 benchmark 真通过。

  对应 AI 编程工具就是：

  - AI 说“已修复”不算；
  - 跑过测试才算；
  - 没跑测试要说明为什么；
  - UI 改动要截图或浏览器验证；
  - 性能/权限/数据改动要有更强验收。

  你可以固定要求：

  > 最终回答必须列出实际运行过的命令和结果，不要只说逻辑上应该可以。

  4. 状态要外部化，别全靠上下文窗口

  论文里的 file-backed state 对你特别有用。长任务里不要让 Codex/Claude Code 只靠聊天历史
  记忆。你可以让它写或维护：

  - 当前目标
  - 已改文件
  - 验收命令
  - 未解决风险
  - 下一步命令
  - 禁止触碰的文件

  例如长任务可以要求：

  > 每完成一个阶段，把当前状态写入 dev-notes/current-task.md，包括已完成、验证结果、剩余
  > 风险和下一步。

  这样换窗口、上下文压缩、交给另一个 agent，都不容易丢状态。

  5. 结构不是越多越好，要对齐验收

  这篇论文最有价值的警告是：更多 verifier、多候选、多 agent，可能只是让过程更复杂，不一定
  更接近最终目标。

  用 AI 编程工具时也是：

  - 简单 bug 不需要 5 个 agent 分析；
  - 小改动不需要大重构；
  - verifier 如果没有跑真实测试，只是多一层自信；
  - 多方案比较如果不落到验收标准，就是“选项剧场”。

  你的原则应该是：

  > 结构服务于验收。凡是不能提高定位、实现、验证、回滚清晰度的流程，都不要加。

  6. 反思要绑定失败信号

  不要让 AI 空泛地“反思一下”。要让它基于失败输出改策略。

  好用的指令是：

  > 测试失败后，先复述失败日志中的关键错误，提出一个可证伪假设，再做最小修改。不要无根据
  > 连续改代码。

  这对应论文里 self-evolution 真正有效的地方：不是“多想”，而是“失败信号 -> 改变下一轮策略
  -> 再验收”。

  一句话总结

  这篇论文给你使用 Codex / Claude Code 的最大帮助是：
  你要设计自己的“AI 编程 harness”。

  具体就是：

  清晰任务契约
  -> 只读审计
  -> 找 owner 和真源
  -> 小步实现
  -> 真实测试/截图/日志验收
  -> 失败后基于证据调整
  -> 状态文件化
  -> 最终输出证据和风险

  这会比单纯换更强模型更稳定。模型能力重要，但你怎么约束它、让它留下证据、让它对齐最终验
  收，往往更决定结果。



## 后续阅读建议

接下来更应该读：

1. **General Modular Harness for LLM Agents in Multi-Turn Gaming Environments**  
   这篇会比 NLAH 更贴近多轮环境评估，适合继续补“harness + environment + trajectory”的线。

2. **Beyond Accuracy: Behavioral Testing of NLP Models with CheckList**  
   用来训练“把能力拆成行为测试项”的思维。

3. **VL-CheckList**  
   用来把具身失败拆成视觉识别、属性理解、空间关系、动作规划等更细维度。

这三篇读完后，再回到 Embodied-Reasoner 项目的评估日志，会更容易把失败案例分层。
