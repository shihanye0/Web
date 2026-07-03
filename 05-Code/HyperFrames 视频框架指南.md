# HyperFrames 使用指南

## 概述

HyperFrames 是由 HeyGen（AI 视频头部玩家）开发的开源视频渲染框架，可将 HTML、CSS、JS 转化为 MP4 视频，支持多种动画类型，适合批量短视频生成。

- GitHub: https://github.com/heygen-com/hyperframes
- Stars: 22.6k

## 注意

HyperFrames 是一个**独立的 Node.js 框架**，不是 Claude Code/Codex/Hermes 的 skill 或 MCP。需要单独安装使用。

## 核心理念

用 HTML 写视频。你写 Web 风格的组合（composition），加上动画，然后渲染为生产级 MP4 视频。不需要时间线编辑器，不需要 After Effects。

## 安装

```bash
npm install hyperframes
# 或
pnpm add hyperframes
```

## 基本用法

1. 用 HTML/CSS/JS 编写视频组合
2. 定义动画时间线
3. 使用 HyperFrames 渲染为 MP4

## 适用场景

- 批量短视频生成
- 产品演示视频
- 社交媒体内容
- AI Agent 自动生成视频
- 数据可视化动画

## 技术特点

- HTML/CSS/JS → MP4 确定性渲染
- 支持 GSAP 动画
- 支持 `<video>` 标签嵌入
- 单命令渲染
- 可在 Agent 管线中使用
