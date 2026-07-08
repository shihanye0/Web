# PDFMathTranslate 使用指南（Ubuntu 版）

> 本文档介绍如何在 Ubuntu 上使用 PDFMathTranslate（PDF翻译工具），支持 Docker 部署和本地 Conda 环境两种方式。

---

## 一、项目信息

- **项目地址**：https://github.com/Byaidu/PDFMathTranslate
- **在线体验**：https://pdf2zh.com/
- **本机路径**：`/home/user/github-product/PDFMathTranslate/`
- **Conda 环境**：`pdf2zh`

---

## 二、本地安装（推荐）

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

## 三、Docker 部署（可选）

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
docker pull byaidu/pdf2zh
```

### 3.3 启动容器

```bash
docker run -d --name pdf-translate -p 7860:7860 byaidu/pdf2zh
```

参数说明：
- `-d`：后台运行
- `--name pdf-translate`：给容器起个名字
- `-p 7860:7860`：端口映射

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

---

## 六、常用管理命令

### 6.1 Docker 管理

```bash
# 查看状态
docker ps

# 停止服务
docker stop pdf-translate

# 启动服务
docker start pdf-translate

# 重启服务
docker restart pdf-translate

# 查看日志
docker logs -f pdf-translate

# 删除容器
docker stop pdf-translate && docker rm pdf-translate

# 删除镜像
docker rmi byaidu/pdf2zh
```

### 6.2 端口冲突解决

如果 7860 端口被占用：

```bash
# 使用 7861 端口
docker run -d --name pdf-translate -p 7861:7860 byaidu/pdf2zh
```

---

## 七、常见问题

### Q1: Docker 容器启动失败

```bash
# 查看日志
docker logs pdf-translate

# 常见原因：内存不足
# 解决：重启 Docker
sudo systemctl restart docker
```

### Q2: 端口被占用

```bash
# 查看占用进程
sudo lsof -i :7860

# 结束进程或换端口
```

### Q3: Conda 环境找不到

```bash
# 确保激活了正确的环境
conda activate pdf2zh

# 检查 Python 路径
which python
```

### Q4: pip 安装太慢

```bash
# 使用清华源
pip install -e /home/user/github-product/PDFMathTranslate -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q5: `ModuleNotFoundError: No module named 'pdf2zh'`

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

---

## 八、快速参考卡

```
┌────────────────────────────────────────────────────────┐
│              PDFMathTranslate 常用命令速查                │
├────────────────────────────────────────────────────────┤
│ 翻译 PDF:     pdf2zh paper.pdf                         │
│ 启动 GUI:     pdf2zh --interactive                      │
│ 启动 Web:     pdf2zh --share                            │
├────────────────────────────────────────────────────────┤
│ Docker 部署:  docker run -d --name pdf-translate \     │
│               -p 7860:7860 byaidu/pdf2zh               │
├────────────────────────────────────────────────────────┤
│ Docker 管理:  docker start/stop/restart pdf-translate   │
│ 查看日志:     docker logs -f pdf-translate              │
├────────────────────────────────────────────────────────┤
│ 访问界面:     http://localhost:7860                     │
└────────────────────────────────────────────────────────┘
```

---

## 九、本机环境信息

| 项目 | 值 |
|------|-----|
| 项目路径 | `/home/user/github-product/PDFMathTranslate/` |
| Conda 环境 | `pdf2zh` |
| Python 版本 | 3.12 |
| 安装方式 | 本地 Conda editable 安装 |

---

*文档更新日期：2026年7月6日*
*系统：Ubuntu 22.04*
