# 知识库使用指南

> 基于 Karpathy "第二大脑" 理念搭建的 AI 驱动知识管理系统。

---

## 核心理念

**知识复利**：每条新信息不是一次性消耗品，而是永久资产。AI 自动帮你提取概念、建立关联，越用越聪明。

## 目录结构

| 文件夹 | 用途 |
|--------|------|
| 00-Inbox | 所有新内容先丢这里，AI 自动处理 |
| 01-Projects | 进行中的项目（论文、课程等） |
| 02-Papers | 论文阅读笔记和引用管理 |
| 03-Knowledge | 概念/知识笔记（核心，AI 自动维护） |
| 04-Thesis | 毕业论文相关资料 |
| 05-Code | 代码片段和技术笔记 |
| 06-Daily | 每日日记和工作日志 |
| 07-Templates | 笔记模板（概念笔记、来源笔记等） |
| 08-Attachments | 图片、PDF 等附件 |
| 09-Archive | 已完成归档 |

## 工作流

### 日常使用

1. **丢材料** → 在 `00-Inbox` 创建笔记，粘贴内容
2. **告诉 Claude** → "处理 Inbox" 或 "把这条加入知识库"
3. **Claude 自动处理** → 提取概念 → 创建/更新笔记 → 更新索引
4. **你 review** → 检查新创建的笔记，补充个人理解

### 快捷命令

| 你说 | Claude 做 |
|------|----------|
| "处理 Inbox" | 扫描并处理所有未处理内容 |
| "把这条加入知识库" | 处理当前对话中的内容 |
| "更新索引" | 重建 INDEX.md |
| "整理概念 X" | 深入扩展某个概念 |
| "搜索关于 Y 的笔记" | 在知识库中检索 |

## 关键文件

- **`cloud.md`** — 增量处理规则（Claude 的操作手册）
- **`INDEX.md`** — 全局概念索引（自动维护）
- **`07-Templates/`** — 笔记模板（concept-note.md, source-note.md）

## 已安装的 AI 能力

| 组件 | 作用 |
|------|------|
| Smart Connections | 语义检索（本地嵌入模型 bge-micro-v2） |
| Real Claudian | Claude 直接在 Obsidian 中对话 |
| MCP Tools | Claude Code ↔ Obsidian 桥接 |
| Claude Skills | obsidian-cli, obsidian-markdown 等 |

## 笔记生命周期

```
seed → growing → mature → evergreen
```

- **seed**：刚创建，内容单薄
- **growing**：3+ 条来源关联
- **mature**：5+ 条关联 + 内容完整
- **evergreen**：核心概念，手动标记

---

*Last updated: 2026-06-01*
