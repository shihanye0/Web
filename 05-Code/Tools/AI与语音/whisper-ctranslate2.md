# whisper-ctranslate2

基于 faster-whisper（CTranslate2 内核）的本地语音转文字命令行工具。本机版本 **0.5.7**（`uv tool install whisper-ctranslate2`，2026-09-12）。

## 它解决什么

不联网、不花钱，把录音转成文字/字幕。CTranslate2 内核比原版 whisper 快数倍、省显存，本机 4G 显存 + CPU 都能跑得动。

## 如何使用

```powershell
# 基本转写（自动检测语言）
whisper-ctranslate2 会议录音.m4a

# 中文内容显式指定语言，模型选 small（本机甜点位）
whisper-ctranslate2 会议录音.m4a --model small --language zh

# 需要英译中时用 translate 任务
whisper-ctranslate2 lecture.mp3 --task translate
```

- 结果以字幕/文本文件形式生成在音频同目录；模型、输出格式等更多参数用 `--help` 查看
- 模型选择：`small` 够日常；重要会议用 `medium`；首次使用会下载对应模型
- 本机 4G 显存：small/medium 可跑 GPU；`--device cpu --compute_type int8` 则纯 CPU（慢但稳）

## 适用场景

- **组会录音 → 文字纪要**：录完扔给转写，10 分钟整理成 Obsidian 笔记
- 讲座/报告视频抽字幕
- 语音备忘录批量转文字归档

## 搭配

- 腾讯会议录音 → 转写 → Obsidian 会议笔记 → 关键待办进日记
- 转写稿里提到的文献 → 手动进 [[Zotero 插件清单]] 里的 Zotero 流程
- 全程本地处理，未公开课题组的讨论内容不出本机

## 参考

- 仓库：<https://github.com/absadiki/whisper-ctranslate2>
