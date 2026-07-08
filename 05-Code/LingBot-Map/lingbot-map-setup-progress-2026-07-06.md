# LingBot-Map 安装配置进度记录

日期：2026-07-06

## 当前目标

先保存当前 LingBot-Map 与 codebase-memory-mcp 的配置进度，后续等 GPU / CUDA 环境恢复后继续完成 FlashInfer、Kaolin、CUDA 扩展、模型权重和 Demo 推理配置。

## 已完成

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

## 当前限制

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

## 后续继续安装步骤

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

## 后续恢复时的最安全起点

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
