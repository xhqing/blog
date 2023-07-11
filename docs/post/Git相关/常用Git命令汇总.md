创建于 2023-07-11<br>
关键词: git.

````sh
## 基于当前分支新建分支xxx并切换到新建的分支xxx
git checkout -b xxx

## 切换到xxx分支
git checkout xxx

## 查看所有分支和当前分支
git branch -a

## 当前目录为项目根目录，添加/提交/推送(个人习惯，这里使用的是设置在~/.bashrc或~/.zshrc里面的alias)
gd && gc "update" && gp   # 原命令：git add . && git commit -m "update" && git push

## 拉取远程仓库的当前分支并合并到本地当前分支(个人习惯，这里使用的是设置在~/.bashrc或~/.zshrc里面的alias)
gpll   # 原命令：git pull

## 同步xxx分支代码到当前分支
git pull origin xxx && git merge xxx
```
````

