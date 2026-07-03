---
tags: [video, animation, html, puppeteer, hyperframes, heygen]
created: 2026-06-13
---

# HyperFrames — HTML 视频合成框架

## 一句话定位

用 HTML/CSS 创建视频帧，通过 Puppeteer 逐帧截图渲染为视频的 CLI 工具。

## 核心概念

HyperFrames 的思路和 Remotion 不同：

| 维度 | Remotion | HyperFrames |
|------|----------|-------------|
| 渲染方式 | React → Canvas/WebGL | HTML/CSS → Puppeteer 截图 |
| 技术栈 | React | 原生 HTML/CSS/JS |
| 定位 | 程序化视频创作 | HTML 动画合成视频 |
| 维护方 | 开源社区 | HeyGen（商业公司） |

HyperFrames 更接近"把网页动画变成视频"的思路，用 Puppeteer 控制 Chrome 逐帧截图，然后合成视频。

## 安装

```bash
# 全局安装
npm install -g hyperframes

# 或直接使用
npx hyperframes
```

## 核心功能

### 1. 创建项目

```bash
hyperframes init my-project
```

### 2. 预览

```bash
hyperframes preview
# 启动本地服务器，实时预览动画效果
```

### 3. 渲染

```bash
hyperframes render
# 将 HTML 动画渲染为视频文件
```

## 项目结构

```
my-project/
├── src/
│   ├── scenes/           # 场景定义
│   ├── components/       # 复用组件
│   └── main.js           # 入口
├── public/               # 静态资源
├── hyperframes.config.js # 配置
└── package.json
```

## 技术栈

- **渲染引擎**：Puppeteer (Headless Chrome)
- **图像处理**：Sharp
- **字体**：Fontkit
- **构建**：ESBuild
- **CSS**：PostCSS
- **运行时**：Hono (HTTP 服务器)

## 与 AI 工具集成

### Claude Code 中使用

HyperFrames 项目本质上是 HTML/CSS/JS 项目，Claude Code 可以直接操作：

```
# 创建动画
"帮我创建一个文字旋转进入的 HTML 动画场景"

# 调整样式
"把背景改为渐变色，文字大小改为 48px"

# 渲染
"渲染这个场景为 1080p 视频"
```

### 与其他工具的定位差异

| 工具 | 输入 | 输出 | 适合 |
|------|------|------|------|
| Remotion | React 代码 | 视频 | 程序化视频 |
| vibe-motion | 自然语言 | 动画视频 | AI 驱动动画 |
| **HyperFrames** | HTML/CSS/JS | 视频 | 网页动画→视频 |
| Video Use | 视频 URL | 关键帧 | 视频分析 |

## 渲染配置

```javascript
// hyperframes.config.js
module.exports = {
  width: 1920,
  height: 1080,
  fps: 30,
  output: 'out/video.mp4',
  // Puppeteer 配置
  puppeteer: {
    headless: true,
  }
};
```

## 适用场景

- HTML/CSS 动画转视频
- 网页截图动画
- 产品演示（网页录制风格）
- UI 动效预览
- 社交媒体内容

## 注意事项

- 依赖 Puppeteer（需要下载 Chrome）
- 渲染速度取决于 Puppeteer 截图性能
- 复杂动画可能需要优化帧率
- HeyGen 商业产品，注意许可证
- 相比 Remotion 生态较小

## 参考链接

- GitHub：https://github.com/heygen-com/hyperframes
- npm：https://www.npmjs.com/package/hyperframes
- 核心包：https://www.npmjs.com/package/@hyperframes/core
