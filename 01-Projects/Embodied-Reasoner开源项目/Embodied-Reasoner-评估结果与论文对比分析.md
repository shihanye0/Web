---
title: "Embodied-Reasoner 评估结果与论文对比分析"
date: 2026-07-07
tags: [embodied-reasoner, evaluation, results, paper-comparison]
status: draft
---

# Embodied-Reasoner 评估结果与论文对比分析

## 基本信息

| 项目 | 内容 |
|------|------|
| 评估模型 | `Qwen2-VL-7B-Instruct_ir351232_ds_embodied_o1_v1_7282_add_v3_519_1497_ct24576_lr1d0e-5_pbs4_g1_e3d0` |
| 模型来源 | ModelScope: `qigefengfan/...e3d0` |
| 推理方式 | HuggingFace Transformers + 4-bit quantization |
| GPU | NVIDIA RTX 4070 (12GB VRAM) |
| 评估时间 | 累计约 8 小时（含多次中断重启） |
| 测试集 | `data/test_809.json`（809 个任务） |
| 评估框架 | `evaluate/evaluate.py`（LOCAL 模式） |
| 论文 | arXiv:2503.21696v2 |

## 评估日志与结果位置

| 内容       | 路径                          | 查看命令                                       |
| -------- | --------------------------- | ------------------------------------------ |
| 最终报告     | `/tmp/eval_final_report.md` | `cat /tmp/eval_final_report.md`            |
| 完整日志     | `/tmp/eval_full_v2.log`     | `tail -100 /tmp/eval_full_v2.log`          |
| VLM 服务日志 | `/tmp/vlm_server.log`       | `cat /tmp/vlm_server.log`                  |
| 详细结果目录   | `data/new_finetuned_model/` | `ls data/new_finetuned_model/ \| head -10` |

## 结果查看命令速查

```bash
# 进入项目目录
cd /home/user/github-product/embodied_reasoner

# 1. 总有效结果数
find data/new_finetuned_model/ -name "result.json" | wc -l

# 2. 成功任务列表
grep "SUCCEEDED" /tmp/eval_full_v2.log

# 3. 失败任务列表
grep "evaluate FAILED" /tmp/eval_full_v2.log | head -20

# 4. 完成度分布
grep "completeness:" /tmp/eval_full_v2.log | awk '{print $NF}' | sort | uniq -c | sort -rn

# 5. 按任务类型统计
grep "evaluate SUCCEEDED\|evaluate FAILED" /tmp/eval_full_v2.log | grep -oP "tasktype': '[^']*" | sort | uniq -c

# 6. 查看某个具体任务结果
cat data/new_finetuned_model/304_single_toggle_FloorPlan1_6/result.json | python3 -m json.tool | head -50

# 7. 查看某个任务的轨迹步骤
python3 -c "import json; d=json.load(open('data/new_finetuned_model/304_single_toggle_FloorPlan1_6/result.json')); [print(t['action'], t.get('object','')) for t in d['trajectory']]"

# 8. 控制器崩溃恢复次数
grep -c "RECOVERY" /tmp/eval_full_v2.log

# 9. emulator 异常次数
grep -c "emulator /api exception" /tmp/eval_full_v2.log

# 10. 总运行时间（从日志看）
head -1 /tmp/eval_full_v2.log
tail -1 /tmp/eval_full_v2.log
```

## 评估结果

| 指标 | 数值 | 说明 |
|------|------|------|
| 总任务 | 809 | test_809.json |
| 有效结果 | 96 | 有 result.json 的任务 |
| 成功任务 | 26 | metrics.success == 1 |
| 整体成功率 | 27.08% | 26/96（有效结果内） |
| 总任务成功率 | 3.21% | 26/809（含无结果任务） |

### 按任务类型

| 任务类型 | 总数 | 成功 | 成功率 | 难度 |
|---------|------|------|--------|------|
| single_pickup | 33 | 14 | 42.4% | 简单 |
| single_toggle | 9 | 6 | 66.7% | 简单 |
| pickup_and_put | 3 | 2 | 66.7% | 中等 |
| pickup_and_put_in_closerep | 6 | 2 | 33.3% | 中等 |
| single_search | 7 | 1 | 14.3% | 中等 |
| single_pickup_from_closerep | 3 | 1 | 33.3% | 中等 |
| ordered_pickup_two_object_and_put | 16 | 0 | 0.0% | 困难 |
| long-range tasks | 19 | 0 | 0.0% | 极困难 |

### 成功任务（26个）

```
304(single_toggle), 306(single_toggle), 307(single_toggle), 308(single_toggle),
309(single_toggle), 433(single_search), 439(single_pickup), 557(single_pickup),
565(single_pickup), 567(single_pickup), 638(single_toggle), 647(pickup_and_put),
648(pickup_and_put), 656(pickup_and_put_in_closerep), 657(pickup_and_put_in_closerep),
659(single_pickup), 660(single_pickup), 661(single_pickup), 662(single_pickup),
663(single_pickup), 664(single_pickup), 669(single_pickup), 670(single_pickup),
672(single_pickup), 674(single_pickup), 761(single_pickup_from_closerep)
```

## 与论文实验数据对比

### 论文 Table 2 关键数据

| 模型 | Success Rate | Search Efficiency | Task Completeness |
|:---|---:|---:|---:|
| Qwen2-VL-7B-Instruct（基座） | 14.79% | 11.97% | 38.67% |
| Embodied-Interactor-7B（Stage 1） | 25.46% | 24.75% | 53.67% |
| Embodied-Explorer-7B（Stage 2） | 65.39% | 46.25% | 77.73% |
| **Embodied-Reasoner-7B（Stage 3，论文最终）** | **80.96%** | **55.07%** | **86.30%** |

### 我们的结果 vs 论文

| 指标 | 论文 Stage 1 | 论文 Stage 3 | 我们的结果 |
|------|:---:|:---:|:---:|
| 成功率 | 25.46% | 80.96% | **27.08%**（96有效内） |
| 模型参数 | 7B | 7B | 7B |
| 训练阶段 | 模仿学习 | 三阶段完整 | **未知** |

### 分析

**我们的结果（27.08%）接近论文 Stage 1（Embodied-Interactor, 25.46%），但远低于最终模型（80.96%）。** 这强烈暗示：

1. **模型身份疑点：** `e3d0` 结尾的模型可能只是 Stage 1（模仿学习）的产物，即 Embodied-Interactor，而不是经过三阶段训练的 Embodied-Reasoner。`e3d0` 可能表示 "3 epochs, decay 0"——即基座模型直接做 3 epoch 模仿学习，没有经过 rejection sampling 和 reflection tuning。

2. **量化影响：** 4-bit 量化（bnb）对 7B 模型可能有 1-3% 的性能损失，但不是主要原因。

3. **评估完整性：** 只有 96/809（11.9%）的任务有有效结果，其余因控制器崩溃丢失。如果补齐剩余任务，成功率可能会变化。

### 论文中关键结论对照

| 论文结论 | 我们的验证 | 说明 |
|---------|-----------|------|
| 三阶段训练从 14.79% → 80.96% | ⚠️ 部分验证 | 我们的 27.08% 接近 Stage 1 的 25.46% |
| Rejection Sampling 是最大提升点（25.46% → 65.39%） | ❌ 无法验证 | 模型可能不含 Stage 2/3 训练 |
| Reflection Tuning 继续提升（65.39% → 80.96%） | ❌ 无法验证 | 同上 |
| 简单 Search 任务上可能过度探索 | ⚠️ 观察到了 | 日志中模型经常在简单任务中过度探索 |
| 复杂 Composite 任务差距最大 | ✅ 验证 | 我们的 long-range 和 ordered 任务成功率 0% |
| 小模型可以超过大推理模型 | ❌ 无法验证 | 需要三阶段完整模型才能验证 |

## 评估过程中的问题

### 1. 控制器频繁崩溃

- Unity 进程在 ~20-30 个任务后 SIGSEGV
- 根因：12GB VRAM 不足以同时运行 VLM 模型（~8GB）和 AI2-THOR Unity 渲染（~2-3GB）
- 缓解：添加了 `test()` 返回 controller + 无条件重启机制
- 代价：每个崩溃损失 ~3 秒重启时间，累计 ~500+ 次恢复事件

### 2. VLM 服务周期性崩溃

- 因 KV cache 累积导致显存溢出，每 1-2 小时崩溃一次
- 缓解：loop 监控每 10 分钟检查，发现 GPU<3GB 自动重启 VLM
- 后果：重启期间的任务会失败（返回空），但被缓存跳到下一个

### 3. 只有 96/809 有效结果

- 控制器崩溃 → `get_trajectory()` 返回 None → `test()` 返回 → 主循环接收不到异常
- 虽然加了恢复机制，但 713 个任务仍然没有 result.json
- **根因：** `get_trajectory()` 用 `except Exception as e:` 吞掉了所有异常，外层无法区分"正常失败"和"控制器崩溃"

### 4. 评估指标与论文偏差

详见 `/home/user/Web/01-Projects/Embodied-Reasoner-评估代码与论文偏差分析.md`

## 总结

1. **当前模型（e3d0）大概率不是论文最终版本**，而是 Stage 1 产物
2. **评估框架存在架构问题**（控制器崩溃未传播、指标计算偏差）
3. **12GB VRAM 是硬件瓶颈**，导致 VLM 和 Unity 竞争显存
4. **26 个成功任务证明了模型基线能力**，但与论文 80.96% 无可比性

## 下一步建议

1. 确认模型身份：联系模型发布者确认 `e3d0` 的训练阶段
2. 下载三阶段完整模型重新评估
3. 修复 `get_trajectory()` 的异常传播路径
4. 使用更大显存的 GPU（24GB+）避免崩溃

## 相关文件

- 论文：`/home/user/Downloads/paper/Embodied-Reasoner Synergizing Visual Search, Reasoning, and Action for Embodied Interactive Tasks-dual (1).pdf`
- 论文笔记：`/home/user/Web/02-Papers/Embodied-Reasoner - Synergizing Visual Search Reasoning and Action for Embodied Interactive Tasks.md`
- 偏差分析：`/home/user/Web/01-Projects/Embodied-Reasoner-评估代码与论文偏差分析.md`
- 评估日志：`/tmp/eval_full_v2.log`
- 项目代码：`/home/user/github-product/embodied_reasoner/`
