# sadai-imagegen 使用指南

## 概述

**技能名称：`sadai-imagegen`**

Codex 在 SADAI 中转（非官方 ChatGPT 登录）下的 Image2 生图 / 改图 skill。官方 `$imagegen` 的内置 `image_gen` 工具只在 ChatGPT 托管会话里出现；换中转后那把工具不会挂进 session。本 skill 用捆绑 CLI 直接打 SADAI Image2。

支持平台：Codex（SADAI / 自定义 OpenAI 兼容中转）。

安装位置：`~/.codex/skills/sadai-imagegen/`

## 安装状态

| 平台 | 状态 |
|------|------|
| Codex | ✅ 已安装（个人 skill） |
| Claude Code | ❌ 未安装（本 skill 为 Codex 中转路径） |
| 官方 `$imagegen` | 仍在 `~/.codex/skills/.system/imagegen/`，中转下不要用 |

## 什么时候用

在 Codex 里说：

```
$sadai-imagegen 生成一张……
生一张产品海报……
改这张图：把背景换成黄昏
```

触发词：`sadai-imagegen`、生图、改图、imagegen、gpt-image-2。

## 不要用的时候

- 视频：`/v1/videos`、`sadai-video`、Seedance（另一套异步 API）
- 仓库里已有 SVG / HTML / CSS，应该改源文件而不是出位图
- 已经 `codex login` 官方帐号、明确要走托管 `image_gen`

## 使用方式

### 自然语言（推荐）

新开一轮 Codex 后直接说：

```
$sadai-imagegen 一张干净明亮的产品海报，玻璃香水瓶，柔和窗光，留出上方文案负空间，无水印无品牌字
```

Agent 会整形提示词，调用：

```bash
python3 "$HOME/.codex/skills/sadai-imagegen/scripts/image_gen.py" generate \
  --prompt "……" \
  --out "$CODEX_HOME/generated_images/output.png"
```

改图（至少一张参考图，本地文件或 `https://` URL）：

```
$sadai-imagegen 只换背景为暖色日落，产品边缘保持不变
```

对应：

```bash
python3 "$HOME/.codex/skills/sadai-imagegen/scripts/image_gen.py" edit \
  --prompt "……" \
  --image /path/to/reference.png \
  --out "$CODEX_HOME/generated_images/edited.png"
```

### 常用参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `--model` | `gpt-image-2` | 上游实际可能回 `gpt-image-2-codex` |
| `--quality` | `high` | Skill 默认；模型广场示例是 `low` |
| `--n` | `1` | 最多 6 |
| `--response-format` | `b64_json` | 本机解码落盘 |
| `--force` | 关 | 覆盖已有 `--out` |
| `--dry-run` | 关 | 只打印 JSON，不联网、不读密钥 |
| `--size` | 忽略 | Image2 不认尺寸字段；比例写进提示词 |

不要发 `size` / `aspect_ratio` / `resolution`。想要 16:9 海报或方形图标，写在 prompt 里。

## 配置（本机已做）

对话和生图不是同一条 Base URL。

| 用途 | Base URL |
|------|----------|
| Codex 对话 | `https://sadai.cc/v1` 或 `verysadai.com` 的 `/responses` |
| gpt-image-2 出图 | `https://verysadai.com/v1/images/generations` |

密钥只走环境变量，优先级：`SADAI_API_KEY` → `NEW_API_KEY` → `OPENAI_API_KEY`。不要把密钥写进 skill、仓库或聊天。

Codex 子进程默认 `inherit = "core"`，读不到带 `KEY` 的变量。本机已在 `~/.codex/config.toml` 写入：

- `ignore_default_excludes = true`
- `SADAI_API_KEY`（仅本机配置文件，权限 `600`）
- `SADAI_IMAGE_BASE_URL = "https://verysadai.com/v1"`

改配置后必须**新开一轮 Codex**。

## 实测（2026-09-02）

- 下午本机 `b64_json` 曾成功：约 45–53 秒 200，模型 `gpt-image-2-codex`，样张 `1536×1024` PNG。
- 同日 `url` 结果链 404；新系统复测 Clash 已停、参数正确，约 2 分钟 `The read operation timed out`，输出目录空。
- **当前不能当作稳定生图。** 配置经验与停测约定见同目录 `sadai-imagegen 配置经验.md`。
- `GET /v1/models` 在 Image2 主机上 404，不要用模型列表探测。

样张路径（仅下午成功那张）：`~/.codex/generated_images/sadai-imagegen-sample.png`

## 和官方 $imagegen 的区别

| | 官方 `$imagegen` | `sadai-imagegen` |
|--|--|--|
| 鉴权 | ChatGPT / Codex 登录 | SADAI API Key |
| 工具 | 内置 `image_gen` | `scripts/image_gen.py` |
| 中转 | 不可用 | 这条路径 |
| 尺寸字段 | CLI 可发 `size` | 禁止发送，服务端自定 |
| 落盘 | `$CODEX_HOME/generated_images/` | 同上，但必须 `b64_json` |

## 故障排查

| 现象 | 处理 |
|------|------|
| `no API key in the environment` | 新开 Codex；检查 `config.toml` 的 `SADAI_API_KEY` |
| `HTTP 404 downloading image` | 不要用 `url`；确认 CLI 默认已是 `b64_json` |
| 打到 `/chat/completions` 或 `/responses` | 那是页面通用模板，不会出图；只用 `/images/generations` |
| 打到 `sadai.cc` | 那是 Codex 对话；出图用 `verysadai.com/v1/images/generations` |
| 内置 `image_gen` 找不到 | 正常；中转下改用 `$sadai-imagegen` |
| 401 / 额度不足 | SADAI 控制台查密钥和余额 |

卸载：删除 `~/.codex/skills/sadai-imagegen/`。不要改官方 `~/.codex/skills/.system/imagegen/`。
