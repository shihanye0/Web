---
title: "{{title}}"
date:
  "{ date }":
tags: []
aliases: []
---
# VLA视觉/物理环境攻击：选题、论文现状、创新空间与复现路线

研究预研整理 · 截至2026年11月8日

结合你与西北农林科技大学唐文兵老师的讨论、你已经阅读的三篇L侧攻击论文，以及课题组现有的Unitree G1、π0.5和多卡服务器，我认为现在可以形成一份相对清晰的研究规划了。

## 一、先给出结论

我建议把V侧物理环境攻击作为主研究方向，把自动化场景生成与闭环安全测试作为潜在方法创新，把G1实机作为重要的实验验证资源。

但这次文献检索也发现了一个必须重视的问题：

截至2026年11月，VLA视觉攻击、实体贴片、三维纹理攻击、环境扰动评测和部分动态环境攻击，都已经有正式发表的代表性论文。因此，单纯把L侧攻击换成V侧攻击，或者证明环境变化能降低任务成功率，都不足以形成有竞争力的论文创新。

### 1.1 我最推荐的课题名称

推荐的初步课题名称

## 面向视觉-语言-动作模型的任务保持型物理场景攻击与闭环安全测试研究

Task-Preserving Physical Scene Attacks and Closed-Loop Safety Testing for Vision-Language-Action Models

一句话定义

在保持原始任务目标和可执行性不变的前提下，通过自然、可控、物理可实现的视觉环境变化，主动寻找VLA模型在连续感知和动作执行过程中的行为偏移与安全失效，并分析其触发条件及失效机制。

这里的“任务保持型”来自你之前对语义保持型语言攻击的思考，但两者含义不同：

- L侧的语义保持： 指令换一种表达方式，任务含义不变。
- V侧的任务保持： 环境发生变化，但目标、成功标准及任务可执行性不变。
- 行为有效： 攻击不仅影响模型内部视觉表示，还要导致可测量的错误动作、轨迹偏移或安全问题。

这可以构成你新课题的基本约束。

### 1.2 目前最适合你的研究定位

主方向：VLA物理环境安全攻击

优先

关注场景中物体、遮挡、背景、光照等可实现的环境变化及其对机器人动作的影响。

方法方向：自动化、黑盒、行为反馈驱动的场景搜索

研究在有限的评测预算内，怎样比随机扰动更有效地发现VLA安全缺陷。

扩展方向：闭环失效机制与恢复能力

分析攻击在何时触发、如何影响后续动作，以及机器人能否恢复任务执行。

我暂时不建议把L+V联合攻击、因果分析、动态攻击和防御方法全部写进课题名称。这些都可能是后续创新点，但在没有实验结果之前，同时承担会导致研究范围过大。

## 二、当前研究已经发展到哪一步？

首先需要明确：V侧攻击不是一个单独的研究类别，它至少可以分成五种。

| 类别      | 典型攻击方式         | 核心研究问题             |
| ------- | -------------- | ------------------ |
| 数字视觉攻击  | 像素扰动、图像贴片      | 如何干扰VLA视觉表示和动作预测   |
| 实体视觉攻击  | 贴纸、实体纹理、物体表面变化 | 数字攻击能否在真实物理环境生效    |
| 自然环境攻击  | 光照、阴影、背景、合理遮挡  | 正常环境变化能否被主动利用来诱发失效 |
| 时序/闭环攻击 | 在关键动作阶段改变环境    | 何时干扰最有效，错误如何积累     |
| 自动化安全测试 | 场景生成、变异、搜索与评价  | 如何系统、高效地发现可复现的安全缺陷 |

从你的资源条件和唐老师的研究基础看，第三类与第五类结合最有价值，第四类适合作为后续深入方向。

也就是：

> 不是单纯优化一张对抗贴片，而是搜索真实环境中合理的场景变化，并观察它们如何影响VLA的闭环行为。

不过，这个组合仍需要与现有工作进行严格对比，才能确定真正的新颖性。

## 三、最相关论文：哪些已经做了，哪些与你重复？

这部分是整个选题最重要的内容。

我把相关工作分为：直接攻击论文、环境鲁棒性基准、安全测试方法三组。

### 3.1 第一组：直接攻击VLA视觉输入的论文

| 论文                                                                                                                                                                                                                                                     | 发表情况        | 已经解决的问题                        | 对你新课题的影响          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------- | ------------------------------ | ----------------- |
| [Exploring the Adversarial Vulnerabilities of VLA Models](https://openaccess.thecvf.com/content/ICCV2025/html/Wang_Exploring_the_Adversarial_Vulnerabilities_of_Vision-Language-Action_Models_in_Robotics_ICCV_2025_paper.html?utm_source=chatgpt.com) | ICCV 2025   | 视觉贴片、动作扰乱、定向轨迹攻击               | 不能把视觉攻击或动作偏移作为首创  |
| [When Robots Obey the Patch](https://openaccess.thecvf.com/content/CVPR2026/html/Lu_When_Robots_Obey_the_Patch_Universal_Transferable_Patch_Attacks_on_CVPR_2026_paper.html?utm_source=chatgpt.com)                                                    | CVPR 2026   | 通用贴片、跨模型迁移、物理执行                | 不能仅以跨模型贴片攻击为创新    |
| [Tex3D](https://arxiv.org/abs/2604.01618?utm_source=chatgpt.com)                                                                                                                                                                                       | ACM MM 2026 | 物体表面3D对抗纹理、轨迹感知优化、真实机器人测试      | 不能把三维物体纹理攻击作为空白   |
| [Phantom Menace](https://ojs.aaai.org/index.php/AAAI/article/view/40881?utm_source=chatgpt.com)                                                                                                                                                        | AAAI 2026   | 相机和麦克风的物理传感器攻击、Real-Sim-Real测试 | 不能仅宣称真实传感器攻击是首次   |
| [Exploiting Vulnerabilities](https://arxiv.org/abs/2609.39178?utm_source=chatgpt.com)                                                                                                                                                                  | 2026预印本     | 将带对抗纹理的实体球体放入相机视野              | 不能仅以添加实体干扰物作为新攻击面 |

这些工作的内容与发表情况，均能从正式会议页面、论文记录或官方仓库核对。Tex3D的作者仓库已标注ACM MM 2026录用。

[image](https://www.google.com/s2/favicons?domain=https://openaccess.thecvf.com\&sz=32)

CVF Open Access+4



这里有一个很重要的区分：

对抗贴片、对抗纹理，与自然物理场景变异不是完全相同的问题。

前者往往需要优化特殊视觉图案；后者可以仅改变已有的真实场景参数，例如无关物体的位置、自然光照、合理遮挡关系等。

不过Tex3D和实体对抗球体已经进一步削弱了“物理攻击很少”的论点，所以不能只靠“攻击发生在物理世界”与现有工作区分。

### 3.2 第二组：与你更容易发生实质性重复的环境评测论文

这是我认为你必须重点警惕的一组。

| 论文                                                                                                                                                                                                                  | 发表情况           | 已有研究内容                           | 重复风险 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | -------------------------------- | ---- |
| [LIBERO-Plus](https://openaccess.thecvf.com/content/CVPR2026/html/Fei_LIBERO-Plus_A_Progressive_Robustness_Benchmark_for_Visual-Language-Action_Models_CVPR_2026_paper.html?utm_source=chatgpt.com)                 | CVPR 2026      | 七大类扰动、自动化生成、多模型鲁棒性分析             | 很高   |
| [VLA-Arena](https://proceedings.mlr.press/v306/zhang26cp.html?utm_source=chatgpt.com)                                                                                                                               | ICML 2026      | Safety、Distractor、任务难度分级、语言和视觉扰动 | 很高   |
| [REALM](https://martin-sedlacek.com/realm/?utm_source=chatgpt.com)                                                                                                                                                  | IEEE RA-L 2026 | 15类扰动、真实与仿真评测一致性、操作任务            | 高    |
| [The Colosseum](https://arxiv.org/abs/2402.08191?utm_source=chatgpt.com)                                                                                                                                            | 2024研究工作       | 14个环境扰动维度及仿真到现实关联分析              | 高    |
| [VLABench](https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_VLABench_A_Large-Scale_Benchmark_for_Language-Conditioned_Robotics_Manipulation_with_Long-Horizon_ICCV_2025_paper.html?utm_source=chatgpt.com) | ICCV 2025      | 大规模语言条件操作、空间与纹理理解、长时序任务          | 中    |

[image](https://www.google.com/s2/favicons?domain=https://openaccess.thecvf.com\&sz=32)

CVF Open Access+4

[LIBERO-Plus: In-depth Robustness Analysis of Vision-Language-Action Models](https://images.openai.com/static-rsc-4/CAcb_b3MMoaCLw5pR-R53haukcapDULpkeNYv2SLF6fvoIYofceKUzPRUPuY39Tz6XHZFeC3JxkphAeV5x2yhKEqGbUCSvJraieA4VT6Mbf4tFjkeQZeNaIxERYhWMCFj6ezKxPRcx3kXZeAMrmVs3ykRfqa0ay7vIdQ5u20ChI?purpose=inline)

LIBERO-Plus — 最需要防止重复的工作

覆盖物体布局、相机视角、机器人初始状态、指令、光照、背景纹理和传感器噪声。

它不仅做单变量评测，还分析扰动组合、不同难度下的模型表现。

[image](https://www.google.com/s2/favicons?domain=https://openaccess.thecvf.com\&sz=32)

CVF Open Access



因此，“增加几种环境扰动，对比成功率”已经不是充分的新贡献。

[VLA-Arena: Comprehensive Benchmark for Vision-Language-Action Models | Leaderboard & Task Store](https://images.openai.com/static-rsc-4/HFkGRgCy8P8T5vyLINUxOnyDih0XEzjpGwFUsQjjK95fzGr3YCl8DRtBdoG67brTLZzJosroq8mMqB0GnZAIV3Md72Ny7k7TUwEdKCHczl9TXyOHQEA-wXcWeZzgA1HpInZepL5OEnp2b2cMQoKsPHGIfiQmKrr-kB42Z6fjlV0?purpose=inline)

VLA-Arena — 需要纳入核心Related Work

已经设计Safety、Distractor、Extrapolation、Long Horizon等任务，并能施加不同级别的语言和视觉变化。

其中的静态/动态干扰物、安全成本评价，与你计划中的研究高度相邻。

[image](https://www.google.com/s2/favicons?domain=https://vla-arena.github.io\&sz=32)

VLA Benchmark and Leaderboard



[REALM: A Real-to-Sim Validated Benchmark for Generalization in Robotic Manipulation | alphaXiv](https://images.openai.com/static-rsc-4/_9aIawxZfx7XJlWRAu_fQSPhADAot24IghVqZAY-qcXgEPXiSeHLk-vOHz76ykkIG6juDWx9EfDZhmbPNe2a2rNeTMKgMsA4fRTYKRgHCXEr200g-eg99G29zSh97V3B2bdYq1vNg3g7mnyk7YJUroqG_OBeIg3iS79o_DvXtIA?purpose=inline)

REALM — 是真机验证方面的强对照

支持视觉、语义和行为扰动，并通过真实操作任务检验仿真评测与实机表现的关联。

官方仓库还提供了π0.5评测的快速入门说明。

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+1



### 3.3 第三组：唐老师方向特别值得看的安全测试方法

| 工作                                                                                                                                                                                                             | 核心贡献                           | 你可以借鉴什么               |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | --------------------- |
| [ILA — Shedding Light on VLN Robustness](https://openaccess.thecvf.com/content/CVPR2026/html/Li_Shedding_Light_on_VLN_Robustness_A_Black-box_Framework_for_Indoor_CVPR_2026_paper.html?utm_source=chatgpt.com) | CVPR 2026，唐文兵参与；静态和动态室内光照黑盒攻击  | 自然物理变量、攻击时机、行为反馈搜索    |
| [Metamorphic Testing of VLA-Enabled Robots](https://conf.researchr.org/details/icst-2026/icst-2026-research/33/Metamorphic-Testing-of-Vision-Language-Action-Enabled-Robots?utm_source=chatgpt.com)            | ICST 2026；使用蜕变关系检测任务失败以外的轨迹异常  | 测试预言问题、任务保持关系、行为异常判定  |
| [Causality-aware Safety Testing for Autonomous Driving Systems](https://ink.library.smu.edu.sg/sis_research/11028/?utm_source=chatgpt.com)                                                                     | IEEE TSE 2026，唐文兵参与；因果感知场景模糊测试 | 从场景变异、动作与安全违反关系设计测试方法 |
| [Resilience Matters](https://arxiv.org/abs/2608.23839?utm_source=chatgpt.com)                                                                                                                                  | 2026预印本；恢复能力、稳定性与承压能力评价        | 超越任务成功率的闭环行为指标        |

[image](https://www.google.com/s2/favicons?domain=https://openaccess.thecvf.com\&sz=32)

CVF Open Access+3

我会把这四篇看作你未来方法设计的四个来源：

- ILA：怎样构造自然物理攻击。
- 蜕变测试：怎样判断模型行为是否异常。
- Causal-Fuzzer：怎样高效搜索不同的失效场景。
- Resilience Matters：怎样衡量失效及恢复过程。

但不能把四篇方法简单拼接起来当作创新，需要提出明确的新问题，并验证现有方法为什么不能解决。

## 四、哪些论文创新已经被占据？

这张表建议你保存下来，以后每次想新idea都拿它对照。

| 可能想到的创新点             | 我的判断       | 最直接的已有工作                    |
| -------------------- | ---------- | --------------------------- |
| 首次对VLA进行视觉攻击         | 已有         | ICCV 2025                   |
| 使用可打印对抗贴片            | 已有         | ICCV 2025、CVPR 2026         |
| 在物体表面优化3D纹理          | 已有         | Tex3D                       |
| 改变光照攻击机器人            | 已有         | ILA、Phantom Menace          |
| 改变物体位置、背景或遮挡，研究成功率下降 | 已有类似工作     | LIBERO-Plus、VLA-Arena、REALM |
| 在机器人运动的关键时刻施加扰动      | 已有相关方法     | ILA动态模式                     |
| 使用语言与视觉联合扰动          | 已有相关评测     | LIBERO-Plus、VLA-Arena       |
| 自动化生成VLA评测场景         | 已有         | LIBERO-Plus、VLA-Arena       |
| 用动作轨迹评价VLA失效         | 已有         | ICCV 2025、ICST 2026         |
| 使用G1做物理攻击实机验证        | 可以成为有价值的证据 | 不能仅凭机器人型号宣称方法创新             |

这里有个重要结论：

目前并没有理由把你的选题判断为“已经被完全做完”，但它的基础攻击面和通用测试框架已经很成熟了。

真正的研究空间，需要进一步缩小到某个现有方法做得不够好的问题。

## 五、我认为真正值得尝试的三个细分方向

我按照创新空间、实验可行性、与唐老师研究积累的契合度，以及是否适合你目前的G1项目进行排序。

### 方向A：任务保持约束下，行为反馈驱动的物理场景攻击搜索

首选研究假设

核心问题：

> 在物理环境变化必须自然、合法且不改变任务的前提下，如何用有限次数的VLA闭环执行，主动发现高风险攻击场景？

例如，机器人需要抓取一个杯子。你不移动目标杯子，也不改变抓取任务，只调整周围无关物体的布局、可允许的遮挡或光照。

普通鲁棒性测试可能随机生成很多场景，然后统计成功率。

你要研究的是：能否根据机器人已经产生的错误行为，指导下一次环境变异，更高效地发现具有不同失效机制的场景？

建议的研究框架

原始任务 + 正常场景

建立可重复成功的闭环执行基线

任务保持型场景变异器

物体布局、背景干扰、光照、合理遮挡

合法性与可执行性检查

剔除碰撞、目标不可达、任务语义改变的场景

VLA闭环Rollout + 行为评价

任务结果、目标偏差、轨迹异常、安全成本

反馈驱动的下一轮场景搜索

搜索新的高风险区域，而非重复相同失败样本

这个方向真正可能形成贡献的地方，不是场景变异本身，而是任务约束下的高效攻击搜索、失效多样性与行为级反馈机制。

必须比较LIBERO-Plus的自动化扰动生成、ILA的黑盒搜索，以及唐老师Causal-Fuzzer的因果覆盖思想，证明新方法在相同预算下确实发现了更多有效、不同类型的失效。

我认为这是最值得先做可行性实验的方向。

### 方向B：面向VLA闭环执行阶段的动态环境攻击

核心问题：

同样的环境变化，发生在不同的执行阶段，影响是否不同？

例如机器人抓杯过程可以分成：

1

识别目标

2

接近目标

3

执行抓取

4

放置/完成

示意性的操作阶段，具体阶段划分需要根据实际VLA策略和动作日志决定。

研究相同干扰发生在阶段1、2、3时的不同影响，以及机器人能否在后续动作中恢复。

它更贴近真实机器人，但也更容易与ILA的动态光照攻击、Tex3D的轨迹关键帧优化发生重合。

因此，新颖性不能只是“寻找最佳攻击时刻”，还需要考虑新的时序失效机制，例如持续控制误差、恢复过程中的风险，或者长期动作序列中的异常传播。

我建议先做方向A，再根据阶段敏感性实验决定是否深入方向B。

### 方向C：视觉环境变化下的跨模态行为失效分析

这部分最适合利用你已读的三篇L侧论文。

研究：

> 当语言指令本身的任务语义保持不变时，环境变化为什么会导致VLA产生不同动作？视觉与语言是否存在不稳定的依赖关系？

可以使用一组受控的2×2实验：

|        | 原始视觉场景 | 合法视觉变化 |
| ------ | ------ | ------ |
| 原始语言指令 | 基准A    | 仅V变化   |
| 语义等价改写 | 仅L变化   | L+V变化  |

但必须明确：LIBERO-Plus、VLA-Arena已经研究过语言与视觉扰动及其组合，因此四组实验本身不是新贡献。

如果将来能证明某种跨模态交互的具体机制，并据此提出更高效的测试方法，才值得发展为独立论文。

### 三个方向的取舍

| 方向         | 发表潜力判断        | 工程难度 | 我的建议    |
| ---------- | ------------- | ---- | ------- |
| A：行为反馈场景搜索 | 较有希望形成方法型论文   | 中高   | 主线      |
| B：执行阶段动态攻击 | 具有吸引力，但重合风险较高 | 高    | A的进阶    |
| C：跨模态失效机制  | 有研究深度，容易做大    | 中高   | 作为扩展或备选 |

这里的发表潜力是基于现有文献的研究判断，不是已经确认存在的novelty，更不是录用概率预测。

## 六、精选阅读路线：不再盲目扩充论文数量

你已经读过：

LIBERO-Para → Q-DIG → Trajectory-Level Redirection

这三篇属于已完成的L侧基础阅读，暂时不需要重新精读。

我建议新阶段采用“核心六篇 + 辅助文献”的方式。

### 6.1 六篇核心论文

## 1

LIBERO-Plus — CVPR 2026

环境鲁棒性和任务保持的基础

精读： 扰动参数、场景生成、任务合法性、渐进难度、扰动组合实验。

读完要能回答：已有的环境变异已经覆盖到什么程度？它是主动搜索失效，还是生成测试场景后进行评测？

[官方代码](https://github.com/sylvestf/LIBERO-plus?utm_source=chatgpt.com)

## 2

ILA — CVPR 2026，唐老师参与

真实合理环境变量与黑盒攻击方法

精读： Threat Model、SILA/DILA、攻击目标、时序权重、搜索算法、Query Budget和消融实验。

重点理解它如何利用环境变化制造导航错误，以及哪些思想能够迁移到VLA操作。

[官方代码](https://github.com/LiChenyang0820/ILA4VLN?utm_source=chatgpt.com)

## 3

Exploring the Adversarial Vulnerabilities — ICCV 2025

VLA攻击目标与动作级评价

精读： Untargeted / Targeted Objectives、动作差异指标、轨迹操纵、数字到物理实验。

重点学会把攻击效果定义为机器人动作错误，而不是只让视觉编码特征发生变化。

[项目主页和代码入口](https://vlaattacker.github.io/?utm_source=chatgpt.com)

## 4

VLA-Arena — ICML 2026

安全任务、干扰物与能力边界

精读： Safety / Distractor任务设计、L0–L2难度层级、视觉扰动、Cumulative Cost评价。

重点找出：哪些场景已经存在，怎样避免重新实现同样的Benchmark。

[项目主页及开源框架](https://vla-arena.github.io/?utm_source=chatgpt.com)

## 5

Metamorphic Testing of VLA-Enabled Robots — ICST 2026

自动化安全测试与行为异常判定

精读： Metamorphic Relations、测试预言、轨迹评价、失败类型与对照实验。

你要弄清楚：任务不变时，究竟应要求哪些行为性质保持不变，哪些变化是合理的？

[官方代码](https://github.com/pablovalle/MT_of_VLAs?utm_source=chatgpt.com)

## 6

Tex3D — ACM MM 2026

物体级真实攻击与关键帧优化

重点读： 3D纹理表示、Trajectory-Aware Optimization、跨视角攻击、EoT和实机实验。

用来判断你是否需要走复杂的可微渲染路线；如果主要做自然场景搜索，不需要先掌握全部优化细节。

[官方代码](https://github.com/vla-attack/tex3d?utm_source=chatgpt.com)

这些论文中，第1、2、4、5篇与你计划研究的自动化场景安全测试最接近；第3、6篇帮助你学习V侧攻击的具体技术。

### 6.2 其余论文怎么处理？

| 文献                         | 建议                    |
| -------------------------- | --------------------- |
| Resilience Matters         | 选读恢复、稳定性和过程指标         |
| REALM                      | 选读真实/仿真一致性及π0.5评测     |
| VLABench                   | 选读任务生成与场景构造，不用全读长时序推理 |
| A2Eval                     | 后续要提高评测效率时再读自动化评测方法   |
| When Robots Obey the Patch | 需要跨模型迁移基线时读、复现        |
| Phantom Menace             | 需要物理传感器攻击对照时再读        |
| SABER                      | 只读黑盒搜索与奖励设计，暂不复现      |
| RoboGCG、AttackVLA及综述       | 写Related Work时按需查阅    |
| Awesome Agentic Robots     | 当文献索引库使用，不是逐篇阅读任务     |

其中VLABench已经公开π0.5相关微调检查点，REALM也有π0.5评测入口，所以它们是你以后需要切换实验环境时的实际候选，而不只是用来引用的论文。

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+1



## 七、最关键：到底应该复现哪些论文？

我的建议是：

不要同时复现六篇。先选一个环境评测基线，再选一个V侧攻击基线，最后实现你自己的搜索方法。

因为你的目标是提出新方法，而不是把现有攻击论文的代码全部运行一遍。

### 7.1 复现优先级

| 工作                       | 复现建议            | 目标                 |
| ------------------------ | --------------- | ------------------ |
| LIBERO + LIBERO-Plus     | 优先完整跑通一部分       | 获得正常场景和环境扰动场景的闭环结果 |
| ICCV 2025视觉攻击 / UPA-RFAS | 选其中一个做小规模基线     | 理解视觉攻击如何引起动作偏移     |
| ILA                      | 优先复现搜索思想，而非全部系统 | 学习黑盒物理变量攻击         |
| ICST 2026蜕变测试            | 借鉴并实现少量行为指标     | 检测任务失败之外的行为异常      |
| Tex3D                    | 暂时不做完整复现        | 与三维纹理优化方法进行对照      |
| REALM / VLABench         | 后续按需求选一个        | 跨环境或π0.5实验验证       |

### 为什么不首先完整复现ILA？

虽然ILA是唐老师参与的工作，但它研究的是视觉语言导航VLN，使用SPOC/CHORES等导航相关资源，并不是直接基于LIBERO的机械臂操作型VLA。官方代码也要求安装相应的导航场景和模型资源。

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub



所以：

ILA适合作为攻击方法的直接参考，不一定适合成为你第一个运行的实验平台。

把它的方法思想移植到已运行的VLA操作环境，比现在就维护两套完全不同的仿真系统更符合你的情况。

## 八、建议采用的实际实验路线

### 阶段1：建立一个真正可用的VLA闭环评测环境

我推荐从 LIBERO + LIBERO-Plus + OpenVLA-OFT 这一组合开始。

LIBERO-Plus官方仓库支持替换原始LIBERO环境，UPA-RFAS也公开了基于OpenVLA-OFT的LIBERO评测脚本及已有贴片检查点。相比从零实现攻击系统，这是一条比较清晰的起点。

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+1



第一阶段验收清单

成功加载一个VLA模型和匹配的评测任务

运行正常场景，保存任务成功率

固定随机种子，保存相机图像、动作与末端轨迹

运行至少一种LIBERO-Plus环境扰动

对比相同初始条件下的正常与扰动执行

能够回放至少一个具体失效案例

0 / 6 项完成 复制清单

第一阶段最重要的产出不是攻击成功率，而是一个稳定、可重复的完整Rollout。

如果正常任务都不能稳定成功，后面就很难判断失败究竟来自攻击还是模型本身。

### 阶段2：复现基础V侧攻击和自然场景扰动

建议先选择三种环境因素：

| 环境因素   | 最小实现            | 攻击重点      |
| ------ | --------------- | --------- |
| 无关物体布局 | 在桌面合法区域添加或移动干扰物 | 视觉注意、目标混淆 |
| 光照变化   | 修改照明强度或方向       | 感知稳定性     |
| 背景干扰   | 改变背景中不影响任务的视觉元素 | 场景依赖与泛化   |

其中建议优先测试无关物体布局和自然遮挡关系。

因为唐老师已经对光照攻击有研究成果，而物体布局更容易和你们的杯子抓取任务相联系。

不过这个优先级是实验便利性的判断，不代表物体布局一定有更大的论文创新空间。LIBERO-Plus和VLA-Arena已经覆盖了相关环境变化。

在这一阶段，不需要复杂攻击算法。

先建立三个基线：

1. Random：在合法参数空间中随机采样。
2. Grid / Uniform：均匀覆盖场景参数。
3. 已有扰动基线：使用LIBERO-Plus已有场景或简单参考其生成方式。

你需要发现：哪些合法环境变化能稳定引起错误？错误是否可以重复？

### 阶段3：设计自己的攻击场景搜索器

这是最可能形成论文方法的阶段。

可以先定义场景参数：

\\[ \theta=(p\_{\mathrm{distractor}},l,o,b) \\]

其中分别代表干扰物位置、光照、遮挡参数和背景参数。

VLA策略保持不变：

\\[ a_t=\pi(o_t,I) \\]

其中 \\(I\\) 为不变的任务指令，\\(o_t\\) 为机器人当前视觉观测。

攻击者搜索：

\\[ \theta^\*=\arg\max\_{\theta\in\Theta\_{\mathrm{valid}}} J\bigl(\tau(\pi,I,\theta)\bigr) \\]

这里：

- \\(\Theta\_{\mathrm{valid}}\\)：任务目标不变、物理可行、场景合法的变化集合。
- \\(\tau\\)：VLA在场景中的完整闭环执行轨迹。
- \\(J\\)：衡量任务失败、轨迹异常或安全失效的目标函数。

这个公式只是问题建模，不是创新算法。

之后才需要考虑搜索算法：随机搜索、贝叶斯优化、进化搜索，或者利用机器人行为反馈的自适应变异。

新方法必须说明它比现有方案多解决了什么困难，例如：

- 在相同Rollout预算下发现更多独立的安全失败。
- 在严格任务保持约束下找到更有效的攻击。
- 能解释并覆盖不同的场景—行为—失效关系。
- 对未参与搜索的任务、模型或真实场景仍然有效。

我尤其建议你跟唐老师讨论因果关系覆盖与行为反馈驱动搜索是否能结合。他的Causal-Fuzzer已经研究了场景、动作和安全违反之间的关联，但这些思想迁移到VLA之后仍需要证明有新的方法贡献。

[image](https://www.google.com/s2/favicons?domain=https://ink.library.smu.edu.sg\&sz=32)

SMU InK



### 阶段4：设计严谨的行为评价体系

只比较攻击前后的任务成功率不够。

我建议至少从以下维度记录结果。

| 指标                          | 评价什么               | 为什么重要       |
| --------------------------- | ------------------ | ----------- |
| Clean Success Rate          | 正常场景成功率            | 确定任务基线      |
| Attack-Induced Failure Rate | 原本可成功的任务，在攻击后失败的比例 | 区分攻击失败与固有失败 |
| Targeted Attack Success     | 是否发生指定的错误结果        | 支持定向攻击研究    |
| Trajectory Deviation        | 相同任务下的动作或轨迹变化      | 检测行为偏移      |
| Safety Violation            | 碰撞、超限或其他安全约束违反     | 体现物理安全价值    |
| Recovery Cost               | 恢复动作数、额外执行时间等      | 衡量失效恢复过程    |
| Query Efficiency            | 每次有效失效所需测试调用       | 比较攻击搜索效率    |
| Transferability             | 新任务、新模型和真实场景表现     | 检查方法是否过拟合   |

其中有两点很关键。

第一，轨迹不同不一定代表攻击成功。 机器人可以通过不同路径成功抓住杯子。所以轨迹偏移必须结合目标偏差、任务结果或安全约束解释。

第二，攻击有效率必须考虑原始成功情况。 如果正常场景已经失败，不能把攻击场景中的失败都算成攻击贡献。

例如，可以对相同任务、相同初始状态、相同随机种子进行配对实验，并单独统计从正常成功转为攻击失败的比例。

### 阶段5：G1实机验证

这是你们课题组的优势，但我建议把它放在仿真方法得到验证之后。

[README.md · nvidia/PhysicalAI-Robotics-GR00T-Teleop-G1 at main](https://images.openai.com/static-rsc-4/7rwddcbwHAzkbVpPc2lyMC2B314Z00rUDRcPh4Z6RD7kIodCcvWobZYIc8Pk2wzmhkWdfJzYyliARudtFZ5UVvAU9hrWsKLRSQ35LhimdTVQiW3ZJgZ7UsP0Vxw9Zw7TGPumSya90_zc2Crw2D7MFcg7-YM2NEtBT2MTyzZ4pQM?purpose=inline)

建议的G1实机验证场景

保持杯子位置、抓取目标和动作任务不变，改变实验桌面上的非目标物体、背景或受控照明条件。

记录π0.5视觉输入、动作输出、末端位姿、任务成功与安全停止情况。

先选择安全、静态、可重复的场景，之后再考虑动态视觉变化。

但要区分三个研究层次：

| 层次       | 要验证的问题              |
| -------- | ------------------- |
| 纯VLA操作   | 攻击是否改变π0.5控制的抓取行为   |
| G1移动操作系统 | 干扰是否影响导航、停稳与抓取之间的交接 |
| 完整具身系统   | 错误是否通过感知、规划和执行链路传播  |

第一篇论文我更建议聚焦纯VLA操作，G1作为真实场景验证。

如果直接同时研究导航、运动控制、策略切换和抓取，系统故障因素会太多，论文很难归因。

另外，你们现有的π0.5抓取策略与公开Benchmark中的π0.5检查点不一定共享机器人形态、动作空间、相机设置或数据分布，不能直接假定一个环境中的攻击可以无缝迁移到G1。必要时应先在对应策略的原生评测环境验证。

真机测试还需要设置工作空间边界、速度限制、急停和人工监督，并使用安全的非易碎道具，避免为了验证攻击效果造成碰撞或硬件损坏。

## 九、怎样判断实验结果够不够构成论文？

这部分建议你在真正开发算法之前就想清楚。

值得继续深入的结果

在相同任务、相同攻击预算和同样的物理约束下，你的方法比现有搜索基线稳定发现更多有效失效；这些失效具有可解释的行为差异，并能在新模型或物理场景中得到一定验证。

可能只够作为实验发现的结果

调整光照、干扰物或背景后，成功率下降，但是与随机扰动、LIBERO-Plus已有场景相比，没有明显新方法或新发现。

需要重新审查实验有效性的结果

攻击后目标被完全挡住、机器人无法到达目标、任务物体被移动到不可抓取位置，或者模型在正常环境下本来就不能完成任务。

一个较有竞争力的论文，理想情况下至少形成三方面贡献：

方法贡献： 提出有明确依据的攻击搜索或安全测试机制。

实验贡献： 在多个模型和任务上，与强基线进行公平比较，并报告攻击预算、约束和统计不确定性。

实证贡献： 揭示一种现有方法未充分刻画的VLA失效现象，最好能够通过实机复现关键案例。

不是每篇论文都必须三者齐全，但不能仅靠展示真实机器人失败的视频来替代方法创新和实验论证。

## 十、我给你的最终执行安排

按阶段推进的研究任务

研究里程碑

0/7

1\. 文献定位

精读LIBERO-Plus、ILA、VLA-Arena，整理已实现功能与潜在差异

2\. 可运行基线

LIBERO正常Rollout、环境扰动、轨迹日志和配对结果

3\. 攻击基线

随机/均匀场景采样，选择一种已有视觉攻击进行对照

4\. 初步新方法

实现任务合法性约束与行为反馈搜索，比较有效性和预算

5\. 跨模型验证

扩展到第二个可兼容VLA模型、任务集合或仿真平台

6\. 实机验证

在满足安全条件后，筛选案例到G1抓取任务中验证

7\. 论文形成

补齐消融、失败归因、可重复性与Related Work

&#x20;复制研究计划

## 十一、下一次和唐老师讨论时，应该带着什么结论？

我建议你把自己的选题理解总结成下面这段话：

我的研究方向初步定位

面向VLA模型在真实物理环境中的视觉脆弱性，研究在任务目标、任务可执行性保持不变的条件下，通过自然环境变化主动诱发模型的行为偏移和安全失效。

前期重点考虑场景参数化、合法性约束、闭环行为反馈和自动化攻击搜索；先在LIBERO类仿真平台建立实验基线，再根据方法结果选择G1实机抓取场景进行验证。

目前希望重点研究的不是普通视觉扰动，而是如何更高效、系统地找到合法环境变化诱发的不同类型的机器人失效。

与老师讨论时，最值得确认的实际上是两件事：第一，老师希望论文的创新更偏攻击优化还是安全测试与失效归因；第二，是否有现成的VLA仿真代码、模型检查点和实机评测接口可继承。 这会直接影响最合适的第一篇复现工作。

### 我的最终阅读与复现推荐

精读主线

LIBERO-Plus → ILA → ICCV 2025视觉攻击 → VLA-Arena → ICST 2026蜕变测试 → Tex3D

复现主线

LIBERO正常执行 → LIBERO-Plus环境扰动 → 一种视觉攻击基线 → 自己的任务保持型场景搜索 → G1验证

最重要的是，现在不要急于直接实现复杂的新攻击算法。先用已有模型和场景完成第一轮受控实验，找到一个稳定、可复现、现有方法尚未充分解决的现象。

这样选题会更扎实，既能利用唐老师在安全测试和物理环境攻击方面的积累，也能把你之前研究L侧自然指令攻击时形成的“任务语义保持、行为级评价”思想真正迁移过来。

对于你未来想争取的具身智能实习和算法岗位，这条路线也能沉淀出一套完整的技术经历：VLA模型部署、仿真环境开发、对抗评测、自动化测试、机器人动作分析和G1实机验证。

这比单纯阅读更多攻击论文，或者仅生成几个视觉对抗样本，更值得投入。