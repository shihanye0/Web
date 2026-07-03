# Inbox 使用说明

> 这是知识库的入口。所有新内容先丢到这里，Claude 会根据 `cloud.md` 规则自动处理。

## 使用方法

### 1. 手动创建笔记
直接在本文件夹创建 `.md` 文件，粘贴你要保存的内容。

### 2. 浏览器剪藏
使用 Obsidian Web Clipper 或手动复制网页内容到此处。

### 3. 告诉 Claude 处理
```
"处理 Inbox"
"把这条加入知识库"
"整理一下 Inbox 里的内容"
```

## 处理流程

```
Inbox（新内容）
    ↓ Claude 读取
提取核心概念
    ↓ 去重检查
概念笔记 → 03-Knowledge/
论文笔记 → 02-Papers/
代码笔记 → 05-Code/
    ↓ 更新关联
INDEX.md 自动更新
    ↓ 标记完成
processed: true
```

## 注意事项

- 不要手动删除 Inbox 中的文件，让 Claude 标记 `processed: true` 后再清理
- 大段内容可以先粗略粘贴，Claude 会帮你提取核心
- 每次只处理新增内容，不会重复扫描已处理的文件
