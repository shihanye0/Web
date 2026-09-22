---
title: "EasyPaper 论文翻译与知识库工具"
date: 2026-07-07
status: active
tags: [code, paper, translation, obsidian, knowledge-base]
---

# EasyPaper 论文翻译与知识库工具

## 项目概述

EasyPaper 是一个本地可部署的论文阅读工具，用来把英文论文 PDF 翻译成中文，同时尽量保留原 PDF 的排版、图片和公式。它底层使用 `pdf2zh / PDFMathTranslate`，在翻译之外还支持 AI 重点高亮、论文知识抽取、知识图谱、闪卡复习，以及导出或同步到 Obsidian。

本机已找到的安装位置：

- 项目路径：`/home/user/github-product/EasyPaper`
- GitHub：`https://github.com/jiaotangxq/easypaper.git`
- Conda 环境：`/home/user/miniconda3/envs/easypaper`
- 中文 README：`/home/user/github-product/EasyPaper/README_zh.md`

## 核心用途

- 上传本地 PDF，输出中文翻译 PDF。
- 粘贴 PDF、arXiv、OpenReview 链接，自动导入并处理。
- 保留论文排版、图片、公式。
- 可选生成中英对照版 PDF。
- 用 AI 标注关键句子：核心结论、方法创新、关键数据。
- 从论文中抽取实体、关系、研究发现、闪卡。
- 导出 EasyPaper JSON、Obsidian Vault、BibTeX、CSL-JSON、CSV。
- 支持直接同步论文笔记和实体笔记到本机 Obsidian vault。

## 快速启动：Docker 方式

适合只是本地试用。

```bash
cd /home/user/github-product/EasyPaper
cp backend/config/config.example.yaml backend/config/config.yaml
```

编辑配置文件：

```bash
nano backend/config/config.yaml
```

至少需要设置：

```yaml
llm:
  api_key: "YOUR_API_KEY"
  base_url: "https://openrouter.ai/api/v1"
  model: "gemini-2.5-flash"
  judge_model: "gemini-2.5-flash"

security:
  secret_key: "CHANGE_THIS_TO_A_SECURE_SECRET_KEY"

agent:
  api_keys:
    - "CHANGE_ME"
```

启动：

```bash
docker compose up --build
```

访问：

```text
http://localhost
```

停止：

```bash
docker compose down
```

注意：默认 `docker-compose.yml` 暴露前端 `80` 端口和后端 `8000` 端口，只适合本地试用，不适合直接公网部署。

## 快速启动：本地开发方式

后端：

```bash
cd /home/user/github-product/EasyPaper/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp config/config.example.yaml config/config.yaml
# 编辑 config/config.yaml，填入 LLM API Key 和模型配置

uvicorn app.main:app --reload
```

前端：

```bash
cd /home/user/github-product/EasyPaper/frontend
npm install
npm run dev
```

访问：

```text
http://localhost:5173
```

## 常用验证命令

后端：

```bash
cd /home/user/github-product/EasyPaper/backend
ruff check app/
pytest
```

前端：

```bash
cd /home/user/github-product/EasyPaper/frontend
npm run lint
npm run type-check
npm test
```

## Obsidian 同步

EasyPaper 支持两种 Obsidian 相关输出：

- 导出 Obsidian Vault：生成包含 Markdown 双链笔记的 `.zip`。
- 本地 Obsidian 同步：直接把论文笔记和实体笔记写入本机 vault。

当前 Obsidian vault：

```text
/home/user/Web
```

如果使用 Docker 方式同步本机 Obsidian，需要把宿主机 vault 挂载到后端容器里，否则容器看不到 `/home/user/Web`。README 中明确说明：Docker 内同步时，需要在 compose 里挂载 vault，并在 EasyPaper 知识库设置中填写容器内路径。

EasyPaper 同步规则：

- 只写入它管理的论文笔记和实体笔记。
- 主笔记里的 `Paper Title - Notes.md` 是 Obsidian 红色链接，点击后才由 Obsidian 创建。
- 删除 EasyPaper 中的论文，不会删除 Obsidian 里已经存在的 `.md` 文件。

## Agent / MCP 接口

EasyPaper 还提供面向 agent 的 PDF 翻译接口。

HTTP：

- `POST /api/agent/v1/translate`
- `GET /api/agent/v1/tasks/{task_id}`
- `GET /api/agent/v1/tasks/{task_id}/artifact`
- 请求头：`X-Agent-Api-Key: <your key>`

MCP：

- 挂载路径：`/mcp`
- 工具：`translate_pdf`
- 工具：`get_translation_task`
- 工具：`get_translation_artifact`

示例：

```bash
curl -X POST http://127.0.0.1:8000/api/agent/v1/translate \
  -H 'Content-Type: application/json' \
  -H 'X-Agent-Api-Key: CHANGE_ME' \
  -d '{"pdf_base64":"JVBERi0xLjQgdGVzdA=="}'
```

如果没有提供 `highlight` 参数，接口不会直接启动翻译任务，而是返回一个 `needs_input` draft，让 agent 继续追问用户是否需要关键句高亮。

## 公网部署要点

公网部署不要使用默认 `docker-compose.yml`，应使用：

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

生产部署特征：

- Caddy 自动 HTTPS。
- 只暴露 80/443。
- 后端 `8000` 和 Postgres 在内部网络。
- 使用 Postgres 而不是 SQLite。
- 关闭自注册，通过 CLI 创建账号。
- `APP_ENV=production` 下，如果 JWT secret 或 agent API key 还是默认占位值，后端会拒绝启动。

创建用户：

```bash
docker compose -f docker-compose.prod.yml exec backend \
  python -m app.cli create-user alice@example.com 'a-strong-password'
```

## 相关链接

- [[PDFMathTranslate_Docker使用指南]]
- 项目 README：`/home/user/github-product/EasyPaper/README_zh.md`
- 部署文档：`/home/user/github-product/EasyPaper/docs/DEPLOYMENT.md`

## 待确认

- [ ] 是否要把 `/home/user/Web` 挂载进 EasyPaper Docker 后端，固定用于本地 Obsidian 同步。
- [ ] 当前实际使用哪个 LLM 服务和模型。
- [ ] 是否需要给 agent/MCP 调用单独配置稳定 API key。
