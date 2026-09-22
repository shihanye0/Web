# VLA 科研工具与论文阅读工作流

> 目标：把“翻译 PDF”升级为“建立可追溯的研究理解、证据与想法”。
>
> 适用方向：VLA、robot learning、adversarial attack、robustness，尤其是 **semantic-preserving instruction attack**。

---

## 1. 两个已配置的论文工具

当前本机工具目录：`E:\论文\科研AI工具`

| 工具 | 它解决什么 | 适合何时使用 | 不负责什么 |
| --- | --- | --- | --- |
| PaperQA2 | 在一组论文中检索证据、综合回答、发现矛盾，并给出原文引用 | 多篇论文比较、找方法共同点、追踪一项主张 | 不能代替回看原文，也不是免费的离线聊天 |
| MinerU | 将复杂 PDF / Office 文档解析成结构化 Markdown、JSON、公式和表格 | 双栏 PDF、扫描件、公式/表格多、准备自建知识库 | 不生成研究结论，不判断论文是否可信 |

> **2026-09-13 更新**：本机新增一批经实际验收的工具，完整清单与搭配见 [[工具总览与高效搭配]]。与本文工作流直接相关的：[[pdf2zh]]（整篇论文双语对照翻译，保留公式排版）、[[Umi-OCR]]（扫描件转可搜索 PDF）、[[AnythingLLM]]（本地零成本知识库问答，与 PaperQA2 互补）、[[whisper-ctranslate2]]（组会录音转写）、[[Zotero 插件清单]]（本机 9 个插件核实）。

### PaperQA2：多论文证据问答

已安装版本：`paper-qa 2026.8.12`。它能处理 PDF、TXT、Markdown、HTML、DOCX、XLSX、PPTX 和常见代码文件。

1. 把一批需要共同研究的论文放到：`E:\论文\科研AI工具\PaperQA2\papers`
2. 在 PowerShell 中执行：

```powershell
Set-Location 'E:\论文\科研AI工具'
$env:OPENAI_API_KEY = '你的 API Key'
.\Start-PaperQA.ps1 '这些论文中，有多少方法在 language instruction 层实施攻击？'
```

3. 首次提问会建立索引；以后会复用索引。索引、缓存和回答历史保存在 `PaperQA2\.pqa`。

推荐从低成本模式开始：

```powershell
.\Start-PaperQA.ps1 '找出保持任务语义不变但导致 policy action 改变的方法。' -Settings fast
```

对关键结论再使用更高证据密度的模式：

```powershell
.\Start-PaperQA.ps1 '逐条比较这些方法的攻击位置、语义约束与 action 变化证据。' -Settings high_quality
```

用于检查一项主张有没有反例或矛盾：

```powershell
.\Start-PaperQA.ps1 '这些方法都只攻击视觉输入，不修改 language instruction。' -Settings contracrow
```

注意：PaperQA2 的答案会调用 LLM/embedding 服务并可能产生 API 费用；不要把 key 写进脚本、笔记或论文目录。任何影响研究结论的回答，都要打开其引用页人工核对。

### MinerU：把文档变成可用结构

已安装版本：`MinerU 3.4.5`。本机是 4 GB 显存 RTX 3050，默认使用官方兼容性更好的 `pipeline` 后端。

1. 把待解析文件放到：`E:\论文\科研AI工具\MinerU\input`
2. 执行：

```powershell
Set-Location 'E:\论文\科研AI工具'
.\Convert-With-MinerU.ps1 '.\MinerU\input\paper_01.pdf'
```

也可直接解析整个目录：

```powershell
.\Convert-With-MinerU.ps1 '.\MinerU\input'
```

输出会保存在 `MinerU\output`。首次真实解析会下载模型，需预留约 20 GB 磁盘空间。先检查输出的 Markdown、公式、表格和图片是否正确；确认后，将该文献的 **Markdown 或原始 PDF 二选一** 放入 PaperQA2 的 `papers` 目录，避免同一篇论文被重复索引、放大其证据权重。

不要在这台机器上直接切换至 `vlm-engine` 或 `hybrid-engine`，它们更适合显存与内存更充足的环境。

---

## 2. 推荐的研究工作流

```text
论文发现 / 下载
        ↓
Zotero：00_Inbox + /status/unread
        ↓
复杂 PDF？──是──→ MinerU 解析 → 检查 Markdown / 表格 / 公式
        │ 否
        ▼
ChatGPT 深读清单 → 单篇论文结构化笔记
        ↓
PaperQA2：多文献证据检索、比较和矛盾检测
        ↓
人工回看引用页 → 形成综述观点、攻击假设、实验设计
```

原则：**原始 PDF 是证据源，Zotero 是文献库，MinerU 是结构化解析器，PaperQA2 是跨论文证据助手，ChatGPT 是研究对话伙伴。** 没有任何一个工具能跳过“人工核对引用原文”这一步。

2026-09 起新增两个分工位：**[[pdf2zh]] 负责整篇双语翻译**（译文给人读，不喂给检索）——精读重要文献时先转对照版；**[[AnythingLLM]] 负责本地零成本速查**——已读文献的高频小问题、隐私文档，不必动用 PaperQA2 的付费额度。两者的回答与翻译同样属于“待核对材料”，关键结论仍回原文。

---

## 3. ChatGPT 单篇论文深读清单

打开论文后，不要只问“帮我总结”。按以下顺序提问：

```markdown
1. 这篇论文究竟解决什么问题？

2. 以前的方法为什么解决不了？

3. 它的核心 idea 是什么？

4. 方法输入、输出分别是什么？

5. 训练数据是什么？

6. loss 是什么？

7. inference 流程是什么？

8. baseline 有哪些？

9. ablation 说明了什么？

10. 它有哪些明显漏洞？

11. 如果从 adversarial attack / robustness 角度攻击它，
    哪些 assumptions 最脆弱？

12. 它和我正在研究的 semantic-preserving instruction attack 有什么关系？
```

建议追问格式：要求回答中区分“论文直接证据”“合理推断”“尚未证明的假设”，并标出页码、图表或章节。这样阅读的目标从翻译英文变成理解研究。

---

## 4. Zotero 文献库结构

```text
00_Inbox

01_VLA
├── Foundation Models
├── OpenVLA
├── π0 / π0.5
├── RT
└── GR00T

02_VLA_Attack
├── Instruction Attack
├── Visual Attack
├── Semantic-Preserving
├── Prompt Sensitivity
└── Adversarial Robustness

03_Robot_Learning
├── Imitation Learning
├── Diffusion Policy
├── ACT
└── Manipulation

04_Safety_Robustness

05_To_Read

06_Core_Papers
```

使用约定：新论文先进 `00_Inbox`；完成粗筛后归档到主题集合；真正决定问题、方法或实验设计的论文，再进入 `06_Core_Papers`。不要用文件夹同时表达状态、重要性和主题，状态与重要性应交给标签。

### 统一标签

```text
/status/unread
/status/reading
/status/read

/importance/core
/importance/important

/type/survey
/type/method
/type/benchmark
/type/attack

/idea/reproduce
/idea/attack
/idea/follow-up
```

一篇论文可同时属于多个主题集合，但建议每类标签只选一个：一个阅读状态、一个重要性等级、一个或多个类型/想法标签。

---

## 5. 每篇核心论文的笔记模板

```markdown
# 论文标题

## 一句话结论
- 它解决：
- 它最重要的结论：

## 问题与缺口
- 以前方法的限制：
- 本文假设：

## 方法
- 输入：
- 输出：
- 核心模块：
- 训练数据：
- Loss：
- Inference：

## 实验
- Baselines：
- 关键指标：
- Ablation：
- 直接证据（页码/图表）：

## 局限与攻击面
- 明确局限：
- 潜在脆弱假设：
- 可能的 adversarial attack：
- 是否满足 semantic-preserving：

## 与我的研究的关系
- 可复现：
- 可攻击：
- 可扩展：
- 下一步实验：
```

---

## 6. 每周最小闭环

1. 把新论文放进 Zotero `00_Inbox` 并标 `/status/unread`。
2. 用标题、摘要和图 1 做 5 分钟粗筛：是否与 VLA attack / robustness 有直接关系？
3. 对入选论文走“12 个问题”清单，生成一份结构化笔记。
4. 每累计 5–10 篇相关论文，放入 PaperQA2 做一次比较问题，而不是逐篇重复总结。
5. 从答案中挑 1–3 条最重要主张，回到原文引用页核验。
6. 每周至少沉淀一个 `/idea/attack` 或 `/idea/follow-up`，写清楚威胁模型、语义保持约束、预期 action 变化和评估指标。

---

## 7. 后续值得配置的 Zotero 自动化

**2026-09-13 核实：以下两项均已安装并启用**（连同其余 7 个插件本机共 9 个，完整清单见 [[Zotero 插件清单]]）：

- **Actions & Tags**（v2.6.1）：自动根据集合、导入路径或规则补阅读状态/主题标签——把第 4 节的标签体系配成规则即可生效。
- **Better Notes**（v3.3.3）：用统一模板创建文献笔记并链接回条目——直接套用第 5 节模板。

插件不是重点。重点是让“导入 → 分类 → 深读 → 证据核对 → 想法沉淀”成为固定习惯；那时 Zotero 才会成为 VLA 研究数据库、阅读器、知识库和写作引用库。

---

## 参考入口

- PaperQA2：<https://github.com/Future-House/paper-qa>
- MinerU：<https://github.com/opendatalab/MinerU>
- pdf2zh：<https://github.com/PDFMathTranslate/PDFMathTranslate>
- Umi-OCR：<https://github.com/hiroi-sora/Umi-OCR>
- AnythingLLM：<https://github.com/Mintplex-Labs/anything-llm>
- whisper-ctranslate2：<https://github.com/absadiki/whisper-ctranslate2>
- 本机工具详细说明：`E:\论文\科研AI工具\README.md`
- 本机工具笔记索引：[[工具总览与高效搭配]]
