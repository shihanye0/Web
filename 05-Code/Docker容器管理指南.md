# Docker 容器管理指南

> 本文档介绍本地 Docker 容器的管理方法，包含 PDFMathTranslate 和股票预测系统的部署与使用。

---

## 一、快速导航

| 项目 | 容器名 | 端口 | 说明 |
|------|--------|------|------|
| [PDFMathTranslate](#pdfmathtranslate-pdf翻译) | pdf-translate | 7860 | PDF翻译工具 |
| [股票预测系统-前端](#股票预测系统-前端) | stock-frontend | 80 | Vue3 前端界面 |
| [股票预测系统-后端](#股票预测系统-后端) | stock-backend | 8000 | FastAPI 后端服务 |
| [MySQL数据库](#mysql数据库) | stock-mysql | 13306 | 数据存储 |
| [Redis缓存](#redis缓存) | stock-redis | 6379 | 缓存服务 |
| [Prometheus监控](#prometheus监控) | stock-prometheus | 19090 | 指标采集 |
| [Grafana看板](#grafana看板) | stock-grafana | 3000 | 可视化监控 |

---

## 二、Docker 基础命令

### 2.1 查看容器状态

```cmd
# 查看运行中的容器
docker ps

# 查看所有容器（包括已停止的）
docker ps -a

# 格式化显示（更清晰）
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### 2.2 启动/停止/重启

```cmd
# 停止单个容器
docker stop <容器名>

# 启动单个容器
docker start <容器名>

# 重启单个容器
docker restart <容器名>

# 停止多个容器
docker stop 容器1 容器2 容器3

# 启动多个容器
docker start 容器1 容器2 容器3
```

### 2.3 查看日志

```cmd
# 实时查看日志
docker logs -f <容器名>

# 只看最后100行
docker logs --tail 100 <容器名>
```

### 2.4 删除容器

```cmd
# 先停止，再删除
docker stop <容器名>
docker rm <容器名>

# 强制删除（不需要先停止）
docker rm -f <容器名>
```

---

## 三、项目一：PDFMathTranslate（PDF翻译）

### 3.1 部署

```cmd
# 拉取镜像
docker pull byaidu/pdf2zh

# 启动容器
docker run -d --name pdf-translate -p 7860:7860 byaidu/pdf2zh
```

### 3.2 使用

访问地址：http://localhost:7860

使用步骤：
1. 上传 PDF 文件
2. 选择目标语言（中/英/日/德等）
3. 点击"翻译"
4. 下载翻译结果

### 3.3 管理命令

```cmd
# 启动
docker start pdf-translate

# 停止
docker stop pdf-translate

# 查看日志
docker logs -f pdf-translate

# 删除
docker stop pdf-translate && docker rm pdf-translate
```

---

## 四、项目二：股票预测系统

> 这是一套完整的前后端分离系统，包含以下组件：

```
┌─────────────────────────────────────────────────────────┐
│                    股票预测系统架构                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌──────────────┐                                     │
│   │   前端 Vue3   │ ← 用户界面 (端口 80)                │
│   │ stock-frontend│                                    │
│   └──────┬───────┘                                     │
│          │                                              │
│          ▼                                              │
│   ┌──────────────┐                                     │
│   │  后端 FastAPI │ ← API服务 (端口 8000)              │
│   │ stock-backend │                                    │
│   └──────┬───────┘                                     │
│          │                                              │
│   ┌──────┴───────┐                                     │
│   │              │                                     │
│   ▼              ▼                                     │
│ ┌────┐       ┌─────┐       ┌────────┐                  │
│ │MySQL│       │Redis │       │Prometheus│               │
│ │  DB │       │Cache │       │  监控   │               │
│ └────┘       └─────┘       └────────┘                  │
│                                        │               │
│                                        ▼               │
│                                  ┌────────┐             │
│                                  │Grafana │             │
│                                  │ 可视化 │             │
│                                  └────────┘             │
└─────────────────────────────────────────────────────────┘
```

### 4.1 容器说明

| 容器名 | 镜像 | 端口 | 说明 |
|--------|------|------|------|
| stock-frontend | stock_predicition-frontend | 80 | 前端界面 |
| stock-backend | stock_predicition-backend | 8000 | 后端 API |
| stock-mysql | mysql:8.0 | 13306 | MySQL 数据库 |
| stock-redis | redis:7-alpine | 6379 | Redis 缓存 |
| stock-prometheus | prom/prometheus:v2.48.0 | 19090 | Prometheus 监控 |
| stock-grafana | grafana/grafana:10.2.2 | 3000 | Grafana 可视化 |

### 4.2 访问地址

| 服务 | 地址 |
|------|------|
| 前端界面 | http://localhost |
| 后端 API | http://localhost:8000 |
| API 文档 | http://localhost:8000/docs |
| Grafana | http://localhost:3000 |
| Prometheus | http://localhost:19090 |

### 4.3 管理命令

#### 启动所有股票系统服务
```cmd
docker start stock-frontend stock-backend stock-mysql stock-redis stock-prometheus stock-grafana
```

#### 停止所有股票系统服务
```cmd
docker stop stock-frontend stock-backend stock-mysql stock-redis stock-prometheus stock-grafana
```

#### 只启动前端
```cmd
docker start stock-frontend
```

#### 只启动后端
```cmd
docker start stock-backend
```

#### 只启动数据库
```cmd
docker start stock-mysql
```

#### 只启动缓存
```cmd
docker start stock-redis
```

#### 查看某个服务日志
```cmd
# 查看前端日志
docker logs -f stock-frontend

# 查看后端日志
docker logs -f stock-backend

# 查看数据库日志
docker logs -f stock-mysql
```

---

## 五、各组件详细说明

### 5.1 股票预测系统 - 前端

**容器名**: `stock-frontend`
**端口**: 80
**说明**: Vue 3 + Vite 构建的前端界面

```cmd
# 启动
docker start stock-frontend

# 停止
docker stop stock-frontend

# 查看日志
docker logs -f stock-frontend
```

**访问**: http://localhost

---

### 5.2 股票预测系统 - 后端

**容器名**: `stock-backend`
**端口**: 8000
**说明**: FastAPI 构建的后端服务

```cmd
# 启动
docker start stock-backend

# 停止
docker stop stock-backend

# 查看日志
docker logs -f stock-backend
```

**访问**: http://localhost:8000/docs （API文档）

---

### 5.3 MySQL数据库

**容器名**: `stock-mysql`
**端口**: 13306
**说明**: 存储股票数据、用户评论、情绪分析结果等

```cmd
# 启动
docker start stock-mysql

# 停止
docker stop stock-mysql

# 查看日志
docker logs -f stock-mysql
```

**连接信息**（供其他容器使用）:
- 主机名: stock-mysql
- 端口: 3306
- 用户: root
- 密码: (需要查看 docker-compose 或环境变量)

---

### 5.4 Redis缓存

**容器名**: `stock-redis`
**端口**: 6379
**说明**: 缓存热点数据，减少数据库压力

```cmd
# 启动
docker start stock-redis

# 停止
docker stop stock-redis

# 查看日志
docker logs -f stock-redis
```

**连接信息**:
- 主机名: stock-redis
- 端口: 6379

---

### 5.5 Prometheus监控

**容器名**: `stock-prometheus`
**端口**: 19090
**说明**: 采集和存储时序数据

```cmd
# 启动
docker start stock-prometheus

# 停止
docker stop stock-prometheus

# 查看日志
docker logs -f stock-prometheus
```

**访问**: http://localhost:19090

---

### 5.6 Grafana看板

**容器名**: `stock-grafana`
**端口**: 3000
**说明**: 可视化监控面板

```cmd
# 启动
docker start stock-grafana

# 停止
docker stop stock-grafana

# 查看日志
docker logs -f stock-grafana
```

**访问**: http://localhost:3000
**默认账号**: admin / admin123

---

## 六、常见场景

### 场景1：只运行前端开发（不需要数据库等）

只启动前端和后端（后端需要数据库才能正常工作）：
```cmd
docker start stock-frontend stock-backend stock-mysql stock-redis
```

### 场景2：只运行后端 API 测试

```cmd
docker start stock-backend stock-mysql stock-redis
# 访问 http://localhost:8000/docs 测试 API
```

### 场景3：只查看监控数据

```cmd
docker start stock-prometheus stock-grafana
# 访问 http://localhost:3000 查看监控
```

### 场景4：关闭所有服务（省资源）

```cmd
docker stop stock-frontend stock-backend stock-mysql stock-redis stock-prometheus stock-grafana
```

### 场景5：重启某个服务

```cmd
docker restart stock-backend
```

### 场景6：查看所有服务状态

```cmd
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

---

## 七、端口冲突检查

如果某个端口被占用，排查方法：

```cmd
# 查看所有端口占用情况
netstat -ano | findstr "80"
netstat -ano | findstr "8000"
netstat -ano | findstr "3000"
netstat -ano | findstr "6379"
netstat -ano | findstr "13306"
netstat -ano | findstr "19090"
```

---

## 八、快速参考卡

```
┌────────────────────────────────────────────────────────┐
│              Docker 快速命令                            │
├────────────────────────────────────────────────────────┤
│                                                        │
│  # 查看所有容器                                         │
│  docker ps -a                                          │
│                                                        │
│  # 启动所有股票系统服务                                  │
│  docker start stock-frontend stock-backend stock-mysql  │
│  docker start stock-redis stock-prometheus stock-grafana│
│                                                        │
│  # 停止所有服务                                         │
│  docker stop stock-frontend stock-backend stock-mysql  │
│  docker stop stock-redis stock-prometheus stock-grafana│
│                                                        │
│  # 查看某个服务日志                                      │
│  docker logs -f <容器名>                               │
│                                                        │
│  # 重启某个服务                                         │
│  docker restart <容器名>                               │
│                                                        │
├────────────────────────────────────────────────────────┤
│              访问地址                                    │
├────────────────────────────────────────────────────────┤
│  前端:    http://localhost                              │
│  后端:    http://localhost:8000                         │
│  API文档: http://localhost:8000/docs                   │
│  Grafana: http://localhost:3000 (admin/admin123)       │
│  Prometheus: http://localhost:19090                    │
│  PDF翻译: http://localhost:7860                        │
└────────────────────────────────────────────────────────┘
```

---

## 九、故障排查

### 问题1：容器显示 Exited

```cmd
# 查看详细日志
docker logs <容器名>

# 尝试重启
docker start <容器名>
```

### 问题2：端口被占用

```cmd
# 查看占用进程
netstat -ano | findstr "<端口号>"

# 结束进程或修改容器端口
```

### 问题3：前端无法访问后端

```cmd
# 确认后端是否运行
docker ps | findstr backend

# 查看后端日志
docker logs stock-backend
```

---

*文档创建日期：2026年4月28日*
*最后更新：2026年4月28日*
