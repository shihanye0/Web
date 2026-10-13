# UniGetUI

开源的软件包管理图形界面（前身 WingetUI，现由 Devolutions 维护）。本机版本 **2026.2.7**（winget id：`Devolutions.UniGetUI`，旧 id `MartiCliment.UniGetUI` 已失效，2026-09-12 安装）。

## 它解决什么

winget/scoop/choco 装的几十个软件分散在各自的更新机制里，UniGetUI 把"谁有新版本"汇总成一个界面，勾选即升级，还能设开机自动检查。

## 如何使用

1. 打开后切到"更新"标签页 → 全选或勾选 → 点更新。
2. 对不想动的软件右键"忽略此更新"（比如大版本变动恐惧的软件）。
3. 设置里可开启"定期自动检查 + 通知"，只提醒不自动装。

## 适用场景

- **每周 5 分钟维护**：yt-dlp、PowerToys、7-Zip、draw.io 这些高频工具保持最新
- 新机器批量装机：软件清单可导出，重装系统时一键还原

## 搭配

- 本机约定：桌面软件一律 winget 安装，升级统一走 UniGetUI；Python 命令行工具例外，走 uv（见 [[工具总览与高效搭配]]）。

## 参考

- 仓库：<https://github.com/marticliment/UniGetUI>
