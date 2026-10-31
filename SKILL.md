---
name: moqian-project-scaffold
description: "基于陌阡AI工程治理模板（GitHub 仓库 zhaoxuejie/moqian-ai-template）为新项目一键初始化工程骨架。当用户要求新建或初始化一个项目、拉取工程模板、生成项目目录骨架、从模板复制一套 README/PRD/架构/接口契约/任务卡/CI 结构、准备 AI 项目工程目录，或给出项目名和本地路径要求把骨架准备好并清理示例任务卡时使用。覆盖 AI Agent、LLM 应用等新项目 0 到 1 的工程目录搭建；不用于已有项目的业务代码开发。"
---

# 陌阡 AI 项目脚手架

## Overview
从远程模板仓库克隆最新骨架，自动清理模板示例、重置业务占位文档，并为新项目建立独立 Git 历史。用户只需提供项目名（可选父目录），无需手动复制、删示例、改占位。

## 前置条件
- 本机已安装 `git` 并可访问 `https://github.com/zhaoxuejie/moqian-ai-template`。
- 运行脚本使用本机 `python`。
- 模板自身的工程规则（先文档后代码、增量任务卡、MAJOR 归档等）见新项目内 `AGENTS.md` 与 `docs/prompt.md`，本技能只负责"把骨架准备好"，不负责后续业务开发。

## 工作流程

### 1. 收集参数
- **项目名（必填）**：小写英文 kebab-case，仅小写字母/数字/连字符，如 `finance-agent`。若用户给了中文名或含空格/大写，先转换为合法 kebab-case 并向用户确认。
- **父目录（可选）**：未指定时，Windows 默认 `D:\projectTrae`，其他平台默认当前工作目录。用户明确给路径时以用户为准。
- 目标目录已存在且非空时，**停止并提示用户**，禁止覆盖已有项目。

### 2. 运行脚手架脚本
脚本位于本技能目录 `scripts/scaffold.py`。在 PowerShell / 终端执行：

```bash
python <本技能目录>/scripts/scaffold.py --name <项目名> --parent <父目录>
```

常用参数：
- `--name`：新项目名（必填）
- `--parent`：目标父目录（可选）
- `--template-url`：替换模板仓库地址（一般不用改）
- `--branch`：模板分支，默认 `main`
- `--no-git`：只拉取清理，不初始化 Git
- `--keep-template-history`：保留模板 Git 历史（默认删除并独立 `git init`）

### 3. 脚本自动完成的处理
1. `git clone --depth 1` 模板到 `<父目录>/<项目名>`
2. 删除模板自带 `.git`，新项目独立 `git init -b main` 并完成首次提交
3. 删除示例任务卡 `docs/tasks/task-00x-xxx.md`，清空 `docs/tasks/readme.md` 索引表示例行（保留表头与规则）
4. 重置 `README.md` 为业务占位骨架（标题填入项目名，业务描述留占位）
5. 重置 `CHANGELOG.md` 为干净的 `[Unreleased]` 基线，不带模板自身版本历史
6. 校验必要文件齐全，打印最终目录树

### 4. 完成后引导（不要继续写业务代码）
骨架就绪后，**不要**直接开始写 PRD 正文或业务代码。按 `references/after-scaffold.md` 告知用户下一步：
- 新开 AI 会话，先粘贴新项目 `docs/prompt.md` 基座规则
- 再按 `docs/stage-prompts.md` 的「阶段1：编写 PRD」推进

## 错误处理
- **克隆失败**（网络/仓库不可达/认证问题）：如实报告错误，提示检查网络或仓库访问权限；不要改用手工拼目录绕过。
- **项目名非法**：脚本以退出码 2 拒绝；按提示转换为 kebab-case 后重试。
- **目标目录非空**：退出码 3；请用户更换项目名或先处理已有目录。
- **缺少必要文件**：退出码 4；说明骨架不完整，需检查模板仓库状态。
- Git 身份缺失时，脚本会在本仓库设置本地兜底身份；若提交仍失败，提示用户配置 `git config user.name` / `user.email`。

## 参考
- `references/after-scaffold.md`：骨架就绪后的目录说明、清理项清单与后续阶段顺序。
- `assets/publish-readme.md`：对外发布到 GitHub / 技能市场时使用的仓库 README 素材；发布时把它复制为仓库根 `README.md`，并把 `<owner>` 替换为实际仓库所有者。技能内部不另建 README.md。
