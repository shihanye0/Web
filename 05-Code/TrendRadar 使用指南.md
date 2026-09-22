# TrendRadar 使用指南（Ubuntu 版）

> AI 驱动的舆情监控助手，聚合多平台热点 + RSS 订阅，支持 MCP 协议

---

## 一、项目信息

- **项目地址**：https://github.com/sansan0/TrendRadar
- **本机路径**：`/home/user/github-product/TrendRadar/`
- **Conda 环境**：`trendradar`
- **版本**：v6.10.0

---

## 二、核心功能

### 数据源
- **热榜平台**：今日头条、百度热搜、华尔街见闻、澎湃新闻、bilibili、微博、抖音、知乎等 30+ 平台
- **RSS 订阅**：Hacker News、阮一峰博客、雅虎财经等
- **自定义源**：支持添加任意 RSS 源

### AI 能力
- **智能筛选**：AI 自动筛选相关新闻
- **AI 翻译**：多语言推送
- **AI 分析**：生成分析简报
- **MCP 集成**：支持自然语言对话分析（13 个 AI 工具）

### 推送渠道
- 微信（企业微信/个人微信）
- Telegram、钉钉、飞书
- 邮件、ntfy/Bark、Slack
- 通用 Webhook

---

## 三、本地安装（推荐）

### 3.1 安装 Conda 环境

```bash
# 创建环境
conda create -n trendradar python=3.12 -y

# 激活环境
conda activate trendradar

# 安装依赖
pip install -e /home/user/github-product/TrendRadar -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3.2 配置 AI API Key

编辑 `/home/user/github-product/TrendRadar/config/config.yaml`：

```yaml
ai:
  model: "deepseek/deepseek-v4-flash"
  api_key: "sk-your-api-key-here"
```

或设置环境变量：

```bash
export AI_API_KEY="sk-your-api-key-here"
```

### 3.3 验证配置

```bash
cd /home/user/github-product/TrendRadar
conda activate trendradar
trendradar --doctor
```

---

## 四、Docker 部署（可选）

### 4.1 安装 Docker

```bash
sudo apt-get update
sudo apt-get install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
```

### 4.2 启动 MCP 服务

```bash
# 拉取镜像
docker pull wantcat/trendradar-mcp:latest

# 创建配置目录
mkdir -p /home/user/trendradar/config
mkdir -p /home/user/trendradar/output

# 下载配置文件
curl -sL "https://raw.githubusercontent.com/sansan0/TrendRadar/master/config/config.yaml" \
  -o /home/user/trendradar/config/config.yaml

# 启动容器
docker run -d --name trendradar-mcp \
  -p 127.0.0.1:8888:3333 \
  -v "/home/user/trendradar/config:/app/config:ro" \
  -v "/home/user/trendradar/output:/app/output:ro" \
  -e TZ=Asia/Shanghai \
  wantcat/trendradar-mcp:latest
```

### 4.3 配置 Claude Code MCP

在 `~/.claude/.mcp.json` 中添加：

```json
"trendradar": {
  "url": "http://127.0.0.1:8888/mcp",
  "type": "streamableHttp",
  "description": "AI舆情监控"
}
```

---

## 五、使用方法

### 5.1 基本运行

```bash
cd /home/user/github-product/TrendRadar
conda activate trendradar

# 正常运行
trendradar

# 查看调度状态
trendradar --show-schedule

# 环境体检
trendradar --doctor

# 测试通知
trendradar --test-notification
```

### 5.2 定时任务

```bash
# 每小时运行一次
0 * * * * cd /home/user/github-product/TrendRadar && conda run -n trendradar trendradar

# 每天早上 8 点运行
0 8 * * * cd /home/user/github-product/TrendRadar && conda run -n trendradar trendradar
```

### 5.3 MCP 工具（13个）

| 工具 | 功能 | 使用场景 |
|------|------|---------|
| `search_news` | 搜索热点新闻 | "搜索最近AI相关新闻" |
| `get_trending` | 获取当前热门话题 | "现在什么最火" |
| `read_article` | 读取文章正文 | "帮我读一下这篇文章" |
| `analyze_sentiment` | 情感分析 | "分析这个话题的情感倾向" |
| `predict_trend` | 趋势预测 | "预测这个话题的走势" |
| `push_to_channel` | 推送到指定渠道 | "推送到飞书" |

---

## 六、配置详解

### 6.1 AI 配置

```yaml
ai:
  model: "deepseek/deepseek-v4-flash"  # 推荐：便宜够用
  api_key: "sk-your-key"
  timeout: 120
  temperature: 1.0
  max_tokens: 5000
```

### 6.2 数据源配置

```yaml
platforms:
  enabled: true
  sources:
    - id: "weibo"
      name: "微博"
    - id: "zhihu"
      name: "知乎"
    - id: "bilibili-hot-search"
      name: "bilibili 热搜"

rss:
  enabled: true
  feeds:
    - id: "hacker-news"
      name: "Hacker News"
      url: "https://hnrss.org/frontpage"
```

### 6.3 推送渠道配置

```yaml
notification:
  enabled: true
  channels:
    - type: "telegram"
      bot_token: "your-bot-token"
      chat_id: "your-chat-id"
```

---

## 七、常用管理命令

```bash
# 查看容器状态（Docker 方式）
docker ps | grep trendradar

# 查看日志
docker logs -f trendradar-mcp

# 停止/启动容器
docker stop trendradar-mcp
docker start trendradar-mcp

# 删除容器
docker rm trendradar-mcp
```

---

## 八、故障排查

| 问题 | 解决方案 |
|------|---------|
| AI API Key 未配置 | 编辑 config.yaml 添加 api_key |
| 通知渠道未配置 | 编辑 config.yaml 添加通知渠道 |
| 端口被占用 | 换端口：`-p 127.0.0.1:8889:3333` |
| Docker 容器启动失败 | 检查日志：`docker logs trendradar-mcp` |

### editable 路径迁移问题

2026-07-06 已修复一次：`trendradar` conda 环境中的 editable 安装仍指向旧路径 `/home/user/TrendRadar`，实际仓库已迁移到 `/home/user/github-product/TrendRadar`。

修复后验证：

```bash
conda run -n trendradar python -c "import trendradar; print(trendradar.__file__)"
conda run -n trendradar python -m pip show trendradar
```

---

## 九、快速参考卡

```
┌────────────────────────────────────────────────────────┐
│              TrendRadar 常用命令速查                      │
├────────────────────────────────────────────────────────┤
│ 体检配置:     trendradar --doctor                        │
│ 正常运行:     trendradar                                 │
│ 查看调度:     trendradar --show-schedule                 │
├────────────────────────────────────────────────────────┤
│ Docker 部署:  docker run -d --name trendradar-mcp \     │
│               -p 127.0.0.1:8888:3333 ...               │
├────────────────────────────────────────────────────────┤
│ 访问界面:     http://localhost:8080                      │
│ MCP 接口:     http://127.0.0.1:8888/mcp                 │
└────────────────────────────────────────────────────────┘
```

---

## 十、本机环境信息

| 项目 | 值 |
|------|-----|
| 项目路径 | `/home/user/github-product/TrendRadar/` |
| Conda 环境 | `trendradar` |
| Python 版本 | 3.12 |
| AI 模型 | DeepSeek v4-flash |
| 安装方式 | 本地 Conda（推荐） |

---

*文档更新日期：2026年7月6日*
*系统：Ubuntu 22.04*
