# blog（藏经阁）

> 个人博客 · docsify 站点 · https://xhqing.github.io/blog

## 这是什么

用户的个人博客「藏经阁」。docsify 站点，文章在 `docs/post/<分类>/` 下；线上由 GitHub Pages 从 `main` 分支的 `docs/` 目录直接发布（legacy 构建，没有前端打包步骤），因此**推送即上线**。

## 归谁负责

**social-agent（Gatsby，社媒运营官）**。2026-11-11 由 Kit（assistant-agent）移交到 Gatsby 名下，归属记在全局 `~/.pi/agent/docs/agents-registry.md` 的子项目映射表里。

## 内容怎么进来

1. **手写**：直接改 `docs/post/`。首行 `创建于 YYYY-MM-DD<br>`，标题用二级 `##`。
2. **自动同步**：`social-agent` 的 `docs/articles/` → 本仓库 `docs/post/`，由 `.github/workflows/sync-articles.yml` 每 10 分钟拉一次（也支持手动 `workflow_dispatch`）。同步脚本是 `scripts/sync_articles.py`，只碰带 `<!-- source: … -->` 标记的文件，不碰手写文章。

**发布不区分「写完没写完」**：源仓库里是什么状态就发什么状态，这是用户 2026-11-11 明确要求的。

## Worker 边界

- 以本仓库或其 worktree 为工作目录的会话是 **Worker**：只干本仓库的具体活（改脚本、修文章、跑校验、提交），干完向 social-agent 的 Leader 汇报。
- 不碰 local `main`、不建 / 不删 worktree。
- **不手改带同步标记的文章**——那些是同步脚本的产出，改了下次同步会被覆盖。要改就改 `social-agent` 里的源文章。

## 规则索引

- 本仓库硬约束：`.pi/APPEND_SYSTEM.md`
- 变更记录：`CHANGELOG.md`（版本号以 `VERSION` 为唯一权威）
- 仓库自检：`python3 scripts/validate.py`（CI 跑的就是这个）
- 全局规则：`~/.pi/agent/AGENTS.md`（任何目录都会加载）