# Zotero 插件清单

本机 Zotero 已装 9 个插件（2026-09-13 从 profile 的 extensions.json 核实，全部启用中）。

## 一览表

| 插件 | 版本 | 干什么 | 何时用 |
| --- | --- | --- | --- |
| Better BibTeX | 9.0.64 | 引用键生成、自动导出 .bib/.json | LaTeX/论文写作时的引用管线核心 |
| Translate for Zotero | 2.4.7 | 阅读器内划词翻译、术语库 | 精读英文文献时随手划词 |
| Better Notes | 3.3.3 | 文献笔记系统、模板 | 用 [[VLA科研工具与论文阅读工作流]] 第 5 节模板建结构化笔记 |
| Actions & Tags | 2.6.1 | 按规则自动打标签/移动 | 自动维护 /status、/importance 标签体系（见 VLA 笔记第 4 节） |
| Linter (format-metadata) | 4.0.1 | 条目元数据规范化 | 导入的条目字段乱时一键整理 |
| Ethereal Style | 6.0.8 | 期刊标签、影响因子、跨库跳转 | 粗筛时快速看期刊档次 |
| Scite | 2.0.5 | 引用支持/争议标记 | 判断一篇论文被支持还是被质疑 |
| Jasminum（茉莉花） | 1.1.38 | 中文文献/CNKI 元数据抓取 | 中文论文、学位论文入库 |
| Add-on Market | 10.0.1 | 插件市场 | 在 Zotero 内搜索安装新插件（如 zotero-pdf2zh） |

## 使用要点

- **粗筛阶段**：新条目进 00_Inbox → Ethereal Style 看期刊 → Actions & Tags 自动补标签
- **精读阶段**：Translate for Zotero 划词 + Better Notes 按模板记笔记
- **写作阶段**：Better BibTeX 引用键 + 自动导出，LaTeX 里 `\cite` 直接用
- **中文文献**：Jasminum 负责抓取 CNKI 元数据，别手动填

## 搭配

- 需要**整篇双语对照 PDF** 时：插件市场装 `zotero-pdf2zh`，或直接命令行 [[pdf2zh]]
- 文献 PDF 想进本地知识库问答 → [[AnythingLLM]]
- 插件从"Add-on Market"或 [Zotero 中文社区](https://zotero-chinese.com/plugins/) 安装更新

## 注意

- 插件数量控制：按上表够用，别再堆——插件互相抢阅读器右键菜单反而降效
- Zotero 大版本升级后先确认插件兼容再更新插件
