# agent-browser 使用指南

## 概述

agent-browser 是一个浏览器自动化 CLI 工具，专为 AI Agent 设计。通过 Chrome/Chromium 的 CDP（Chrome DevTools Protocol）实现网页导航、点击按钮、填写表单、截图等操作，无需编写脚本，直接用自然语言指令控制浏览器。

支持平台：Claude Code、Codex、Hermes。

## 安装状态

| 平台 | 状态 |
|------|------|
| Claude Code | ✅ 已安装 |
| Codex | ✅ 已安装 |
| Hermes | ✅ 已安装 |

## 使用方式

直接用自然语言描述浏览器操作即可，skill 会自动触发：

### 打开网页
```
打开 https://example.com
```

### 填写表单
```
在登录页面输入用户名 admin，密码 123456，然后点击登录
```

### 截图
```
截取当前页面的截图
```

### 点击操作
```
点击页面上的"提交"按钮
```

### 数据抓取
```
从这个页面提取所有商品名称和价格
```

### 测试 Web 应用
```
测试这个登录页面的各种场景
```

## 进阶使用

### Electron 桌面应用自动化
支持自动化控制 VS Code、Slack、Discord、Figma、Notion、Spotify 等 Electron 应用。

### Slack 操作
- 检查 Slack 未读消息
- 发送 Slack 消息
- 搜索 Slack 对话

### 云浏览器
- 支持 Vercel Sandbox microVM 中运行浏览器自动化
- 支持 AWS Bedrock AgentCore 云浏览器

## 技术原理

- 使用 Chrome DevTools Protocol (CDP) 连接浏览器
- 通过 accessibility-tree 获取页面快照
- 使用 `@eN` 格式的元素引用进行精确定位
- 比传统的 CSS selector 方式更可靠

## 与其他浏览器工具的区别

agent-browser 优先于 Claude Code 内置的浏览器自动化工具（如 Playwright MCP），因为它：
- 专为 AI Agent 优化
- accessibility-tree 快照比截图更适合 LLM 理解
- 元素引用更稳定
- 支持 Electron 应用自动化
