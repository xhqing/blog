# CHANGELOG

本文件记录本项目（blog，个人博客仓库）每次文件增删改的变更，写清「为什么改」和「改了什么」。版本号以项目根 `VERSION` 文件为唯一权威。

## [未发布]

### 移除（撤下全部同步文章，2026-11-13）

- **为什么改**：用户 2026-11-13 裁定「这些文章也从博客撤掉，以后不往博客发送未完成的文章，没有我的同意不能往博客发布任何文章」。2026-11-11 的旧口径「不论写完没写完都发布」作废。
- **改了什么**：删除 6 篇带 `<!-- source: … -->` 标记的文章（复利系列 5 篇、《为什么 AI 一定能做到你满意为止？》1 篇）及其 6 张配图；`docs/README.md` 与 `docs/_sidebar.md` 删掉「复利与交易」「方法与实战」两个已空的分类块；两个空目录一并清掉。手写文章不受影响。

### 变更（同步改为需用户同意，2026-11-13）

- **为什么改**：自动定时同步等于绕过用户同意直接发布，与新规则冲突。
- **改了什么**：`.github/workflows/sync-articles.yml` 去掉 `schedule`（每 10 分钟），只保留 `workflow_dispatch`，新增必填输入 `user_approved`，job 加 `if: inputs.user_approved == 'approved'` 闸门。`AGENTS.md` 的「内容怎么进来」节重写；新建 `.pi/APPEND_SYSTEM.md` 承载硬约束。

## [1.2.1] - 2026-11-12

### 变更（许可页面：去掉代码授权交代，联系方式对齐个人主页）

- **为什么改**：用户 2026-11-12 指出两处。① 代码不是重点：CC BY 4.0 项目里附带的脚本只是附属物，许可页面不该单独交代它们的授权；② 联系方式应当与 `xhqing/xhqing` 仓库 README 里写的一致（GitHub / 微信 / 邮箱 / 小红书），而不是只给一个 Issue 链接。
- **改了什么**：`docs/license.md` 删掉「关于代码」整节；「联系」改为四项（GitHub、微信、邮箱、小红书），与个人主页仓库同一套。
- **边界**：文章与仓库的许可证不变（仍是 CC BY 4.0），只是不再在许可页面里专门谈代码。

## [1.2.0] - 2026-11-12

### 新增（版权许可页面 `/license.md`：讲清 CC BY 4.0 允许什么、要求什么）

- **为什么改**：仓库里有 `LICENSE.md` 全文，但那是法律文本，普通读者看不懂也不愿读；转载者真正需要知道的是“能不能用、需不需要问、署名怎么写”。用户 2026-11-11 要求专门做一个许可页面。
- **改了什么**：
  - 新增 `docs/license.md`：「可以做什么」（分发 / 改编 / 商用）、“需要做的三件事”（署名 / 标注许可 / 说明改动）、可直接抄的署名句式（全文转载 / 节选翻译 / 英文场景）、“不在授权范围内”（他人素材 / 站名与商标 / 单独声明的文章）、代码部分与联系方式；页头写明“有法律意义的只有官方全文”。
  - `deploy.py`：新增 `FIXED_PAGES` 常量（固定页面 → 分组 → 链接），侧边栏与首页末尾多一组「关于 → 版权与许可」；`collect_problems()` 多一项检查——固定页面文件必须在位（避免侧边栏里挂一个死链）。为此把侧边栏与首页的条目生成抽成 `render_entries()` / `render_fixed_entries()`，文章列表与固定页各自一段。
  - `docs/_sidebar.md` 与 `docs/README.md` 为 `deploy.py` 重新生成的结果（现有文章列表一字未动，只在末尾追加一组）。
- **边界**：这不是又一份许可文本，而是 CC BY 4.0 的说明页；两者冲突以官方全文为准。以后新增固定页面（如关于作者、友链）只需在 `deploy.py` 的 `FIXED_PAGES` 里加一行，不必手改侧边栏与首页。

## [1.1.2] - 2026-11-11

### 修复（LICENSE.md 改为纯官方全文：GitHub 只认零追加的 CC BY 4.0）

- **为什么改**：1.1.1 之后仓库侧边栏的许可证显示「Other」，`gh api repos/xhqing/blog/license` 返回 `{"key":"other","spdx_id":"NOASSERTION"}`——等于在 GitHub 眼里没有许可证，读者看不到 CC BY 4.0。
- **怎么查出来的**：对照两个同样用 CC BY 4.0 的知名仓库——`microsoft/autogen` 与 `EbookFoundation/free-programming-books`，两者的 `LICENSE` 都是**纯 `legalcode.txt` 全文、零追加**（18650 / 18658 字节），GitHub 都识别为 `cc-by-4.0` / `CC-BY-4.0`。我们那两版都在官方文本前后加了自己的段落（先是版权行 + 中文说明在顶部，后来版权行改到末尾），两版都还是 `NOASSERTION`。结论：**GitHub 的 CC BY 识别要求 LICENSE 文件就是纯官方文本，加一个版权行都不算**——这和 MIT 不同（MIT 模板本身就把版权行和许可正文写在一个文件里）。
- **改了什么**：`LICENSE.md` 换成官方 `legalcode.txt` 全文（原样下载、一字不改）；版权声明行与许可要点、署名要求写进 `README.md` / `README_cn.md` 的「License & Attribution」/「版权与署名」节，并明说「文件是纯文本、为什么」。
- **没改什么**：徽章、两份 CONTRIBUTING、`.commit-cache.md` 均不动。
- **代价（要记住）**：版权声明从此不在 `LICENSE.md` 里，而在两版 README 里——这是 CC BY 项目为了「GitHub 能认出许可证」必须交换的一步。团队规则中「CC BY 4.0 项目 LICENSE.md 顶部放版权声明行」那条因此改成「纯官方全文 + 版权行写 README」。

## [1.1.1] - 2026-11-11

### 变更（许可证类型修正：MIT → CC BY 4.0）

- **为什么改**：本仓库主体是供人阅读的文章，属 2026-11-08 团队许可证规则里的**非软件项目**，应当用 CC BY 4.0；仓库里一直挂着 MIT——MIT 的授权对象是「software and associated documentation files」，对纯文字作品是用语错位（它也不要求以指定方式署名，而这正是文字作品最在意的）。用户 2026-11-11 当场指出这一点。
- **改了什么**：
  - `LICENSE.md` 顶部改为版权声明行 + 许可要点说明（可共享、可演绎、含商业用途；条件是署名、给出许可链接、标明是否修改、不加额外限制），正文原样收录官方 `legalcode.txt` 全文（https://creativecommons.org/licenses/by/4.0/legalcode.txt，未加改动）。
  - `README.md` / `README_cn.md`：License 徽章由 MIT 改为 CC BY 4.0，底部版权与署名段改为 CC BY 口径（署名要求写清：保留版权声明、链接回本仓库、说明是否修改）。
  - `CONTRIBUTING.md` / `CONTRIBUTING_cn.md`：贡献授权条款由 MIT License 改为 CC BY 4.0（贡献者保留著作权、按项目许可证授权这两条不变）。
- **边界**：仓库里的配套脚本（`deploy.py` / `scripts/` / `.github/`）随主产物一并置于 CC BY 4.0 之下——按团队规则「软件 MIT / 非软件 CC BY 4.0，二选一、没有第三种」，本仓库按主产物（文章）定性。

## [1.1.0] - 2026-11-11

### 新增（自动发布管道：social-agent 的文章自动同步进博客）

- **为什么改**：用户 2026-11-11 把博客移交到 social-agent（Gatsby）名下作为子项目，同时提两条要求——① social-agent 的 `docs/articles/` 里**所有**文章都发到博客，**不看写完没写完**；② 每次 PR 更新文章内容就自动发布。此前本仓库的文章只能手写到 `docs/post/`，与写作源头（social-agent 的公众号稿）完全脱节。
- **改了什么**：
  - 新增 `scripts/sync_articles.py`：拉 social-agent 的文章 → 转成博客体例（一级标题改二级、补 `创建于` / `关键词` 首行、相对图片拷进 `img/<源文件名>/` 并改写链接）→ 跑 `deploy.py` → **有变化时先跑一遍 `validate`，通过再提交并直推 main**（没有变化就不提交，站点不会动）。带 `<!-- source: … -->` 标记认领自己写的文章：源文章改名或删除时，博客上对应那篇跟着另存或删除；**没有标记的手写文章永远不会被碰**。支持 `--source`（本地副本调试）与 `--dry-run`（只看计划）。
  - 新增 `.github/workflows/sync-articles.yml`：每 10 分钟拉一次 + 手动 `workflow_dispatch`。用定时拉取而不是跨仓库推送，是因为跨仓库触发需要额外 token，而定时拉取零配置、不会因为对方仓库权限变动而失效；合并后最迟十分钟上线，不需要人工点。
  - 新增 `.github/workflows/validate.yml` + `scripts/validate.py`：CI 自检——Python 语法能过、每篇首行是「创建于 YYYY-MM-DD」、没有一级标题、每篇都进了侧边栏、侧边栏链接都指向真实文件。
  - **重写 `deploy.py`**：删掉旧版 `refference_modify()` 的目录拷贝逻辑——它先 `shutil.rmtree("./docs/post")` 再 `cp -r ./post ./docs/`，而根目录 `post/` 早已不存在，**一次运行就清空全站文章**；改为原地修复，不再有拷贝步骤。侧边栏与首页改为按 `order` 标记 + 文件名排序（结果可复现），新增 `--check` 只检不写。
  - 新增 `AGENTS.md` 与 `.pi/APPEND_SYSTEM.md`（2026-11-08 子项目新规：本仓库实体文件，不挂软链接）、`CONTRIBUTING.md` / `CONTRIBUTING_cn.md`（2026-11-09 团队标准，`{{LICENSE_NAME}}` 已替换为 MIT License）。
  - `README.md` / `README_cn.md` 双语同步：补「文章从哪来」与真实可用的命令（原文档里的 `new_post.py` / `preview.py` 在仓库里并不存在），版本徽章改为 1.1.0。`LICENSE.md` 与 README 版权行按 2026-11-08 新规改为 `xhqing and contributors`，`.commit-cache.md` 的署名口径同步。
- **首次同步结果**：5 篇（复利系列）进 `docs/post/复利与交易/`，6 张配图进 `img/<源文件名>/`，侧边栏按系列阅读顺序 1–5 排列。
- **已知边界**：定时拉取意味着合并后最迟十分钟才上线；要立即发布可以手动触发 workflow。未合并的 PR 分支内容不会发——发布的是 `main` 上的状态。
- **为什么机器人不按「分支 + PR + 必过检查」的团队标准走**：用 `GITHUB_TOKEN` 建的 PR 不会触发其它 workflow（GitHub 防递归规则），`validate` 这个必过检查永远不会出现在机器人 PR 上，自动合并会一直等下去（2026-11-11 实测：PR 开出来、检查栏一直空着）。所以改成「推送前先跑 `validate`，通过再直推 `main`」——门禁放在提交前，不放在 PR 上。真要做到「每次同步都过一个 PR」，需要一个能触发 workflow 的 PAT，届时换回来即可。

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
