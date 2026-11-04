# moqian-project-scaffold · AI Agent Skill

> 一个面向 **AI 编程**场景的 Agent Skill：基于陌阡工程治理模板一键初始化新项目骨架。模板把"需求先写成文档、增量拆任务、决策留痕、上下文存本地"固化为固定流程，帮你在 AI 协作开发中**锁定需求、抑制需求漂移、避免 AI 自由发挥跑偏**；不熟悉 AI 编程协作方式的人，也能照着阶段指令把项目从 0 规范推进到 1。你只需提供项目名，克隆模板、清理示例、重置占位文档、独立 Git 历史全部自动完成。

- **Skill 名称：** `moqian-project-scaffold`
- **适用场景：** 用 AI / AI Agent 辅助从零启动新项目；尤其适合担心需求跑偏，或不熟悉 AI 编程协作规范的开发者
- **依赖模板：** [zhaoxuejie/moqian-ai-template](https://github.com/zhaoxuejie/moqian-ai-template)
- **运行环境：** Python 3.11+、Git；跨平台（Windows / macOS / Linux）

---

## 安装后会得到什么

运行技能后，新项目会得到一套完整的 AI 工程治理骨架：

```
<project-name>/
├── README.md / AGENTS.md / CONTRIBUTING.md / CHANGELOG.md / LICENSE
├── .env.example / .gitignore / .gitattributes / .markdownlint.json
├── docs/
│   ├── prompt.md          # 新会话基座提示词，粘贴即可恢复完整规范上下文
│   ├── stage-prompts.md   # 分阶段指令库（PRD / 架构 / 接口 / 拆任务 / 开发 / 发布）
│   ├── prd.md             # 产品需求文档模板
│   ├── architecture.md    # 架构方案 + ADR 决策记录模板
│   ├── api-contract.md    # 接口契约模板
│   ├── tasks/             # 增量任务卡看板（一任务一文件）
│   └── archive/           # MAJOR 版本快照归档
├── scripts/release.sh     # 版本发布脚本
├── tests/                 # 测试与评测集目录
└── .github/workflows/ci.yml
```

> 脚手架只准备骨架、不编写业务代码；生成后按 `docs/stage-prompts.md` 从 PRD 阶段依次推进。

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

### 方式一：一句话让当前 Agent 自动安装（推荐，跨工具）
在你正在使用的 Agent 工具对话框里直接粘贴下面这段指令，Agent 会自己识别工具类型、定位技能目录、克隆仓库并校验安装结果，无需手动进入文件夹操作：

```text
请帮我安装 GitHub 技能仓库 https://github.com/zhaoxuejie/moqian-project-scaffold ：
1. 识别当前 Agent 工具，定位它对应的全局技能目录（见下方对照表）；
2. 将整个仓库克隆为 <技能目录>/moqian-project-scaffold/；
3. 校验 moqian-project-scaffold/SKILL.md 与 scripts/scaffold.py 都存在；
4. 告诉我重启会话后如何触发该技能。
```

各主流 Agent 工具的技能目录约定：

| Agent 工具 | 全局（用户级）目录 | 项目级目录 |
| ---- | ---- | ---- |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.codex/skills/`（亦识别 `.agents/skills/`） | `.codex/skills/` |
| DeepSeek Harness / Deep Code | `~/.agents/skills/` | `./.deepcode/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| 通用 Agent Skills 标准 | `~/.agents/skills/` | `./.agents/skills/` |
| 豆包 / Doubao 工作区 | `~/.doubao/agent_mode/workspace/.user_skills/` | — |

> 跨工具最通用的落点是 `~/.agents/skills/moqian-project-scaffold/`；不确定当前工具目录时，让 Agent 先探测本机已有的 skills 目录再安装。
> 新安装的技能需要**重启会话**（Claude Code 可用 `/reload-skills`）后才会被扫描识别。

### 方式二：skills CLI 一键安装（需 Node.js）
在兼容 Agent Skills 规范、且提供 `skills` CLI 的环境中，可直接命令行安装到指定工具：

```bash
# 安装到 Codex 全局技能目录
npx skills add zhaoxuejie/moqian-project-scaffold --skill moqian-project-scaffold --agent codex --global

# 安装到 Claude Code 全局技能目录
npx skills add zhaoxuejie/moqian-project-scaffold --skill moqian-project-scaffold --agent claude-code --global
```

> 说明：本仓库 `SKILL.md` 位于仓库根目录；若所用 CLI 要求技能放在 `skills/<name>/` 子目录结构中，请改用方式一或方式三。

### 方式三：手动克隆 / 复制（兜底）
将整个技能目录放入上表对应工具的技能目录：

```bash
git clone https://github.com/zhaoxuejie/moqian-project-scaffold.git \
  <技能目录>/moqian-project-scaffold
```

也可以下载 ZIP 解压后，把 `moqian-project-scaffold/` 文件夹整体复制到技能目录，保持 `SKILL.md` 在技能根下即可。

安装后无需额外配置；Agent 会根据 `SKILL.md` 的 `description` 自动识别触发场景。安装校验：目录内同时存在 `SKILL.md`、`scripts/scaffold.py`、`references/after-scaffold.md`。

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
| `--parent` | 否 | 新项目所在父目录 | 当前工作目录 |
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
- 已安装 Python 3.11 及以上（脚本兼容 3.11 / 3.12 / 3.13）
- Git 已配置提交身份（`user.name` / `user.email`）；缺失时脚本会在新仓库设置本地兜底身份

## 工程规范
生成的项目遵循陌阡 AI 工程治理框架：先文档后代码、增量任务卡、ADR 追加式记录、MAJOR 版本快照归档。详见新项目内 `AGENTS.md`。

## License
MIT
