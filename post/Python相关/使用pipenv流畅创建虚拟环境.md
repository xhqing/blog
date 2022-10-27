创建于 2022-09-04
关键词: pipenv, pyenv.

实验基于pyenv-2.3.2, pipenv-2022.7.24.

使用过 pipenv 的应该都知道`pipenv --python path/to/python `可以用 path 指向的 Python 解释器版本创建 Python 虚拟环境，然而实际上如果每次都要去找 Python 解释器的路径还是比较麻烦的，实际上 pipenv 也可以直接指定 Python 版本：如`pipenv --python 3.19.12`，如果 pipenv 在本机没有找到相应版本的 Python 则会从 www.python.org 下载相应的版本，这里 pipenv 实际上调用了 pyenv 来下载相应的 Python 版本，这里存在 2 个问题：

- 1、安装pipenv的时候并没有自动安装pyenv，使用了`pipenv --python 3.9.12`这个命令，报错提示也不会提示你安装pyenv；
- 2、经过一番查看文档，知道要先安装 pyenv，然而安装了 pyenv 后从 www.python.org 下载 Python 不知到要等到什么时候才能下载完。

第 1 个问题很简单，安装一下 pyenv 就好了:
```sh
brew install pyenv
```

第 2 个问题可以通过以下代码解决：

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