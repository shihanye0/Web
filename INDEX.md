# INDEX.md — 全局概念索引

> 本文件由 Claude 自动维护，记录知识库中所有核心概念及其关联。
> 每次增量处理后自动更新。**不要手动编辑。**

---

## 统计

- 概念总数：3
- 最近更新：2026-06-01

---

## AI / 机器学习

| 概念 | 状态 | 关联数 | 路径 |
|------|------|--------|------|
| [[RAG]] | growing | 2 | 03-Knowledge/RAG.md |
| [[向量数据库]] | seed | 2 | 03-Knowledge/向量数据库.md |
| [[Transformer]] | seed | 3 | 02-Papers/Transformer_-_Attention_Is_All_You_Need.md |

## 目标检测

| 概念 | 状态 | 关联数 | 路径 |
|------|------|--------|------|
| [[DETR]] | seed | 3 | 02-Papers/DETR_-_End-to-End_Object_Detection_with_Transformers.md |
| [[Deformable DETR]] | seed | 3 | 02-Papers/Deformable_DETR.md |

## 工具 / 框架

| 概念 | 状态 | 关联数 | 路径 |
|------|------|--------|------|
| [[Obsidian]] | seed | 1 | 03-Knowledge/Obsidian/ |

---

## 关系图谱（简化版）

```
RAG ─── 向量数据库
 │
 ├── Embedding模型
 │
 └── 检索策略

Transformer ─── DETR ─── Deformable DETR
     │
     └── Attention机制
```

---

## 待扩展

以下概念在笔记中被提及但尚未创建独立笔记：
- Embedding模型
- 语义检索
- Chroma / Pinecone / Weaviate
- Attention机制

---

*本索引由 Claude 根据 cloud.md 规则自动维护*
