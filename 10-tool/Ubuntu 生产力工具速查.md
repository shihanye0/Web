---
tags:
  - ubuntu
  - linux
  - productivity
  - tools
created: 2026-08-24
---

# Ubuntu 生产力工具速查

这套工具覆盖剪贴板历史、窗口分屏、电脑间文件同步、手机联动和远程桌面。当前机器为 Ubuntu 22.04（GNOME 42、X11）。

## 当前已配置

| 工具 | 状态 | 入口 |
| --- | --- | --- |
| CopyQ | 已运行、开机启动 | `Win+V` |
| Tiling Shell | 已安装并启用 | 重载 GNOME Shell 后生效 |
| Syncthing | 已开机启动 | http://127.0.0.1:8384/ |
| KDE Connect | 已安装，待与手机配对 | 应用菜单中的 `KDE Connect` |
| Remmina | 已安装 | 应用菜单中的 `Remmina` |

## CopyQ：剪贴板历史

按 `Win+V` 打开复制历史；单击条目可重新放回剪贴板，再用普通 `Ctrl+V` 粘贴。它会在登录后自动运行，并保留最近 200 条记录。

常用操作：

```text
Win+V       打开或关闭历史窗口
输入关键字  搜索历史
右键条目    删除或固定常用内容
```

不要把密码、恢复码或其他长期敏感信息留在历史里；用完后从 CopyQ 中删除。

## Tiling Shell：窗口分屏

Tiling Shell 给 GNOME 增加类似 Windows 11 的分屏布局。首次安装后，在 X11 会话按 `Alt+F2`，输入 `r` 后回车重载 GNOME Shell；也可注销后重新登录。

之后把窗口拖到屏幕边缘或顶部，按出现的布局提示选择分屏位置。需要调整布局、间距和快捷键时，打开“扩展管理器”，在 `Tiling Shell` 右侧点设置按钮。

先从左右两栏分屏开始；自动平铺等更激进的行为按实际习惯再启用。

## Syncthing：多台电脑自动同步

Syncthing 已作为当前用户服务开机启动。默认同步目录是：

```text
/home/user/Sync
```

把需要跨设备同步的文件放入该目录。另一台电脑也安装并启动 Syncthing 后：

1. 两台电脑分别打开 `http://127.0.0.1:8384/`。
2. 在“操作”中查看本机设备 ID。
3. 双方点击“添加远程设备”，互填设备 ID，并接受配对请求。
4. 共享 `Default Folder`；另一台设备选择本地保存目录后确认。

网页状态显示 `Up to Date` 表示同步完成。不要一开始同步整个“桌面”或“文档”目录，先用 `~/Sync` 验证没有冲突后再添加其他目录。

```bash
systemctl --user status syncthing.service
systemctl --user restart syncthing.service
```

## KDE Connect：安卓手机与电脑联动

电脑和手机连到同一 Wi-Fi。手机安装 KDE Connect 后：

1. 打开电脑端 `KDE Connect`。
2. 在设备列表中选择手机，发送配对请求。
3. 在手机上确认配对。
4. 按需开启文件传输、通知、剪贴板和媒体控制插件。

配对后可直接互传文件、在电脑查看手机通知。剪贴板同步会传输正在复制的文本，涉及敏感内容时应关闭该插件。

## Remmina：远程连接 Windows 或服务器

打开 Remmina，点击新建连接：

```text
Windows 电脑：协议选 RDP，填写主机名或 IP、用户名和密码
Linux 服务器：协议选 SSH，填写主机名和用户名
```

首次连接先核对目标地址和证书指纹。非个人设备不要保存远程密码。

## 参考

- [CopyQ](https://github.com/hluk/CopyQ)
- [Tiling Shell](https://extensions.gnome.org/extension/7065/tiling-shell/)
- [Syncthing 入门](https://docs.syncthing.net/intro/getting-started)
- [KDE Connect](https://apps.kde.org/kdeconnect/)
- [Remmina](https://remmina.org/)
