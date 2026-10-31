# moqian-project-scaffold · AI Agent Skill

> 一个可复用的 **Agent Skill**：基于陌阡 AI 工程治理模板，为新项目一键初始化完整工程骨架——克隆模板、清理示例、重置占位文档、建立独立 Git 历史。只需提供项目名。

- **Skill 名称：** `moqian-project-scaffold`
- **适用场景：** AI Agent、LLM 应用等新项目 0 → 1 的工程目录搭建
- **依赖模板：** [zhaoxuejie/moqian-ai-template](https://github.com/zhaoxuejie/moqian-ai-template)
- **运行环境：** Python 3、Git；跨平台（Windows / macOS / Linux）

---

## 它能做什么

| 步骤 | 自动处理 |
| ---- | ---- |
| 1 | `git clone --depth 1` 拉取最新工程模板 |
| 2 | 删除模板自带 `.git`，新项目独立 `git init -b main`（不带模板历史与标签） |
| 3 | 删除示例任务卡，清空任务索引表示例行 |
| 4 | 重置 `README.md` 为业务占位（标题自动填入项目名） |
| 5 | 重置 `CHANGELOG.md` 为干净的 `Unreleased` 基线 |
| 6 | 恢复 `scripts/release.sh` 可执行位，校验必要文件齐全并完成首次提交 |

## 目录结构

```
moqian-project-scaffold/
├── README.md                   # 本说明
├── SKILL.md                    # 技能元数据与执行规则（供 Agent 读取）
├── .gitignore / .gitattributes / .markdownlint.json
├── .github/workflows/ci.yml    # Markdown 与 Python 静态检查
├── scripts/
│   └── scaffold.py            # 确定性脚手架脚本
├── references/
│   └── after-scaffold.md       # 骨架就绪后的后续阶段指引
└── assets/
    └── publish-readme.md       # 本 README 的素材来源
```

## 安装方式

### 方式一：克隆到技能目录
将整个技能目录放入目标环境的技能目录（不同 Agent 宿主位置略有差异）：

```bash
# 通用 Agent Skills 目录示例
git clone https://github.com/zhaoxuejie/moqian-project-scaffold.git \
  /path/to/skills/moqian-project-scaffold
```

常见宿主目录：
- 豆包 / Doubao 工作区：`~/.doubao/agent_mode/workspace/.user_skills/`
- 通用规范：`.agents/skills/`、`.skills/`

### 方式二：手工复制
把 `moqian-project-scaffold/` 文件夹整体复制到上述技能目录，保持 `SKILL.md` 在技能根下即可。

安装后无需额外配置；Agent 会根据 `SKILL.md` 的 `description` 自动识别触发场景。

## 使用方法

### 自然语言触发（推荐）
直接对 Agent 说：

- 新建一个项目 `finance-agent`，用脚手架初始化骨架
- 在 `D:\projects` 目录下初始化 `daily-ai-insights` 项目

### 命令行直接调用脚本

```bash
python scripts/scaffold.py --name <项目名> [--parent <父目录>]
```

## 参数说明

| 参数 | 必填 | 说明 | 默认值 |
| ---- | ---- | ---- | ---- |
| `--name` | 是 | 项目名，小写 kebab-case（小写字母、数字、连字符） | — |
| `--parent` | 否 | 新项目所在父目录 | Windows `D:\projectTrae`，其他平台当前目录 |
| `--template-url` | 否 | 自定义模板仓库 Git 地址 | 陌阡官方模板 |
| `--branch` | 否 | 模板分支 | `main` |
| `--no-git` | 否 | 只拉取清理，不初始化 Git | 关闭 |
| `--keep-template-history` | 否 | 保留模板 Git 历史与标签 | 关闭（默认独立历史） |

### 示例

```bash
# 标准用法：初始化到默认父目录
python scripts/scaffold.py --name finance-agent

# 指定父目录
python scripts/scaffold.py --name daily-ai-insights --parent /home/me/projects

# 仅生成文件，不初始化 Git
python scripts/scaffold.py --name demo --no-git
```

## 退出码

| 退出码 | 含义 | 处理建议 |
| ---- | ---- | ---- |
| 0 | 成功 | — |
| 2 | 项目名非法 | 改为小写 kebab-case 后重试 |
| 3 | 目标目录已存在且非空 | 更换项目名或先清空目标目录 |
| 4 | 骨架缺少必要文件 | 检查模板仓库是否完整 |

## 前置条件
- 已安装 `git`，并能访问模板仓库
- 已安装 Python 3
- Git 已配置提交身份（`user.name` / `user.email`）；缺失时脚本会在新仓库设置本地兜底身份

## 生成的新项目包含什么

```
<project-name>/
├── README.md / AGENTS.md / CONTRIBUTING.md / CHANGELOG.md / LICENSE
├── .env.example / .gitignore / .gitattributes / .markdownlint.json
├── docs/
│   ├── prompt.md              # 新会话基座提示词
│   ├── stage-prompts.md       # 分阶段指令库
│   ├── prd.md / architecture.md / api-contract.md
│   ├── archive/
│   └── tasks/                 # 空任务索引看板
├── scripts/release.sh
├── tests/
└── .github/workflows/ci.yml
```

> 脚手架只负责准备骨架，不编写业务代码。生成后按 `docs/stage-prompts.md` 从 PRD 阶段依次推进。

## 工程规范
生成的项目遵循陌阡 AI 工程治理框架：先文档后代码、增量任务卡、ADR 追加式记录、MAJOR 版本快照归档。详见新项目内 `AGENTS.md`。

## License
MIT
