---
tags: [video, animation, ai, claude-code, remotion, vibe-motion]
created: 2026-06-13
---

# vibe-motion — AI 驱动的动画生成工具

## 一句话定位

通过自然语言描述，用 Claude Code 等 AI 工具自动生成动画并渲染为视频的工具链。

## 核心概念

vibe-motion 是一个基于 Remotion 的脚手架工具，核心理念是：

```
自然语言描述 → AI 生成动画代码 → 预览调整 → 渲染视频
```

它不是从零创造动画，而是**魔改开源动效代码**——从 GSAP/CodePen 社区获取动画模板，用 AI 替换内容和参数，最终渲染为视频。

## 与 seedance 的对比

| 工具 | 定位 | 适用场景 |
|------|------|---------|
| **seedance** | AI 视频生成（70%） | 常规 AI 视频内容 |
| **vibe-motion** | 精准控制动画（25%） | 科普动画、卡片动效、饼图动画等需要像素级控制的场景 |

## 安装

```bash
# 一行命令搭建开发环境
npx create-vibe-motion@latest my-project

# 进入项目
cd my-project

# 启动开发服务器
pnpm dev
```

## 项目结构

```
vibe-motion-project/
├── shared/
│   ├── features/              # 动画插件目录
│   │   └── demoMotion/        # 默认 Demo 插件
│   │       ├── config/        # 默认参数
│   │       ├── plugins/       # 插件定义
│   │       └── scenes/        # React 动画场景
│   ├── project/               # 项目配置
│   │   ├── projectRegistry.js # 插件注册
│   │   └── projectConfig.js   # 活跃 composition
│   └── scaffold/              # 脚手架运行时
├── preview/                   # 预览 UI（Vite）
├── remotion/                  # Remotion 渲染入口
└── package.json
```

## 在 Claude Code 中使用

### 基本流程

```
1. 找动画模板（GSAP 社区 / CodePen）
2. 下载代码（CodePen → Export Zip）
3. 在 Claude Code 中描述需求
4. AI 自动替换动画内容
5. 预览调整参数
6. 渲染输出视频
```

### 实操示例

```
# 步骤1：在 Claude Code 中
"帮我把 rolling text 动画的文字改为 'vibe motion'，颜色改为黑色"

# 步骤2：调整参数
"把动画时长改为 5 秒，背景设为透明"

# 步骤3：渲染
"渲染一个 ProRes 4444 格式的视频，带透明通道"
```

### 可调参数

```javascript
// shared/features/demoMotion/config/demoMotionDefaults.js
{
  title: "Scaffold Demo",        // 标题文字
  subtitle: "...",               // 副标题
  badgeText: "Vibe Motion",      // 标签文字
  cardDarkMode: false,           // 暗色模式
  durationSeconds: 3,            // 动画时长
  speed: 1,                      // 播放速度
  videoWidth: 480,               // 视频宽度
  videoHeight: 480,              // 视频高度
  accentHue: 210,                // 主题色调
  backgroundHue: 195,            // 背景色调
}
```

## 渲染命令

```bash
# 渲染默认 Demo
pnpm remotion:render:demo

# 自定义渲染
pnpm remotion:render

# 输出格式
# - ProRes 4444（带透明通道，无损）
# - H.264（体积小，无透明）
```

## 插件系统（Skill）

vibe-motion 的核心扩展机制是 **Skill（技能）**：

1. 在 `shared/features/` 下创建新目录
2. 实现 Plugin Contract（SceneComponent、buildSceneProps 等）
3. 在 `projectRegistry.js` 中注册
4. 社区可共享 Skill 到 GitHub 仓库

## 社区

- GitHub：https://github.com/vibe-motion
- npm：https://www.npmjs.com/package/create-vibe-motion
- Skills 仓库：vibe-motion/skills（可提交 PR 分享自制动画）

## 适用场景

- 科普动画（尺子动画、卡片动效、饼图动画）
- 产品演示动画
- 社交媒体短视频
- 数据可视化动画

## 注意事项

- 基于 Remotion，需要 Node.js 环境
- 推荐搭配 MiniMax M2.7 模型使用（编程能力强）
- 动画模板来源：GSAP 社区、CodePen
- 输出格式：ProRes 4444（专业）或 H.264（通用）
