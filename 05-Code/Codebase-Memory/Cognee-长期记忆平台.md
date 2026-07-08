# Cognee：智能体长期记忆平台

## 基本信息

- 仓库：https://github.com/topoteretes/cognee
- 定位：开源智能体记忆平台，把不同类型的数据组织成自托管知识图谱，让智能体跨会话保留和调用长期信息。

## 本机状态

未安装，未配置。

## 判断

- P1：值得关注，但暂缓接入。
- 与以下系统存在重叠：
  - Codex memory MCP
  - claude-context
  - codebase-memory-mcp
  - 普通项目文档/Obsidian 笔记

## 使用边界建议

- 如果接入，Cognee 应负责跨会话、跨资料的长期知识，不应和 `codebase-memory-mcp` 抢代码结构索引职责。
- 接入前要定义：数据源、存储位置、删除策略、隐私边界、重建方式。
