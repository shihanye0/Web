# Academic Research Skills（ARS）使用指南

> 版本：v3.12.0 | 更新日期：2026-06-10
> GitHub: https://github.com/Imbad0202/academic-research-skills
> 许可证：CC-BY-NC-4.0（非商用）

## 一、概述

ARS 是一套**生产级学术研究 Claude Code 技能包**，涵盖从研究到论文出版的全流程。它不是替你写论文，而是帮你处理繁琐工作：搜文献、排格式、验数据、查逻辑一致性。这样你就能专注在真正需要思考的事上：定义问题、选择方法、解读数据意义。

### 核心理念

> **AI 是你的副驾驶，不是机长。**

与 humanizer 不同，ARS 不是帮你隐藏使用 AI 协作的事实，而是帮你把关文章质量。风格校准会从你过去的文章中学习你的声音，写作质量检查会识别让文字读起来像机器生成的模式。目标是质量，不是掩饰。

### 为什么选「人机协作」而不是「全自动」

Lu 等人（2026，Nature）发表的 The AI Scientist 是第一个端到端全自动 AI 研究系统，其 Limitations 段落列出了结构性失败模式：实现错误、幻觉实验结果、取巧特征依赖、方法论伪造、引用幻觉。ARS 建立在前提上：**人类研究者 + AI 的组合，比纯自动或纯人工更能避开这些失败模式。**

---

## 二、安装与配置

### 当前安装状态

| 项目 | 状态 |
|------|------|
| 安装方式 | Claude Code Plugin |
| 安装路径 | `C:\Users\Lenovo\.claude\plugins\marketplaces\academic-research-skills` |
| 版本 | v3.12.0 |
| Skills | ✅ 4 个全部就绪 |
| Commands | ✅ 14 个 slash 命令 |
| Hooks | ✅ SessionStart + PreToolUse |
| Agents | ✅ 3 个 plugin agent |

### 安装命令（供参考）

```
/plugin marketplace add Imbad0202/academic-research-skills
/plugin install academic-research-skills
```

### 前置条件

- Claude Code（建议最新版）
- 已导出 `ANTHROPIC_API_KEY`
- 可选：Pandoc（DOCX 输出）、tectonic + 思源宋体 TC（APA 7.0 PDF）

---

## 三、四个核心 Skill

### 3.1 Deep Research — 深度研究

| 属性 | 值 |
|------|-----|
| 版本 | v2.9.4 |
| Agent 数量 | 13 |
| 模式数 | 7 |
| 数据访问级别 | raw |

**13 个 Agent 团队**：研究问题制定、苏格拉底导师、方法论设计、系统性文献搜索、来源验证、跨来源综合、偏倚风险评估、元分析、APA 7.0 报告编译、编辑审查、魔鬼代言人挑战、伦理审查、研究后文献监测。

**7 种模式**：

| 模式 | 用途 | 输出 | 时间 |
|------|------|------|------|
| `full` | 完整研究 | APA 7.0 报告，3000-8000 字 | 1-2 小时 |
| `quick` | 快速摘要 | 研究简报，500-1500 字 | 30 分钟 |
| `socratic` | 苏格拉底引导 | 研究计划摘要 + INSIGHT 收集 | 5-15 轮对话 |
| `review` | 论文评估 | 审稿报告 | 30-60 分钟 |
| `lit-review` | 文献回顾 | 带注释的参考文献 + 综合 | 1 小时 |
| `fact-check` | 事实核查 | 逐条验证报告 | 30 分钟 |
| `systematic-review` | 系统性综述 | PRISMA 2020 报告，5000-15000 字 | 2-3 小时 |

**触发词**：研究、深度研究、文献回顾、系统性回顾、事实查核、引导我的研究、research、deep research、literature review、systematic review、fact-check

---

### 3.2 Academic Paper — 学术论文撰写

| 属性 | 值 |
|------|-----|
| 版本 | v3.2.0 |
| Agent 数量 | 12 |
| 模式数 | 10 |
| 数据访问级别 | redacted |

**12 个 Agent 团队**：配置访谈、文献策略师、结构架构师、论证构建师、草稿撰写师、引用合规、双语摘要、同行评审、格式化、苏格拉底导师、可视化、修订教练。

**10 种模式**：

| 模式 | 用途 | 输出 |
|------|------|------|
| `full` | 完整论文撰写 | 完整论文草稿（IMRaD 或学科适当格式） |
| `plan` | 引导式规划 | 章节计划 + INSIGHT 收集（苏格拉底式） |
| `outline-only` | 只做大纲 | 详细大纲 + 证据映射 |
| `revision` | 修订论文 | 修订稿 + 逐点 R&R 回复 |
| `revision-coach` | 修订指导 | 修订路线图 + 回复信骨架 |
| `abstract-only` | 只写摘要 | 双语摘要（中文 + 英文）+ 关键词 |
| `lit-review` | 文献综述论文 | 论文格式的带注释参考文献 |
| `format-convert` | 格式转换 | LaTeX/DOCX/PDF/Markdown |
| `citation-check` | 引用检查 | 引用错误报告 |
| `disclosure` | AI 使用声明 | 特定会议/期刊的 AI 使用声明 |

**支持的引用格式**：APA 7、Chicago、MLA、IEEE、Vancouver

**支持的输出格式**：LaTeX、DOCX（via Pandoc）、PDF、Markdown

**触发词**：写论文、学术论文、论文大纲、写摘要、修改论文、检查引用、转 LaTeX、write paper、academic paper、guide my paper、revise paper

---

### 3.3 Academic Paper Reviewer — 论文审查

| 属性 | 值 |
|------|-----|
| 版本 | v1.10.0 |
| Agent 数量 | 7 |
| 模式数 | 6 |
| 数据访问级别 | verified_only |

**7 个 Agent 团队**：领域分析师、主编（EIC）、方法论审稿人、领域审稿人、视角审稿人、**魔鬼代言人**、编辑综合师。

**6 种模式**：

| 模式 | 用途 | 输出 |
|------|------|------|
| `full` | 全面审查 | 5 份审稿报告 + 编辑决定 + 修订路线图 |
| `re-review` | 修订验收 | 修订验证清单 + 残留问题 |
| `quick` | 快速评估 | 主编快速评估 + 关键问题列表（15 分钟） |
| `methodology-focus` | 方法论聚焦 | 深度方法论审查 |
| `guided` | 引导式改进 | 苏格拉底式逐问题对话 |
| `calibration` | 校准 | 校准报告（FNR/FPR/AUC）+ 置信度披露 |

**触发词**：审查论文、同行评审、稿件审查、review paper、peer review、calibrate reviewer

---

### 3.4 Academic Pipeline — 全流程调度器

| 属性 | 值 |
|------|-----|
| 版本 | v3.12.0 |
| 依赖 | deep-research + academic-paper + academic-paper-reviewer |
| 数据访问级别 | verified_only |

**10 阶段 Pipeline**：

| 阶段 | 名称 | 说明 |
|------|------|------|
| Stage 1 | RESEARCH | 研究探索，确定研究问题和方法论 |
| Stage 2 | WRITE | 论文撰写 |
| Stage 2.5 | INTEGRITY CHECK | 学术诚信验证（100% 引用和数据验证） |
| Stage 3 | REVIEW | 第一轮同行评审 |
| Stage 3' | RE-REVIEW | 修订后再审验收 |
| Stage 4 | REVISE | 根据审稿意见修订 |
| Stage 4.5 | FINAL INTEGRITY | 最终诚信检查 |
| Stage 5 | FINALIZE | 定稿输出 |
| Stage 6 | PROCESS RECORD | 过程记录 + 6 维度协作质量评估 |

**中间进入支持**：
- "我已经有论文，帮我审查" → 从 Stage 2.5 进入
- "我收到审稿意见了" → 从 Stage 4 进入

---

## 四、Slash 命令列表

| 命令 | 用途 | 对应 Skill |
|------|------|-----------|
| `/ars-plan` | 苏格拉底式对话规划章节结构 | academic-paper |
| `/ars-full` | 完整研究 pipeline | academic-pipeline |
| `/ars-lit-review` | 文献回顾 | deep-research |
| `/ars-reviewer` | 论文审查 | academic-paper-reviewer |
| `/ars-revision` | 修订论文 | academic-paper |
| `/ars-revision-coach` | 修订指导 | academic-paper |
| `/ars-outline` | 只做大纲 | academic-paper |
| `/ars-abstract` | 只写摘要 | academic-paper |
| `/ars-citation-check` | 检查引用格式 | academic-paper |
| `/ars-format-convert` | 格式转换 | academic-paper |
| `/ars-disclosure` | 生成 AI 使用声明 | academic-paper |
| `/ars-mark-read` | 标记已读 | 通用 |
| `/ars-unmark-read` | 取消已读标记 | 通用 |
| `/ars-cache-invalidate` | 清除引用验证缓存 | 通用 |

---

## 五、3 个 Plugin Agent

| Agent | 职责 |
|-------|------|
| `report_compiler_agent` | 报告编译 — 将研究结果编译为 APA 7.0 格式报告 |
| `research_architect_agent` | 研究架构设计 — 设计研究方案和方法论蓝图 |
| `synthesis_agent` | 综合分析 — 跨来源综合、交叉论文矛盾清单 |

---

## 六、使用场景与示例

### 场景 1：探索模糊想法（苏格拉底模式）

```
你："我有一个模糊的想法，关于 AI 对高等教育质量保障的影响，
     但不确定怎么框定研究问题。能引导我吗？"
```

AI 会通过 5-15 轮提问帮你理清思路，最终产出研究计划摘要和 INSIGHT 收集。

### 场景 2：快速文献综述

```
你："给我一份 AI 在教育评估中应用的快速摘要"
```

30 分钟内产出 500-1500 字的研究简报。

### 场景 3：从零写论文

```
你："帮我写一篇关于出生率下降对私立大学管理策略影响的论文"
```

触发完整流程：配置访谈 → 文献搜索 → 结构设计 → 论证构建 → 全文撰写 → 引用合规 → 双语摘要 → 同行评审 → 格式输出。

### 场景 4：审查已有论文

```
你："审查这篇论文"（然后粘贴或附上论文）
```

产出 5 份独立审稿报告（主编 + 3 位审稿人 + 魔鬼代言人）+ 编辑决定 + 修订路线图。

### 场景 5：端到端全流程

```
你："我想做一篇关于 agentic AI 如何重塑学生学习成果测量的完整论文"
```

触发 10 阶段 pipeline，预计 API 成本 $4-6，协作时间 2-4 小时。

### 场景 6：收到审稿意见后修订

```
你："我收到审稿意见了，帮我修订"
```

可以先用 `revision-coach` 模式解析审稿意见生成修订路线图，再用 `revision` 模式逐点修订。

---

## 七、环境变量配置

| 变量 | 用途 | 默认值 |
|------|------|--------|
| `ARS_CLAIM_AUDIT` | 启用 L3 主张诚信审计门控 | `0`（关闭） |
| `ARS_PASSPORT_RESET` | 启用 Material Passport 作为上下文重置边界 | `0`（关闭） |
| `ARS_CROSS_MODEL` | 启用跨模型学术诚信验证 | `0`（关闭） |
| `ARS_VERIFICATION_CACHE_PATH` | 引用验证缓存路径 | `~/.cache/ars/verification.db` |

**启用方式**：在 Claude Code 会话前设置环境变量，例如：
```bash
export ARS_CLAIM_AUDIT=1
claude
```

---

## 八、核心亮点功能

### 8.1 学术诚信闸门

7 类阻断式检查清单：
- 虚构引用检测
- 统计错误检测
- 数据伪造检测
- 方法论不一致检测
- 引用忠实度检查（L3 claim-faithfulness）
- 实验来源凭证验证
- 图表保真度验证

### 8.2 四索引引用验证

跨四个学术索引交叉验证引用真实性：
- Semantic Scholar
- OpenAlex
- Crossref
- arXiv

### 8.3 风格校准

提供 3+ 篇你过去的文章，pipeline 会学习你的写作风格：
- 句子节奏
- 词汇偏好
- 引用整合风格

### 8.4 写作质量检查

自动检测 AI 典型的写作问题：
- 过度使用的 AI 术语
- 破折号滥用
- 开场白冗余
- 段落长度均匀
- 句子节奏单调

### 8.5 Material Passport

实验来源凭证系统：
- 记录研究者在外部做过的实验
- 论文主张与实验记录自动对齐
- ALIGNED / OVERSTATED / NOT_SUPPORTED_BY_PROVENANCE 判定

---

## 九、费用估算

| 场景 | 预计费用 |
|------|---------|
| 单次快速摘要（quick mode） | $0.3-0.5 |
| 完整研究（full mode） | $1-2 |
| 论文撰写（full mode） | $2-3 |
| 论文审查（full mode） | $1-2 |
| 完整 pipeline（10 阶段） | $4-6 |

---

## 十、与其他工具的关系

### ARS vs Thesis-Rewrite

| 维度 | ARS | thesis-rewrite |
|------|-----|----------------|
| 定位 | 从零到一的学术研究全流程 | 已有论文的改写/降重/润色 |
| 适用场景 | 研究→撰写→审查→修订 | 论文降重、格式调整、语言润色 |
| 学术诚信 | 内置引用验证、诚信闸门 | 侧重去 AI 化 |

### ARS vs Humanizer-CN

| 维度  | ARS         | humanizer-cn |
| --- | ----------- | ------------ |
| 目标  | 文章质量        | 去除 AI 痕迹     |
| 方法  | 写作质量检查、风格校准 | 句式变化、词汇替换    |

**可以搭配使用**：ARS 产出论文草稿 → humanizer-cn 去 AI 化 → 最终定稿。

---

## 十一、常见问题

### Q: 重启 Claude Code 后命令不生效？

检查插件是否正确注册：
```
cat ~/.claude/plugins/installed_plugins.json | grep academic
```

### Q: 引用验证失败？

检查网络连接，或清除缓存：
```
/ars-cache-invalidate
```

### Q: 可以只用其中一个 Skill 吗？

可以。每个 Skill 都可以独立使用，不需要走完整 pipeline。

### Q: 支持中文论文吗？

支持。双语摘要是默认功能，支持中文论文写作。触发词也支持中文。

### Q: 和 Experiment Agent 的关系？

[Experiment Agent](https://github.com/Imbad0202/experiment-agent) 填补 ARS Stage 1（研究）和 Stage 2（写作）之间的空缺，用于执行代码实验或人工研究。ARS 不执行实验，只处理写作和审查。

---

## 十二、参考链接

- [完整 README（中文）](https://github.com/Imbad0202/academic-research-skills/blob/main/README.zh-CN.md)
- [架构文档](https://github.com/Imbad0202/academic-research-skills/blob/main/docs/ARCHITECTURE.md)
- [安装指南](https://github.com/Imbad0202/academic-research-skills/blob/main/docs/SETUP.md)
- [性能与费用](https://github.com/Imbad0202/academic-research-skills/blob/main/docs/PERFORMANCE.md)
- [Pipeline 产出展示](https://github.com/Imbad0202/academic-research-skills/tree/main/examples/showcase)
- [Experiment Agent](https://github.com/Imbad0202/experiment-agent)
