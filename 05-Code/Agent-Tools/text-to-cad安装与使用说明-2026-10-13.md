---
title: "text-to-cad安装与使用说明-2026-10-13"
date: 2026-10-13
tags: [tool, CAD, STEP, MCP, shared-config, modeling]
status: seed
sources:
  - "https://github.com/earthtojake/text-to-cad"
  - "E:/github-product/shared-config-verification/geometry-receipt.json"
  - "C:/Users/Lenovo/.agent-config/manifests/opensource-tools-20261013.json"
---

# text-to-cad 安装与使用说明

text-to-cad 已安装固定版本 `cadgen==0.7.21`，MCP ID 为 `cad`，接入四个 Agent。适用用途是精确尺寸的参数化零件、STEP 与后续工程工作流；本机 Blender 保留用于艺术建模、动画和已有课程任务。

本轮通过 Windows 内核加载、真实 STEP/STL/GLB 导出、尺寸回读与截图查看。工程图、制造检查和机器人描述 Skill 已接入，尚未进行对应工程任务验收。

## 固定版本与共享入口

运行器：`C:/Users/Lenovo/anaconda3/Scripts/uvx.exe`（本轮 uv 0.9.18）。Python 使用 uv 管理的 3.13 环境，本轮实际为 3.13.11，不向系统 Python 全局安装 CAD 依赖。

MCP 共享启动规格：

```json
{
  "command": "C:/Users/Lenovo/anaconda3/Scripts/uvx.exe",
  "args": [
    "--no-config", "--managed-python", "--python", "3.13",
    "--from", "cadgen==0.7.21", "cadgen", "mcp"
  ],
  "env": {
    "CADGEN_TELEMETRY": "0",
    "DO_NOT_TRACK": "1",
    "CADGEN_UPDATE_CHECK": "0"
  }
}
```

四个客户端分别将该规格写入自己的原生配置；路径见 [[开源工具多Agent共享配置-2026-10-13]]。不要固定引用 uv 缓存中的 Python 目录，它是可重建缓存。

共享源新增 `cad`、`engineering-drawing`、`dfm`、`urdf` 四个 Skill，版本来源为上游提交 `a499253845c717e5144471ca75f9eb0f90e7964f`；文件 SHA-256 记录在 manifest。没有同时安装整套 text-to-cad 插件，以免产生重复 Skill 或加载不同版本。其他八个专项 Skill 未安装，后续按真实需要接入。

## 在 Agent 中使用

新建或重载会话后，可先提出明确尺寸、输出和验证要求：

> 使用 cad Skill 建立一块 40×20×6 mm 的矩形板，保留 Python 模型源，输出 STEP；回读实体数、尺寸、体积，再使用 cad_show 展示。之后按需要输出 STL/GLB。

`cad` MCP 主要提供 `cad_show` 和 `cad_telemetry`；建模由 Skill 引导 Agent 写 Python 并运行本地 CAD 内核，不是一个远程模型生成 API。输入尺寸、材料、制造约束和输出格式应明确。工程图用 `engineering-drawing`，制造适配分析用 `dfm`，机器人描述用 `urdf`；可调用方式依客户端而异。

## 可复现的本地样例

本轮模型源 `E:/github-product/shared-config-verification/plate.py`：

```python
from cadgen import build123d as bd
from cadgen import step

@step(out="STEP/plate.step")
def plate():
    shape = bd.Box(40, 20, 6)
    shape.label = "verification_plate_40x20x6_mm"
    return shape

if __name__ == "__main__":
    plate()
```

模型入口不接收参数，参数化工厂或常量写在模型源中；修改源文件并重建。生成的 STEP/网格是输出，不直接当成 Python 源编辑。

以下固定环境运行方式已在本机实际执行成功，重复执行会识别当前模型并复用已有产物：

```powershell
$env:CADGEN_TELEMETRY = '0'
$env:DO_NOT_TRACK = '1'
$env:CADGEN_UPDATE_CHECK = '0'
$uvx = 'C:/Users/Lenovo/anaconda3/Scripts/uvx.exe'
& $uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 python 'E:/github-product/shared-config-verification/plate.py' --json
& $uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 cadgen doctor
```

该样例的 `@step` 只声明 STEP 输出。STL/GLB 可以按共享 Skill 的 `references/supported-exports.md` 声明输出或调用已安装版本的导出命令；本轮已有的 STL/GLB 文件是另行导出的验证产物，不是上面单个 STEP 装饰器自动生成的。

## Viewer 与首次启动排障

本轮 Viewer 位于 [本机 CAD Viewer](http://127.0.0.1:3245/)。端口属于当前实例，重启后以实际命令输出为准。Viewer 按需运行，没有设置 Windows 开机自启。

首次并发冷启动测试出现一次 Viewer 启动失败，根因未确认。通过官方启动命令启动后，四个入口重测均成功：

```powershell
$env:CADGEN_TELEMETRY = '0'
$env:DO_NOT_TRACK = '1'
$env:CADGEN_UPDATE_CHECK = '0'
& 'C:/Users/Lenovo/anaconda3/Scripts/uvx.exe' --no-config --managed-python --python 3.13 --from cadgen==0.7.21 cadgen viewer --host 127.0.0.1 --json --detach
```

使用输出的本机 URL，并从 Agent 调用 `cad_show` 指定真实 STEP 文件。部分客户端展示交互 UI，缺少相关能力的客户端可能返回浏览器链接；本轮验证走的是链接回退。并发冷启动稳定性没有因为一次重测通过而得到全面证明。

## 验收证据

| 验证项 | 实际结果 |
| --- | --- |
| 四份原生配置的 MCP 初始化 | 各返回 2 个工具 |
| `cad_telemetry` 状态查询 | 关闭遥测 |
| `cad_show` 真实 STEP 展示 | 四个入口重测通过 |
| STEP 回读 | 1 个实体，40×20×6 mm，体积约 4800 mm³ |
| STL | 二进制结构有效，12 个三角形，外包尺寸符合样例 |
| GLB | glTF 2 容器结构有效，1 个网格 |
| PNG | 已生成并查看，矩形板模型可见 |

产物目录：`E:/github-product/shared-config-verification/`。对应文件为 `STEP/plate.step`、`STL/plate.stl`、`GLB/plate.glb`、`plate.png`。`geometry-receipt.json` 保存尺寸、实体数、格式信息、文件长度和哈希；`mcp-receipt.json` 保存四个 Agent 的接入验收。

这只证明样例模型与当前配置；复杂装配、工程图精度、DFM 结果质量、URDF 仿真以及真实桌面宿主重载后的工具发现尚未覆盖。

## 维护

升级时保持 `cadgen` 运行版本与共享 Skill 同批调整，在独立目录验证后再更新四个入口和 manifest。不要单个 Agent 使用浮动版本。遥测当前关闭状态应在升级后重查。回退前核对当前配置差异，按条目移除，避免覆盖后续原生配置。

## 关联和来源

- [[开源工具多Agent共享配置-2026-10-13]] — 原生入口、版本清单、备份及工具对照。
- [[Agent Assets Hub 使用指南  agent同步指南]] — 多 Agent 共享资产约定。
- [text-to-cad 上游](https://github.com/earthtojake/text-to-cad) — 项目安装与 CLI 文档；运行时以固定 0.7.21 版本为准。
