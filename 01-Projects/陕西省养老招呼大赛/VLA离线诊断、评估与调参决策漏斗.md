# VLA 离线诊断、评估与调参决策漏斗

> 目的：在机器人不动时判断一个 checkpoint 值不值得上机，并把失败归到唯一 owner。离线 artifact 必须写 `physical_actions_emitted=0`。

## 先冻结比较条件

每次诊断先写不可变身份：checkpoint SHA、训练数据/`stats.json` SHA、action layout/mapping SHA、task 文本、seed、serve 版本、输入 RGB/state 的 episode/frame。一次只改一个变量。

不要用 val loss、训练步数、一次肉眼 rollout 或“writer 成功”决定上机；它们都不能说明 policy、映射和执行层分别是否正确。

## 推荐漏斗

| 关 | 要回答的问题 | 最小证据 | 失败后只查/改的 owner |
| --- | --- | --- | --- |
| 0 身份 | 比较的是不是同一个任务与动作合同？ | checkpoint/stats/layout/task/seed manifest | 身份、task、stats、serve；不是 controller |
| 1 管线 | GT 能否无歧义走完 dataset → action layout → normalize → denormalize → adapter？ | shape、关节名称、round-trip error、stats、时间对齐、padding mask | mapping、stats、时间/掩码；不要先补数据或调模型 |
| 2 训练拟合 | 喂**训练集抓取前 GT 帧**时，输出是否像该帧 GT？ | raw vs GT、reach/grasp、关键关节、训练帧与新帧各一条 | loss/mask、训练配方、目标；不是 OOD 或机器人 |
| 3 重复性 | 同一输入是否稳定？ | 固定 seed 下 N 次 chunk 的 pairwise L∞ | serve/seed/采样；不要以更多 eval steps 当部署修复 |
| 4 原始轨迹预算 | 模型原始 chunk 是否已经抖动或跳变？ | arm 相邻 `|Δq|` p50/p90/p99、关键关节反转数、horizon 1/3/5/30 | 时间建模、平滑目标、history；不是 slew |
| 5 执行保真 | 安全层有没有删掉一个原本有效的意图？ | raw → mapped → sent → returned 的同帧记录 | candidate bound、slew、adapter/runner；仅 raw 合格时才查这里 |
| 6 泛化反事实 | 是现场输入失败，还是 checkpoint 在训练帧也失败？ | 同一模型上的 field、train、image/state crossed request | 数据覆盖、视觉、状态或两者交互；不要猜 |

Gate 1 以前不谈模型；Gate 2–4 失败不让机器人动；Gate 5 只在 raw 通过后才有资格成为 root cause；Gate 6 用来区分 field generalization 与训练本身就没学会。

## 指标怎样读

### 1. 不只看数值，要看任务意图和时序

对抓取任务，至少记录 `reach`、`grasp`、`grasp_onset_frame`、连续窗口内是否持续抓取，以及关键指关节（如 `Ri0`）的最大值。模型“轨迹很平滑但一直张手”仍不合格；很晚才抓也不等于抓取阶段正确。

### 2. `|Δq|` 同时看幅度和形状

以 arm 维度为主算相邻帧 `|Δq|` 的 p50/p90/p99，并记录肩、腕的符号反转。GT 连续轨迹接近 `0.008 rad` 而模型为 `0.4 rad`，说明问题已在 raw policy 内；同一 chunk 中反复正负跳变则是高频轨迹问题，即使终点看上去接近也不能上机。

手指的全维误差常比手臂大，不能用“24D max error 约 1 rad”直接宣布手臂塌缩。手臂相对 GT、手指意图和 raw→sent 的各自指标必须分开报告。

### 3. 先 raw，后 sent，最后 returned

```text
observation/RGB → model raw → layout/map → safety sent → robot returned observation
```

- raw 已无抓取：模型、训练或数据 owner；不要改 runner。
- raw 有抓取、sent 没有：安全/adapter owner；不可以放宽限位来掩盖高频 arm。
- sent 有、returned 无：控制通路或观测 owner；先做受监督的执行验证。

## 从结论到下一步

| 离线结论 | 下一步 | 不该做的事 |
| --- | --- | --- |
| 身份 Gate 通过 | 记录“不是 task/stats 身份导致”，进入下一关 | 因字符串不同就重训 |
| mapping/stats/时间/掩码失败 | 修该管线，重跑同一 probe | 同时改数据、模型和 controller |
| train frame 也拟合失败 | 检查 loss/mask、训练目标和优化；新配方只改一个变量 | 直接怪现场、先大规模采数据 |
| raw 跳变/反转超预算 | 在模型侧处理 temporal/smoothness/history，并用同一 probe 比较 | 调大 slew 或压低门槛 |
| raw 合格但 sent 丢意图 | 定位 candidate/slew/adapter 的具体帧和关节 | 把被限速后的结果说成模型效果 |
| train 成功、field 失败 | 做 image/state crossed counterfactual，再针对缺失因素补采 | 只看现场失败就改 controller |
| 固定输入输出不稳定 | 固定或审计 seed/serve；确认采样行为 | 把“多采样步”当最终部署方案 |

## Gate 2 有两把尺子，不能混用

1. **Pi0.5 P511 身份 Gate 2**：同一输入只换短 task / 官方 task，量 `50×24` 前 30 步 arm 的相邻 `|Δq|` p50。官方 task 已 `<0.05` 时，只能说明“身份缺口不是本次开训理由”。
2. **模型 train-fit Gate**：模型在训练集抓取前 GT 帧的 raw 轨迹、相对 GT 误差与任务意图。它回答模型是否学会该阶段；即使身份 Gate 通过，train-fit 仍可能失败。

把两把尺子写在同一个报告里时，要明确名称、输入、输出和决策作用，不能拿其中一把替另一把放行实机。

## 最小 artifact 模板

```json
{
  "candidate": {"checkpoint_sha256": "…", "stats_sha256": "…", "task": "…", "seed": 0},
  "probe": {"dataset": "…", "episode": 4, "frame": 50, "physical_actions_emitted": 0},
  "pipeline": {"name_check": "…", "roundtrip_max_abs": 0.0, "alignment": "…"},
  "raw": {"intent": "…", "adjacent_arm_p50": 0.0, "sign_changes": {}},
  "execution": {"sent_keeps_intent": false, "first_lost_joint": "…"},
  "decision": {"gate": 0, "owner": "…", "next_change": "…", "robot_allowed": false}
}
```

保留对应的 request、raw action、sent action、returned observation 和摘要；用 hash 指向，不覆盖旧 artifact。这样下一颗 checkpoint 能直接在同一 frame、同一指标、同一安全合同下比较。

## 当前项目的反例结论

- HEX 30k：训练帧与现场帧都不抓，且 batch/online 一致，先冻结 checkpoint；不是去改 G1 runner。
- Psi0：mapping/stats/对齐和固定 seed 已排除为首因，当前主要问题是 train-fit 与 raw temporal；安全 slew 不应被放宽。
- Pi0.5：official task 的身份 Gate 2 已过，只停止“因 task/stats 不一致就开训”的冲动；它不是任务成功认证。

离线通过也不等于任务成功。只有完成本漏斗、明确需要验证的物理问题，并获得一次受监督、有界实机确认后，才允许让机器人执行。
