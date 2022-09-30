"""
   cp gd.py ~
   vim ~/.zshrc
   alias gd="python ~/gd.py"
"""

import os

curr_abspath = os.path.abspath(".")

if curr_abspath.split("/")[-1] == "blog":
    os.system("pipenv run python dp.py")

os.system("git add .")
