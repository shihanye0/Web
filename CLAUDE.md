# Claude Code Configuration for Obsidian Vault

## Obsidian CLI Usage Guidelines

### Core Principles
1. **优先使用 obsidian-cli skill**：操作 Obsidian 时，优先通过 obsidian-cli skill 调用命令
2. **静默模式**：所有命令默认加上 `silent` 参数，除非用户特别要求在前台打开
3. **标签搜索优先**：标签搜索优先使用 `obsidian tag` 命令，比全搜索更精确

### Command Patterns

#### 基本操作
```bash
# 读取笔记（静默模式）
obsidian read file="Note Name" silent

# 创建笔记（静默模式）
obsidian create name="New Note" content="# Title" silent

# 追加内容（静默模式）
obsidian append file="Note Name" content="New content" silent

# 搜索笔记
obsidian search query="search term" limit=10 silent

# 设置属性
obsidian property:set name="status" value="done" file="Note Name" silent
```

#### 标签操作（优先使用）
```bash
# 列出所有标签及计数
obsidian tags sort=count counts silent

# 搜索特定标签
obsidian tag="#project" silent

# 按标签过滤笔记
obsidian search query="tag:#important" silent
```

#### 日记操作
```bash
# 读取今日日记
obsidian daily:read silent

# 向今日日记追加内容
obsidian daily:append content="- [ ] New task" silent
```

#### 链接和反向链接
```bash
# 查看笔记的反向链接
obsidian backlinks file="Note Name" silent

# 查看笔记的所有链接
obsidian links file="Note Name" silent
```

#### 任务管理
```bash
# 查看每日任务
obsidian tasks daily todo silent

# 查看所有任务
obsidian tasks all silent
```

### Workflow Examples

#### 1. 创建研究笔记
```bash
# 创建笔记
obsidian create name="Research Topic" content="# Research Topic\n\n## Notes\n\n## References" silent

# 添加标签
obsidian property:set name="tags" value='["research", "project"]' file="Research Topic" silent

# 添加状态
obsidian property:set name="status" value="in-progress" file="Research Topic" silent
```

#### 2. 搜索和整理
```bash
# 按标签搜索
obsidian tag="#todo" silent

# 按关键词搜索
obsidian search query="machine learning" limit=20 silent

# 查看特定笔记的反向链接
obsidian backlinks file="ML Notes" silent
```

#### 3. 日记和任务管理
```bash
# 读取今日日记
obsidian daily:read silent

# 添加任务到日记
obsidian daily:append content="- [ ] Review research papers\n- [ ] Update notes" silent

# 查看待办任务
obsidian tasks daily todo silent
```

### Plugin Development

When working on Obsidian plugins or themes:

```bash
# 重新加载插件
obsidian plugin:reload id=my-plugin silent

# 检查错误
obsidian dev:errors silent

# 截图验证
obsidian dev:screenshot path=screenshot.png silent

# 检查控制台
obsidian dev:console level=error silent

# 执行 JavaScript
obsidian eval code="app.vault.getFiles().length" silent
```

### Best Practices

1. **文件定位**：
   - 使用 `file="Name"` 像 wikilink 一样解析（只需名称，无需路径或扩展名）
   - 使用 `path="folder/note.md"` 精确路径

2. **Vault 定位**：
   - 默认使用最近聚焦的 vault
   - 使用 `vault="Vault Name"` 指定特定 vault

3. **输出控制**：
   - 使用 `--copy` 将输出复制到剪贴板
   - 使用 `silent` 防止文件打开
   - 使用 `total` 获取列表命令的计数

4. **多行内容**：
   - 使用 `\n` 表示换行
   - 使用 `\t` 表示制表符

### Troubleshooting

如果命令不工作：
1. 确保 Obsidian 已打开
2. 检查 vault 是否正确加载
3. 验证文件名或路径是否正确
4. 使用 `obsidian help` 查看所有可用命令

### References

- Obsidian CLI 文档：https://help.obsidian.md/cli
- Agent Skills 规范：https://github.com/kepano/obsidian-skills

---

## 知识库增量处理规则

### 核心规则文件

**`cloud.md`** 是知识库的生长规则，定义了 Claude 处理新内容的完整流程。

### 处理触发

当 Boss 说以下命令时，启动增量处理：
- "处理 Inbox" — 扫描 00-Inbox，执行完整流程
- "把这条加入知识库" — 处理当前讨论的内容
- "更新索引" — 只重建 INDEX.md
- "整理概念 X" — 深入扩展某个概念笔记

### 处理流程（简化版）

```
1. 扫描 00-Inbox 中未处理的文件（无 processed: true）
2. 分类：论文→02-Papers / 概念→03-Knowledge / 代码→05-Code
3. 提取核心概念，与 INDEX.md 去重
4. 新概念 → 创建笔记（用 07-Templates/concept-note.md）
5. 已有概念 → 追加来源到已有笔记
6. 更新 INDEX.md
7. 标记原始文件 processed: true
```

### 关键约束

- **只处理增量** — 不重复扫描已处理文件
- **只关联已有** — 不凭空创造不存在的关联
- **来源可追溯** — 每条信息必须链接到原始文件
- **不删除** — 永远不删除已有笔记，只追加和更新

### 笔记状态

```
seed → growing → mature → evergreen
```

- seed：刚创建，内容单薄
- growing：3+ 条来源关联
- mature：5+ 条关联 + 内容完整
- evergreen：Boss 手动标记的核心概念

---

*Last updated: 2026-06-01*
