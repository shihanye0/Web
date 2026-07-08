# codebase-memory-mcp：代码库长期记忆 MCP

## 基本信息

- 仓库：https://github.com/DeusData/codebase-memory-mcp
- 版本：`0.8.1`
- 许可证：MIT
- 定位：把代码库索引为持久知识图谱，为 agent 提供函数、类、调用关系、项目结构等代码理解能力。

## 本机安装

已安装 portable 静态 Linux 版本：

```bash
/home/user/.local/bin/codebase-memory-mcp --version
```

验证结果：

```text
codebase-memory-mcp 0.8.1
```

安装来源：

```text
https://github.com/DeusData/codebase-memory-mcp/releases/download/v0.8.1/codebase-memory-mcp-linux-amd64-portable.tar.gz
```

SHA256 已校验：

```text
6ab87a6c05d049dde57700803ca0ab4199fcf25973a0606618af0fcee73f5abd
```

## Codex 配置

配置文件：

```bash
/home/user/.codex/config.toml
```

新增 MCP：

```toml
[mcp_servers.codebase-memory-mcp]
type = "stdio"
command = "/home/user/.local/bin/codebase-memory-mcp"
startup_timeout_sec = 60
```

配置备份：

```bash
/home/user/.codex/config.toml.backup-20260706-agent-tools
```

## 重要安装记录

第一次下载的普通 Linux amd64 包不能运行，原因是当前系统缺少较新的 glibc/libstdc++：

```text
GLIBC_2.38 not found
GLIBCXX_3.4.32 not found
```

解决方式是使用 `linux-amd64-portable` 静态链接包。

## 可用工具

根据 `--help`，MCP 工具包括：

- `index_repository`
- `search_graph`
- `query_graph`
- `trace_path`
- `get_code_snippet`
- `get_graph_schema`
- `get_architecture`
- `search_code`
- `list_projects`
- `delete_project`
- `index_status`
- `detect_changes`
- `manage_adr`
- `ingest_traces`

## 使用边界

- 适合大代码库理解、调用链追踪、架构查询。
- 不应替代当前源码、测试、schema、生成物这些真源。
- 接入多个 memory 系统时，要避免真源分裂：`codebase-memory-mcp` 负责代码结构记忆，Cognee/通用 memory 负责跨会话知识。
