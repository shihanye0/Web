---
title: "Natural-Language Agent Harnesses 图表解读"
date: 2026-07-08
tags: [paper, agent-harness, evaluation, codex, claude-code, figure-reading]
status: done
source:
  - "/home/user/Downloads/paper/Natural-Language Agent Harnesses-dual.pdf"
related:
  - "[[Natural-Language Agent Harnesses-]]"
  - "[[Natural-Language-Agent-Harnesses-4plus-integrated-notes]]"
  - "[[Natural-Language-Agent-Harnesses-与-Embodied-Reasoner-关联和心得]]"
---

# Natural-Language Agent Harnesses 图表解读

## 总览

这篇论文的图表不只是展示实验结果，而是在搭一条完整论证链：

> **Harness 不是 prompt 装饰，而是可以被显式表示、执行、迁移、消融和评估的系统对象。**

如果只看文字，容易把这篇论文理解成“用自然语言写 agent 流程”。但从图表看，作者真正想强调的是：现代 agent 的能力越来越取决于控制层，也就是任务怎么分解、状态怎么保存、工具怎么调用、验证怎么做、失败后怎么恢复。

全文主要图表包括：

- Figure 1：现代 agent harness pattern 总览
- Figure 2：NLAH / IHR 总架构
- Figure 3：实验实现映射
- Figure 4：RQ2 的成本-效果补充视图
- Table 1-2：RQ1 行为效应和配对翻转
- Table 3-4：RQ2 模块消融和子 agent 使用拆分
- Table 5：RQ3 代码到文本迁移
- Table 6：file-backed state 工作区结构
- Table 7：RQ1 组件敏感案例

这份笔记按图表逐个解释：它画了什么、表达什么、想传达什么观点，以及我该如何理解它。

## Figure 1：现代 Agent Harness 设计模式总览

Figure 1 中间是 **Orchestration**，周围连着 Memory、Planning、Flow、ReAct、Native CLI、Self-Evolving、Subagents、Test-Time Scaling、RAG、Reflexion 等模块。

这张图想先把 **harness** 这个抽象词变得具体。作者不是凭空发明一个新概念，而是在说：现代 agent 里已经有很多控制模式，只是它们通常散落在不同代码、prompt、框架默认值和工具适配器里。

这些模式可以理解为：

- **ReAct**：控制模型如何在 reasoning 和 acting 之间循环。
- **RAG**：控制模型如何检索外部资料。
- **Memory**：控制历史状态如何保留。
- **Reflection / Self-Evolving**：控制失败后如何调整策略。
- **Planning / Flow**：控制任务如何分阶段。
- **Subagents**：控制任务如何委派给多个 agent。
- **Native CLI**：控制模型如何调用真实系统工具。
- **Test-Time Scaling**：控制推理时是否投入更多计算。

这张图真正传达的观点是：

> 现代 agent 的性能越来越由这些外围控制模式决定，而不只是由基础模型决定。

所以 Figure 1 是论文的问题入口：既然这些 harness pattern 很重要，就应该把它们作为独立研究对象，而不是继续埋在工程代码里。

## Figure 2：NLAH / IHR 总架构图

Figure 2 是整篇论文最关键的架构图。它分成左右两部分。

左边比较两种 harness：

| 类型 | 特征 |
|---|---|
| Traditional Code-Coupled Harness | Complex、Framework-Locked、Opaque Logic |
| Natural Language Harness | Explicit、Portable、Composable |

传统方式里，plan、execute、verify、repair loop 都写在代码控制器里。这样做的问题是：逻辑复杂、依赖具体框架、不容易迁移，也很难单独消融某个模块。

NLAH 的做法是把高层控制逻辑写成结构化自然语言。例如：

- 阶段：PLAN、EXECUTE、VERIFY、REPAIR
- 角色：Planner、Solver、Debugger
- 契约：必须输出合法 Python 文件
- 失败分类：format_error、test_failure、tool_error
- 停止条件：测试通过或达到最大重试次数

右边展示 IHR 如何执行 NLAH：

- 上层是 **Natural-Language Agent Harness**
  - Contracts & Gates
  - State & Artifacts
  - Control & Prompts
- 中层是 **Intelligent Harness Runtime**
  - In-loop LLM
  - Runtime Charter / Policy Semantics
  - Backend / Tool Interface / Agent Calls
- 下层是 **File-Backed State Module**
  - Workspace
  - Artifacts
  - Ledgers
  - task_state.json
  - response.txt

这张图要防止一个误解：论文不是说“自然语言替代代码”。更准确地说：

> 自然语言负责表达高层 orchestration logic；代码、脚本和工具负责确定性执行；IHR 负责解释并调度两者。

我最该关注的是右下角的 **File-Backed State Module**。它说明 agent 的状态不应该只存在上下文窗口里，而应该写到文件、ledger 和 artifact 中，变成 path-addressable、compaction-stable、persistent across steps 的对象。

这对 Codex / Claude Code 的启发很直接：长任务不能只靠聊天历史，应该有任务文件、状态文件、验证记录和交接文档。

## Figure 3：实验实现映射图

Figure 3 很小，但非常重要。它展示三组映射：

| 抽象层 | 实验实现 |
|---|---|
| Backend | Codex |
| Runtime Charter | Runtime Skill |
| Harness Logic | Harness Skill |

这张图解释了实验中如何把系统拆成可控变量。作者想研究 harness，就不能把所有东西混在一起比较，否则无法判断性能变化来自哪里。

这张图说明：

- Codex 只是 backend，提供终端工具和多 agent 接口。
- Runtime Skill 承载共享运行时规则。
- Harness Skill 承载基准专属逻辑。

因此后面的 RQ1/RQ2 消融不是随便删 prompt，而是在删不同层：

- 去掉 runtime skill，看共享运行时章程影响；
- 去掉 harness skill，看任务专属控制逻辑影响；
- 保持 backend 不变，避免把模型/工具能力混进结论。

Figure 2 是系统架构图，Figure 3 是实验变量图。

## Table 1：RQ1 结果与过程指标

Table 1 比较 Full IHR、w/o RTS、w/o HS 在 SWE-bench Verified 上的表现。

表中指标包括：

- Perf.
- Prompt Tokens
- Completion Tokens
- Tool Calls
- LLM Calls
- Runtime

TRAE 的关键数字：

| Setting | Perf. | Prompt Tokens | Tool Calls | LLM Calls | Runtime |
|---|---:|---:|---:|---:|---:|
| Full IHR | 74.4 | 16.3M | 642.6 | 414.3 | 32.5 min |
| w/o RTS | 76.0 | 11.1M | 451.9 | 260.5 | 16.6 min |
| w/o HS | 75.2 | 1.2M | 51.1 | 34.0 | 6.7 min |

如果只看 Perf，Full IHR 并没有更高，甚至低于 w/o RTS。但它的过程指标明显更重：更多 token、更多工具调用、更多 LLM 调用、更长运行时间。

这张表想表达的不是“Full IHR 更强”，而是：

> Harness logic 和 runtime charter 确实改变了 agent 的行为。

也就是说，NLAH/IHR 不是 prompt wrapper。它真的改变了运行过程。

但这张表同时提醒我：

> 行为改变不等于性能一定提升。

这是整篇论文最克制也最重要的地方。作者没有把结果包装成“结构化一定更好”，而是把它解释为：harness 是真实控制变量，但这个控制变量有好有坏。

## Table 2：RQ1 配对翻转

Table 2 统计同一批 125 个 SWE 样本中，Full IHR 和消融版本谁解决了任务。

表中：

- **F**：只有 Full IHR 解决。
- **A**：只有 ablation 解决。
- **S**：两者结果一致。

关键数字：

| Harness | 对比 | F | A | S |
|---|---|---:|---:|---:|
| TRAE | vs w/o RTS | 4 | 6 | 115 |
| TRAE | vs w/o HS | 7 | 8 | 110 |
| Live-SWE | vs w/o RTS | 4 | 8 | 113 |
| Live-SWE | vs w/o HS | 4 | 7 | 114 |

这张表说明，大多数样本并不会因为 harness 变化而翻转。超过 110/125 个样本在 Full IHR 和消融版本之间结果一致。

真正有信息量的是少数边界样本：

- 有些只有 Full IHR 解出；
- 有些反而只有轻量版本解出。

作者的核心判断是：

> Full IHR behaves more like a solved-set replacer than a uniform frontier expander.

也就是：Full IHR 更像是在替换已解决集合，而不是把所有任务的能力边界整体往前推。

这对我使用 AI 编程工具很有启发。更多流程、更多 agent、更多 verifier 并不一定统一提升能力，它可能只是改变了哪些 case 能解、哪些 case 反而被复杂流程拖累。

## Table 3：RQ2 模块组合与消融

Table 3 是全文最值得反复看的结果表之一。它从 Basic 起点出发，逐个添加 harness 模块：

- File-Backed State
- Evidence-Backed Answering
- Verifier
- Self-Evolution
- Multi-Candidate Search
- Dynamic Orchestration

结果如下：

| Benchmark | Basic | File-backed State | Evidence-backed | Verifier | Self-evolution | Multi-candidate | Dynamic orchestration |
|---|---:|---:|---:|---:|---:|---:|---:|
| SWE Verified | 75.2 | 76.8 | 76.8 | 74.4 | 80.0 | 72.8 | 75.2 |
| OSWorld | 41.7 | 47.2 | 41.7 | 33.3 | 44.4 | 36.1 | 44.4 |

这张表最直接的结论是：

> Harness 模块可以被消融，但模块效果不是单调的。

比较明显的正向模块：

- **Self-Evolution**：SWE 从 75.2 提升到 80.0。
- **File-Backed State**：OSWorld 从 41.7 提升到 47.2。

中性或温和模块：

- Evidence-Backed Answering 在 SWE 有小幅提升，在 OSWorld 基本不变。
- Dynamic Orchestration 在 SWE 持平，在 OSWorld 有小幅提升。

负向模块：

- Verifier 在两个 benchmark 都下降，尤其 OSWorld 从 41.7 降到 33.3。
- Multi-Candidate Search 也下降，说明更大搜索树未必带来更好结果。

这张表真正想传达：

> 结构不是越多越好，关键是结构是否对齐最终 evaluator。

Self-Evolution 有用，不是因为“反思”这个词有魔法，而是因为它把失败信号、下一轮尝试和验收门绑在一起。File-Backed State 有用，是因为它让状态、产物和交接更稳定。Verifier 失败，是因为局部 verifier 的判断可能和最终 benchmark evaluator 不一致。

## Table 4：TRAE NLAH 使用量拆分

Table 4 比较 Full IHR 中 runtime-owned parent 和 delegated child agents 的资源占比：

| Metric | Runtime-owned parent | Delegated child agents |
|---|---:|---:|
| Prompt tokens | 8.5% | 91.5% |
| Completion tokens | 8.1% | 91.9% |
| Tool calls | 9.8% | 90.2% |
| LLM calls | 9.4% | 90.6% |

这张表说明：Full IHR 中绝大多数实际工作发生在 delegated child agents 里，而不是父 agent 自己完成。

它想证明：

> Full IHR 真的改变了执行拓扑，不是同一个 agent 多写了一些 prompt。

运行结构更接近：

```text
runtime parent
  -> child agents
  -> artifacts
  -> verification
  -> handoff
```

这张表和 Table 1 要放在一起看。Table 4 证明多 agent / child-agent 结构真实存在；Table 1 则说明这种结构带来明显成本。结合 Table 3，进一步说明：真实结构不等于一定带来更好结果。

## Table 5：RQ3 代码到文本 Harness 迁移

Table 5 比较 OS-Symphony 原生代码 harness 和迁移后的 NLAH 版本：

| Realization | Perf. | Prompt Tokens | Completion Tokens | Agent Calls | Tool Calls | LLM Calls | Runtime |
|---|---:|---:|---:|---:|---:|---:|---:|
| Code | 30.4 | 11.4M | 147.2k | 99 | 651 | 1.2k | 361.5 min |
| NLAH | 47.2 | 15.7M | 228.5k | 72 | 683 | 34 | 140.8 min |

表面上看，NLAH 版本分数更高、运行时间更短、LLM calls 大幅减少。

但作者更强调行为差异，而不是只强调数值。原生 OS-Symphony 更像：

- 看截图；
- 判断当前屏幕；
- 选择 GUI 动作；
- 出错后修复焦点或选择；
- 依赖屏幕合理性判断。

迁移到 NLAH/IHR 后，更像：

- 生成任务文件；
- 写 ledger；
- 使用 file-backed state；
- 使用 artifact-backed verification；
- 在 shell、文件、package-level 操作能给出更强完成凭证时，绕开脆弱 GUI 修复。

这张表传达的核心观点是：

> 代码到文本迁移的关键不是自然语言更精确，而是可靠性机制发生了迁移。

可靠性从本地屏幕修复转向持久运行时状态和基于产物的闭环验证。这对 OSWorld 这类任务尤其重要，因为很多失败不是第一次意图错，而是恢复、收尾和验证不稳。

## Table 6：File-Backed State 的规范工作区

Table 6 展示 file-backed state 的 canonical workspace：

```text
run/
  TASK.md
  harness-skill/
    SKILL.md
    references/
    scripts/
  state/
    task_history.jsonl
  children/
    001/
      TASK.md
      SKILL.md
      inputs/
      scripts/
      scratch/
      RESPONSE.md
      artifacts/
  RESPONSE.md
  artifacts/
```

每类文件对应一种抽象对象：

- `TASK.md`：任务对象
- `harness-skill/SKILL.md`：任务族控制逻辑
- `state/task_history.jsonl`：子任务调用和状态提升历史
- `children/*/TASK.md`、`children/*/RESPONSE.md`：子 agent 的任务包和返回
- `artifacts/`：最终可评判产物
- `RESPONSE.md`：标准化最终响应、成功/失败状态和 artifact 指针

这张表不是普通目录说明，而是在定义一种状态哲学：

> 重要状态不能只存在模型上下文里，必须变成路径可寻址的文件和产物。

它对应三个关键词：

- **Externalized**：状态写入外部文件，而不是只存在 transient context。
- **Path-addressable**：后续阶段可以通过路径重新打开具体对象。
- **Compaction-stable**：上下文压缩、重启、委派后仍能恢复状态。

这张表对我使用 Codex / Claude Code 最直接。长任务应该写进度文件、任务状态、验证结果、子任务产物，而不是指望 agent 永远记得聊天历史。

## Table 7：RQ1 组件敏感 SWE 案例

Table 7 选了 4 个代表性 SWE 案例，解释为什么 Table 2 里会出现配对翻转。

### `matplotlib__matplotlib-24570`

结果模式：

- Live-SWE Full 解决；
- Live-SWE without runtime skill、shared baseline、TRAE Full 都失败。

主要教训：

> 适度 delegated topology 能帮助一些边界样本，但过重候选搜索也可能 overshoot。

### `django__django-14404`

结果模式：

- Live-SWE Full 失败；
- 更轻量的 coding conditions 解决。

主要教训：

> 某些本地 repository repair 更适合最短直接补丁路径，额外 workflow structure 可能增加摩擦。

### `sympy__sympy-23950`

结果模式：

- 较重 Full 条件失败；
- 较轻结构化条件解决。

主要教训：

> 模块价值依赖任务类型。如果 bug 主要需要紧凑本地 repair loop，额外 orchestration 不一定有帮助。

### `django__django-13406`

结果模式：

- 结构化运行报告本地 revalidation 成功；
- 官方 evaluator 仍失败。

主要教训：

> 局部 acceptance layer 可能偏离 benchmark 的最终 acceptance object。

Table 7 是全文最工程化的一张表。它把“结构不是越多越好”讲得非常具体。真正的问题不是 verifier 有没有、候选搜索有没有，而是这些结构是否对齐最终验收。

## Figure 4：RQ2 补充视图

Figure 4 有两个子图。

### 左图：Score-cost view

横轴是估算 API cost per sample，纵轴是 resolved rate。

大致趋势：

- Self-Evolution：分数最高，成本没有明显右移。
- File / Evidence：成本增加一些，分数小幅提升。
- Verifier：成本不低，分数不占优。
- Multi-Candidate Search：成本最高，分数反而低。
- Dynamic Orchestration：分数接近 Basic，但成本更高。

左图想说明：

> 不能只看分数，还要看成本。

Self-Evolution 是比较好的模块，因为它不是靠扩大搜索树堆成本，而是收紧求解循环。Multi-Candidate Search 是反例，它花费更高，但没有换来更好解决率。

### 右图：Complementarity with Basic

右图比较每个模块的 standalone solved rate，以及它和 Basic 的 union solved rate。

这张图解释为什么有些模块即使平均分不高，仍然值得研究。比如 Dynamic Orchestration 和 Verifier 单独表现可能弱，但它们可能解出 Basic 解不出的边界样本。

所以右图传达的是：

> 模块不一定提高平均分，但可能改变 solved set。

这和 Table 2 的结论一致：harness 模块更像改变哪些任务可恢复，而不是均匀提升所有任务。

## 图表共同构成的论证链

这些图表合起来，可以串成一条完整逻辑：

1. **Figure 1**：现代 agent 已经依赖多种 harness pattern。
2. **Figure 2**：这些 pattern 可以被外部化为 NLAH，并由 IHR 执行。
3. **Figure 3**：实验中把 backend、runtime charter、harness logic 分开，方便控制变量。
4. **Table 1**：Full IHR 明显改变 token、调用和运行过程，说明 harness 是真实控制变量。
5. **Table 2**：差异集中在边界样本，不是整体单调提升。
6. **Table 3**：模块可消融，但效果不一致。
7. **Table 4**：Full IHR 真的把工作转移到 child agents，不是 prompt wrapper。
8. **Table 5**：代码 harness 可以迁移到 NLAH，且可靠性机制发生迁移。
9. **Table 6**：file-backed state 是长任务可靠性的状态基础。
10. **Table 7**：具体案例说明适度结构、过度结构和局部验收错位。
11. **Figure 4**：成本视角进一步证明“更多结构不等于更好”。

## 我应该抓住的三个核心观点

### 1. Harness 是真实控制变量

Table 1 和 Table 4 证明 Full IHR 明显改变 token、工具调用、LLM 调用、运行时间和子 agent 占比。它不是换了几句 prompt，而是真的改变了 agent 的执行方式。

### 2. 结构必须对齐最终验收

Table 3、Table 7、Figure 4 都在强调：verifier、多候选、多 agent、证据产物不是越多越好。只有当这些结构收紧最终验收链路时，它们才有价值。

### 3. 状态外部化是长任务的关键

Figure 2 和 Table 6 都强调 file-backed state。长任务、跨会话、多 agent 协作，必须把状态写成文件、artifact、ledger，而不是只靠上下文窗口。

## 对我使用 Codex / Claude Code 的启发

这篇论文的图表可以直接迁移到 AI 编程工具使用方式：

- Figure 2 提醒我：不要只写 prompt，要设计任务契约、状态、验证和产物。
- Table 1 提醒我：更多 agent 流程会改变行为，但不一定提高结果。
- Table 3 提醒我：self-evolution 有用，是因为它绑定失败信号和验收门。
- Table 4 提醒我：多 agent 有用时，必须有清楚的父子边界和产物交接。
- Table 6 提醒我：长任务要写状态文件，不能只靠聊天记录。
- Figure 4 提醒我：成本也要评估，不能为了“看起来严谨”无限加 verifier 和候选搜索。

总结成一句话：

> AI agent 的质量不只看模型，而要看 harness 是否把任务、状态、工具、验证和失败恢复组织成一个对齐最终验收的系统。

