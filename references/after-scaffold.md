# 骨架就绪后的后续指引

## 目录结构（新项目生成后）
```
<project-name>/
├── README.md                     # 业务占位，标题已填项目名，简介待 PRD 阶段补
├── AGENTS.md                     # AI 开发运行约束（框架规则，一般不改）
├── CONTRIBUTING.md               # 分支 / 提交 / PR / 命名规范
├── CHANGELOG.md                  # 干净 Unreleased 基线
├── LICENSE                       # 沿用模板版权，开源前按需改作者
├── .env.example                  # 环境变量样例
├── .gitignore / .gitattributes   # 忽略规则、LF 换行锁定
├── docs/
│   ├── readme.md                 # docs 导览与版本规则
│   ├── prompt.md                 # 基座启动提示词（新会话首段粘贴）
│   ├── stage-prompts.md          # 分阶段指令库
│   ├── prd.md                    # 待填写需求文档
│   ├── architecture.md           # 待填写架构 + ADR
│   ├── api-contract.md           # 待填写接口契约
│   ├── archive/.gitkeep          # MAJOR 版本归档目录（初始为空）
│   └── tasks/
│       ├── readme.md             # 空索引看板（示例行已清空）
│       └── （暂无任务卡）
├── scripts/release.sh            # 版本发布脚本
├── tests/.gitkeep                # 测试 / 评估集目录（初始为空）
└── .github/workflows/ci.yml      # markdownlint + shellcheck 检查
```

## 本次脚手架已自动清理的内容
- 删除示例任务卡 `docs/tasks/task-00x-xxx.md`
- 清空任务索引表中的 `TASK-001` 示例行
- `README.md` 替换为业务占位骨架
- `CHANGELOG.md` 重置为干净基线
- 删除模板 `.git`，新项目独立 Git 历史，不含模板标签

## 仍需在后续阶段填写的占位符
- `README.md`：一句话简介、概述、前置依赖、启动命令
- `docs/prd.md`、`architecture.md`、`api-contract.md` 内的 `{{项目名称}}` 等占位
- `LICENSE`：开源前确认版权年份与作者

## 后续阶段顺序（严格遵守，禁止跳步）
1. **新开会话**：先粘贴 `docs/prompt.md` 全文（基座规则）。
2. **阶段1 PRD**：复制 `docs/stage-prompts.md` 中「阶段1：编写 PRD」指令，附上项目需求，产出 `docs/prd.md`，人工审阅通过。
3. **阶段2 架构**：PRD 通过后，用「阶段2」指令产出 `docs/architecture.md`（含 ADR）。
4. **阶段3 接口契约**：架构通过后，用「阶段3」指令产出 `docs/api-contract.md`。
5. **阶段4 拆任务卡**：文档齐备后，用「阶段4」指令增量拆第一批任务卡（3～5 张以内），人工确认入库。
6. **阶段5 开发**：仅开发前置依赖全部 done 的任务，逐任务验收评测后标记 done。

## 注意
- 骨架生成后不要在当前会话直接补 PRD 正文；按框架要求新开会话并先喂基座 `prompt.md`。
- `docs/archive/`、`tests/` 初始为空属正常，由 `.gitkeep` 保留目录。
