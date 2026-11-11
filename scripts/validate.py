"""仓库自检：语法能过、文章体例统一、侧边栏不漏文章。

CI 里跑（`.github/workflows/validate.yml`），本地也能直接跑：

    python3 scripts/validate.py

检查项：
1. `deploy.py` 与 `scripts/*.py` 能被 Python 解析；
2. 每篇文章首行是「创建于 YYYY-MM-DD」，且没有一级标题（docsify 侧边栏只认到二级）；
3. 每篇文章都出现在 `docs/_sidebar.md` 里，侧边栏的每个链接都指向真实文件；
4. 站点必备文件在位（`docs/index.html`、`docs/.nojekyll`）。

刻意不检查「文章写完了没有」——博客是发布草稿的地方，正式与否由内容自己说明。
"""

from __future__ import annotations

import compileall
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main() -> int:
    problems: list[str] = []

    scripts = [ROOT / "deploy.py", *sorted((ROOT / "scripts").glob("*.py"))]
    for script in scripts:
        if script.exists() and not compileall.compile_file(str(script), quiet=2):
            problems.append(f"{script.relative_to(ROOT).as_posix()}: Python 语法错误")

    for required in ("docs/index.html", "docs/.nojekyll", "docs/_sidebar.md"):
        if not (ROOT / required).exists():
            problems.append(f"{required}: 缺失")

    if (ROOT / "docs" / "_sidebar.md").exists():
        import deploy  # noqa: PLC0415 - 依赖运行时路径，放这里导入

        problems.extend(deploy.collect_problems())
    else:
        problems.append("docs/_sidebar.md: 缺失，无法检查文章是否入侧边栏")

    for item in problems:
        print(f"✗ {item}")
    if problems:
        print(f"\n共 {len(problems)} 个问题")
        return 1
    print("✓ 全部检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())