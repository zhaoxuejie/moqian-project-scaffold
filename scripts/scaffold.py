#!/usr/bin/env python3
"""
陌阡 AI 工程模板脚手架。

从 GitHub 模板仓库克隆一个新项目骨架，自动清理模板示例内容，重置业务占位文档，
并为新项目初始化独立的 Git 仓库（不带模板自身的提交历史与标签）。

用法:
    python scaffold.py --name <project-name> [--parent <dir>] [--template-url <url>]
                        [--branch main] [--no-git] [--keep-template-history]

示例:
    python scaffold.py --name finance-agent --parent D:\\projectTrae
"""

import argparse
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

DEFAULT_TEMPLATE_URL = "https://github.com/zhaoxuejie/moqian-ai-template.git"
DEFAULT_BRANCH = "main"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# 新项目初始 CHANGELOG（干净基线，不含模板自身的版本历史）
CHANGELOG_RESET = """# Changelog
所有版本变更记录遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/)
版本语义化：MAJOR.MINOR.PATCH
- MAJOR：不兼容破坏性变更
- MINOR：兼容新增功能
- PATCH：兼容bug修复、微调

## [Unreleased]
### Added

### Changed

### Fixed

### Removed
"""


def readme_template(project_name: str) -> str:
    """生成新项目业务 README 占位骨架；业务描述留待 PRD 阶段填写。"""
    return f"""# {project_name}
{{一句话项目简介}}

## 版本信息
当前版本：v0.1.0

## 概述
{{详细描述项目定位、能力、适用场景、核心目标}}

## 快速启动
> 前置依赖：{{运行时 / 版本，例如 Python 3.11、Node 20}}

1. 安装依赖
```bash
# 示例
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 填入密钥、配置
```

3. 启动服务
```bash
# 示例
```

## 目录概览
```
{project_name}/
├── docs/                # PRD、架构、接口契约、任务卡、归档快照
├── scripts/             # 发布、迁移等辅助脚本
├── tests/               # 单元测试、契约测试、评估集
└── .github/workflows/   # CI 静态检查
```

## 规范
- 贡献规范：见 `CONTRIBUTING.md`
- AI 开发约束：见 `AGENTS.md`
- 版本变更记录：见 `CHANGELOG.md`
"""


def run(cmd, cwd=None, check=True):
    """执行命令并返回 CompletedProcess；失败时打印 stderr 并按需退出。"""
    proc = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if check and proc.returncode != 0:
        print(f"[ERROR] 命令执行失败: {' '.join(cmd)}", file=sys.stderr)
        if proc.stdout.strip():
            print(proc.stdout.strip(), file=sys.stderr)
        if proc.stderr.strip():
            print(proc.stderr.strip(), file=sys.stderr)
        sys.exit(proc.returncode)
    return proc


def force_rmtree(path: Path) -> None:
    """递归删除目录；Windows 上 Git pack 对象为只读，先清除只读位再删。"""

    def onexc(func, p, _exc):
        os.chmod(p, stat.S_IWRITE)
        func(p)

    shutil.rmtree(path, onexc=onexc)


def validate_name(name: str) -> None:
    if not NAME_RE.match(name):
        print(
            "[ERROR] 项目名必须为小写英文 kebab-case：仅小写字母、数字、连字符，"
            "且不以连字符开头/结尾，例如 finance-agent。",
            file=sys.stderr,
        )
        sys.exit(2)
    if len(name) > 40:
        print("[ERROR] 项目名长度不能超过 40 字符。", file=sys.stderr)
        sys.exit(2)


def default_parent() -> Path:
    """Windows 下优先使用 D:\\projectTrae，否则使用当前工作目录。"""
    win_default = Path(r"D:\projectTrae")
    if sys.platform.startswith("win") and win_default.exists():
        return win_default
    return Path.cwd()


def clone_template(target: Path, template_url: str, branch: str) -> None:
    if target.exists():
        if any(target.iterdir()):
            print(f"[ERROR] 目标目录已存在且非空，拒绝覆盖: {target}", file=sys.stderr)
            sys.exit(3)
        target.rmdir()
    run(["git", "clone", "--depth", "1", "--branch", branch, template_url, str(target)])


def reset_task_index(tasks_dir: Path) -> None:
    """清空任务索引表中的示例任务行，保留表头、规则与说明。"""
    index = tasks_dir / "readme.md"
    if not index.exists():
        return
    lines = index.read_text(encoding="utf-8").splitlines(keepends=True)
    kept = [ln for ln in lines if not ln.lstrip().startswith("| TASK-")]
    index.write_text("".join(kept), encoding="utf-8", newline="\n")

    # 删除示例任务卡模板
    sample = tasks_dir / "task-00x-xxx.md"
    if sample.exists():
        sample.unlink()


def reset_business_docs(target: Path, project_name: str) -> None:
    (target / "CHANGELOG.md").write_text(CHANGELOG_RESET, encoding="utf-8", newline="\n")
    (target / "README.md").write_text(
        readme_template(project_name), encoding="utf-8", newline="\n"
    )
    reset_task_index(target / "docs" / "tasks")


def init_git(target: Path, project_name: str, keep_history: bool) -> None:
    if not keep_history:
        git_dir = target / ".git"
        if git_dir.exists():
            force_rmtree(git_dir)
        run(["git", "init", "-b", "main"], cwd=target)

    run(["git", "add", "."], cwd=target)
    # 重新 init 会丢失模板的可执行位，恢复 release.sh 的 +x 权限
    release_sh = target / "scripts" / "release.sh"
    if release_sh.exists():
        run(["git", "update-index", "--chmod=+x", "scripts/release.sh"], cwd=target)
    # 若全局未配置身份，在本仓库设置本地兜底身份，避免首次提交失败
    name = run(["git", "config", "--global", "user.name"], check=False).stdout.strip()
    email = run(["git", "config", "--global", "user.email"], check=False).stdout.strip()
    if not name:
        run(["git", "config", "user.name", "moqian"], cwd=target)
    if not email:
        run(["git", "config", "user.email", "moqian@example.com"], cwd=target)

    run(
        ["git", "commit", "-m", f"chore: 初始化 {project_name} 陌阡AI工程骨架"],
        cwd=target,
    )


def print_tree(target: Path) -> None:
    print("\n===== 新项目骨架 =====")
    for path in sorted(target.rglob("*")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(target)
        prefix = "├── " if path.is_dir() else "├── "
        print(f"{prefix}{rel}{'/' if path.is_dir() else ''}")


def main() -> None:
    parser = argparse.ArgumentParser(description="从陌阡AI工程模板初始化新项目骨架")
    parser.add_argument("--name", required=True, help="新项目名称，小写 kebab-case")
    parser.add_argument("--parent", default=None, help="新项目所在父目录，默认 D:\\projectTrae（Windows）或当前目录")
    parser.add_argument("--template-url", default=DEFAULT_TEMPLATE_URL, help="模板仓库 Git 地址")
    parser.add_argument("--branch", default=DEFAULT_BRANCH, help="模板仓库分支，默认 main")
    parser.add_argument("--no-git", action="store_true", help="只拉取并清理，不初始化 Git 仓库")
    parser.add_argument(
        "--keep-template-history",
        action="store_true",
        help="保留模板自带的 Git 历史与标签（默认删除并独立 init）",
    )
    args = parser.parse_args()

    validate_name(args.name)
    parent = Path(args.parent).resolve() if args.parent else default_parent()
    parent.mkdir(parents=True, exist_ok=True)
    target = parent / args.name

    print(f"[1/4] 克隆模板: {args.template_url} (branch: {args.branch})")
    clone_template(target, args.template_url, args.branch)

    print("[2/4] 清理模板示例并重置业务占位文档")
    reset_business_docs(target, args.name)

    if not args.no_git:
        print("[3/4] 初始化独立 Git 仓库并提交")
        init_git(target, args.name, args.keep_template_history)
    else:
        print("[3/4] 跳过 Git 初始化（--no-git）")

    print("[4/4] 校验骨架")
    required = [
        "README.md",
        "AGENTS.md",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        ".env.example",
        "docs/readme.md",
        "docs/prompt.md",
        "docs/stage-prompts.md",
        "docs/prd.md",
        "docs/architecture.md",
        "docs/api-contract.md",
        "docs/tasks/readme.md",
        "scripts/release.sh",
        ".github/workflows/ci.yml",
    ]
    missing = [rel for rel in required if not (target / rel).exists()]
    if missing:
        print(f"[ERROR] 缺少必要文件: {missing}", file=sys.stderr)
        sys.exit(4)

    print_tree(target)
    print(f"\n✅ 新项目已就绪: {target}")
    print("下一步：新开 AI 会话，先粘贴 docs/prompt.md，再按 docs/stage-prompts.md 的「阶段1 PRD」推进。")


if __name__ == "__main__":
    main()
