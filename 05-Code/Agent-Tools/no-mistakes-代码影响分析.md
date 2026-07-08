# no-mistakes：TS/JS 代码影响分析工具

## 基本信息

- 精确仓库：https://github.com/jonathanong/no-mistakes
- npm 包：`no-mistakes`
- 当前验证版本：`0.30.0`
- 定位：静态分析 TS/JS 项目的依赖、被依赖、符号、导入使用、测试影响等。

## 链接纠偏

原始记录里的 `BuilderIO/no-mistakes` 当前不可访问。按 npm 包和仓库搜索，真实可用项目为：

```text
jonathanong/no-mistakes
```

## 本机状态

未全局安装，已验证可按需运行：

```bash
npx -y no-mistakes --help
npx -y no-mistakes --version
```

验证版本：

```text
no-mistakes 0.30.0
```

## 主要命令

- `dependencies`
- `dependents`
- `symbols`
- `import-usages`
- `dead-exports`
- `call-sites`
- `resolve-check`
- `tests`
- `ci`
- `impacted-checks`
- `playwright`
- `react`
- `server`
- `infra`

## 使用建议

- P1：只在 TS/JS 项目中重点使用。
- 适合在修改前后分析影响面，而不是替代项目自己的 `test/lint/typecheck/build`。
- 可作为交付门禁的一部分，但不要把它描述成覆盖所有语言和所有质量问题的通用工具。
