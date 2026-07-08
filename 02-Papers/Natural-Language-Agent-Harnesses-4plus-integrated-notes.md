# Natural-Language Agent Harnesses 整合阅读笔记

来源：

- 论文：`/home/user/Downloads/paper/Natural-Language Agent Harnesses-dual.pdf`
- 已读笔记：`/home/user/Web/02-Papers/Natural-Language Agent Harnesses-.md`

## 一句话主线

这篇论文不是在证明“自然语言 harness 一定比代码 harness 更强”，而是在证明：**harness 可以被从代码胶水中抽出来，变成可读、可执行、可迁移、可消融的研究对象**。第 4 节之后的结果也很克制：NLAH/IHR 会真实改变 agent 行为，但更多结构不必然带来更高分，关键是中间控制结构是否对齐最终评估器的验收目标。

## 你前面笔记的重点保留

### 1. Harness 是比 Prompt / Context 更高一层的对象

- **Prompt Engineering**：设计一次模型调用的指令文本。
- **Context Engineering**：组织一次模型调用可见的上下文、检索材料、工具返回和历史信息。
- **Harness Engineering**：控制整个任务生命周期，包括多步推理、工具调用、状态持久化、验证门控、子任务委派、错误恢复和终止条件。

重点理解：论文把 harness 从“辅助代码/胶水逻辑”提升为一等系统对象。它不是 prompt 模板，也不只是上下文窗口管理，而是 agent 如何持续运行的控制层。

### 2. NLAH / IHR 的核心分工

- **NLAH（Natural-Language Agent Harness）**：用自然语言表达任务族级控制逻辑，例如角色、阶段、契约、状态语义、验证规则和失败恢复策略。
- **IHR（Intelligent Harness Runtime）**：共享执行引擎，负责解释并执行 NLAH，提供统一的状态、工具、子 agent、产物和审计语义。
- **运行时宪章 Runtime Charter**：所有 harness 共用的底层执行纪律。
- **Harness Skill**：基准或任务族专属的控制逻辑。

重点理解：作者想分离“怎么控制 agent”和“在哪个底座上执行”。NLAH 是可迁移的路线图，IHR 是统一执行底座。

### 3. 论文三个 RQ 的逻辑

- **RQ1：行为效应**  
  共享运行时和 harness 逻辑是否真的改变 agent 行为？

- **RQ2：模块组合/消融**  
  显式化后的 harness pattern 能否像模块一样添加、移除和比较？

- **RQ3：代码到文本迁移**  
  传统代码 harness 能否迁移成 NLAH，并保持任务级等价或可比较行为？

这三个问题构成递进：先证明 harness 不是装饰，再证明它可拆解，最后证明自然语言表示能承载原本代码中的高层控制逻辑。

## 第 4 节 Results 之后的新增重点

## 4.1 RQ1：NLAH/IHR 的主要证据是“行为改变”，不是“单调涨分”

### 核心结果

在 SWE-bench Verified 上，Full IHR 相比消融版本显著改变过程指标：

| Harness | Setting | Perf. | Prompt Tokens | Tool Calls | LLM Calls | Runtime |
|---|---:|---:|---:|---:|---:|---:|
| TRAE | Full IHR | 74.4 | 16.3M | 642.6 | 414.3 | 32.5 min |
| TRAE | w/o RTS | 76.0 | 11.1M | 451.9 | 260.5 | 16.6 min |
| TRAE | w/o HS | 75.2 | 1.2M | 51.1 | 34.0 | 6.7 min |
| Live-SWE | Full IHR | 72.8 | 1.4M | 58.4 | 41.4 | 7.6 min |
| Live-SWE | w/o RTS | 76.0 | 1.1M | 41.0 | 28.2 | 5.5 min |
| Live-SWE | w/o HS | 75.2 | 1.2M | 51.1 | 34.0 | 6.7 min |

作者的解读很重要：**性能分数变化不大，甚至 Full IHR 不一定最高；但 token、工具调用、LLM 调用、运行时间和轨迹结构都明显变化。** 所以 RQ1 支持的是“harness 是真实控制变量”，不是“Full IHR 总是更强”。

### 配对翻转说明

在 125 个 SWE 样本中，多数样本不翻转：Full IHR 与消融设置在 110 个以上样本上结果一致。真正有信息量的是少数边界样本：

- 有些样本只有 Full IHR 解出。
- 有些样本反而只有轻量消融解出。
- 说明 Full IHR 更像“已解决集合替换器”，不是统一扩展 frontier 的方法。

### 你要重点记住的判断

**结构化 harness 会改变搜索路径和局部成功信号，但这些信号未必对齐官方 evaluator。**

例子：

- `matplotlib__matplotlib-24570`：TRAE Full 做了大量候选搜索、选择、再验证，但最终补丁仍没过官方评估器。
- `django__django-14404`、`sympy__sympy-23950`、`django__django-13406`：额外结构让过程更有组织，但偏离最短的基准对齐修复路径或最终验收对象。

结论：harness 不是无效装饰，它确实改变行为；但行为改变是否有益，取决于它是否贴近任务验收机制。

## 4.2 RQ2：模块消融的结论是“结构要对齐”，不是“结构越多越好”

RQ2 从 Basic 起点逐个添加模块：

- file-backed state
- evidence-backed answering
- verifier stage
- self-evolution
- multi-candidate search
- dynamic orchestration

### 主要结果表

| Benchmark | Basic | File-backed State | Evidence-backed | Verifier | Self-evolution | Multi-candidate | Dynamic orchestration |
|---|---:|---:|---:|---:|---:|---:|---:|
| SWE Verified | 75.2 | 76.8 | 76.8 | 74.4 | 80.0 | 72.8 | 75.2 |
| OSWorld | 41.7 | 47.2 | 41.7 | 33.3 | 44.4 | 36.1 | 44.4 |

### 模块分成两类

**第一类：直接收紧求解循环，可能提高最终分数**

- self-evolution 是最清晰的正向模块。
- 它的价值不是无限反思，而是让 agent 围绕明确验收门做尝试、失败分析和下一次尝试。
- 在 SWE 上从 75.2 提到 80.0，是最明显的提升。

**第二类：提高过程结构、审计性和交接质量，但不一定提高语义修复能力**

- file-backed state：让状态、交接、子任务产物外部化、路径可寻址。
- evidence-backed answering：要求最终结论前有独立 evidence artifact。
- 这些模块改善可审计性、handoff discipline、trace quality，但分数提升通常温和。

### 负向或混合模块

- verifier：有独立检查价值，但如果 verifier 的局部验收目标和 benchmark evaluator 不一致，会产生“局部通过、官方失败”。
- multi-candidate search：让搜索更可见，但当前预算下开销重，对基础设施敏感，未转化成更好结果。
- dynamic orchestration：会改变哪些样本被解出，但整体更像 solved-set replacer。

### RQ2 的核心读法

不要把 RQ2 看成模块排行榜，而要看成：**不同 harness 模块如何改变困难边界样本的可恢复性，以及中间控制结构是否对齐最终 evaluator。**

这点和你平时做 agent/skill/AGENTS.md 规则很相关：加更多流程、更多 verifier、更多候选分支，并不自动等于更强。关键是这些流程是不是收紧了真实验收链路。

## 4.3 RQ3：代码到文本迁移的关键是可靠性机制迁移

RQ3 比较 OS-Symphony 的原生代码 harness 与迁移后的 NLAH 版本。

| Benchmark | Harness | Realization | Perf. | Prompt Tokens | Tool Calls | LLM Calls | Runtime |
|---|---|---|---:|---:|---:|---:|---:|
| OSWorld | OS-Symphony | Code | 30.4 | 11.4M | 651 | 1.2k | 361.5 min |
| OSWorld | OS-Symphony | NLAH | 47.2 | 15.7M | 683 | 34 | 140.8 min |

作者强调：目标不是复现完全相同内部轨迹，而是实现任务级等价，包括可比较的逻辑、契约和面向 benchmark 的产物。

### 迁移后行为发生了什么变化

原生 OS-Symphony 更像：

- 看截图
- 判断当前屏幕
- 选择 GUI 动作
- 遇到焦点/选择问题就局部修复

NLAH/IHR 版本更像：

- 生成任务文件、ledger、artifact
- 使用 file-backed state
- 使用 artifact-backed verification
- 当 shell、文件或 package-level 操作能提供更强完成证据时，从脆弱 GUI 修复转向这些确定性操作

### 关键结论

RQ3 不是说自然语言比代码更会操作 GUI，而是说：**迁移把可靠性机制从本地屏幕修复，转移到了持久运行时状态和基于产物的闭环验证。**

这解释了为什么 NLAH 版本在 OSWorld 上没有因为“自然语言不精确”而崩掉，反而取得了更好结果。

## 5 Discussion：作者的立场很克制

### 代码与自然语言不是替代关系

作者明确说：不是用自然语言替代代码。

- 自然语言负责高层 harness 逻辑：角色、契约、阶段、验证、状态、委派。
- 代码负责确定性操作：工具接口、脚本、沙箱、文件操作、系统调用。

真正的科学主张是：比较对象应该从“整套混杂代码系统”变成“共享运行时下的可执行 harness 表示”。

### 为什么自然语言仍然重要

即使模型更强，复杂 prompt engineering 的收益可能下降，但自然语言仍适合表达 harness-level control：

- roles
- contracts
- verification gates
- durable state semantics
- delegation boundaries

这和你前面笔记中的“自然语言从说明书变成机器可执行构件”一致。

### Harness 表示可以成为搜索空间

一旦 harness 是显式对象，它就可以被：

- 手动设计
- 检索
- 迁移
- 重组
- 消融
- 自动搜索/优化

这是论文后续愿景：从 harness engineering 走向 harness representation science。

## 6 Related Work：论文把自己放在哪里

### 与 LLM programming / prompt-as-program 的区别

LMQL、DSPy、APPL、SGLang 等关注 prompt、pipeline、structured LM programs。

本文关注的是更外层的 harness layer：

- 多步 agent call
- artifact contracts
- delegation
- verification
- durable state

### 与 agent orchestration 的区别

ReAct、RAG、reflection、多智能体路由等是控制模式或算法。

本文不提出新的 orchestration algorithm，而是把已有 harness pattern 变成共享运行时下的可执行表示。

### 与 AGENTS.md / skills 的关系

AGENTS.md、AgentSkills、skill bundles 已经证明文本可以携带可复用操作知识。

本文进一步推进：从“可复用局部指导”扩展到“可执行 harness-level control”。

## Limitations / Risks：这部分很重要

### 技术局限

- 自然语言不如代码精确。
- 有些机制无法从文本忠实恢复，尤其依赖隐藏服务端状态、专有 scheduler、训练诱导行为时。
- Runtime contamination：强共享运行时可能吸收本应归因于 harness 文本的行为。
- 模块级消融不是严格因果识别，因为文本表示会引入指令显著性、prompt 长度等混淆。

### 安全风险

可移植 harness 会降低复用成本，也可能降低传播危险工作流的门槛。

风险面包括：

- prompt injection
- malicious tool grafting
- supply-chain contamination
- 工具使用、产物处理、委派链路上的新攻击面

作者建议部署时结合 provenance tracking、review、permission control、sandbox isolation。

## 附录补充：对理解结果最有用的部分

### Appendix A：从 model call 到 agent call

论文把普通模型调用提升为 agent call：

- 任务不仅是 prompt，还包括输入文件/资源和执行契约。
- 执行契约包含输出要求、预算、权限、完成条件、指定输出路径。
- agent call 会产生 artifact set、环境修改和规范化最终响应。

重点：这为“agent call 是一等执行单元”提供形式化表达。

### Appendix B：file-backed state 的规范工作区

file-backed state 把跨步骤状态放进规范工作区：

- `TASK.md`：任务说明
- `harness-skill/SKILL.md`：任务族控制逻辑
- `state/task_history.jsonl`：子任务和状态提升历史
- `children/*/TASK.md`、`children/*/RESPONSE.md`：子 agent 任务包和返回
- `artifacts/`：最终可评判产物
- `RESPONSE.md`：规范化结果和产物指针

重点：状态不是靠上下文窗口“记住”，而是通过文件路径成为可恢复、可审计对象。

### Appendix C：共享运行时技能的五个规则

1. 父 agent 只做 runtime orchestration，实质工作交给 child agent。
2. 没有 harness skill 时，先构造最薄可运行基线，再叠加额外 skill。
3. 从 skill 文本恢复调用图、角色、阶段、循环和上下文继承语义。
4. 分离 runtime state 与最终 artifacts。
5. 以 contract-first completion 和可审计性为完成纪律。

重点：IHR 移除的不是“几句 prompt”，而是一整层编排、上下文、产物和报告纪律。

### Appendix D/E：RQ1/RQ2 的案例教训

代表性结论：

- 适度委派拓扑可能帮助边界样本。
- 过重候选搜索可能 overshoot。
- 有些代码修复更适合最短直接路径，额外流程会增加摩擦。
- verifier 有价值的前提是本地验收目标接近官方 evaluator。
- self-evolution 的正向模式是：明确尝试契约 + 真实失败信号 + 贴近 benchmark gate，而不是盲目扩大搜索树。

### Appendix F：RQ2 模块行为速记

- **file-backed state**：状态根目录、子任务包、历史和 manifest 都文件化。
- **evidence-backed answering**：最终答案/补丁前必须有 evidence artifact，关键 claim 要有来源。
- **verifier separation**：verifier 只检查候选，不替候选修复。
- **self-evolution**：真实 baseline attempt 起步，失败后基于信号重设 prompt/tool/workflow，最多若干轮。
- **multi-candidate search**：显式候选预算、多样化、去重、比较和扩展。
- **dynamic orchestration**：只在委派能改善覆盖、延迟、专业性或质量控制时增加子 agent，并要求职责不重叠。

## 这篇论文你现在最该抓的重点

1. **不要把 NLAH 理解成“用自然语言写代码”。**  
   它表达的是高层控制逻辑；确定性操作仍应由代码、工具和沙箱完成。

2. **第 4 节结果的核心不是 SOTA，而是可研究性。**  
   NLAH/IHR 让 harness 成为可执行、可比较、可消融对象。

3. **更多结构不是自动更好。**  
   verifier、多候选、多 agent、证据门控都可能让过程更漂亮，但如果验收对象错了，会偏离最终目标。

4. **file-backed state 是贯穿全文的关键机制。**  
   它把长任务中的状态、委派、证据和产物从上下文窗口里拿出来，变成路径可寻址的稳定对象。

5. **self-evolution 的价值不是“反思”这个词，而是验收门驱动的尝试循环。**  
   它有效时，是因为它把失败信号、下一轮策略和最终 benchmark gate 对齐了。

6. **代码到文本迁移的可靠性来自 artifact-backed closure。**  
   迁移成功不是因为自然语言更精确，而是因为 IHR 把状态和验收证据组织得更稳定。

## 推荐你接下来阅读的顺序

1. 先重读 4.1 的最后两段：理解“行为改变但非单调增益”。
2. 再读 Table 3 和 4.2：建立模块效果直觉。
3. 接着读 4.3：抓住“GUI 修复 -> 文件/产物验证”的迁移机制。
4. 最后读 Limitations：防止把论文理解成过度乐观的“自然语言替代代码”。
5. 附录只重点看 A/B/C/F；D/E 当案例辅助理解即可。

## 我的判断

这篇论文真正有价值的地方，不是某个 benchmark 数字，而是把你熟悉的 `AGENTS.md`、skill、子 agent、状态文件、验证门控这些实践，抽象成一个可实验的研究对象。它也给了一个很实用的警告：agent 系统设计中，流程结构的价值必须由最终验收链路来定义；否则越结构化，越可能只是更有条理地走偏。
