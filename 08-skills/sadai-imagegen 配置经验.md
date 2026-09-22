# sadai-imagegen 配置经验

日期：2026-09-02

**结论：本地 skill 能正常发 Image2 请求，但不能当作稳定可用的生图能力。** 问题在 SADAI Image2 上游响应链路，不是本机 Clash、密钥、模型名或请求参数。在上游恢复稳定前，不要再打付费 live 请求。

技能名称：`sadai-imagegen`  
安装：`~/.codex/skills/sadai-imagegen/`  
说明：`/home/user/Web/08-skills/sadai-imagegen 使用指南.md`

---

## 还能生图吗

分三层看：

| 层 | 状态 |
|---|---|
| 本机 skill / CLI / 密钥注入 | 可用。`--dry-run` 通过。当前默认打 `POST https://verysadai.com/v1/images/generations` |
| 上游一次成功 | 2026-09-02 下午，本机 `b64_json` 约 45–53 秒返回 PNG（`gpt-image-2-codex`，`1536×1024`，约 2 MB） |
| 稳定交付 | **否。** 同日 `url` 结果链 404；新系统再次 live 约 2 分钟 `The read operation timed out`，输出目录空 |

所以：不是“skill 坏了”，是“请求能出去，图片不能稳定回来”。新系统当前不可以当生产生图用。

---

## 已排除（不要再在这些点上耗额度）

- **Clash**：两个服务保持停止后仍然超时，不是代理拦截。
- **密钥**：Codex `config.toml` 已注入 `SADAI_API_KEY`，`ignore_default_excludes = true`，权限 `600`。缺密钥会立刻报 `no API key`，不会空等两分钟。
- **模型 / 参数**：`gpt-image-2`、`n=1`、`response_format=b64_json`。模型广场示例是 `quality=low`；较早 Image2 文档是 `auto`。未发 `size` / `aspect_ratio` / `resolution`。
- **对话 vs 生图**：Codex 对话可走 `sadai.cc`。gpt-image-2 出图按模型广场走 `https://verysadai.com/v1/images/generations`，不要打 `/chat/completions` 或 `/responses`。
- **分组**：文档写「全 pro 出图，非 plus；非 pro 分组成功率可能不足 50%」。超时/失败优先查令牌是否在 `codex_pro`。
- **`GET /v1/models`**：该主机 404，不能用来判断生图是否可用。

---

## 配置清单（本机已落地）

对话和生图不是同一条路由。

| 项 | 值 |
|---|---|
| Codex 对话 | `base_url = "https://sadai.cc/v1"` |
| Image2（模型广场 gpt-image-2） | `SADAI_IMAGE_BASE_URL = "https://verysadai.com/v1"` |
| Image2（较早文档，曾 404/超时） | `https://api.sadai.top/v1` |
| 密钥 | `~/.codex/config.toml` 的 `[shell_environment_policy.set] SADAI_API_KEY`，不要写进 skill / Git / 聊天 |
| 子进程环境 | `inherit = "core"` + `ignore_default_excludes = true`（否则 `*KEY*` 传不进 CLI） |
| 默认落盘 | `response_format=b64_json`（见下一节） |
| CLI 读超时 | `GENERATE_TIMEOUT_S = 180` |

改 `config.toml` 后必须新开一轮 Codex。

密钥不要再粘贴到文档或聊天。轮换后只改 `config.toml` 那一处。

---

## 上游响应链路上已经看到的两种失败

这两次失败形态不同，但都发生在 **SADAI 接受请求之后、本机拿到可写文件之前**。

### 1. HTTP 200 + 结果 URL 404

- `POST /images/generations` 约 50 秒返回 200。
- `data[0].url` 形如 `https://api.sadai.top/api/image-result/task_…/0/image_1.png`。
- 对该 URL 做 GET/HEAD，带或不带同一把 Bearer，都是 **404 `not found`**。
- 同一时段改 `b64_json` 能解出 PNG。说明生成算过，结果对象存储/回源 URL 不可用。

### 2. 读超时（新系统复测）

- 已用 `b64_json`，Clash 停，脚本语法正确。
- 等待约两分钟：`The read operation timed out`。
- 输出目录仍空。
- 这是连接已建立后读响应体超时，不是 DNS/TLS 立刻失败，也不是 401。

CLI 超时上限是 180 秒；约 120 秒就报 read timeout，更像对端没把完整 JSON（尤其是很大的 `b64_json`）传完。下午成功过一次，说明不是参数永久错误，而是上游不稳定。

---

## 本机 skill 怎么确认“还能发请求”（不产生图片费）

只允许这条，不要 live：

```bash
python3 "$HOME/.codex/skills/sadai-imagegen/scripts/image_gen.py" generate \
  --prompt "dry-run payload check" \
  --out /tmp/sadai-imagegen-dry.png \
  --dry-run
```

期望 JSON 仅含 `model` / `prompt` / `quality` / `n` / `response_format`，且 `response_format` 为 `b64_json`。

缺密钥的 live 才会立刻失败；**不要用 live 生图来确认配置**。

---

## 上游恢复后怎么验（只打一次）

等 SADAI 控制台日志显示 Image2 能完整返回后再测，仍用 `b64_json`，不要用 `url`。成功标准：

1. `POST` 在超时前返回 200；
2. `data[0].b64_json` 能解成 PNG/JPEG；
3. 文件写到 `--out`，目录非空。

若再出现 404 URL 或 read timeout，仍然记为上游问题，停止加试。

---

## 模型广场 gpt-image-2 页（2026-09-02 晚）

站点「调用示例」有多栏，**只有 image-generation 能出图**：

```text
POST https://verysadai.com/v1/images/generations
{"model":"gpt-image-2","prompt":"...","quality":"low","n":1}
```

不要用同一页的 openai-response / chat 模板。那些是把 `gpt-image-2` 误塞进 `/v1/chat/completions` 或 `/v1/responses`，prompt 还是「解释量子纠缠」，**不会生图**。

页面还写了：全 pro 出图，非 plus；非 pro 分组成功率可能不足 50%。本机已把 `SADAI_IMAGE_BASE_URL` 改到 `https://verysadai.com/v1`，quality 默认改为 **`high`**。今天上游异常，不打付费 live，明天再试。

---

## 不要做的事

- 不要为了“再试一次”连续 live 生图。
- 不要把超时理解成本机 Clash / 密钥错误而去改对话 `base_url`。
- 不要改官方 `~/.codex/skills/.system/imagegen/`，也不要在中转 session 里调内置 `image_gen`。
- 不要发 `size` / `aspect_ratio` / `resolution`。
- 不要把 gpt-image-2 打到 `/chat/completions` 或 `/responses`。
- 不要用 `GET /v1/models` 当健康检查。

---

## 当前状态一句话

`$sadai-imagegen` 配置和发起路径是通的；SADAI Image2 没有稳定把图片结果送回。新系统目前不能生图。暂停计费请求，等上游结果链路（对象 URL 或 `b64_json` 完整响应）恢复后再验一次。
