# CHANGELOG

本文件记录本项目（blog，个人博客仓库）每次文件增删改的变更，写清「为什么改」和「改了什么」。版本号以项目根 `VERSION` 文件为唯一权威。

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
