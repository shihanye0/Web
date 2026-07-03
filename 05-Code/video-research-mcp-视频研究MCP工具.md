---
tags: [video, mcp, gemini, research, claude-code, video-research-mcp]
created: 2026-06-13
---

# video-research-mcp — 视频研究 MCP 工具

## 一句话定位

51 个视频分析工具的 MCP Server，基于 Gemini 3.5 Flash，支持视频分析、深度研究、内容提取、解说视频创建。

## 安装状态

| 项目 | 状态 |
|------|------|
| npm 包 | ✅ 已全局安装 (v0.6.1) |
| MCP 配置 | ✅ 已自动写入 `.mcp.json` |
| Gemini API Key | ✅ 已配置 |
| Skills | ✅ 10+ 个已安装 |
| Agents | ✅ 5 个已安装 |

## 核心能力

### 28 个 MCP 工具

| 分类 | 工具 | 功能 |
|------|------|------|
| **视频分析** | `video_analyze` | 分析任意视频（YouTube/本地文件） |
| | `video_metadata` | 获取视频元数据（标题、播放量、标签） |
| | `video_playlist` | 列出播放列表中的视频 |
| | `video_create_session` | 创建多轮视频分析会话 |
| | `video_continue_session` | 在会话中追问 |
| **内容分析** | `content_analyze` | 分析任意内容（URL/文件/文本） |
| | `content_batch_analyze` | 批量分析多个文档 |
| | `content_extract` | 按自定义 Schema 提取结构化数据 |
| **深度研究** | `research_deep` | 多阶段深度研究 |
| | `research_plan` | 生成研究计划蓝图 |
| | `research_document` | 基于文档的深度研究 |
| | `research_web` | 启动 Gemini 深度研究 Agent |
| | `research_web_status` | 查询深度研究状态 |
| | `research_web_followup` | 对深度研究结果追问 |
| | `research_web_cancel` | 取消深度研究任务 |
| | `research_assess_evidence` | 评估某个声明的可信度 |
| **搜索** | `web_search` | Google 搜索（通过 Gemini） |
| **基础设施** | `infra_cache` | 管理分析缓存 |
| | `infra_configure` | 运行时配置修改 |

### 10+ 个 Skills

| Skill | 功能 |
|-------|------|
| `video-research` | 视频分析核心 Skill |
| `video-explainer` | 视频解说生成 |
| `video-generation` | AI 视频生成 |
| `video-production` | 视频制作流程 |
| `video-editing` | 视频剪辑 |
| `gemini-visualize` | 知识图谱可视化 |
| `research-brief-builder` | 研究简报生成 |
| `manim-video` | Manim 数学动画 |
| `remotion-video-creation` | Remotion 视频创作 |
| `short-video-script` | 短视频脚本 |

### 5 个 Agents

| Agent | 功能 |
|-------|------|
| `video-analyst` | 视频分析专家 |
| `video-producer` | 视频制作专家 |
| `researcher` | 深度研究员 |
| `visualizer` | 知识可视化 |
| `content-to-video` | 内容转视频 |

## 使用方式

### 方式1：直接对话（推荐）

```
# 分析 YouTube 视频
"帮我分析这个视频的制作技法：https://youtube.com/watch?v=xxx"

# 分析本地视频（需先用 video-use 下载）
"分析 E:\video\dy\vibe-motion.mp4 的内容结构"

# 深度研究
"深度研究一下 AI 科普视频的制作流程"

# 批量分析
"对比这3个视频的剪辑风格差异"
```

### 方式2：Slash 命令

```bash
/gr:video "视频URL或描述"     # 视频分析
/gr:research "研究主题"       # 深度研究
/gr:analyze "内容URL"         # 内容分析
/gr:recall "关键词"           # 知识库搜索
/ve:explain-video "视频URL"   # 生成视频解说
```

### 方式3：MCP 工具直接调用

```python
# 视频分析
video_analyze(url="https://youtube.com/watch?v=xxx", 
              instruction="提取所有使用的工具和特效")

# 内容提取
content_extract(content=text, 
                schema={"tools": [{"name": "string", "purpose": "string"}]})

# 深度研究
research_deep(topic="AI视频制作工具对比", scope="deep")
```

## 拉片工作流集成

### 完整拉片流程

```
Step 01 定维度
    └─ 用户选择要分析的维度

Step 02 拆素材
    ├─ video-use: 下载视频 + 提取关键帧
    └─ video_analyze: 分析视频内容、时间戳、工具链

Step 03 判型
    └─ video_analyze(instruction="判断视频类型：口播/教程/叙事")

Step 04 逐帧细看
    ├─ video_create_session: 创建分析会话
    └─ video_continue_session: 逐段追问细节

Step 05 逐段填表
    ├─ content_extract: 按 L0-L6 框架提取结构化数据
    └─ 自定义 Schema: 对齐画面/台词/图形/节奏

Step 06 出报告
    ├─ research_deep: 生成深度分析报告
    └─ 输出: 拉片报告 + 复现 SOP
```

### 拉片报告模板

```json
{
  "video_title": "视频标题",
  "video_type": "口播|教程|叙事",
  "duration": "4:30",
  "replicability_score": "8.5/10",
  "segments": [
    {
      "time_range": "00:00-00:30",
      "content": "段落内容描述",
      "technique": "使用的拍摄/剪辑技法",
      "tools": ["工具1", "工具2"],
      "key_frame": "代表帧路径"
    }
  ],
  "tool_chain": ["剪映", "Remotion", "yanvideotext"],
  "key_findings": ["发现1", "发现2"],
  "replicate_sop": {
    "steps": ["步骤1", "步骤2"],
    "tools_per_step": {"步骤1": ["工具A"]}
  }
}
```

## 与其他工具配合

### 工具链闭环

```
video-use（下载+提帧）
    ↓
video-research-mcp（分析+研究）
    ↓
vibe-motion / Remotion（复刻制作）
    ↓
输出视频
```

### 配合示例

```bash
# 1. 下载参考视频
video-use extract "https://抖音链接"

# 2. 分析视频
"用 video_analyze 分析 .video-use/frames/ 中的关键帧，
 提取制作技法和工具链"

# 3. 生成复现 SOP
"基于分析结果，生成可复刻的制作 SOP"

# 4. 用 vibe-motion 复刻
"按照 SOP，用 vibe-motion 制作类似动画"
```

## Token 消耗参考

| 操作 | 模型 | 预估消耗 | 费用 |
|------|------|---------|------|
| 视频元数据 | YouTube API | 0 Gemini | 免费 |
| 视频分析（默认） | Gemini Pro | ~10K token | ~$0.01 |
| 深度研究 | Gemini Pro | ~50K token | ~$0.05 |
| 完整拉片（30分钟视频） | Opus + Gemini | ~400K token | ~$25 |

## 常见问题

### Q: 抖音视频能直接分析吗？

A: 不能直接分析抖音 URL。需要先用 video-use 下载到本地，再用 `video_analyze(file_path=...)` 分析本地文件。

### Q: 需要配置 Weaviate 吗？

A: 不需要。Weaviate 是可选的知识库组件，用于语义搜索历史分析结果。基础功能不需要。

### Q: Gemini API Key 怎么获取？

A: 访问 https://aistudio.google.com/apikey 免费申请。

### Q: 支持哪些视频格式？

A: 支持所有 ffmpeg 能处理的格式（MP4, MOV, AVI, WebM 等）。

## 参考链接

- GitHub：https://github.com/Galbaz1/video-research-mcp
- npm：https://www.npmjs.com/package/video-research-mcp
- Gemini API：https://aistudio.google.com/apikey
- MCP 协议：https://modelcontextprotocol.io
