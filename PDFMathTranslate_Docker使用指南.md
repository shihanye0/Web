# PDFMathTranslate 使用指南（Ubuntu 版）

> 本文档介绍如何在 Ubuntu 上使用 PDFMathTranslate / Zotero PDF2zh，支持 Zotero 插件 + Docker Server（当前主用）、本地 Conda 环境、以及独立 GUI Docker 部署。

dp密钥：sk-3c044e00c14f492c83189b785075aa37 

---

## 〇、当前主用方案（2026-09-22）

**Zotero 插件 `pdf2zh@guaguastandup.com` v4.1.7 + Docker Server `zotero-pdf2zh` v4.1.7**

| 项目 | 值 |
|------|-----|
| 服务地址 | `http://127.0.0.1:8890` |
| 健康检查 | `http://127.0.0.1:8890/health` |
| 进度监控 | `http://127.0.0.1:8890/` |
| 容器名 | `zotero-pdf2zh` |
| 部署目录 | `/home/user/zotero-pdf2zh_docker/docker/` |
| 译文输出 | `/home/user/zotero-pdf2zh_docker/docker/translated/` |
| 配置目录 | `/home/user/zotero-pdf2zh_docker/docker/config/` |
| 自动启动 | Docker `enabled` + 容器 `restart: unless-stopped` |
| 翻译引擎镜像 | `awwaawwa/pdfmathtranslate-next:latest`（已预拉） |

### 插件侧配置

1. Zotero → **工具 → PDF2zh 首选项**
2. **Python Server IP**：`http://127.0.0.1:8890`（不要用 `localhost`，避免 IPv6 解析到 `::1`）
3. 点 **「检查连接」** → 显示连接成功即可
4. 翻译引擎选 `pdf2zh_next`；翻译服务按需配置（DeepSeek / siliconflowfree 等）

### Docker 管理命令

```bash
# 查看状态 / 日志
sg docker -c "docker ps --filter name=zotero-pdf2zh"
sg docker -c "docker logs -f zotero-pdf2zh"

# 启停
sg docker -c "docker start zotero-pdf2zh"
sg docker -c "docker stop zotero-pdf2zh"
sg docker -c "docker restart zotero-pdf2zh"

# 健康检查
curl -s http://127.0.0.1:8890/health

# 重建（改 Dockerfile 后）
sg docker -c "docker compose -f /home/user/zotero-pdf2zh_docker/docker/docker-compose.yaml --project-directory /home/user/zotero-pdf2zh_docker/docker up -d --build"
```

> 当前用户已在 `docker` 组，但已打开的终端可能未生效，用 `sg docker -c "..."` 最稳；或重新登录后直接 `docker ...`。

### 关键坑：FlClash / 系统代理与 Docker

**现象**：已开 FlClash（`http://127.0.0.1:7890`），但 `docker pull` 仍失败。

**原因**：FlClash 只代理系统/应用流量；**Docker 守护进程拉镜像走自己的网络**，不会自动使用系统代理。另外若把 `127.0.0.1:7890` 写进 `~/.docker/config.json` 的 proxies，构建容器里访问的是容器自己，apt/pip 会全部失败。

**正确做法（本机已采用）**：
1. 不给 Docker 配 `127.0.0.1` 代理
2. 基础镜像走 daocloud：`docker.m.daocloud.io/library/python:3.12-slim`
3. 翻译引擎镜像走 `docker.1ms.run/awwaawwa/pdfmathtranslate-next:latest`，再 `docker tag` 成 `awwaawwa/pdfmathtranslate-next:latest`
4. 构建时 apt / pip 用 USTC 镜像源
5. `server.zip` 用本地文件 `COPY` 进镜像，不在构建时访问 GitHub

### 关键坑：容器内必须 `--host 0.0.0.0`

官方 `entrypoint` 默认绑 `127.0.0.1`，Docker 端口映射进不去，宿主机 `curl` 会「连接被对方重置」。  
本机 Dockerfile 已改为：

```dockerfile
exec python /app/server/server.py --host 0.0.0.0 --enable_venv=False --check_update=False --port="${PORT:-8890}" --env_tool=auto
```

> 注意：server v4.1.7 的 `--env_tool` 只接受 `auto|uv|conda`，**没有** `system`。

### 本地 Python Server（备用，非 Docker）

```bash
cd /home/user/zotero-pdf2zh/server
/home/user/miniconda3/envs/pdf2zh/bin/python server.py --port=8890 --env_tool=conda --check_update=False
```

Server 包：`/home/user/zotero-pdf2zh/server/`（v4.1.7）

---

## 一、项目信息

- **PDFMathTranslate**：https://github.com/Byaidu/PDFMathTranslate
- **Zotero PDF2zh 插件**：https://github.com/guaguastandup/zotero-pdf2zh
- **插件文档**：https://zotero-pdf2zh.github.io/zh/
- **在线体验**：https://pdf2zh.com/
- **本机路径**：`/home/user/github-product/PDFMathTranslate/`
- **Conda 环境**：`pdf2zh`（Python 3.12）
- **插件 xpi**：`/home/user/.zotero/zotero/hc4uiqxc.default/extensions/pdf2zh@guaguastandup.com.xpi`

---

## 二、本地安装（Conda）

### 2.1 安装 Conda 环境

```bash
# 创建环境
conda create -n pdf2zh python=3.12 -y

# 激活环境
conda activate pdf2zh

# 安装依赖
pip install -e /home/user/github-product/PDFMathTranslate -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2.2 验证安装

```bash
conda activate pdf2zh
pdf2zh --help
```

---

## 三、独立 GUI Docker 部署（可选，端口 7860）

> 这是 PDFMathTranslate 自带 Gradio GUI，与 Zotero 插件用的 8890 Server **不是同一个**。

### 3.1 检查 Docker 是否安装

```bash
docker --version
```

如果未安装：

```bash
# 安装 Docker
sudo apt-get update
sudo apt-get install docker.io -y

# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker

# 将当前用户加入 docker 组（避免每次用 sudo）
sudo usermod -aG docker $USER
newgrp docker
```

### 3.2 拉取镜像

```bash
# 直连失败时用镜像站
docker pull byaidu/pdf2zh
# 或
docker pull docker.1ms.run/byaidu/pdf2zh
```

### 3.3 启动容器

```bash
docker run -d --name pdf-translate -p 7860:7860 --restart unless-stopped byaidu/pdf2zh
```

参数说明：
- `-d`：后台运行
- `--name pdf-translate`：给容器起个名字
- `-p 7860:7860`：端口映射
- `--restart unless-stopped`：开机自启

### 3.4 验证

```bash
docker ps
```

---

## 四、使用方法

### 4.1 CLI 命令行翻译

```bash
conda activate pdf2zh

# 基本翻译
pdf2zh paper.pdf

# 指定输出目录
pdf2zh paper.pdf --output ./translated

# 指定语言
pdf2zh paper.pdf --lang-in en --lang-out zh

# 使用 DeepL 翻译
pdf2zh paper.pdf --service deepl

# 使用 OpenAI 翻译
pdf2zh paper.pdf --service openai --api-key your-key

# 翻译指定页面
pdf2zh paper.pdf --pages 1-5

# 高精度模式
pdf2zh paper.pdf --mode precise
```

### 4.2 启动 GUI 界面

```bash
conda activate pdf2zh

# 启动交互式界面
pdf2zh --interactive

# 启动 Web 界面（可分享）
pdf2zh --share
```

访问 `http://localhost:7860` 即可使用。

### 4.3 Docker 方式访问

浏览器访问：

```
http://localhost:7860
```

### 4.4 Zotero 内使用（推荐）

1. 确保 `zotero-pdf2zh` 容器在跑（见「〇、当前主用方案」）
2. 在 Zotero 中选中条目 / 打开 PDF
3. 使用 PDF2zh 菜单翻译；进度可在 `http://127.0.0.1:8890/` 查看
4. 双语 PDF 输出到容器挂载目录 `.../docker/translated/`

---

## 五、翻译服务配置

### 5.1 支持的翻译服务

| 服务 | 命令 | 需要 API Key |
|------|------|-------------|
| Google | `--service google` | ❌ |
| DeepL | `--service deepl` | ✅ |
| OpenAI | `--service openai` | ✅ |
| Ollama | `--service ollama` | ❌（本地） |
| 百度翻译 | `--service baidu` | ✅ |
| 腾讯翻译 | `--service tencent` | ✅ |

### 5.2 环境变量配置

```bash
# OpenAI
export OPENAI_API_KEY="your-key"

# DeepL
export DEEPL_AUTH_KEY="your-key"

# 百度翻译
export BAIDU_APP_ID="your-app-id"
export BAIDU_SECRET_KEY="your-secret"
```

### 5.3 Zotero 插件侧（pdf2zh_next）

在「LLM API 配置管理」中新增服务：

| 服务类型 | 说明 |
|----------|------|
| `siliconflowfree` | 免费，无需 Key，可能漏译 |
| `deepseek` | 推荐，效果好，有缓存 |
| `openailiked` | 任意 OpenAI 兼容端点（填 URL + Key + Model） |
| `bing` / `google` | 免费但限流，并发建议 ≤2 |

当前本机插件已选 `deepseek`，需在 LLM API 配置里填好 API Key。

---

## 六、常用管理命令

### 6.1 Docker 管理

```bash
# ===== Zotero Server（8890，主用）=====
sg docker -c "docker ps --filter name=zotero-pdf2zh"
sg docker -c "docker logs -f zotero-pdf2zh"
sg docker -c "docker start/stop/restart zotero-pdf2zh"

# ===== 独立 GUI（7860，可选）=====
docker ps
docker stop pdf-translate
docker start pdf-translate
docker restart pdf-translate
docker logs -f pdf-translate
docker stop pdf-translate && docker rm pdf-translate
docker rmi byaidu/pdf2zh
```

### 6.2 端口冲突解决

```bash
# 查看占用
ss -tlnp | grep -E '8890|7860'

# Zotero Server 换端口（示例 9999）需两处一起改：
# 1) 启动参数 / compose ports
# 2) 插件里的 Python Server IP
```

---

## 七、常见问题

### Q1: Zotero 插件提示「连接失败 / 无法连接到 Server」

排查顺序：

1. **Server 是否在跑**：`curl -s http://127.0.0.1:8890/health`
2. **地址是否写对**：插件里填 `http://127.0.0.1:8890`（优先不用 `localhost`）
3. **端口是否被占**：`ss -tlnp | grep 8890`
4. **Docker 容器是否起来**：`sg docker -c "docker ps --filter name=zotero-pdf2zh"`
5. **看容器日志**：`sg docker -c "docker logs zotero-pdf2zh"`

### Q2: Docker 容器起来了但 curl 连不上

多半是容器内只绑了 `127.0.0.1`。确认 entrypoint 带 `--host 0.0.0.0`（本机已改）。

### Q3: 已开 FlClash / 代理，docker pull 仍失败

见上文「关键坑：FlClash / 系统代理与 Docker」。用镜像源，不要给 Docker 配 `127.0.0.1:7890`。

### Q4: 构建时 apt 报 `Unable to locate package curl`

构建容器里代理指到自己导致 apt 失败。删掉 `~/.docker/config.json` 里的 proxies，并在 Dockerfile 里用 USTC Debian 源。

### Q5: `server.py: error: argument --env_tool: invalid choice: 'system'`

v4.1.7 只支持 `auto|uv|conda`。改成 `--env_tool=auto` 并加 `--enable_venv=False`。

### Q6: Docker 容器启动失败

```bash
sg docker -c "docker logs pdf-translate"   # 或 zotero-pdf2zh
sudo systemctl restart docker
```

### Q7: 端口被占用

```bash
sudo lsof -i :7860
# 或
ss -tlnp | grep 7860
```

### Q8: Conda 环境找不到

```bash
conda activate pdf2zh
which python
```

### Q9: pip 安装太慢

```bash
pip install -e /home/user/github-product/PDFMathTranslate -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q10: `ModuleNotFoundError: No module named 'pdf2zh'`

2026-07-06 已遇到一次：`pdf2zh` 命令存在，但 editable 安装指向了旧路径 `/home/user/PDFMathTranslate`，真实仓库在 `/home/user/github-product/PDFMathTranslate`。

检查：

```bash
conda activate pdf2zh
python -m pip show pdf2zh
python -c "import pdf2zh; print(pdf2zh.__file__)"
cat /home/user/miniconda3/envs/pdf2zh/lib/python3.12/site-packages/_editable_impl_pdf2zh.pth
```

本机已修复为：

```text
/home/user/github-product/PDFMathTranslate
```

修复后验证：

```bash
conda activate pdf2zh
python -c "import pdf2zh; print(pdf2zh.__file__); print(pdf2zh.__version__)"
pdf2zh --help
```

### Q11: pdf2zh_next 首次翻译卡住 / assets download failed

首次要下字体和模型，可能 10–30 分钟。耐心等待，或看插件文档「网络问题」页手动预热。

---

## 八、快速参考卡

```
┌────────────────────────────────────────────────────────────┐
│              PDFMathTranslate / Zotero PDF2zh 速查           │
├────────────────────────────────────────────────────────────┤
│ Zotero Server:  http://127.0.0.1:8890   （主用）            │
│ 健康检查:        curl -s http://127.0.0.1:8890/health        │
│ 容器:            zotero-pdf2zh                              │
│ 自动启动:        restart=unless-stopped + docker enabled     │
├────────────────────────────────────────────────────────────┤
│ 翻译 PDF(CLI):   pdf2zh paper.pdf                           │
│ 启动 GUI:        pdf2zh --interactive                       │
│ 独立 Web GUI:    http://localhost:7860                       │
├────────────────────────────────────────────────────────────┤
│ 查看日志:        sg docker -c "docker logs -f zotero-pdf2zh"│
│ 启停:            sg docker -c "docker start/stop zotero-pdf2zh" │
└────────────────────────────────────────────────────────────┘
```

---

## 九、本机环境信息

| 项目 | 值 |
|------|-----|
| PDFMathTranslate 路径 | `/home/user/github-product/PDFMathTranslate/` |
| Zotero Server Docker 目录 | `/home/user/zotero-pdf2zh_docker/docker/` |
| 本地 Server 包（备用） | `/home/user/zotero-pdf2zh/server/` |
| Conda 环境 | `pdf2zh` |
| Python 版本 | 3.12 |
| Zotero 插件 | `pdf2zh@guaguastandup.com` v4.1.7 |
| Zotero Server | v4.1.7（Docker） |
| 系统 | Ubuntu 22.04 |

---

*文档更新日期：2026年9月22日*
*更新内容：补充 Zotero PDF2zh 插件 + Docker Server 主用方案、自动启动、FlClash/代理与 Docker 网络坑、`--host 0.0.0.0` 与 `--env_tool` 兼容性说明*