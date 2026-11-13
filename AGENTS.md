# blog（藏经阁）

> 个人博客 · docsify 站点 · https://xhqing.github.io/blog

## 这是什么

用户的个人博客「藏经阁」。docsify 站点，文章在 `docs/post/<分类>/` 下；线上由 GitHub Pages 从 `main` 分支的 `docs/` 目录直接发布（legacy 构建，没有前端打包步骤），因此**推送即上线**。

## 归谁负责

**social-agent（Gatsby，社媒运营官）**。2026-11-11 由 Kit（assistant-agent）移交到 Gatsby 名下，归属记在全局 `~/.pi/agent/docs/agents-registry.md` 的子项目映射表里。

## 内容怎么进来

1. **手写**：直接改 `docs/post/`。首行 `创建于 YYYY-MM-DD<br>`，标题用二级 `##`。
2. **同步**：`social-agent` 的 `docs/articles/` → 本仓库 `docs/post/`，脚本 `scripts/sync_articles.py`，只碰带 `<!-- source: … -->` 标记的文件，不碰手写文章。

**发布红线（2026-11-13 用户立）**：没有用户当轮明确同意，不能往博客发布任何文章；未完成的文章不发。`.github/workflows/sync-articles.yml` 已去掉定时触发，只保留需显式确认的 `workflow_dispatch`；触发前必须取得用户同意。源仓库 `docs/articles/` 里的文章只是稿件，落盘不等于发布。

2026-11-11 的旧口径「发布不区分写完没写完」已作废，当日同步过来的 6 篇文章与配图已于 2026-11-13 全部撤下。

## Worker 边界

- 以本仓库或其 worktree 为工作目录的会话是 **Worker**：只干本仓库的具体活（改脚本、修文章、跑校验、提交），干完向 social-agent 的 Leader 汇报。
- 不碰 local `main`、不建 / 不删 worktree。
- **不手改带同步标记的文章**——那些是同步脚本的产出，改了下次同步会被覆盖。要改就改 `social-agent` 里的源文章。

## 规则索引

- 本仓库硬约束：`.pi/APPEND_SYSTEM.md`
- 变更记录：`CHANGELOG.md`（版本号以 `VERSION` 为唯一权威）
- 仓库自检：`python3 scripts/validate.py`（CI 跑的就是这个）
- 全局规则：`~/.pi/agent/AGENTS.md`（任何目录都会加载）