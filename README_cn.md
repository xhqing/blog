<div align="center">
  <img src="assets/logo.svg" alt="blog" width="640">

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE.md)
  [![Version](https://img.shields.io/badge/Version-1.0.0-blue)](CHANGELOG.md)
  [![Type](https://img.shields.io/badge/Type-Project-lightgrey)](#)

  [English](README.md)
</div>

# blog

基于 [docsify](https://docsify.js.org/) 的个人博客，线上地址：**https://xhqing.github.io/blog**。

## Python 环境

```sh
conda create --name py3912 python=3.9.12
conda activate py3912
```

## 常用命令

```sh
python new_post.py    # 新建文章
python deploy.py      # 部署文章
python preview.py     # 预览文章
```

## 自动部署配置

```sh
cp .auto_deploy.py ~
vim ~/.zshrc
gd="python ~/.auto_deploy.py"
source ~/.zshrc
```

## 版权与署名

Copyright (c) 2021 All Contributors，基于 [MIT License](LICENSE.md) 发布。

署名：使用或引用本项目时，请保留版权声明并注明来源：[blog](https://github.com/xhqing/blog)。
