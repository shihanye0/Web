# Codex 桌面 App 换肤指南（Linux）

> 更新：2026-09-12 · 环境：Ubuntu 22.04 + 官方 ChatGPT/Codex App (deb) · 工具目录 `~/codex-skin/`
> 状态：✅ 已完成归档。12 套皮肤全部逐套截图验收，可读性加固内置于注入器（tint + inline scrim）。
> 当前默认皮肤 `skin-gothic-bright`（哥特晨光）；「ChatGPT (Dream Skin)」桌面图标启动即自动带皮肤。

## 一句话原理

官方 [Codex Dream Skin](https://github.com/Fei-Away/Codex-Dream-Skin)（MIT，14k+ Star）只有
macOS/Windows 版。本项目把它的主题包与渲染器移植到 Linux：启动 App 时附加本地调试端口，
通过 CDP 向渲染进程注入官方 CSS + 背景图。**不改二进制、不碰 `~/.codex` 配置、登录不丢，
重启即恢复原样。**

## 快速换肤（三条路任选）

```bash
codex-skin            # ⭐ 交互菜单：看清单输编号即可
codex-skin use skin-sakura        # 按名字切换
codex-skin off                    # 摘掉皮肤（App 保持运行）
codex-skin restore                # 恢复官方模式并重启 App
codex-skin status                 # 查看当前皮肤状态
```

- 应用列表里的 **「ChatGPT (Dream Skin)」** 图标启动即自动带皮肤（当前默认哥特晨光）；
- 用普通 ChatGPT 图标启动 = 官方无皮肤，此时跑一次 `codex-skin use skin-gothic-bright` 即可挂回；
- App 内 **Settings → 外观** 只能切浅色/深色/跟随系统，**Settings → Themes → Import**
  可粘贴 `codex-theme-v1:` 字符串导入官方格式**配色主题**（只有颜色没有壁纸），与注入皮肤互不冲突。

## 当前皮肤库（12 套，全部逐套截图验收 ✔）

| 目录名                            | 风格                    | 来源                                                                                                  |
| ------------------------------ | --------------------- | --------------------------------------------------------------------------------------------------- |
| `skin-gothic-bright` ⭐当前       | 黑金大教堂·提亮版，暗色，写代码最舒服   | 官方壁纸二次加工                                                                                            |
| `preset-arina-hashimoto`       | 粉色玫瑰人像，Dream-Skin 招牌款 | Dream-Skin 官方预设                                                                                     |
| `preset-gothic-void-crusade`   | 黑金哥特原版（已加固可读性）        | Dream-Skin 官方预设                                                                                     |
| `skin-cyberpunk-night`         | 赛博朋克霓虹夜城              | wallhaven 高收藏壁纸自制                                                                                   |
| `skin-sakura`                  | 樱花武士动漫风               | wallhaven 高收藏壁纸自制                                                                                   |
| `skin-aurora`                  | 极光雪山夜色                | wallhaven 高收藏壁纸自制                                                                                   |
| `sayram-lake`                  | 赛里木湖·天山清晨，清爽浅色        | [Charlielin-Fan/codex-sayram-lake-theme](https://github.com/Charlielin-Fan/codex-sayram-lake-theme) |
| `heige-miku`                   | 初音未来·葱色舞台，浅色          | [HeiGeAi/heige-codex-skin-studio](https://github.com/HeiGeAi/heige-codex-skin-studio)               |
| `heige-genshin-night`          | 原神·夜幕（钟离）             | 同上                                                                                                  |
| `heige-naruto-sasuke`          | 火影·佐助写轮眼              | 同上                                                                                                  |
| `kimetsu-thunder-breathing`    | 鬼灭之刃·雷之呼吸（善逸）         | [GodLei902/Codex-Kimetsu-Skin](https://github.com/GodLei902/Codex-Kimetsu-Skin)                     |
| `preset-terraria-forest-night` | 泰拉瑞亚像素森林之夜            | [pttydou/Codex-Terraria-Theme](https://github.com/pttydou/Codex-Terraria-Theme)                     |

> 注：鬼灭套的 `codex-skin use` 参数是目录名 `kimetsu-thunder-breathing`（列表里显示的 id 略不同）。
> HeiGeAi 工作室还有龙珠/鸣潮/深空等 12+ 套，想要哪套说一声即可批量搬运。

## 可读性加固（重点机制）

**问题**：暗色复杂壁纸上，侧边栏菜单文字和顶栏会被 wallpaper 淹没。
官方主题包格式里没有"调亮"开关（渲染器把 `--ds-theme-image-dim` 硬编码为 0）。

**方案**（`~/codex-skin/tools/inject.mjs` 内置）：`theme.json` 里 `"tint": "#RRGGBB"` 即启用。

1. `theme.json` 声明显式 `text` / `muted` / `panel` / `background` 配色，避免自适应配色在复杂壁纸上失灵；
2. 深色皮肤：`tint` 填深色（如 `#0D1020`），注入器对顶栏和侧边栏打 inline `!important` 渐变纱罩 +
   侧边栏文字强制白色 `-webkit-text-fill-color` + 描边阴影；
3. **浅色皮肤**：`tint` 填浅色并加 `"tintText"` 指定深色文字，纱罩同理。
   已配置：春樱 `#FDF3F8`/`#3D3648` · 桥本有菜 `#FFF2F5`/`#4A3A40` · 初音 `#F2FBFD`/`#1F4A5A` · 赛里木湖 `#F4FAFD`/`#1E4A5E`；
4. 纱罩覆盖的选择器：顶栏菜单条其实是 `div[class*="_ApplicationMenuTopBar_"]`（不是 header！），
   另含 `header[data-ds-part="header"]`、`aside.app-shell-left-panel`；
5. 内置 3 秒定时重申防 React 冲掉，且带**代数令牌**（`__CODEX_SKIN_SCRIM_TOKEN__`）——
   切换皮肤后旧皮肤的定时器自动自杀，不会互相打架；`codex-skin off` 时令牌自增并清除
   inline 残留，官方外观完整还原。

**踩坑记录**：① 官方 CSS 选择器带 `html[data-dream-skin="active"]` 前缀，普通补丁规则的优先级打不过，
必须 inline `!important`；② 侧边栏文字被 App token 样式在 paint 层覆盖，只有 `-webkit-text-fill-color`
能压住；③ 顶部菜单栏（文件/编辑/窗口控制按钮）不是 `<header>` 而是 `_ApplicationMenuTopBar_` 这个 div，
选择器打错地方就白干；④ 旧皮肤的 scrim 定时器不会自动消失，必须用代数令牌让旧定时器退出。

## 添加自定义皮肤

```bash
mkdir -p ~/codex-skin/skins/my-skin
cp 你喜欢的图.jpg ~/codex-skin/skins/my-skin/background.jpg
# 抄一份别人的 theme.json 改名（image 对应文件名）
codex-skin use my-skin
```

- 图片建议横版 16:9、≤5MB；暗色复杂图请把 `theme.json` 的 `tint` 字段带上（见上）；
- 关键字段：`name` / `tagline` / `quote`（首页大字）/ `appearance`（auto/light/dark）/
  `art.focusX,focusY`（画面焦点）/ `colors.accent`（主题色）。

## 故障排查

| 症状 | 处理 |
|---|---|
| 重启 App 后皮肤没了 | 正常现象，`codex-skin use <名字>` 重挂，或用 Dream Skin 图标启动 |
| 切换时卡在"重启中" | App 冷启动慢，注入器会自动等页面就绪（最多 30s），再跑一次即可 |
| 皮肤错乱/样式半失效 | `codex-skin off` 恢复；App 升级后重新从上游拉 `tools/renderer-inject.js` 和 `tools/dream-skin.css` |
| 想彻底回官方 | `codex-skin restore` |
| 侧边栏文字又看不清了 | 检查 theme.json 是否带 `tint`；可调大 `inject.mjs` 里 scrim 的 alpha |

## 找更多皮肤的地方

- [awesome-codex-themes](https://github.com/mcpso/awesome-codex-themes) — 主题大合集（CLI/桌面/生成器全都有）
- [GitHub Topic: codex-theme](https://github.com/topics/codex-theme) — 30+ 换肤仓库
- [DreamSkin.cc](https://dreamskin.cc) — 官方皮肤市场（App 内一键套用，macOS/Win）
- [HeiGeAI 工作室](https://github.com/HeiGeAi/heige-codex-skin-studio) — 12+ 动漫风预设
- [Codex-Terraria-Theme](https://github.com/pttydou/Codex-Terraria-Theme) — 泰拉瑞亚 44 生态皮肤
- [wallhaven.cc](https://wallhaven.cc) — 壁纸库，搜 toplist 按收藏排序，任意图都能做成皮肤

## 文件布局

```
~/codex-skin/
├── bin/codex-skin          # 主控命令（菜单/切换/恢复）
├── tools/
│   ├── renderer-inject.js  # Dream-Skin 官方渲染器（上游同步）
│   ├── dream-skin.css      # 官方 Safe CSS（上游同步）
│   ├── inject.mjs          # Linux 版 CDP 注入器（含可读性加固）
│   └── shot.mjs            # 验收截图工具
├── skins/<名字>/            # theme.json + 背景图 (+ 可选 overlay.css)
└── state.json              # 注入会话状态
```
