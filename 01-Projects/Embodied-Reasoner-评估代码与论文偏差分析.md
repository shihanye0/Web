---
title: "Embodied-Reasoner 评估代码与论文指标口径偏差分析"
date: 2026-07-06
tags: [embodied-reasoner, evaluation, paper-alignment, metrics]
status: draft
---

# Embodied-Reasoner 评估代码与论文指标口径偏差分析

> 本文档记录项目 `evaluate/` 目录当前评估代码与论文 `arXiv:2503.21696v2` 指标定义之间发现的口径差异，供 Boss 结合代码、论文和实验复现需求核实。
>
> 结论先行：当前证据支持“论文指标文字定义与开源评估实现存在未充分说明的口径差异”。其中 `Search Efficiency` 的 `+1`、`Task Completeness` 的分母、以及缺少显式 `final_state` 检查是最强证据。本文不直接断言代码一定错误；更准确的表述是：若论文表 2 使用该代码计算，则论文需要补充实现口径；若按论文文字复现，则结果可能与代码输出不一致。

## 核查范围

- 论文：`/home/user/Downloads/paper/Embodied-Reasoner Synergizing Visual Search, Reasoning, and Action for Embodied Interactive Tasks-dual (1).pdf`
- 评估入口：`/home/user/github-product/embodied_reasoner/evaluate/evaluate.py`
- 指标实现：`/home/user/github-product/embodied_reasoner/evaluate/utils.py`
- 离线汇总：`/home/user/github-product/embodied_reasoner/evaluate/show_result.py`
- 测试数据：`/home/user/github-product/embodied_reasoner/data/test_809.json`

说明：当前仓库工作区已有未提交改动，以下判断基于当前工作区版本。

## 论文定义（原始文本）

> **Success Rate (%)**: "measures whether a task is successfully completed by evaluating if the key actions align correctly and if the final state meets the task criteria."
>
> **Search Efficiency**: "the ratio of key action numbers to predicted action numbers."
>
> **Task Completeness (%)**: "the proportion of predicted actions that belong to the set of key actions."

## 总体判断

| 指标 / 事项           | 论文口径                                  | 代码口径                                                    | 判断                               |
| ----------------- | ------------------------------------- | ------------------------------------------------------- | -------------------------------- |
| Success Rate      | key actions 对齐 + final state 满足任务标准   | `reward / total_reward` 是否满分；`single_search` 额外看当前可交互对象 | 方向接近，但没有显式 final-state evaluator |
| Search Efficiency | key action 数 / predicted action 数     | `(len(key_actions) + 1) / len(trajectory)`，失败任务为 0      | 存在明确公式口径差异                       |
| Task Completeness | predicted actions 中属于 key actions 的比例 | 命中的非导航关键交互 / 非导航关键交互总数                                  | 存在明确分母差异                         |
| Final state       | 测试格式声明包含 final state                  | 当前 `test_809.json` 未见 `final_state` 字段，代码未读取            | 论文描述与开源数据/代码不完全对应                |
| RER               | revisits / total explorations         | 重复 `navigate to` 目标数 / `navigate to` 总数                 | 基本一致，但“位置/区域”粒度不同                |

## 偏差 1：Success Rate 没有显式 final state 检查

**论文要求两个条件同时满足才算成功：**
1. key actions 对齐正确
2. **final state 满足任务标准**

**代码实际：`evaluate/utils.py:82-85`**
```python
"success": int(reward/total_reward),
```
`int(reward/total_reward)` 等价于 `1 if reward == total_reward else 0`。

**问题：**
- 代码没有读取 `final_state` 字段，也没有在任务结束后基于 AI2-THOR 状态做独立 final-state 校验。
- 对普通任务，成功主要由命中计入 reward 的关键交互动作决定；`end` 动作本身也会给 reward。
- 对 `single_search`，代码会额外检查 `legal_interactions` 中是否出现任务目标，或前一动作是否属于 key actions。这能近似判断搜索任务完成，但仍不是通用 final-state checker。
- `int()` 向下取整意味着必须命中 100% 的“计入 reward 的关键动作”才算成功；但这些动作不等于全部 key actions，因为 `navigate to`、`observe`、`move forward` 会被排除在 `total_reward` 之外。

**疑问：**
- 论文中 "key actions align correctly" 是指所有计入 reward 的关键交互都匹配，还是包含导航/观察动作在内的完整关键动作序列都匹配？
- 如果模型完成了 80% 的 key actions，这算不算 partially successful？
- 如果论文表 2 使用当前代码计算，是否应在论文中说明 Success Rate 是基于 key-action reward 满分，而不是独立 final-state verifier？

## 偏差 2：Search Efficiency 公式有 +1 偏移

**论文定义：** "ratio of key action numbers to predicted action numbers"

**代码实际：`evaluate/utils.py:84`**
```python
"efficiency": (len(key_actions)+1)/len(trajectory) if int(reward/total_reward) else 0.0,
```

**问题：**
- 分子是 `len(key_actions) + 1`，不是 `len(key_actions)`。`+1` 的来源不明。
- 分母 `len(trajectory)` 包含 `init`、`navigate to`、`observe`、`move forward` 等动作。论文的 "predicted action numbers" 是否应该排除这些？
- 失败时直接给 `0.0`，但论文没有说失败时 efficiency 为 0

**更严谨的解释：**
- `+1` 不一定是 bug。它可能是在补偿评估轨迹里固定存在的 `init` 记录，使“最短成功轨迹”的效率接近 1。
- 但论文没有披露这一实现细节。若读者按论文文字使用 `len(key_actions) / predicted_actions` 复现，会与开源代码结果不同。

**疑问：**
- `+1` 是否表示把 `init` 也视为评估轨迹中的固定动作？
- 论文中的 predicted action numbers 是否等于 `len(trajectory)`，还是只统计模型输出的可执行动作？
- 失败任务的 efficiency 置为 0 是否为论文表 2 口径？

## 偏差 3：Task Completeness 分母不一致

**论文定义：** "proportion of predicted actions that belong to the set of key actions"

按此定义：`completeness = 模型预测中属于 key_actions 的动作数 / 模型预测的总动作数`

**代码实际：`evaluate/utils.py:85`**
```python
"completeness": reward/total_reward,
```
其中 `total_reward` 是**去掉 navigate to / observe / move forward 后的 key_actions 数量**，不是论文说的 "predicted actions 总数"。

**问题：**
- 代码的分母是"非导航类 key_actions 数"（来自 ground truth）
- 论文的分母是"predicted actions 总数"（来自模型输出）
- 两者可能差异很大：如果模型输出了大量导航动作，代码会忽略它们，论文会算进分母

**更准确的代码口径：**

```text
Task Completeness = 命中的非导航关键交互数 / 非导航关键交互总数
```

其中非导航关键交互主要包括 `pickup`、`put`、`open`、`close`、`toggle`、`end` 等。`navigate to`、`observe`、`move forward` 不进入 `total_reward`。

**疑问：**
- 这种偏差在什么场景下会显著影响结果？
- 论文的 Table 2 中 completeness 数据（86.30%）是用哪种方式算出来的？
- 如果实际使用代码口径，论文是否应将定义改为 “proportion of required non-navigation key interactions completed”？

## 偏差 4：代码没有检查 final state

论文的测试数据格式是 `⟨Instruction, Key Action, Final state⟩`。但当前代码在 `metric()` 中只用了 `key_actions`，没有读取或检查 `Final state`。

**当前数据格式验证：**

`data/test_809.json` 中任务主要包含：

```json
{
  "scene": "FloorPlan1",
  "tasktype": "single_search",
  "taskname": "...",
  "task_metadata": {
    "taskname": "...",
    "tasktype": "...",
    "metadatapath": "...",
    "actions": [...],
    "totalreward": 2
  },
  "taskquery": "...",
  "identity": 1,
  "target_objects": [...],
  "related_objects": [...],
  "navigable_objects": [...]
}
```

当前检查未发现 `final_state` / `final state` / `finalstate` 字段。评估入口 `evaluate/evaluate.py` 也只从 `task_metadata.actions` 提取 `key_actions`。

**疑问：**
- 论文中 `Final state` 是人工标注但未开源，还是被编码进 `actions` / `target_objects` / `related_objects`？
- 如果要严格对齐论文，应新增显式 final-state schema 和基于 AI2-THOR metadata 的 final-state checker。

## 关于重复搜索检测

论文在 Metrics 章节的三个主指标之外，还在后文/附录定义了 Repeat Exploration Rate (RER)：

```text
RER = revisits to previous locations / total explorations
```

离线汇总代码中已有 `repeat_rate`：统计 `navigate to` 的目标列表，用重复目标数除以导航总数。这个方向与论文 RER 基本一致，但有一个口径差异：代码的“重复位置”是 `item` 字符串级别，不一定等价于论文中的 same location / same area。

因此这里不应写成“评估代码不需要为此新增 metrics”。更准确的是：主评估指标不包含 RER，但论文分析指标 RER 在 `evaluate/show_result.py` 中已有近似实现，若用于论文图 6，应说明位置粒度。

## 关于 Prompt 与 Observation-Thought-Action 格式

论文的训练数据是 Observation-Thought-Action 交错轨迹。评估时 prompt 没有强制要求模型输出 Thought（用 "can" 而非 "must"），但模型因训练习惯会自发输出推理文本。这不影响评估指标计算。

## 建议给 Boss 的一句话版本

当前开源评估代码并不是论文 Metrics 段落的逐字公式实现，而是一个带任务启发式的 automatic evaluator。它可能就是作者计算表 2 的真实口径，但论文没有充分披露这些实现细节。若要做复现或审稿式质疑，最稳的表述是：**论文指标定义与代码实现存在口径不透明和可复现性风险，尤其是 Search Efficiency、Task Completeness 和 final-state 检查。**

## 建议后续核查

1. 用当前 `evaluate/show_result.py` 重新汇总已有 `data/new_finetuned_model/**/result.json`，确认是否能复现论文表 2 的 80.96 / 55.07 / 86.30。
2. 构造 2-3 个最小轨迹样例，分别比较“论文文字公式”和“代码公式”的输出差异。
3. 检查作者是否在 README、supplementary 或 issue 中解释过 `+1`、失败 efficiency 置 0、以及 final state 的替代检查方式。
4. 如果要修代码，应先决定目标：复现论文结果，还是按论文文字定义重写指标。两者可能不能同时满足。

## 参考

- 论文：`/home/user/Downloads/paper/Embodied-Reasoner Synergizing Visual Search, Reasoning, and Action for Embodied Interactive Tasks-dual (1).pdf`
- 笔记：`/home/user/Web/02-Papers/Embodied-Reasoner - Synergizing Visual Search Reasoning and Action for Embodied Interactive Tasks.md`
- 评估代码：`/home/user/github-product/embodied_reasoner/evaluate/utils.py`（metric 函数 26-88 行）
- 评估日志：`/tmp/eval_full_v2.log`
