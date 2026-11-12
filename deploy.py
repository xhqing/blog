"""藏经阁（docsify 博客）的构建步骤。

`docs/post/` 就是文章本体，本脚本只做三件事：

1. 生成侧边栏 `docs/_sidebar.md` 与首页 `docs/README.md`（按目录结构，链接文字取文章标题）；
2. 给首行「创建于 …」补 `<br>`（docsify 里单换行不断行，日期和关键词会挤成一行）；
3. 把 `\\tr` 换成 `\\operatorname{tr}`（KaTeX 不认 `\\tr`）。

**为什么删掉了旧版的目录拷贝**：旧版 `refference_modify()` 先
`shutil.rmtree("./docs/post")`、再 `cp -r ./post ./docs/`，而根目录的 `post/`
早在某次整理时就不存在了——于是这段逻辑会**先删掉全部文章、再拷贝失败**，
等于一次运行清空整站。现在文章直接活在 `docs/post/`，构建只读不改，不再有拷贝步骤。

用法：
    python3 deploy.py          # 重新生成侧边栏与首页、修首行与公式宏
    python3 deploy.py --check  # 只检查有没有格式问题，不写文件
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DOCS = Path("docs")
POSTS = DOCS / "post"
DATE_RE = re.compile(r"^创建于 \d{4}-\d{2}-\d{2}(<br>)?$")
ORDER_RE = re.compile(r"<!-- order: (\d+) -->")

# 固定页面：不属于任何文章分类、但要出现在侧边栏与首页的页面。
# 结构：分组名 → （链接文字, docs 下的相对路径）。加页面时在这里登记一行即可。
FIXED_PAGES: tuple[tuple[str, tuple[tuple[str, str], ...]], ...] = (
    ("关于", (("版权与许可", "license.md"),)),
)


def post_title(path: Path) -> str:
    """侧边栏显示的文章名：用文件名（不带 .md）。

    为什么不读正文里的第一个 `## `？旧文章里第一个二级标题经常是小节名
    （如「## 导读」），拿它当标题会把侧边栏写成小节名。旧版 deploy.py 也是用
    文件名，同步脚本又按标题命名文件，两边口径一致。
    """
    return path.stem


def post_order(path: Path) -> int:
    """同步脚本给系列文章写的顺序标记；手写文章没有标记，排在后面、按文件名排。"""
    m = ORDER_RE.search(path.read_text(encoding="utf-8")[:500])
    return int(m.group(1)) if m else 999


def iter_posts() -> list[tuple[str, Path]]:
    """按「分类目录 → 顺序标记 → 文件名」列出全部文章（结果稳定、可复现）。"""
    items: list[tuple[str, Path]] = []
    for category in sorted(p for p in POSTS.iterdir() if p.is_dir()):
        for post in sorted(category.glob("*.md"), key=lambda f: (post_order(f), f.stem)):
            items.append((category.name, post))
    return items


def render_entries() -> list[str]:
    """文章列表（分类 → 顺序标记 → 文件名），侧边栏与首页共用这一份。"""
    lines: list[str] = []
    current: str | None = None
    for category, post in iter_posts():
        if category != current:
            current = category
            lines.append(f" - :books: **{category}**")
        lines.append(f"   - [{post_title(post)}](post/{category}/{post.name})")
    return lines


def render_fixed_entries() -> list[str]:
    """固定页面（如许可页），排在文章列表之后。"""
    lines: list[str] = []
    for group, pages in FIXED_PAGES:
        lines.append(f" - :scroll: **{group}**")
        for title, path in pages:
            lines.append(f"   - [{title}]({path})")
    return lines


def render_sidebar() -> str:
    return "\n".join(render_entries() + render_fixed_entries()) + "\n"


def render_readme() -> str:
    lines = ["# 藏经阁", "", " - **Repo Address**: https://github.com/xhqing/blog/"]
    return "\n".join(lines + render_entries() + render_fixed_entries()) + "\n"


def fix_first_line(text: str) -> str:
    """首行「创建于 …」补 `<br>`，否则日期和关键词会被 docsify 渲染成同一行。"""
    lines = text.split("\n")
    if lines and lines[0].startswith("创建于") and not lines[0].endswith("<br>"):
        lines[0] = lines[0].rstrip() + "<br>"
    return "\n".join(lines)


def fix_math_macros(text: str) -> str:
    return text.replace("\\tr", "\\operatorname{tr}")


def collect_problems() -> list[str]:
    """检查文章格式：一级标题、首行日期、是否进了侧边栏。"""
    problems: list[str] = []
    sidebar = (DOCS / "_sidebar.md").read_text(encoding="utf-8") if (DOCS / "_sidebar.md").exists() else ""
    for category, post in iter_posts():
        rel = post.relative_to(DOCS).as_posix()
        text = post.read_text(encoding="utf-8")
        first = text.split("\n", 1)[0]
        if not DATE_RE.match(first):
            problems.append(f"{rel}: 首行应为「创建于 YYYY-MM-DD<br>」，实际是 {first[:40]!r}")
        for n, line in enumerate(text.splitlines(), 1):
            if line.startswith("# "):
                problems.append(f"{rel}:{n}: 一级标题请改用二级（`## `），docsify 侧边栏只认到二级")
                break
        if rel not in sidebar:
            problems.append(f"{rel}: 没有出现在 docs/_sidebar.md 里（跑一次 python3 deploy.py）")
    for link in re.findall(r"\]\((post/[^)]+)\)", sidebar):
        if not (DOCS / link).exists():
            problems.append(f"docs/_sidebar.md: 链接指向不存在的文件 {link}")
    for _, pages in FIXED_PAGES:
        for _, path in pages:
            if not (DOCS / path).exists():
                problems.append(f"docs/{path}: 固定页面缺失（deploy.py 的 FIXED_PAGES 登记了它，侧边栏里有链接）")
    return problems


def build(check_only: bool = False) -> int:
    if check_only:
        problems = collect_problems()
        for p in problems:
            print(f"✗ {p}")
        print(f"\n检查完成：{len(problems)} 个问题")
        return 1 if problems else 0

    changed: list[str] = []
    for _, post in iter_posts():
        original = post.read_text(encoding="utf-8")
        fixed = fix_first_line(fix_math_macros(original))
        if fixed != original:
            post.write_text(fixed, encoding="utf-8")
            changed.append(post.relative_to(DOCS).as_posix())

    for name, content in (("_sidebar.md", render_sidebar()), ("README.md", render_readme())):
        target = DOCS / name
        if not target.exists() or target.read_text(encoding="utf-8") != content:
            target.write_text(content, encoding="utf-8")
            changed.append(f"docs/{name}")

    print(f"构建完成：更新 {len(changed)} 个文件" + (f"（{', '.join(changed)}）" if changed else ""))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="藏经阁构建步骤")
    parser.add_argument("--check", action="store_true", help="只检查格式，不写文件")
    args = parser.parse_args()
    if not POSTS.is_dir():
        sys.exit(f"找不到文章目录 {POSTS}，请在仓库根目录运行本脚本")
    return build(check_only=args.check)


if __name__ == "__main__":
    raise SystemExit(main())