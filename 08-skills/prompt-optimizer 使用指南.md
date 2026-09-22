# prompt-optimizer 使用指南

## 概述

prompt-optimizer 是一个提示词优化器，能分析原始提示词、识别意图和缺口，匹配 ECC 生态组件（skills/commands/agents/hooks），输出一个可直接使用的优化提示词。它是一个顾问角色——只优化提示词，不执行任务本身。

支持平台：Claude Code、Codex、Hermes。

## 安装状态

| 平台 | 状态 |
|------|------|
| Claude Code | ✅ 已安装（原始位置） |
| Codex | ✅ 已安装（从 Claude Code 复制） |
| Hermes | ✅ 已安装（从 Claude Code 复制） |

## 触发条件

当用户说出以下内容时自动触发：

### 英文触发词
- "optimize prompt"
- "improve my prompt"
- "how to write a prompt for"
- "help me prompt"
- "rewrite this prompt"

### 中文触发词
- "优化prompt"
- "改进prompt"
- "怎么写prompt"
- "帮我优化这个指令"

### 不会触发的情况
- 用户说"优化代码"、"优化性能" — 这些是重构/性能任务
- 用户说"直接做" / "just do it" — 用户想直接执行，不需要优化

## 使用示例

### 基本用法
```
你：帮我优化这个 prompt："帮我写个登录页面"
```

prompt-optimizer 会：
1. 分析原始提示词的意图和缺口
2. 匹配合适的 ECC 生态组件
3. 输出一个优化后的、可直接粘贴使用的完整提示词

### 优化前 vs 优化后

**优化前**：
```
帮我写个登录页面
```

**优化后**（示例）：
```
使用 /frontend-design 创建一个登录页面：
- 包含用户名/密码输入框
- 包含"记住我"复选框
- 包含登录按钮
- 包含忘记密码链接
- 使用 React + TypeScript
- 支持表单验证
- 移动端响应式
```

## 工作原理

1. **分析意图**：理解用户真正想要什么
2. **识别缺口**：找出原始提示词缺失的关键信息
3. **匹配组件**：从 ECC 生态中找到最合适的 skill/agent/hook
4. **输出优化提示词**：生成一个完整的、可直接执行的提示词

## 最佳实践

- 当你觉得 Claude 的回答不符合预期时，先用 prompt-optimizer 优化你的提示词
- 优化后的提示词包含了更明确的约束、技术栈、输出格式等信息
- 这是一个"顾问"工具——它告诉你怎么写更好的 prompt，但不会替你执行任务
