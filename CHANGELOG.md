# CHANGELOG

本文件记录本项目（blog，个人博客仓库）每次文件增删改的变更，写清「为什么改」和「改了什么」。版本号以项目根 `VERSION` 文件为唯一权威。

## [1.1.0] - 2026-11-11

### 新增（自动发布管道：social-agent 的文章自动同步进博客）

- **为什么改**：用户 2026-11-11 把博客移交到 social-agent（Gatsby）名下作为子项目，同时提两条要求——① social-agent 的 `docs/articles/` 里**所有**文章都发到博客，**不看写完没写完**；② 每次 PR 更新文章内容就自动发布。此前本仓库的文章只能手写到 `docs/post/`，与写作源头（social-agent 的公众号稿）完全脱节。
- **改了什么**：
  - 新增 `scripts/sync_articles.py`：拉 social-agent 的文章 → 转成博客体例（一级标题改二级、补 `创建于` / `关键词` 首行、相对图片拷进 `img/<源文件名>/` 并改写链接）→ 跑 `deploy.py` → 有变化时提交到 `sync/articles` 分支并开 PR，CI 过了自动合并（main 上有必过的 `validate` 检查，直推会被挡）。带 `<!-- source: … -->` 标记认领自己写的文章：源文章改名或删除时，博客上对应那篇跟着另存或删除；**没有标记的手写文章永远不会被碰**。支持 `--source`（本地副本调试）与 `--dry-run`（只看计划）。
  - 新增 `.github/workflows/sync-articles.yml`：每 10 分钟拉一次 + 手动 `workflow_dispatch`。用定时拉取而不是跨仓库推送，是因为跨仓库触发需要额外 token，而定时拉取零配置、不会因为对方仓库权限变动而失效；合并后最迟十分钟上线（同步 PR 自动合并，不需要人工点）。
  - 新增 `.github/workflows/validate.yml` + `scripts/validate.py`：CI 自检——Python 语法能过、每篇首行是「创建于 YYYY-MM-DD」、没有一级标题、每篇都进了侧边栏、侧边栏链接都指向真实文件。
  - **重写 `deploy.py`**：删掉旧版 `refference_modify()` 的目录拷贝逻辑——它先 `shutil.rmtree("./docs/post")` 再 `cp -r ./post ./docs/`，而根目录 `post/` 早已不存在，**一次运行就清空全站文章**；改为原地修复，不再有拷贝步骤。侧边栏与首页改为按 `order` 标记 + 文件名排序（结果可复现），新增 `--check` 只检不写。
  - 新增 `AGENTS.md` 与 `.pi/APPEND_SYSTEM.md`（2026-11-08 子项目新规：本仓库实体文件，不挂软链接）、`CONTRIBUTING.md` / `CONTRIBUTING_cn.md`（2026-11-09 团队标准，`{{LICENSE_NAME}}` 已替换为 MIT License）。
  - `README.md` / `README_cn.md` 双语同步：补「文章从哪来」与真实可用的命令（原文档里的 `new_post.py` / `preview.py` 在仓库里并不存在），版本徽章改为 1.1.0。`LICENSE.md` 与 README 版权行按 2026-11-08 新规改为 `xhqing and contributors`，`.commit-cache.md` 的署名口径同步。
- **首次同步结果**：5 篇（复利系列）进 `docs/post/复利与交易/`，6 张配图进 `img/<源文件名>/`，侧边栏按系列阅读顺序 1–5 排列。
- **已知边界**：定时拉取意味着合并后最迟十分钟才上线；要立即发布可以手动触发 workflow。未合并的 PR 分支内容不会发——发布的是 `main` 上的状态。

## [Unreleased]

### 变更（commit skill 标配补全：双语 README + LOGO + 徽章 + LICENSE.md + 检测缓存）

- **为什么改**：`/commit` 流程第 9 步标配检测发现本仓库缺 README 中文版、LOGO、徽章、`LICENSE.md` 与 commit 检测缓存（2026-09-12 接管时未补齐），按 commit skill 规则自动补全。
- **改了什么**：① `README.md` 重排——顶部加 LOGO + License / Version / Type 三枚徽章 + 跳「简体中文」链接，底部加「License & Attribution」段；② 新建 `README_cn.md`（中文版，与英文版互链）；③ 新建 `assets/logo.svg`（640×200 圆角渐变，📝 + blog + Personal Blog · docsify，文字边界硬校验通过）；④ 新建 `LICENSE.md`（MIT，版权人归一为 All Contributors）、删除冗余 `LICENSE`；⑤ 新建 `.commit-cache.md`（commit 检测缓存）；⑥ GitHub About 补中英双语 description + topics（blog / docsify）。

### 变更（按 2026-10-12 新规清理随附的智能体专属文件 .claude/CLAUDE.md）

- **为什么改**：用户 2026-10-12 修订团队规则——智能体专属文件（`CLAUDE.md` / `AGENTS.md` / `.claude/` / 项目级 `.pi/`）只有 Agent 项目允许拥有，非 Agent 项目（含本仓库这类子项目）一律不得存在；后台开启 pi 会话只能以 Agent 项目根目录为工作目录（细则见全局 `~/.claude/docs/agents-registry.md`「智能体专属文件归属与子项目映射」节）。本仓库此前按旧「超集」规则随附了 Kit 的 CLAUDE.md 全文，需按新规清理。
- **改了什么**：删除 `.claude/` 目录（仅含 `CLAUDE.md`——内容＝「blog 子项目」指代说明 + Kit CLAUDE.md 全文随附，删除无内容损失）。

### 变更（CLAUDE.md 删去「由 Claude Code 自动加载」说明句）

- **为什么改**：用户 2026-09-12 要求 CLAUDE.md 不再强调本文由 Claude Code 加载，团队全部项目的 CLAUDE.md 统一清理此类语句。
- **改了什么**（2026-09-12）：`.claude/CLAUDE.md` 开头角色定位行删去句尾「本文件由 Claude Code 在每次会话开头自动加载。」，角色描述本身保留。

## [1.0.0] - 2026-09-12

### 新增（项目接管：交由 Kit 负责，落地超集 + 补齐标配）

- **为什么改**：本仓库 2026-09-12 起交由 Kit（ExecutiveAssistantAgent，总经理助理）负责。接管时按团队项目标配规则补齐缺失文件；并按「Agent 项目与子项目的 `.claude/` 超集关系」规则把 Kit 的 CLAUDE.md 内容落入本仓库，使本仓库会话也运行同一套 Kit 规则。本条目同时作为 VERSION 建档的初始版本 1.0.0（仓库自 2023 年起在线运行、无历史版本号，接管时刻即 1.0.0）。
- **改了什么**：① 本地克隆到 `/Users/xhq/Developer/blog`（原无本地副本）；② 新建 `.claude/CLAUDE.md`（Kit CLAUDE.md 全文 + 子项目指代说明，方式与既有子项目 xhqing / CyberRipple 一致，进 git 跟踪）；③ 新建 `VERSION`（1.0.0）、`CHANGELOG.md`（本文件）；④ `.gitignore` 追加团队标准忽略项（`.env.*`、`settings.local.json`、`tmp/`、`artifacts/`、`node_modules/`）——注意本仓库 `docs/` 是 docsify 博客的内容目录，是站点本体，**不得**加入忽略清单。`LICENSE`、`.gitignore` 原已存在，未动原有内容。
