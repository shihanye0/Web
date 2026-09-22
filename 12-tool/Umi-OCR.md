# Umi-OCR

免费、离线、开源的中文 OCR 工具（PaddleOCR 引擎）。本机版本 **Paddle v2.1.5**，绿色解压版，位置：

```text
E:\Tools\Umi-OCR\Umi-OCR_Paddle_v2.1.5\Umi-OCR.exe
```

（2026-09-12 安装；Rapid 引擎版更轻量，本机选了精度更高的 Paddle 版，i7-11800H 跑起来无压力。）

## 它解决什么

把图片/扫描件里的文字变成可复制的文本——完全离线运行，论文和隐私文档不出本机。对中文的识别质量远超本机原有的 Tesseract。

## 核心功能与用法

| 功能 | 用法 | 何时用 |
| --- | --- | --- |
| 截图识别 | 在设置里自定义全局快捷键，框选屏幕区域即出文字 | 网页/PPT 里"不可复制"的文字、看文献时随手取段落 |
| 批量图片 | 把一批图片拖进"批量截图"页，一键全部识别 | 实验记录照片、白板照片批量转文字 |
| PDF 识别 | PDF 页签导入，逐页 OCR | **扫描版文献**转成文字 |
| 生成双层可搜索 PDF | PDF 识别后导出 | 原版式保留 + 全文可搜索可复制，之后能直接喂给 MinerU/Zotero |
| 二维码 | 扫码/生成 | 偶尔用 |

## 适用场景

- 扫描版老论文、老师给的扫描讲义
- 手机拍的实验记录（配合 [[LocalSend]] 传到电脑）
- 隐私敏感、不能传在线 OCR 的文档

## 搭配（重点）

- Umi-OCR 出的可搜索 PDF → **MinerU** 结构化解析（E:\论文\科研AI工具 wrapper）→ Markdown 进 Obsidian 或 [[AnythingLLM]] 知识库
- 屏幕上"顺手取一段字"用 [[PowerToys]] 的 Text Extractor 更快；整页/整份文档识别才上 Umi-OCR
- 与 Tesseract 的关系：Tesseract 保留给脚本化批处理场景，交互式识别一律用 Umi-OCR

## 参考

- 仓库：<https://github.com/hiroi-sora/Umi-OCR>
