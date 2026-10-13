---
tags:
  - ssh
  - linux
  - terminal
  - tools
created: 2026-08-14
---

# SSH 终端工具速查

这四个工具覆盖 SSH 最常见的四件事：浏览文件、断线续连、查看负载、查磁盘空间。

## 一次安装

在服务器上执行：

```bash
sudo apt update
sudo apt install mc tmux btop ncdu
```

## mc：可视化浏览和管理文件

```bash
mc
```

- 方向键：选择文件或目录。
- `Enter`：进入目录或打开文件。
- `Tab`：切换左右面板。
- `F5`：复制；`F6`：移动；`F7`：新建目录。
- `F10` 或 `q`：退出。

若希望退出 `mc` 后，Shell 也停留在最后浏览的目录，在 `~/.bashrc` 加入：

```bash
source /usr/lib/mc/mc.sh
```

## tmux：断线后保留工作会话

```bash
tmux new -s work
```

在 tmux 中运行编译、下载或服务。即使 SSH 断开，这些命令也会继续运行；服务器重启除外。

```text
Ctrl-b d             暂时离开会话，任务继续在后台运行
tmux ls              列出会话
tmux attach -t work  回到 work 会话
Ctrl-b %             左右分屏
Ctrl-b "             上下分屏
```

说明：`Ctrl-b d` 表示先按并松开 `Ctrl-b`，再按 `d`。

## btop：查看服务器负载

```bash
btop
```

可视化查看 CPU、内存、磁盘 I/O、网络和进程。方向键选择进程，`q` 退出。发现异常进程时先确认服务用途，不要直接结束生产进程。

## ncdu：找出占满磁盘的目录

```bash
ncdu ~
ncdu /var
ncdu /var/log
```

方向键选择，`Enter` 进入目录，`q` 退出。优先从 `~`、`/var/log`、`/var/lib/docker` 等范围开始；遇到权限不足被跳过是正常的。先定位原因，再删除文件。

## 日常连接方式

```bash
ssh 用户名@服务器地址
tmux attach -t work || tmux new -s work
mc
```

需要排查性能时，在另一个 tmux 窗格启动 `btop`；磁盘空间紧张时，用 `ncdu /var` 排查。

## 暂不需要安装的工具

- `Mosh`：仅在网络经常断开或频繁切换网络时再考虑；它需要服务器开放 UDP 端口。
- `fzf`、Yazi：当前 `mc` 已覆盖目录浏览需求，先不增加工具和配置。

## 参考

- [Midnight Commander](https://midnight-commander.org/)
- [tmux](https://github.com/tmux/tmux/wiki/Getting-Started)
- [btop](https://github.com/aristocratos/btop)
