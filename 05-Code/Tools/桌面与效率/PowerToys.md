# PowerToys

微软官方开源的 Windows 增强工具集。本机版本 **0.101.2362**（winget user 权限安装，2026-09-12）。

## 它解决什么

补齐 Windows 原生缺失的效率功能：窗口布局管理、批量重命名、屏幕取词 OCR、文件预览增强等，全部集成在一个设置面板里。

## 常用模块与快捷键

| 模块 | 默认快捷键 | 干什么 | 何时用 |
| --- | --- | --- | --- |
| Text Extractor（取词 OCR） | `Win+Shift+T` | 框选屏幕任意区域，把其中文字提取到剪贴板 | PPT/图片/不可复制的网页里取文字；论文截图取段落 |
| FancyZones | `Win+Shift+\`` | 自定义窗口网格布局，拖窗口时按 Shift 吸附 | 双屏/多窗口写论文时固定"文献区+写作区+终端区" |
| PowerRename | 右键菜单 → PowerRename | 正则批量重命名 | 整理实验结果截图、批量改下载文件名 |
| Always On Top | `Win+Ctrl+T` | 让任意窗口置顶 | 一边看 PDF 一边写笔记，让 PDF 钉在角落 |
| Color Picker | `Win+Shift+C` | 取屏幕颜色 | 做图时取配色 |
| Peek | 选中按 Peek 键 | 大图预览 | 看长图/大 PDF 缩略图 |
| PowerToys Run | `Alt+Space` | 启动器 | 本机默认未启用；若手动启用会与 Flow Launcher 抢键（见下） |

## 如何使用

1. 开始菜单搜 "PowerToys" 打开设置面板，首次把"开机自启"打开。
2. 每个模块独立开关——**只开自己用的**，减少后台占用（本机 16G 内存紧张）。
3. **PowerToys Run 本机默认未启用**（2026-09-13 核实全局开关为关），启动器统一用 [[Flow Launcher]] 即可；若日后手动启用 Run，注意它会占用 `Alt+Space`，与 Flow Launcher 二选一。
4. 其余模块快捷键都可以在设置里改。

## 搭配

- 取词 OCR 拿到的是纯文字，中文扫描件效果不如 [[Umi-OCR]]（后者是专业 OCR 引擎）；PowerToys 适合"顺手取一段"，Umi-OCR 适合"整页识别"。
- FancyZones + Obsidian + Zotero 三窗布局是写论文的标配。

## 参考

- 官方文档：<https://learn.microsoft.com/windows/powertoys/>
- 仓库：<https://github.com/microsoft/PowerToys>
