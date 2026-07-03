# TrendRadar MCP 部署指南

## 概述

TrendRadar 是一个 AI 驱动的舆情监控工具，GitHub 获近 5 万星。聚合知乎、微博、抖音等十多个平台热点，可进行情感分析与趋势预测，简报可直推至手机。

**核心能力**：
- 聚合 10+ 平台热点（知乎、微博、抖音、微信公众号等）
- AI 情感分析与趋势预测
- 多渠道推送（飞书、钉钉、Telegram、邮件、微信等）
- MCP 协议支持，可通过自然语言与新闻数据对话

**GitHub**：https://github.com/sansan0/TrendRadar

---

## 项目介绍

### TrendRadar 是什么

TrendRadar 是一个开源的 AI 舆情监控与趋势分析平台，v6.8.1 版本，GitHub 获近 5 万星。它通过爬虫聚合多个平台的热点数据，并提供 MCP（Model Context Protocol）接口，让 AI 助手能够直接与新闻数据对话，进行深度分析。

### 核心架构

```
┌─────────────────────────────────────────────────────────┐
│                    TrendRadar 系统                       │
├─────────────────┬─────────────────┬─────────────────────┤
│   新闻爬虫模块   │   MCP 分析模块   │    推送通知模块     │
│  - 知乎热榜     │  - 13个AI工具    │  - 飞书/钉钉       │
│  - 微博热搜     │  - 情感分析      │  - Telegram        │
│  - 抖音热点     │  - 趋势预测      │  - 邮件/Bark       │
│  - 微信公众号   │  - 自然语言搜索  │  - 企业微信        │
│  - GitHub       │  - 文章正文提取  │  - 个人微信        │
│  - Hacker News  │  - 日期范围解析  │  - ntfy            │
│  - V2EX         │                 │                    │
│  - 36kr         │                 │                    │
└─────────────────┴─────────────────┴─────────────────────┘
```

### 支持的数据源

| 平台 | 数据类型 | 更新频率 |
|------|---------|---------|
| 知乎 | 热榜、推荐 | 实时 |
| 微博 | 热搜、热门 | 实时 |
| 抖音 | 热点、挑战 | 实时 |
| 微信公众号 | 热门文章 | 每日 |
| GitHub | Trending | 每日 |
| Hacker News | Top stories | 实时 |
| V2EX | 热门主题 | 实时 |
| 36kr | 科技新闻 | 实时 |
| 少数派 | 热门文章 | 实时 |
| RSS订阅 | 自定义源 | 可配置 |

### MCP 工具列表（13个）

| 工具 | 功能 | 使用场景 |
|------|------|---------|
| `search_news` | 搜索热点新闻 | "搜索最近AI相关新闻" |
| `get_trending` | 获取当前热门话题 | "现在什么最火" |
| `read_article` | 读取文章正文 | "帮我读一下这篇文章" |
| `read_articles_batch` | 批量读取文章 | "读取这5篇文章" |
| `get_channel_format_guide` | 获取推送渠道格式 | "飞书推送格式是什么" |
| `resolve_date_range` | 自然语言日期解析 | "本周、最近7天" |
| `analyze_sentiment` | 情感分析 | "分析这个话题的情感倾向" |
| `predict_trend` | 趋势预测 | "预测这个话题的走势" |
| `get_keyword_stats` | 关键词统计 | "AI这个词最近热度如何" |
| `get_platform_summary` | 平台汇总 | "知乎今天有什么" |
| `push_to_channel` | 推送到指定渠道 | "推送到飞书" |
| `list_channels` | 列出可用渠道 | "能推送到哪些地方" |
| `get_server_status` | 服务状态 | "TrendRadar运行正常吗" |

### 使用示例

```
# 搜索热点
你：帮我看看最近AI领域有什么热点
MCP：search_news(query="AI", platforms=["zhihu", "weibo"])

# 深度分析
你：分析一下DeepSeek的舆情趋势
MCP：read_article(url="...") → analyze_sentiment() → predict_trend()

# 批量处理
你：读取最近3天的AI新闻并总结
MCP：resolve_date_range("最近3天") → search_news() → read_articles_batch()

# 推送通知
你：把分析结果推送到飞书
MCP：push_to_channel(channel="feishu", content="...")
```

### 配置文件结构

```
E:/edge/TrendRadar-master/TrendRadar-master/
├── config/
│   ├── config.yaml          # 主配置（关键词、推送、平台）
│   └── keywords.yaml        # 关键词详细配置
├── output/                   # 生成的报告
├── main.py                  # 主程序入口
├── manage.py                # 管理脚本
└── docker-compose.yml       # Docker编排
```

---

## 架构

```
┌─────────────────────┐
│  TrendRadar 主服务    │  定时抓取新闻 + 推送通知
│  (Docker Container)  │
└─────────┬───────────┘
          │ 共享卷 (config/, output/)
┌─────────▼───────────┐
│  TrendRadar MCP      │  AI 分析接口 (端口 3333)
│  (Docker Container)  │
└─────────┬───────────┘
          │ HTTP streamableHttp
┌─────────▼───────────┐
│  Claude Code MCP     │  连接 http://127.0.0.1:8888/mcp
└─────────────────────┘
```

---

## 前置条件

- Docker Desktop 已安装并运行
- 网络可访问 Docker Hub（拉取镜像）

---

## 部署步骤

### Step 1：启动 Docker Desktop

确保 Docker Desktop 正在运行（系统托盘图标显示绿色）。

```bash
# 验证 Docker 是否可用
docker --version
```

### Step 2：拉取 MCP 镜像

```bash
docker pull wantcat/trendradar-mcp:latest
```

### Step 3：创建配置目录

TrendRadar 需要配置文件和输出目录。首次运行前需要创建：

```bash
# 创建项目目录
mkdir -p E:/trendradar/config
mkdir -p E:/trendradar/output
```

### Step 4：下载默认配置

从 GitHub 下载默认配置文件：

```bash
# 下载 config.yaml
curl -sL "https://raw.githubusercontent.com/sansan0/TrendRadar/master/config/config.yaml" -o E:/trendradar/config/config.yaml
```

或手动从 https://github.com/sansan0/TrendRadar 下载 `config/config.yaml` 放到 `E:/trendradar/config/` 目录。

### Step 5：启动 MCP 服务容器

```bash
docker run -d --name trendradar-mcp `
  -p 127.0.0.1:8888:3333 `
  -v "E:/trendradar/config:/app/config:ro" `
  -v "E:/trendradar/output:/app/output:ro" `
  -e TZ=Asia/Shanghai `
  wantcat/trendradar-mcp:latest
```

**参数说明**：

| 参数 | 说明 |
|------|------|
| `-d` | 后台运行 |
| `--name trendradar-mcp` | 容器名称 |
| `-p 127.0.0.1:8888:3333` | 端口映射（仅本地访问） |
| `-v .../config:/app/config:ro` | 配置目录（只读） |
| `-v .../output:/app/output:ro` | 输出目录（只读） |
| `-e TZ=Asia/Shanghai` | 时区设置 |

### Step 6：验证容器运行

```bash
# 查看容器状态
docker ps | grep trendradar

# 查看容器日志
docker logs trendradar-mcp

# 测试 MCP 端口
curl http://127.0.0.1:8888/mcp
```

### Step 7：配置 Claude Code MCP

在 `~/.claude/.mcp.json` 中添加：

```json
"trendradar": {
  "url": "http://127.0.0.1:8888/mcp",
  "type": "streamableHttp",
  "description": "AI舆情监控"
}
```

### Step 8：重启 Claude Code

重启 Claude Code 使 MCP 配置生效。

---

## 常用命令

```bash
# 查看容器状态
docker ps | grep trendradar

# 查看日志
docker logs -f trendradar-mcp

# 停止容器
docker stop trendradar-mcp

# 启动容器
docker start trendradar-mcp

# 删除容器
docker rm trendradar-mcp

# 重新拉取最新镜像
docker pull wantcat/trendradar-mcp:latest
docker rm -f trendradar-mcp
docker run -d --name trendradar-mcp -p 127.0.0.1:8888:3333 -v "E:/trendradar/config:/app/config:ro" -v "E:/trendradar/output:/app/output:ro" -e TZ=Asia/Shanghai wantcat/trendradar-mcp:latest
```

---

## 自定义配置

编辑 `E:/trendradar/config/config.yaml`：

```yaml
# 关键词配置
keywords:
  - name: "AI"
    platforms: ["zhihu", "weibo"]
  - name: "编程"
    platforms: ["zhihu", "github"]

# 推送配置（可选）
push:
  enable: false
  # telegram:
  #   bot_token: "your_bot_token"
  #   chat_id: "your_chat_id"
```

详细配置参考：https://github.com/sansan0/TrendRadar

---

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| Docker 命令找不到 | 启动 Docker Desktop |
| 容器启动失败 | 检查端口 3333 是否被占用：`netstat -an | grep 3333` |
| MCP 连接失败 | 确认容器运行中：`docker ps | grep trendradar` |
| 配置不生效 | 重新创建容器（删除旧容器后重新 `docker run`） |
| 镜像拉取失败 | 检查网络，或使用镜像加速器 |

---

## 相关链接

- GitHub：https://github.com/sansan0/TrendRadar
- Docker Hub：https://hub.docker.com/r/wantcat/trendradar-mcp
- MCP 协议：https://modelcontextprotocol.io/

---

**创建日期**：2026-06-01
**最后更新**：2026-06-01
