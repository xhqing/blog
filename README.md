<div align="center">
  <img src="assets/logo.svg" alt="blog" width="640">

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE.md)
  [![Version](https://img.shields.io/badge/Version-1.0.0-blue)](CHANGELOG.md)
  [![Type](https://img.shields.io/badge/Type-Project-lightgrey)](#)

  [简体中文](README_cn.md)
</div>

# blog

Personal blog built with [docsify](https://docsify.js.org/), published at **https://xhqing.github.io/blog**.

## Python environment

```sh
conda create --name py3912 python=3.9.12
conda activate py3912
```

## Useful commands

```sh
python new_post.py    # new post
python deploy.py      # deploy post
python preview.py     # preview post
```

## Auto deployment setup

```sh
cp .auto_deploy.py ~
vim ~/.zshrc
gd="python ~/.auto_deploy.py"
source ~/.zshrc
```

## License & Attribution

Copyright (c) 2021 All Contributors. Released under the [MIT License](LICENSE.md).

Attribution: if you use or reference this project, please keep the copyright notice and credit the source: [blog](https://github.com/xhqing/blog).
