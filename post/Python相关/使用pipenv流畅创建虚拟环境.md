创建于 2022-09-04
关键词: pipenv, pyenv.

实验基于pyenv-2.3.2, pipenv-2022.7.24.

## 流畅使用pipenv需要的准备

使用过 pipenv 的应该都知道`pipenv --python path/to/python `可以用 path 指向的 Python 解释器版本创建 Python 虚拟环境，然而实际上如果每次都要去找 Python 解释器的路径还是比较麻烦的，实际上 pipenv 也可以直接指定 Python 版本：如`pipenv --python 3.19.12`，如果 pipenv 在本机没有找到相应版本的 Python 则会从 www.python.org 下载相应的版本，这里 pipenv 实际上调用了 pyenv 来下载相应的 Python 版本，这里存在 2 个问题：

- 1、安装pipenv的时候并没有自动安装pyenv，使用了`pipenv --python 3.9.12`这个命令，报错提示也不会提示你安装pyenv；
- 2、经过一番查看文档，知道要先安装 pyenv，然而安装了 pyenv 后从 www.python.org 下载 Python 不知到要等到什么时候才能下载完。

第 1 个问题很简单，安装一下 pyenv 就好了:
```sh
brew install pyenv
```

第 2 个问题可以通过以下方式解决：

```python
import os

first = ["3"]
second = [str(x) for x in range(6,11)]
third = [str(x) for x in range(14)]
versions = []
for f in first:
    for s in second:
        for t in third:
            versions.append(f+"."+s+"."+t)

for v in versions:
    try:
        os.system(f"wget https://npm.taobao.org/mirrors/python/{v}/Python-{v}.tar.xz -P ~/.pyenv/cache/")
    except:
        continue
```

 也就是先把大部分 Python 版本缓存在`~/.pyenv/cache/`，pyenv 知道缓存目录已经有了相应版本的 Python 就不会去下载了。

## 结合实际得出的个人感觉更好的方法

虽然在`~/.pyenv/cache/`有了 Python 的压缩文件，但此时 Python 还未编译安装(编译安装好的 Python 版本会保存在`~/.pyenv/versions/`下)，虽然在使用 `pipenv --python x.x.xx`的时候如果 `~/.pyenv/versions/`目录下没有相应的 Python 版本 pipenv 会提示是否使用 pyenv 安装相应的版本，但此时有 2 个问题：

- 1）并不能够百分百保证`~/.pyenv/cache/`目录下有你想要的版本，如果没有的话，pyenv 又会跑到 Python 官网去下载，又不知道要等到猴年马月，最后只能`Ctr+C`中断；
- 2）就算`~/.pyenv/cache/`中有你想要的 Python 版本，此时使用 pyenv 安装并不一定能安装成功，这个和系统环境等各方面的原因有关，但此时还是在使用`pipenv --python x.x.xx`这个命令的过程中，从使用体验上会有`pipenv --python x.x.xx`不好用的感觉，实际上相比于`pipenv --python path/to/python`这个命令要好用的多，因为后者还经常要去查一下 python 解释器的路径；

所以目前除了更改`pyenv`和`pipenv`的源码外，最方便的方法是：把 pyenv 安装 Python 和使用 pipenv 创建虚拟环境这两件事隔离开来操作，当使用`pipenv --python x.x.xx`时如果提示是否使用 pyenv 安装 Python，直接选择拒绝，转而手动去使用 pyenv 安装相应版本的解释器到`~/.pyenv/versions/`下，或者选择其它的 Python 解释器路径，这个时候确实有点麻烦，为了尽可能避免这种麻烦事的发生，在使用 pipenv 之前应该手动使用 pyenv 把尽可能多的 Python 版本安装进`~/.pyenv/versions/`目录下。使用 pyenv 批量安装 Python 参见：https://github.com/xhqing/pipenv-prepare

