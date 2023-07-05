"""
   cp .auto_deploy.py ~
   vim ~/.zshrc
   alias gd="git pull && python ~/.auto_deploy.py"
   source ~/.zshrc
"""

import os

curr_abspath = os.path.abspath(".")

if curr_abspath.split("/")[-1] == "blog":
    os.system("python deploy.py")

os.system("git add .")
