# Blog Repo
Based on [docsify](https://docsify.js.org/).

## Blog Address
https://xhqing.github.io/blog

## Python Environment
```sh
conda create --name blog python=3.9.12
conda activate blog
```

## Useful Commands
```sh
python new_post.py    # new post
python deploy.py      # deploy post
python preview.py    # preview post
```

## Auto Deployment Setting
```sh
cp .auto_deploy.py ~
vim ~/.zshrc
gd="git pull && python ~/.auto_deploy.py"
source ~/.zshrc
```
