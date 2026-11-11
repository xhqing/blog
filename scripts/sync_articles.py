"""把 social-agent 的文章同步到藏经阁（docs/post/<分类>/<标题>.md）。

内容源头是 social-agent 仓库的 `docs/articles/*.md`——那份文章是公众号 / 口播稿的底稿，
本脚本只做「搬家 + 适配 docsify 体例」，不改正文观点：

- 一级标题 `# 标题` 改成二级 `## 标题`（docsify 侧边栏只认到二级）；
- 首行补 `创建于 YYYY-MM-DD<br>` 与 `关键词: …`（博客的既有体例，见 docs/post 下其它文章）；
- 相对图片拷进 `docs/post/<分类>/img/<源文件名>/` 并改写链接（不同文章同名图不会互相覆盖）；
- 每篇写一行 `<!-- source: … -->` 标记，用来认领「这篇是同步来的」——标题变了能删掉旧文件，
  源文章删了能一并清理，同时绝不碰手写的旧文章。

发布不区分「写完没写完」：源仓库里有什么就发什么。

用法：
    python3 scripts/sync_articles.py                    # 从 GitHub 拉 social-agent 最新提交
    python3 scripts/sync_articles.py --source ~/Developer/social-agent   # 用本地副本（调试）
    python3 scripts/sync_articles.py --dry-run          # 只打印计划，不落盘
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DOCS = Path("docs")
POSTS = DOCS / "post"

SOURCE_REPO = "https://github.com/xhqing/social-agent.git"
SOURCE_PATH = "docs/articles"          # 源仓库里文章的目录
DEFAULT_CATEGORY = "方法与实战"
# 分类按源文件名前缀匹配，匹配不上落 DEFAULT_CATEGORY
CATEGORY_BY_PREFIX = [
    ("compounding-", "复利与交易"),
    ("three-switches-", "复利与交易"),
]
# 系列文章的阅读顺序（写进文章头部的 order 标记，侧边栏据此排序）
ORDER = {
    "compounding-three-switches.md": 1,
    "compounding-verify.md": 2,
    "compounding-size.md": 3,
    "three-switches-derivation.md": 4,
    "compounding-assumptions.md": 5,
}
KEYWORDS = {
    "compounding-three-switches.md": "复利, 复利公式, 几何平均, 大数定律",
    "compounding-verify.md": "正期望, 样本量, t 检验, 置信区间",
    "compounding-size.md": "凯利公式, 仓位管理, 波动率拖累",
    "three-switches-derivation.md": "复利, 数学推导, 凯利公式",
    "compounding-assumptions.md": "相关性, 非正态, 多重比较",
}

MARKER = "<!-- source: social-agent/{path} -->"
MARKER_RE = re.compile(r"<!-- source: social-agent/(?P<path>[^ ]+) -->")
DATE_RE = re.compile(r"^创建于 (?P<date>\d{4}-\d{2}-\d{2})")
IMG_RE = re.compile(r'(?P<prefix>!\[[^\]]*\]\(|src=")(?P<path>(?!https?://|//)[^")]+)"?')
BAD_FILENAME = re.compile(r'[\\/:*?"<>|]')


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def fetch_source(explicit: str | None, keep: Path) -> Path:
    """返回源仓库根目录：显式指定的本地副本，或现克隆一份（只取文章目录）。"""
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if not (root / SOURCE_PATH).is_dir():
            sys.exit(f"{root} 下没有 {SOURCE_PATH}，--source 应指向 social-agent 仓库根目录")
        return root

    clone = keep / "social-agent"
    print(f"克隆 {SOURCE_REPO}（只取 {SOURCE_PATH}）…")
    steps = [
        ["git", "clone", "-q", "--filter=blob:none", "--no-checkout", SOURCE_REPO, str(clone)],
        ["git", "-C", str(clone), "sparse-checkout", "set", "--no-cone",
         f"/{SOURCE_PATH}/*.md", f"/{SOURCE_PATH}/img/**"],
        ["git", "-C", str(clone), "checkout", "-q"],
    ]
    for cmd in steps:
        r = run(cmd)
        if r.returncode != 0:
            sys.exit(f"拉取源仓库失败：{' '.join(cmd)}\n{r.stderr.strip()}")
    return clone


def articles(src: Path) -> list[Path]:
    """源仓库里要发布的文章：docs/articles/*.md，跳过软链接与隐藏文件。"""
    base = src / SOURCE_PATH
    out = []
    for p in sorted(base.glob("*.md")):
        if p.is_symlink() or p.name.startswith("."):
            continue
        out.append(p)
    return out


def category_of(name: str) -> str:
    for prefix, category in CATEGORY_BY_PREFIX:
        if name.startswith(prefix):
            return category
    return DEFAULT_CATEGORY


def post_title(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip().lstrip("*").strip("*").strip()
    return None


def creation_date(src: Path, rel: str, existing: Path | None) -> str:
    """创建日期：优先沿用博客里已有的，其次取源仓库里该文件首次提交的日期。"""
    if existing and existing.exists():
        first = existing.read_text(encoding="utf-8").split("\n", 1)[0]
        m = DATE_RE.match(first)
        if m:
            return m.group("date")
    r = run(["git", "-C", str(src), "log", "--follow", "--diff-filter=A", "--format=%as",
             "-1", "--", rel])
    stamp = r.stdout.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", stamp):
        return stamp
    return dt.date.today().isoformat()


def copy_images(text: str, src_file: Path, src_root: Path, img_root: Path, link_base: Path,
                dry: bool) -> str:
    """把正文里引用的本地图片拷到 img/<源文件名>/ 并改写链接。

    链接写成相对父目录的形式（`img/<源文件名>/…`）：docsify 里文章链接是相对
    文章自身路径解析的，写成 `post/…` 会多套一层而 404。
    """
    base = src_file.parent

    def repl(m: re.Match[str]) -> str:
        raw = m.group("path").strip()
        rel = Path(raw.lstrip("./")) if raw.startswith("./") else Path(raw)
        candidate = (base / rel).resolve()
        if not candidate.is_file():
            print(f"  ! 图片找不到，保留原链接：{raw}")
            return m.group(0)
        try:
            candidate.relative_to(src_root.resolve())
        except ValueError:
            print(f"  ! 图片在源仓库之外，跳过：{raw}")
            return m.group(0)
        target = img_root / candidate.name
        if not dry:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(candidate, target)
        new_path = target.relative_to(link_base).as_posix()
        quote = '"' if m.group("prefix").endswith('"') else ""
        return f'{m.group("prefix")}{new_path}' + ('"' if quote else "")

    return IMG_RE.sub(repl, text)


def render(src_file: Path, src_root: Path, category: str, date: str, existing: Path | None,
           dry: bool) -> tuple[str, Path]:
    text = src_file.read_text(encoding="utf-8")
    title = post_title(text)
    if not title:
        raise SystemExit(f"{src_file.name} 没有一级标题（`# …`），无法命名博客文章")
    slug = src_file.stem
    img_root = POSTS / category / "img" / slug
    body = text.replace(f"# {title}", f"## {title}", 1)
    body = copy_images(body, src_file, src_root, img_root, POSTS / category, dry).strip() + "\n"

    keywords = KEYWORDS.get(src_file.name)
    head = f"创建于 {date}<br>\n"
    if keywords:
        head += f"关键词: {keywords}.\n"
    head += f"\n{MARKER.format(path=src_file.relative_to(src_root).as_posix())}\n"
    if src_file.name in ORDER:
        head += f"<!-- order: {ORDER[src_file.name]} -->\n"
    head += "\n"
    target = POSTS / category / f"{BAD_FILENAME.sub('-', title)}.md"
    return head + body, target


def existing_posts() -> dict[str, Path]:
    """博客里所有「同步来的」文章：源相对路径 → 当前文件。"""
    found: dict[str, Path] = {}
    for post in POSTS.rglob("*.md"):
        m = MARKER_RE.search(post.read_text(encoding="utf-8")[:400])
        if m:
            found[m.group("path")] = post
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description="把 social-agent 的文章同步到藏经阁")
    parser.add_argument("--source", help="social-agent 仓库本地路径（调试用，不走网络）")
    parser.add_argument("--dry-run", action="store_true", help="只打印计划，不写文件")
    args = parser.parse_args()

    if not POSTS.is_dir():
        sys.exit(f"找不到 {POSTS}，请在仓库根目录运行本脚本")

    with tempfile.TemporaryDirectory() as tmp:
        src = fetch_source(args.source, Path(tmp))
        current = existing_posts()
        planned: dict[str, Path] = {}
        written: list[str] = []
        removed: list[str] = []
        active: set[tuple[str, str]] = set()

        try:
            for src_file in articles(src):
                rel = src_file.relative_to(src).as_posix()
                category = category_of(src_file.name)
                active.add((category, src_file.stem))
                prev = current.get(rel)
                text, target = render(src_file, src, category,
                                      creation_date(src, rel, prev), prev, args.dry_run)
                planned[rel] = target
                if prev and prev != target:
                    removed.append(prev.relative_to(DOCS).as_posix())
                if args.dry_run:
                    print(f"计划写入 {target.relative_to(DOCS).as_posix()}")
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists() or target.read_text(encoding="utf-8") != text:
                    target.write_text(text, encoding="utf-8")
                    written.append(target.relative_to(DOCS).as_posix())
        except SystemExit:
            raise
        except Exception as exc:  # noqa: BLE001 - 同步失败要给出人看得懂的报错
            print(f"同步失败：{exc}")
            return 1

        # 源文章已删除同步来的文件
        for rel, path in current.items():
            if rel not in planned:
                removed.append(path.relative_to(DOCS).as_posix())

        if args.dry_run:
            for path in dict.fromkeys(removed):
                print(f"计划删除 {path}")
            return 0

        for path in dict.fromkeys(removed):
            target = DOCS / path
            if target.exists():
                target.unlink()

        # 清掉不再有人用的配图目录（文章改名后旧图会留在盘上）
        for category_dir in POSTS.iterdir():
            img_root = category_dir / "img"
            if not img_root.is_dir():
                continue
            for slug_dir in img_root.iterdir():
                if (category_dir.name, slug_dir.name) not in active and slug_dir.is_dir():
                    shutil.rmtree(slug_dir)

    for directory in sorted(POSTS.rglob("*"), reverse=True):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()

    deploy = Path("deploy.py")
    if deploy.exists():
        r = run([sys.executable, str(deploy)])
        print(r.stdout.strip())
        if r.returncode != 0:
            print(r.stderr.strip())
            return r.returncode

    print(f"同步完成：写入 {len(written)} 篇，删除 {len(dict.fromkeys(removed))} 篇")
    for item in written:
        print(f"  ✎ {item}")
    for item in dict.fromkeys(removed):
        print(f"  − {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())