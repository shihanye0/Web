---
tags: [video, animation, react, remotion, ai-coding]
created: 2026-06-13
---

# Remotion — React 视频创作框架

## 一句话定位

用 React 代码程序化创建视频的框架，把"写代码"变成"做视频"。

## 核心概念

Remotion 让你用 React 组件来定义视频的每一帧，然后渲染成真实视频文件。本质上是把 React 的声明式 UI 能力应用到了视频创作领域。

```
React 组件 → 逐帧渲染 → MP4/MOV/WebM 视频
```

## 安装

```bash
# 创建新项目
npx create-video@latest my-video

# 或在已有项目中安装
npm install remotion @remotion/cli @remotion/bundler
```

## 核心 API

### composition — 定义视频

```jsx
import { Composition } from 'remotion';

export const RemotionRoot = () => {
  return (
    <Composition
      id="MyVideo"
      component={MyVideoComponent}
      durationInFrames={300}  // 30fps × 10秒
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
```

### useCurrentConfig — 获取当前帧

```jsx
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

const MyComponent = () => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();

  // 0-30帧内从0渐变到1
  const opacity = interpolate(frame, [0, 30], [0, 1]);

  return <div style={{ opacity }}>Hello World</div>;
};
```

### 渲染命令

```bash
# 渲染为 MP4
npx remotion render MyVideo out/video.mp4

# 渲染为 GIF
npx remotion render MyVideo out/video.gif --image-format=png

# 渲染特定帧范围
npx remotion render MyVideo out/video.mp4 --frames=0-100
```

## 与 AI 工具集成

### Claude Code 中使用

Remotion 项目本质上是 React 项目，Claude Code 可以直接帮你：

1. **创建动画组件** — 描述想要的效果，AI 生成 React 代码
2. **调试渲染问题** — 分析帧率、性能、样式问题
3. **批量生成** — 用循环/数据驱动生成系列视频

```
# 在 Claude Code 中
"帮我创建一个文字从左飞入的动画，持续2秒，30fps"
"把这个数据可视化做成动态图表视频"
"渲染这个 composition 为 1080p MP4"
```

### 常用 AI 提示词

| 需求 | 提示词示例 |
|------|-----------|
| 入门 | "用 Remotion 创建一个 10 秒的渐变背景视频" |
| 文字动画 | "创建文字逐字出现的效果，打字机风格" |
| 数据可视化 | "把 CSV 数据做成动态柱状图视频" |
| 转场 | "实现两个场景之间的淡入淡出转场" |

## 输出格式

| 格式 | 命令 | 特点 |
|------|------|------|
| MP4 (H.264) | `--codec=h264` | 通用，体积小 |
| MP4 (H.265) | `--codec=h265` | 更小体积，兼容性差 |
| WebM | `--codec=vp8/vp9` | Web 友好 |
| ProRes | `--codec=prores` | 专业剪辑，无损 |
| GIF | `--codec=gif` | 动图 |
| PNG 序列 | `--image-format=png` | 后期合成用 |

## 项目结构

```
my-video/
├── src/
│   ├── Root.tsx          # Composition 注册入口
│   ├── MyVideo.tsx       # 视频主组件
│   └── components/       # 复用组件
├── public/               # 静态资源
├── remotion.config.ts    # Remotion 配置
└── package.json
```

## 适用场景

- 科普动画 / 教学视频
- 数据可视化视频
- 社交媒体短视频批量生成
- 产品演示视频
- 片头/片尾动画

## 注意事项

- 需要 Node.js 16+
- 渲染需要 Chrome/Chromium（Remotion 会自动下载 Headless Shell）
- 大视频渲染耗时较长，建议先小尺寸调试
- 许可证：免费用于个人/开源，商用需要付费

## 参考链接

- 官网：https://remotion.dev
- 文档：https://remotion.dev/docs
- GitHub：https://github.com/remotion-dev/remotion
- npm：https://www.npmjs.com/package/remotion
