---
tags: [video, mcp, ai-agent, ffmpeg, yt-dlp, video-use]
created: 2026-06-13
---

# Video Use — MCP 视频分析与帧提取工具

## 一句话定位

MCP Server + CLI，让 AI Agent 能够下载视频、提取关键帧、分析视频内容。

## 核心概念

Video Use 和前面三个工具**完全不同**——它不是视频创作工具，而是**视频分析工具**：

| 工具 | 方向 | 输入 → 输出 |
|------|------|-------------|
| Remotion | 创作 | 代码 → 视频 |
| vibe-motion | 创作 | 自然语言 → 视频 |
| HyperFrames | 创作 | HTML → 视频 |
| **Video Use** | 分析 | 视频 → 帧/元数据 |

它的核心价值是让 AI Agent（如 Claude Code、Cursor）能够"看懂"视频。

## 安装

```bash
# 全局安装
npm install -g video-use

# 或直接使用
npx video-use
```

## 核心功能

### 1. 下载视频

```bash
# 使用 yt-dlp 下载视频
video-use download "https://www.youtube.com/watch?v=xxx"

# 支持平台：YouTube、B站、抖音等
```

### 2. 提取关键帧

```bash
# 提取视频关键帧
video-use frames input.mp4 --output ./frames/

# 按时间间隔提取
video-use frames input.mp4 --interval 5  # 每5秒一帧

# 按场景变化提取
video-use frames input.mp4 --scene-detect
```

### 3. 获取视频元数据

```bash
video-use info input.mp4
# 返回：时长、分辨率、帧率、编码格式等
```

## MCP Server 模式

Video Use 可以作为 MCP Server 运行，让 Claude Code 等工具直接调用：

```json
// ~/.claude/.mcp.json
{
  "mcpServers": {
    "video-use": {
      "command": "npx",
      "args": ["-y", "video-use", "mcp"]
    }
  }
}
```

### Claude Code 中的使用方式

配置 MCP 后，Claude Code 可以直接：

```
# 下载并分析视频
"帮我下载这个抖音视频并分析内容：https://..."

# 提取关键帧
"把这个视频的关键帧提取出来，每10秒一帧"

# 视频对比
"对比这两个视频的帧差异"
```

## 技术栈

| 依赖 | 用途 |
|------|------|
| `@modelcontextprotocol/sdk` | MCP 协议实现 |
| `execa` | 子进程管理 |
| `commander` | CLI 参数解析 |
| `zod` | 数据校验 |
| `@clack/prompts` | 交互式提示 |

外部依赖（需要系统安装）：
- **ffmpeg** — 视频处理
- **yt-dlp** — 视频下载

## MCP 工具列表

配置为 MCP Server 后，提供以下工具：

| 工具名 | 功能 |
|--------|------|
| `download-video` | 下载视频 |
| `extract-frames` | 提取关键帧 |
| `get-video-info` | 获取视频元数据 |
| `analyze-scene` | 场景分析 |

## 与其他 AI 工具配合

### Claude Code + Video Use

```
用户：帮我分析这个视频讲了什么
↓
Claude Code 调用 video-use MCP
↓
下载视频 → 提取关键帧 → 保存到本地
↓
Claude Code 读取帧图片 → 分析内容
↓
输出视频内容摘要
```

### Cursor + Video Use

Cursor 也可以通过 MCP 配置使用 Video Use，实现类似的视频分析能力。

## 适用场景

- 视频内容分析（让 AI "看"视频）
- 视频关键帧提取（缩略图、预览图）
- 视频对比（A/B 测试）
- 批量视频处理
- 视频元数据提取

## 注意事项

- 需要系统安装 ffmpeg 和 yt-dlp
- MCP 模式需要 Claude Code 支持 MCP
- 视频下载受平台限制（部分平台需要登录）
- 大视频提取帧可能耗时较长
- 版本 0.1.1，较新，功能可能不完善

## 参考链接

- npm：https://www.npmjs.com/package/video-use
- GitHub：https://github.com/therealfloatdev/video-use
- MCP 协议：https://modelcontextprotocol.io
