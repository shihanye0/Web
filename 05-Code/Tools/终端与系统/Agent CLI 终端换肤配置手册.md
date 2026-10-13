# Agent CLI 终端换肤配置手册（可移植）

> 更新：2026-09-12 · 已归档 ✅ · 适用：Ubuntu/Debian 系 + bash + Terminator · 主题：**Catppuccin Mocha**
> 用途：给另一台电脑上的 ZCode/agent 参照执行，从零复刻一套统一的终端 + CLI 换肤。
> 原则：全部用户级安装（`~/.local` + 用户配置），不动系统，改前必备份。

## 0. 前置检查

```bash
# 确认终端类型（本手册以 Terminator 为例；GNOME Terminal/Kitty 等配色值通用，写法不同）
ps -e -o comm= | grep -i -E "terminator|gnome-terminal|kitty|alacritty|ghostty"
# 确认 jq（状态栏脚本依赖）
command -v jq || sudo apt install -y jq   # 或者用户级: 下载静态二进制到 ~/.local/bin
```

## 1. Terminator 终端配色

备份后把颜色写进 `~/.config/terminator/config` 的 `[[default]]` profile：

```ini
[profiles]
  [[default]]
    background_color = "#1e1e2e"
    foreground_color = "#cdd6f4"
    cursor_color = "#f5e0dc"
    use_theme_colors = False
    palette = "#45475a:#f38ba8:#a6e3a1:#f9e2af:#89b4fa:#f5c2e7:#94e2d5:#bac2de:#585b70:#f38ba8:#a6e3a1:#f9e2af:#89b4fa:#f5c2e7:#94e2d5:#a6adc8"
```

要点：`use_theme_colors = False` 必须有，否则自定义色不生效；palette 是冒号分隔的 16 色。
重启 Terminator 生效。备份命令：`cp ~/.config/terminator/config{,.bak-$(date +%Y%m%d-%H%M)}`

## 2. starship 提示符（免 sudo 用户级安装）

```bash
cd /tmp
curl -sfLO "https://github.com/starship/starship/releases/latest/download/starship-x86_64-unknown-linux-gnu.tar.gz"
tar xzf starship-x86_64-unknown-linux-gnu.tar.gz && mkdir -p ~/.local/bin && mv starship ~/.local/bin/
# 接入 bash（若用 zsh 则 init zsh）
printf '\n# starship 提示符\ncommand -v starship >/dev/null && eval "$(starship init bash)"\n' >> ~/.bashrc
```

新开终端生效，提示符自动带 git 分支/语言图标。

## 3. Codex CLI 主题

```bash
# config.toml 末尾追加（无 [tui] 段时）
grep -q "^\[tui\]" ~/.codex/config.toml || printf '\n[tui]\ntheme = "catppuccin-mocha"\n' >> ~/.codex/config.toml
```

- 内置 32 套，CLI 里 `/theme` 实时预览；自定义：TextMate `.tmTheme` 丢 `~/.codex/themes/`；
- 选 `"catppuccin-mocha"` 是为了和终端配色一致；浅色终端用 `"catppuccin-latte"`。

**全部有效主题 ID**（2026-09-12 从 v0.153.4 二进制提取；写错名字会静默回退默认）：

```
catppuccin-latte  catppuccin-frappe  catppuccin-macchiato  catppuccin-mocha
dracula  nord  zenburn  dark-neon  sublime-snazzy  github  inspired-github
gruvbox-dark  gruvbox-light  solarized-dark  solarized-light
one-half-dark  one-half-light  coldark-cold  coldark-dark
monokai-extended-origin  monokai-extended-bright  monokai-extended-light
base16-256  base16-eighties  base16-eighties-dark  base16-mocha-dark
base16-ocean-dark  base16-ocean-light
```

本机当前：`theme = "dracula"`（2026-09-12 起）。

## 4. Claude Code + Cursor CLI 状态栏（共用一份脚本）

写 `~/.claude/statusline.sh`（Claude Code 与 Cursor CLI 的 payload 格式相同，共用）：

```bash
#!/usr/bin/env bash
# 状态栏：模型 | 目录 | git 分支 | 上下文进度条
input=$(cat)
model=$(echo "$input" | jq -r '.model.display_name // "AI"')
dir=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // "~"' | sed "s|$HOME|~|")
pct=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
branch=$(git -C "$(echo "$input" | jq -r '.workspace.current_dir // .cwd // "."')" branch --show-current 2>/dev/null)

BAR_WIDTH=12
FILLED=$((pct * BAR_WIDTH / 100)); EMPTY=$((BAR_WIDTH - FILLED))
BAR=""
[ "$FILLED" -gt 0 ] && printf -v F "%${FILLED}s" && BAR="${F// /█}"
[ "$EMPTY" -gt 0 ] && printf -v E "%${EMPTY}s" && BAR="${BAR}${E// /░}"

printf "\033[1;35m%s\033[0m \033[2m│\033[0m \033[1;34m%s\033[0m" "$model" "${dir##*/}"
[ -n "$branch" ] && printf " \033[2m│\033[0m \033[1;32m %s\033[0m" "$branch"
printf " \033[2m│\033[0m \033[33m%s %d%%\033[0m" "$BAR" "$pct"
```

```bash
chmod +x ~/.claude/statusline.sh
# 测试: echo '{"model":{"display_name":"T"},"workspace":{"current_dir":"/tmp"},"context_window":{"used_percentage":30}}' | ~/.claude/statusline.sh
```

然后分别合并进 `~/.claude/settings.json` 和 `~/.cursor/cli-config.json`（**JSON merge，别整文件覆盖**）：

```json
"statusLine": { "type": "command", "command": "~/.claude/statusline.sh", "padding": 0 }
```

## 5. Gemini CLI 主题扩展

```bash
mkdir -p ~/.gemini/extensions
git clone --depth 1 https://github.com/jackwotherspoon/gemini-cli-themes ~/.gemini/extensions/gemini-cli-themes
# settings.json 增加（扩展提供 6 套: Catppuccin Mocha / Gruvbox Dark / Nord / Tokyo Night / Monokai / Nanobanana）
# "theme": "Catppuccin Mocha"
```

`gemini` 里 `/theme` 可随时切换。

## 6. 验收清单

- [ ] Terminator 重开后：深蓝底、柔和字、新提示符（starship）
- [ ] `codex` 启动无报错、配色协调（`/theme` 可见当前主题）
- [ ] `claude` / cursor cli 底部出现状态栏（模型+目录+分支+进度条）
- [ ] `gemini` 启动配色为 Catppuccin Mocha

## 7. 备份约定

改动前对每个要动的文件做 `cp file file.bak-$(date +%Y%m%d-%H%M)`。
本机（2026-09-12）备份后缀：`.bak-20260912-181906`。

---

相关文档：Codex **桌面 App** 的换肤（另一套体系，需 CDP 注入）见同目录
《Codex 桌面 App 换肤指南.md》，工具与 12 套皮肤需从原机拷贝 `~/codex-skin/` 整个目录。
