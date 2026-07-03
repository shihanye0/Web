# PDFMathTranslate Docker 部署指南

> 本文档介绍如何使用 Docker 在本地部署 PDFMathTranslate（PDF翻译工具）

---

## 一、前置要求

### 1.1 检查 Docker 是否安装

按 `Win + R`，输入 `cmd`，打开命令提示符，输入：

```cmd
docker --version
```

如果显示版本号（如 `Docker version 24.x.x`），说明已安装。

**如果没有安装：**
1. 访问 https://www.docker.com/products/docker-desktop/
2. 下载 Docker Desktop for Windows
3. 安装（需要 WSL2 支持，按提示安装即可）
4. 安装完成后重启电脑

### 1.2 启动 Docker Desktop

安装完成后，需要确保 Docker Desktop 正在运行：
- 任务栏右下角应该有 Docker 图标（鲸鱼）
- 图标如果是灰色的，说明没运行，点击启动

---

## 二、部署 PDFMathTranslate

### 2.1 拉取镜像

打开 CMD（命令提示符），输入：

```cmd
docker pull byaidu/pdf2zh
```

等待下载完成（可能需要几分钟，取决于网速）。

### 2.2 启动容器

```cmd
docker start pdf-translate
docker run -d --name pdf-translate -p 7860:7860 byaidu/pdf2zh

```

参数说明：
- `-d`：后台运行
- `--name pdf-translate`：给容器起个名字，方便管理
- `-p 7860:7860`：将容器内的 7860 端口映射到本机的 7860 端口

### 2.3 验证是否成功

```cmd
docker ps
```

如果看到 `pdf-translate` 正在运行，说明部署成功！

---

## 三、使用服务

### 3.1 访问 Web 界面

打开浏览器，访问：

```
http://localhost:7860
```

即可看到 PDFMathTranslate 的图形界面。

### 3.2 使用步骤

1. 点击上传按钮，选择 PDF 文件
2. 选择目标语言（中/英/日/德等）
3. 点击"翻译"按钮
4. 等待翻译完成
5. 下载翻译后的 PDF

---

## 四、常用管理命令

### 4.1 查看容器状态

```cmd
# 查看运行中的容器
docker ps

# 查看所有容器（包括已停止的）
docker ps -a
```

### 4.2 停止/启动服务

```cmd
# 停止服务
docker stop pdf-translate

# 启动服务
docker start pdf-translate

# 重启服务
docker restart pdf-translate
```

### 4.3 查看日志

```cmd
docker logs -f pdf-translate
```

### 4.4 删除容器

```cmd
# 先停止
docker stop pdf-translate

# 再删除
docker rm pdf-translate
```

---

## 五、多容器管理

### 5.1 同时管理多个服务

如果您部署了多个 Docker 服务，可以用以下方式查看：

```cmd
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

示例输出：
```
NAMES           STATUS          PORTS
pdf-translate   Up 2 hours     0.0.0.0:7860->7860/tcp
redis           Up 5 days       0.0.0.0:6379->6379/tcp
mysql           Up 3 hours      0.0.0.0:3306->3306/tcp
```

### 5.2 常用容器命名参考

| 服务 | 容器名 | 端口 |
|------|--------|------|
| PDF翻译 | pdf-translate | 7860 |
| Redis | my-redis | 6379 |
| MySQL | my-mysql | 3306 |

### 5.3 启动多个服务

```cmd
# 启动 PDF 翻译
docker start pdf-translate

# 启动 Redis
docker start my-redis

# 启动所有服务
docker start pdf-translate my-redis mysql
```

---

## 六、端口冲突问题

如果 7860 端口被占用，可以换一个端口：

```cmd
# 使用 7861 端口
docker run -d --name pdf-translate -p 7861:7860 byaidu/pdf2zh
```

访问时改成 `http://localhost:7861`

---

## 七、常见问题

### Q1: docker ps 显示容器 Exited

原因：容器意外停止了，可能是内存不足。

解决：
```cmd
# 查看详细日志
docker logs pdf-translate

# 重新启动
docker start pdf-translate
```

### Q2: 端口被占用

```cmd
# 查看哪个进程占用了 7860 端口
netstat -ano | findstr "7860"

# 结束占用进程或换端口
docker run -d --name pdf-translate -p 7861:7860 byaidu/pdf2zh
```

### Q3: pull 镜像太慢

可以使用国内镜像加速器，在 Docker Desktop 设置中添加：

```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
```

### Q4: 容器删除了但镜像还在

删除镜像：
```cmd
# 删除镜像
docker rmi byaidu/pdf2zh

# 强制删除
docker rmi -f byaidu/pdf2zh
```

---

## 八、一键脚本

为了方便管理，可以创建一个批处理文件 `pdf-docker.bat`：

```bat
@echo off
echo ===== PDFMathTranslate 管理脚本 =====

:menu
echo.
echo 1. 启动服务
echo 2. 停止服务
echo 3. 查看状态
echo 4. 查看日志
echo 5. 重启服务
echo 6. 退出
echo.

set /p choice=请选择 (1-6):

if "%choice%"=="1" goto start
if "%choice%"=="2" goto stop
if "%choice%"=="3" goto status
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto restart
if "%choice%"=="6" goto end

:start
docker start pdf-translate
echo 服务已启动，访问 http://localhost:7860
goto menu

:stop
docker stop pdf-translate
echo 服务已停止
goto menu

:status
docker ps --filter "name=pdf-translate"
goto menu

:logs
docker logs -f pdf-translate
goto menu

:restart
docker restart pdf-translate
echo 服务已重启
goto menu

:end
echo 退出
```

使用方法：
1. 将以上内容保存为 `pdf-docker.bat`
2. 双击运行即可

---

## 九、快速参考卡

```
┌────────────────────────────────────────────────┐
│              常用命令速查                         │
├────────────────────────────────────────────────┤
│ 部署服务:    docker run -d --name pdf-translate │
│              -p 7860:7860 byaidu/pdf2zh         │
├────────────────────────────────────────────────┤
│ 启动服务:    docker start pdf-translate         │
│ 停止服务:    docker stop pdf-translate          │
│ 重启服务:    docker restart pdf-translate       │
├────────────────────────────────────────────────┤
│ 查看状态:    docker ps                           │
│ 查看日志:    docker logs pdf-translate          │
├────────────────────────────────────────────────┤
│ 访问界面:    http://localhost:7860              │
└────────────────────────────────────────────────┘
```

---

## 十、参考资料

- 项目地址：https://github.com/PDFMathTranslate/PDFMathTranslate
- 在线体验：https://pdf2zh.com/

---

*文档创建日期：2026年4月28日*
