<div align="center">
  <img src="assets/logo.svg" alt="blog" width="640">

  [![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey)](LICENSE.md)
  [![Version](https://img.shields.io/badge/Version-1.2.1-blue)](CHANGELOG.md)
  [![Type](https://img.shields.io/badge/Type-Project-lightgrey)](#)

  [简体中文](README_cn.md)
</div>

# blog

Personal blog "藏经阁" built with [docsify](https://docsify.js.org/), published at **https://xhqing.github.io/blog**.

## Where posts come from

Two sources:

- **Written by hand**: drop a Markdown file into `docs/post/<category>/`. The first line should read `创建于 YYYY-MM-DD<br>`, and the title uses a second-level `##` heading.
- **Synced automatically**: articles living in the `docs/articles/` folder of the `social-agent` project are pulled in every ten minutes by `.github/workflows/sync-articles.yml` (manual runs are also supported) and written into category folders such as `docs/post/复利与交易/`. It only commits when something actually changed, and runs the repo self-check before pushing.

**A post does not need to be finished to be published** — whatever state the source repo is in is what the blog shows.

The sync only touches its own output: each synced post carries a `<!-- source: … -->` marker, so deleting or renaming a source article removes or moves the matching post, while hand-written posts are never touched.

## Useful commands

```sh
python3 deploy.py                             # regenerate sidebar and home page, fix first line and math macros
python3 deploy.py --check                     # check formatting only, write nothing
python3 scripts/sync_articles.py              # sync the social-agent articles right now
python3 scripts/sync_articles.py --dry-run    # print the sync plan only
python3 scripts/validate.py                   # repo self-check (the same script CI runs)
```

To preview locally, point any static server at `docs/`, e.g. `python3 -m http.server -d docs 8000`.

## Auto deployment setup

Syncing runs on GitHub Actions, so no local setup is required. To rebuild the sidebar and home page by hand, run `python3 deploy.py` and commit.

## License & Attribution

Copyright (c) 2021-2026 xhqing and contributors. Released under [CC BY 4.0](LICENSE.md).

`LICENSE.md` holds the official CC BY 4.0 legal code, verbatim and with nothing added — GitHub only recognises the licence when the file is the pure text, so the copyright line and the summary live here instead.

Attribution: the licence requires credit. If you reuse or adapt this material, keep the copyright notice above, link back to [blog](https://github.com/xhqing/blog), and say whether you changed anything.