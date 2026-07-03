---
title: "RAG (检索增强生成)"
date: 2026-05-13
tags: [concept, RAG, AI]
---

# RAG (检索增强生成)

## 定义

RAG (Retrieval-Augmented Generation) 是一种将信息检索与大语言模型生成相结合的技术框架。

## 核心流程

1. **检索** — 根据用户查询从知识库中检索相关文档片段
2. **增强** — 将检索到的上下文注入到 prompt 中
3. **生成** — LLM 基于增强后的 prompt 生成回答

## 关键组件

- 向量数据库（存储文档嵌入）
- 嵌入模型（文本转向量）
- 检索策略（相似度搜索、混合检索）
- 生成模型（LLM）

## 与我的研究关联

> 我的毕业论文题目：《基于RAG的学科问答导学智能体设计与实现》

## 相关笔记

- [[向量数据库]]
- [[Embedding模型]]
- [[语义检索]]

## 参考资料

- Lewis et al. (2020) "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
