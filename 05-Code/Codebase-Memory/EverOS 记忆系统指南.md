# EverOS 使用指南

## 概述

EverOS 是由 EverMind 团队（盛大集团孵化）开发的 AI 智能体开源长期记忆操作系统。核心组件 EverCore 受脑启发，采用四层架构，解决 AI 超出上下文窗口就失忆的问题。超图记忆架构入选 ACL 2026。

- GitHub: https://github.com/EverMind-AI/EverOS
- Stars: 6.3k
- 官网: https://evermind.ai/everos

## 注意

EverOS 是一个**独立的 Python 框架**，不是 Claude Code/Codex/Hermes 的 skill 或 MCP。需要单独部署使用。

## 项目结构

```
methods/EverCore/         — 长期记忆操作系统
methods/HyperMem/         — 超图分层记忆架构
benchmarks/EverMemBench/  — 记忆质量评估
benchmarks/EvoAgentBench/ — Agent 自进化评估
use-cases/                — 基于记忆层的应用和 demo
```

## 快速启动

```bash
cd methods/EverCore
docker compose up -d          # 启动基础设施
uv sync                       # 安装依赖
uv run python src/run.py      # 运行应用
make test                     # 运行测试
make lint                     # 代码检查
```

## 关键入口

- `methods/EverCore/src/run.py` — 应用入口
- `methods/EverCore/src/agentic_layer/memory_manager.py` — 核心记忆管理器
- `methods/EverCore/src/infra_layer/adapters/input/api/` — REST API 控制器
- `methods/EverCore/docs/` — 文档
- `methods/EverCore/evaluation/` — 评估运行器和报告

## 开发注意事项

- 所有 I/O 是异步的；使用 `await`
- EverCore 是多租户的；数据必须保持租户隔离
- 提示词在 `methods/EverCore/src/memory_layer/prompts/` 中，有中英文版本
- 优先使用现有仓库的模式和组件边界
