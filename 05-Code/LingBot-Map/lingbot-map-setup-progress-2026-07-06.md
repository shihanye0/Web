# LingBot-Map 安装配置进度记录

创建日期：2026-07-06  
最终更新：2026-07-12

## 2026-07-12 最终状态

LingBot-Map 的核心交互 Demo 已完成配置并在 RTX 4070 上成功运行。2026-07-06 记录的 `nvidia-smi` 阻塞已解除；问题根因不是宿主机 NVIDIA 驱动损坏，而是当时的 Codex 受限沙箱没有映射 `/dev/nvidia*` 设备。

本轮完成边界：GPU 环境、项目依赖、官方模型权重、示例数据推理和 Viser 交互 Viewer 均已验收。FlashInfer、Kaolin 和 `demo_render` 离线渲染栈不是核心 `demo.py` 的必要依赖，本轮明确不安装。

### 最终环境

- GPU：NVIDIA GeForce RTX 4070，12 GB 显存
- NVIDIA 驱动：`535.309.01`
- `nvidia-smi` 显示的驱动 CUDA API 版本：`12.2`
- Conda 环境：`lingbot-map`
- Python：`3.10.20`
- PyTorch：`2.8.0+cu126`
- torchvision：`0.23.0+cu126`
- 推理后端：PyTorch SDPA，通过 `--use_sdpa` 启用
- `viser`：`1.0.30`
- `rich`：`14.3.4`，用于解决与 `viser 1.0.30` 的兼容问题
- 项目以隔离方式重新安装：`pip install -e '.[vis]'`

虽然 PyTorch wheel 自带 CUDA 12.6 runtime，而 `nvidia-smi` 显示 12.2，但不能仅根据版本字符串判断不可用。本机已用真实 CUDA 张量、BF16 矩阵计算和完整 Demo 推理验证该组合可运行。

### GPU 验收证据

宿主机执行：

```bash
nvidia-smi
```

结果可识别 RTX 4070、驱动 `535.309.01`，并能看到 LingBot-Map Python 推理进程占用 GPU。

项目环境执行：

```bash
PYTHONNOUSERSITE=1 \
/home/user/miniconda3/envs/lingbot-map/bin/python -c "\
import torch, torchvision, lingbot_map, viser; \
print(torch.__version__, torchvision.__version__); \
print(torch.cuda.is_available(), torch.cuda.get_device_name(0), torch.cuda.is_bf16_supported()); \
x=torch.randn((1024,1024), device='cuda', dtype=torch.bfloat16); \
print(float((x@x).float().mean())); \
print('imports_ok')"
```

关键结果：

```text
2.8.0+cu126 0.23.0+cu126
True NVIDIA GeForce RTX 4070 True
imports_ok
```

注意：在不映射 NVIDIA 设备的受限沙箱中，`torch.cuda.is_available()` 仍可能返回 `False`。判断机器 GPU 是否正常，应以宿主机 `nvidia-smi` 和宿主权限下的 CUDA 实算为准。

### 项目依赖验收

为避免项目隐式使用 `~/.local` 中的用户级 Python 包，所有验证均加上：

```bash
PYTHONNOUSERSITE=1
```

已执行：

```bash
PYTHONNOUSERSITE=1 \
/home/user/miniconda3/envs/lingbot-map/bin/python -m pip check
```

结果：

```text
No broken requirements found.
```

### 模型权重

Hugging Face 下载持续连接超时，最终改用 ModelScope 官方仓库 `Robbyant/lingbot-map` 下载：

```text
/home/user/github-product/lingbot-map/weights/lingbot-map.pt
```

- 文件大小：`4,632,303,465` 字节
- SHA256：`ee665103348e07e6b826d529b8e61de8f413d5432a4f2e84970d6c8fd2e1cd72`
- 校验结果：与 ModelScope 官方元数据一致
- Git 边界：项目现有 `.gitignore` 已忽略 `weights/`，模型不会进入 Git

复核命令：

```bash
cd /home/user/github-product/lingbot-map
sha256sum weights/lingbot-map.pt
stat -c '%n %s bytes' weights/lingbot-map.pt
```

### Demo 复现命令

```bash
cd /home/user/github-product/lingbot-map
conda activate lingbot-map

PYTHONNOUSERSITE=1 python -u demo.py \
  --model_path weights/lingbot-map.pt \
  --image_folder example/courthouse \
  --first_k 12 \
  --use_sdpa \
  --num_scale_frames 2 \
  --offload_to_cpu \
  --camera_num_iterations 1 \
  --port 8090
```

Viewer 地址：

```text
http://localhost:8090
```

### Demo 实测结果

- 官方权重成功加载，没有 missing keys 或 unexpected keys 报告
- 输入：`example/courthouse` 前 12 帧
- 输入分辨率：`518 x 294`
- 推理时间：约 `2.6` 秒
- 流式速度：约 `9.24 FPS`
- 模型加载后 GPU allocated：约 `2.84 GB`
- 推理峰值 GPU allocated：约 `9.27 GB`
- 推理峰值 GPU reserved：约 `10.39 GB`
- Viewer 普通 HTTP GET：`200`
- Viewer HTML 大小：`2,888,259` 字节

`curl -I` 可能得到空响应，因为当前 Viser 服务不处理 HEAD 请求；这不代表 Viewer 不可用。应使用普通 GET 验证：

```bash
curl -sS -o /tmp/lingbot-map-viewer-index.html \
  -w 'http_code=%{http_code}\nsize_download=%{size_download}\n' \
  http://127.0.0.1:8090
```

### 本轮未安装的可选组件

以下组件仅在需要 `demo_render/batch_demo.py`、离线视频渲染或特定加速后端时再配置：

- `flashinfer-python`
- NVIDIA Kaolin
- `onnxruntime-gpu`
- `demo_render/render_cuda_ext` CUDA 扩展
- `pip install -e '.[vis,render]'` 对应的完整渲染依赖

本轮不安装的原因：

- 核心 `demo.py` 已通过 SDPA 完整运行，不依赖 FlashInfer。
- Kaolin 可用的预编译组合更偏向 torch 2.8 + CUDA 12.8，贸然安装可能破坏当前已验证的 cu126 环境。
- 离线渲染不是本轮“模型加载、GPU 推理、交互查看”的验收目标。

停止条件：在明确需要离线批量渲染之前，不继续修改当前可运行环境。后续若安装这些组件，应新建独立 Conda 环境或先导出当前环境，避免破坏已完成闭环。

### 当前 Git 边界

仓库当前 commit：`78e9f6c`。`git status --short` 仍只有用户原有的：

```text
 M .gitignore
```

该修改用于忽略 `.codegraph/`，本轮没有覆盖、回滚或提交它。

## 2026-07-06 当时目标（历史）

先保存当前 LingBot-Map 与 codebase-memory-mcp 的配置进度，后续等 GPU / CUDA 环境恢复后继续完成 FlashInfer、Kaolin、CUDA 扩展、模型权重和 Demo 推理配置。

## 2026-07-06 已完成（历史）

### codebase-memory-mcp

- 已安装并配置到 Claude Code、Codex CLI、Gemini CLI、VS Code。
- 二进制路径：`/home/user/.local/bin/codebase-memory-mcp`
- 版本：`0.8.1`
- Claude Code / Codex 需要重启后读取新 MCP 配置。
- 已索引 `lingbot-map`：
  - 项目名：`home-user-github-product-lingbot-map`
  - 本地路径：`/home/user/github-product/lingbot-map`
  - 节点数：`1500`
  - 边数：`4521`
- 已验证 `search_graph` 可搜索 `GCTStream`，能返回核心类和方法。

### CodeGraph

- 已安装并配置到 Claude Code / Codex CLI。
- 已在 `/home/user/github-product/lingbot-map` 执行 `codegraph init`。
- 当前 CodeGraph 索引：
  - Files：`118`
  - Nodes：`1695`
  - Edges：`3587`
  - DB Size：`4.76 MB`
  - Backend：`node:sqlite — built-in (full WAL)`
  - Journal：`wal`
- 已验证 `codegraph explore "GCTStream"` 可返回 `GCTStream` 源码、调用方和 blast radius。
- `.codegraph/` 是本地索引目录，已加入项目 `.gitignore`，避免污染 git 状态。

### LingBot-Map 仓库

- GitHub 仓库：`https://github.com/Robbyant/lingbot-map`
- 本地路径：`/home/user/github-product/lingbot-map`
- 当前 commit：`78e9f6c`
- Git 状态：存在本轮新增的 `.gitignore` 修改：忽略 `.codegraph/` 本地索引目录。
- 项目定位：流式 3D 重建 / Geometric Context Transformer，偏机器人视觉建图、空间感知、3D 世界模型底座。

### Conda 环境

- 环境名：`lingbot-map`
- Python：`3.10`
- 已安装 CPU 版 PyTorch：`torch 2.8.0+cpu`
- 已安装 torchvision：`0.23.0+cpu`
- 已安装项目本体：`pip install -e '.[vis]'`
- 已安装可视化/基础依赖：`viser`、`trimesh`、`matplotlib`、`onnxruntime`、`huggingface_hub` 等。

### 验证结果

执行过：

```bash
conda run -n lingbot-map python -c "import torch, lingbot_map, onnxruntime; print('torch', torch.__version__); print('cuda_available', torch.cuda.is_available()); print('onnxruntime', onnxruntime.__version__); print('lingbot_map_import_ok')"
```

结果：

```text
2026-07-07 15:15 onnxruntime warning: GPU device discovery failed
torch 2.8.0+cpu
cuda_available False
onnxruntime 1.23.2
lingbot_map_import_ok
```

执行过：

```bash
conda run -n lingbot-map python demo.py --help
```

结果：命令正常返回帮助信息。

执行过：

```bash
codegraph status
codegraph explore "GCTStream"
```

结果：CodeGraph 索引可用，`GCTStream` 查询可返回当前源码和影响面。

## 2026-07-06 当时限制（已解除）

`nvidia-smi` 当前失败：

```text
NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver.
```

这说明当前系统读不到 NVIDIA 驱动。LingBot-Map 真正跑 3D 重建、长序列推理和离线渲染通常需要 CUDA/GPU，因此本次没有继续安装：

- `flashinfer-python`
- NVIDIA Kaolin
- `demo_render/render_cuda_ext` CUDA 扩展
- GPU 版 `onnxruntime-gpu`
- 大模型权重 `lingbot-map.pt` / `lingbot-map-long.pt`

HuggingFace 文件列表查询曾出现连接超时，属于外网访问问题，不是项目本身配置错误。

当前仍未发现模型权重文件：

```bash
find /home/user/github-product/lingbot-map -maxdepth 3 -type f \( -name '*.pt' -o -name '*.pth' -o -name '*.onnx' \)
```

结果为空。

## 2026-07-06 原计划（核心闭环已完成）

### 1. 先恢复 GPU 驱动

重新检查：

```bash
nvidia-smi
```

必须能看到 GPU、驱动版本、CUDA 版本后，再继续 GPU 依赖安装。

### 2. 进入项目环境

```bash
cd /home/user/github-product/lingbot-map
conda activate lingbot-map
```

### 3. 根据驱动/CUDA 状态决定 PyTorch

当前是 CPU 版 PyTorch。如果要按 README 推荐跑 GPU，后续可能需要替换为 CUDA 版：

```bash
pip install torch==2.8.0 torchvision==0.23.0 --index-url https://download.pytorch.org/whl/cu128
```

只在本机驱动支持 CUDA 12.8 或兼容条件明确时执行。

### 4. 安装 FlashInfer

```bash
pip install --index-url https://pypi.org/simple flashinfer-python
```

如果只想先用 PyTorch SDPA 后端，可以运行 Demo 时加 `--use_sdpa`，暂时不装 FlashInfer。

### 5. 下载模型权重

模型来源：

- HuggingFace：`robbyant/lingbot-map`
- ModelScope：`Robbyant/lingbot-map`

建议优先下载：

- `lingbot-map-long.pt`：更适合长序列、大场景。
- `lingbot-map.pt`：论文和 benchmark 使用的平衡版本。

建议保存目录：

```text
/home/user/github-product/lingbot-map/checkpoints/
```

### 6. 试运行 Demo

示例：

```bash
python demo.py \
  --model_path /home/user/github-product/lingbot-map/checkpoints/lingbot-map-long.pt \
  --image_folder example/courthouse \
  --mask_sky \
  --use_sdpa
```

Viewer 默认地址：

```text
http://localhost:8080
```

### 7. 离线渲染另行配置

如果需要 `demo_render/batch_demo.py`，再额外安装：

- `pip install -e '.[vis,render]'`
- `onnxruntime-gpu`
- NVIDIA Kaolin
- `ffmpeg`
- `demo_render/render_cuda_ext` 下的 CUDA 扩展

这部分强依赖 GPU/CUDA，不建议在当前驱动不可用状态下继续。

## 2026-07-06 原恢复起点（仅作历史参考）

```bash
cd /home/user/github-product/lingbot-map
git status --short
conda activate lingbot-map
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
nvidia-smi
/home/user/.local/bin/codebase-memory-mcp cli list_projects '{}'
codegraph status
```

如果 `torch.cuda.is_available()` 仍是 `False`，先不要装/跑 FlashInfer、Kaolin、CUDA 扩展和完整推理。
