# design.md：设计系统给编码智能体

## 基本信息

- 仓库：https://github.com/google-labs-code/design.md
- npm 包：`@google/design.md`
- 当前验证版本：`0.3.0`
- 定位：用统一 `DESIGN.md` 格式描述品牌视觉、颜色、字体、组件和设计规则，让编码智能体稳定理解同一套设计系统。

## 本机状态

未全局安装，已验证可按需运行：

```bash
npx -y @google/design.md --help
```

## 适用场景

- 多次让 agent 生成页面，但视觉风格不一致。
- 项目需要稳定的颜色、字体、圆角、间距、组件 token。
- 需要把设计规则从自然语言 prompt 下沉成可 lint、可 diff、可导出的真源文件。

## 推荐用法

在具体前端项目根目录创建：

```text
DESIGN.md
```

常用命令：

```bash
npx -y @google/design.md lint DESIGN.md
npx -y @google/design.md diff DESIGN.md DESIGN-v2.md
npx -y @google/design.md export --format css-tailwind DESIGN.md
npx -y @google/design.md spec
```

## 接入建议

- P0：进入前端项目模板。
- `DESIGN.md` 应作为设计真源，不要把关键颜色/字体只写在 prompt 或一次性任务说明里。
- 修改 UI 规则后，应先更新 `DESIGN.md`，再让 agent 消费它。
