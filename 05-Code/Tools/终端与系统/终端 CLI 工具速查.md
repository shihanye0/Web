---
tags:
  - ubuntu
  - cli
  - terminal
  - tools
  - kubernetes
created: 2026-09-12
---

# 终端 CLI 工具速查

2026-09-12 配置的一批终端工具，全部装在 `~/.local/bin`（用户目录，不碰系统）。与 [[Ubuntu 生产力工具速查]] 的 GUI 工具互补。当前机器为 Ubuntu 22.04，glibc 2.35——**下载预编译二进制时选 musl 静态版**，gnu 版会报 `GLIBC_2.38+ not found`。

## 总览

| 分组 | 工具 | 入口 |
| --- | --- | --- |
| Shell 体验 | zoxide · atuin · direnv · yazi | `z` · `Ctrl+R` · 自动 · `y` |
| Git / Docker | lazygit · delta · lazydocker · dive · gtrash | `lazygit` · 自动 · `lazydocker` · `dive` · `gtrash` |
| Kubernetes | k9s · kind | `k9s` · `kind` |
| 开发 / AI | uv · just · hyperfine · witr · herdr · llmfit · nvitop · topgrade | 见下文 |
| 学术 | papis · artui | `papis` · `artui` |

配置文件位置：shell 挂钩在 `~/.config/shell/{bashrc,zshrc}.extra` 和 `common.sh`；git 的 delta 配置在 `git config --global`；papis 在 `~/.config/papis/config`。

## Shell 体验

### zoxide：智能 cd

记录去过的目录，之后用目录名片段直接跳转，不用再敲完整路径。已挂到 bash/zsh。

```bash
z proj        # 跳到最常去的名字含 proj 的目录
z foo bar     # 多个关键词缩小匹配
zi            # 交互式选择（配合 fzf）
```

### atuin：历史命令超进化

历史命令存进 SQLite，`Ctrl+R` 模糊搜索、显示目录和退出码、可多机同步。已导入旧的 bash 历史，并接管了 `Ctrl+R` 和上箭头（绑定顺序在 fzf 之后，atuin 生效）。

```bash
Ctrl+R        搜索历史（输入关键词实时过滤，Tab 预览，回车执行）
atuin stats   查看统计
atuin search -c "$(pwd)" git   # 只搜当前目录下敲过的 git 命令
```

不想让它接管上箭头：把 `~/.config/shell/bashrc.extra` 里的 `atuin init bash` 改成 `atuin init bash --disable-up-arrow`。注册账号后 `atuin register` 可多机同步，纯本地用无需注册。

### direnv：目录级环境变量

进入含 `.envrc` 的目录自动加载其中环境变量，离开自动卸载。适合项目各自的 API key、虚拟机激活等。

```bash
echo 'export FOO=bar' > .envrc
direnv allow     # 首次必须手动批准，之后进目录自动生效
```

### yazi：终端文件管理器

Rust 异步实现，速度极快，支持图片预览、压缩包预览（已装 p7zip-full）。**用 `y` 启动**（包装函数），退出时 shell 会自动 cd 到你浏览的目录。

```text
y             启动（退出后跟随目录）
j/k/g/G       上下移动 / 顶部底部
o / O         用编辑器打开 / 选择程序打开
Space         多选，y/p/x  复制 / 粘贴 / 删除
q             退出
```

## Git / Docker

### lazygit：git 图形界面

终端里的 git TUI：暂存/提交/分支/rebase/cherry-pick 全部按键化，diff 实时预览。

```text
lazygit       在仓库根目录启动
Space         暂存/取消暂存文件
c             提交
Shift+P / Shift+F   push / pull
?             查看全部快捷键
```

### delta：git diff 美化

已配置为全局 pager 和 diff 渲染器（`git config --global core.pager delta`），带语法高亮、行号、side-by-side。`git diff`、`git log -p`、`git show` 自动生效，无需额外操作。想临时绕开：`git --no-pager diff`。

### lazydocker：Docker 图形界面

一屏看容器/镜像/卷/日志/资源占用，支持重启、进 shell。

```text
lazydocker    启动（需 docker 组权限，已配置）
←/→           切换 面板
Enter         查看日志 / 详情
r             重启容器，s 进入 shell
```

### dive：镜像逐层分析

看每一层改了哪些文件、占多少空间，标出浪费的空间（如重复的依赖层）。

```bash
dive 镜像名          # 逐层浏览，Ctrl+U 聚焦"浪费空间"
dive build           # 分析当前目录 Dockerfile 的构建结果
```

### gtrash：可恢复的 rm

符合 freedesktop 回收站规范，`rm` 手滑还有后悔药。没有动系统 `rm`，需主动使用。

```bash
gtrash put 文件      # 移入回收站（替代 rm 的第一步）
gtrash restore       # 交互式找回
gtrash summary       # 查看各回收站占用
gtrash prune --days 30   # 清理 30 天前的
```

## Kubernetes

### k9s：集群 TUI

资源全览、实时日志、端口转发、进入容器，比 `kubectl get/edit/logs` 快得多。

```text
k9s                 启动（读取 ~/.kube/config）
: Pods / : deploy   冒号输入资源类型跳转
: ctx               切换集群 context
l                   看日志，s 进 shell，d describe
Ctrl+C              退出
```

### kind：本地集群

本机 `dev` 集群（k8s v1.37，容器名 `dev-control-plane`）已创建，kubeconfig 在 `~/.kube/config`。

```bash
kubectl get nodes                    # 验证集群 Ready
kind delete cluster --name dev       # 删除
kind create cluster --name dev       # 重建（约 2 分钟）
docker stop dev-control-plane        # 临时停机，用前 start
```

接真集群时：把 kubeconfig 合并进 `~/.kube/config`（或设 `KUBECONFIG` 多路径），k9s 里 `: ctx` 切换。

## 开发 / AI

### uv：Python 包管理

比 pip + venv 快一个数量级，自动管理 Python 版本。

```bash
uv venv && source .venv/bin/activate   # 建环境
uv pip install requests                # 装包
uv run script.py                       # 免手动激活直接跑
uv tool install xxx                    # 安装 CLI 工具（隔离环境）
```

### just：现代 make

项目里写 `justfile` 定义任务，比 make 语法友好。项目根目录示例：

```makefile
dev:
    python main.py

test:
    pytest -v
```

```bash
just          # 列出所有任务
just test     # 执行
```

### hyperfine：命令基准测试

自动多次运行、预热、统计分布，比较两个命令谁快。

```bash
hyperfine 'rg pattern' 'grep -r pattern'    # 对比两个搜索工具
hyperfine --warmup 3 'some-cmd'             # 带预热
```

### witr：进程溯源

回答"这个端口/进程/容器是谁启动的"——沿父子链向上追溯，直到找出源头命令和配置文件。

```bash
witr 8080             # 谁在监听 8080
witr <PID>            # 这个进程从哪来
witr --output json    # 供脚本使用
```

### herdr：编码 agent 运行时

2026 年的 multi-agent 编排 TUI，把多个编码 agent（claude code、codex 等）放到统一界面并行管理、观察状态。

### llmfit：本地跑模型体检

扫描本机硬件（32G 内存 + RTX 4070 12G），列出哪些开源模型能跑、量化到什么档位。

```bash
llmfit                # 列出适配本机的模型
llmfit qwen3-32b      # 查特定模型
```

### nvitop：GPU 监控

比 `nvidia-smi` 直观：进程级占用、显存趋势图、可直接 kill 进程。

```text
nvitop        全屏监控
a             查看所有用户的进程
k             杀掉选中的进程
```

### topgrade：一键全量升级

按顺序升级 apt、snap、npm 全局包、uv/cargo 工具、rustup 等，一条命令不用挨个跑。

```bash
topgrade              # 全部升级（会逐项询问）
topgrade -y           # 跳过确认
topgrade --edit-config    # 配置要跳过的环节
```

## 学术

### papis：文献管理

CLI 文献库，配合 LaTeX 工作流（对比 Zotero 的 GUI）。库目录：`~/Documents/papers/library`，配置：`~/.config/papis/config`。

```bash
papis add paper.pdf --from doi:10.xxxx    # 按 DOI 自动抓元数据入库
papis open                                # 打开 PDF
papis edit                                # 编辑文献信息（yaml）
papis explore                             # 交互式浏览
```

### artui：终端刷 arXiv

TUI 浏览最新 arXiv 论文，按分类/关键词过滤、标记已读。

## 维护备忘

- 所有二进制在 `~/.local/bin`（已在 PATH 最前），升级用 `topgrade` 或重下 GitHub Release。
- 新装预编译工具选 `x86_64-unknown-linux-musl` 版（本机 glibc 2.35 过旧）。
- sudo 图形弹窗方案：`SUDO_ASKPASS=/tmp/askpass.sh sudo -A apt install 包名`（zenity askpass 脚本）。
- docker 组已加入（2026-09-12），重新登录后 `docker`/`kind` 免 sudo。

## 参考

- [zoxide](https://github.com/ajeetdsouza/zoxide) · [atuin](https://github.com/atuinsh/atuin) · [direnv](https://github.com/direnv/direnv) · [yazi](https://github.com/sxyazi/yazi)
- [lazygit](https://github.com/jesseduffield/lazygit) · [delta](https://github.com/dandavison/delta) · [lazydocker](https://github.com/jesseduffield/lazydocker) · [dive](https://github.com/wagoodman/dive) · [gtrash](https://github.com/umlx5h/gtrash)
- [k9s](https://github.com/derailed/k9s) · [kind](https://github.com/kubernetes-sigs/kind)
- [uv](https://github.com/astral-sh/uv) · [just](https://github.com/casey/just) · [hyperfine](https://github.com/sharkdp/hyperfine) · [witr](https://github.com/pranshuparmar/witr) · [herdr](https://github.com/herdrdev/herdr) · [llmfit](https://github.com/AlexsJones/llmfit) · [nvitop](https://github.com/XuehaiPan/nvitop) · [topgrade](https://github.com/topgrade-rs/topgrade)
- [papis](https://github.com/papis/papis) · [arTui](https://github.com/fjonasALICE/arTui)
