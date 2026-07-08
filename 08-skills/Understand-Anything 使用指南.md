# Understand-Anything 使用指南

## 概述

Understand-Anything 是一个代码仓库知识图谱工具，能将任意代码库、知识库、文档转化为交互式知识图谱，支持节点依赖路径查找、引导式架构学习、模糊搜索等功能。

支持平台：Claude Code、Codex、Hermes、Cursor、Copilot、Gemini CLI 等。

- GitHub: https://github.com/Lum1104/Understand-Anything
- Stars: 45.9k
- License: MIT

## 安装状态

| 平台 | 安装路径 |
|------|----------|
| Claude Code | `~/.claude/plugins/known_marketplaces.json` 注册 |
| Codex | `~/.codex/skills/understand-anything/` → 符号链接 |
| Hermes | `~/.hermes/skills/understand-anything/` → 符号链接 |

仓库位置：`~/.understand-anything/repo/`

## 核心命令

### 分析代码库
```
/understand
```
多 Agent 管线扫描项目，提取所有文件、函数、类和依赖关系，生成知识图谱保存到 `.understand-anything/knowledge-graph.json`。

### 中文输出
```
/understand --language zh
```
支持语言：en（默认）、zh、zh-TW、ja、ko、ru

### 查看交互式图谱面板
```
/understand-dashboard
```
打开 Web 面板，可平移、缩放、搜索、点击节点查看详情。

### 提问代码库
```
/understand-chat 支付流程是怎么工作的？
```

### 分析变更影响
```
/understand-diff
```
查看当前修改影响了系统的哪些部分。

### 深入查看某个文件
```
/understand-explain src/auth/login.ts
```

### 生成新人入职指南
```
/understand-onboard
```

### 提取业务领域知识
```
/understand-domain
```

### 分析知识库（Karpathy 模式 wiki）
```
/understand-knowledge ~/path/to/wiki
```

### 增量更新（默认只分析变更文件）
```
/understand
```

### 自动更新（每次 commit 自动更新图谱）
```
/understand --auto-update
```

### 限定子目录（大型 monorepo）
```
/understand src/frontend
```

## 技术架构

### Tree-sitter + LLM 混合方案

- **Tree-sitter（确定性）**：解析源码为具体语法树，提取结构性事实（导入、导出、函数/类定义、调用点、继承）。相同输入 → 相同输出。
- **LLM（语义性）**：读取解析结构和原始源码，生成解析器无法产出的内容：英文摘要、标签、架构层分配、业务领域映射、引导式学习。

### 多 Agent 管线

| Agent | 角色 |
|-------|------|
| `project-scanner` | 发现文件，检测语言和框架 |
| `file-analyzer` | 提取函数、类、导入；生成图节点和边 |
| `architecture-analyzer` | 识别架构层 |
| `tour-builder` | 生成引导式学习路径 |
| `graph-reviewer` | 验证图谱完整性和引用完整性 |
| `domain-analyzer` | 提取业务领域、流程和步骤 |
| `article-analyzer` | 从 wiki 提取实体、声明和隐含关系 |

文件分析器并行运行（最多 5 个并发，每批 20-30 个文件）。支持增量更新。

## 输出文件

图谱保存在 `.understand-anything/` 目录下：
- `knowledge-graph.json` — 主图谱文件
- `intermediate/` — 中间产物（不需要提交）
- `diff-overlay.json` — diff 分析覆盖（不需要提交）

## 适用场景

- 新人入职大型代码库
- PR 审查前了解影响范围
- 架构文档自动生成
- 业务领域知识提取
- 团队知识共享（提交图谱到 git）
