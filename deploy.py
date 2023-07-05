"""Blog deployment script.
"""
import os
import shutil
import platform
print("Using Python:", platform.python_version())

class TitleError(Exception):
    """TitleError class"""

class LengthError(Exception):
    """length too long error"""

def post_title_stdlen(post_title):

    cn_len = sum(list(map(lambda x: 1 if '\u4e00' <= x <= '\u9fa5' else 0, post_title)))
    return len(post_title) - cn_len + 2*cn_len

def gen_mdfile(filename: str) -> None:
    """
    finename: "_sidebar", "README"
    """
    post_dirs = []
    for string in os.listdir("docs/post"):
        if "." not in string: post_dirs.append(string)

    with open(f"docs/{filename}.md", "w") as f:
        if filename=="README": 
            f.write("# 藏经阁\n")
            f.write(" - **Repo Address**: https://github.com/xhqing/blog/\n")
        for dirname in post_dirs:
            f.write(f" - :books: **{dirname}**\n")
            post_mdfiles = []
            for string in os.listdir(f"docs/post/{dirname}"):
                if string[-3:] == ".md": post_mdfiles.append(string)
            for mdf in post_mdfiles:
                f.write(f"   - [{mdf[:-3]}](post/{dirname}/{mdf})\n")

def gen_readme():
    gen_mdfile("README")

def gen_sidebar():
    gen_mdfile("_sidebar")

def modify_tr_operator():

    post_dirs = []
    for string in os.listdir("docs/post"):
        if "." not in string: post_dirs.append(string)

    for dirname in post_dirs:
        post_mdfiles = []
        for string in os.listdir(f"docs/post/{dirname}"):
            if string[-3:] == ".md": post_mdfiles.append(string)
        
        if post_mdfiles:
            for mdf in post_mdfiles:
                with open(f"docs/post/{dirname}/"+mdf, "r") as f:
                    lines = f.readlines()
            for line in lines:
                if "\\tr" in line:
                    index = lines.index(line)
                    lines[index] = lines[index].replace("\\tr","\operatorname{tr}")

            with open(f"docs/post/{dirname}/"+mdf, "w") as f:
                for line in lines:
                    f.write(line)

def first_line_add_br():

    post_dirs = []
    for string in os.listdir("docs/post"):
        if "." not in string: post_dirs.append(string)
    
    for dirname in post_dirs:
        post_mdfiles = []
        for string in os.listdir(f"docs/post/{dirname}"):
            if string[-3:]==".md": post_mdfiles.append(string)

        for mdf in post_mdfiles:
            with open(f"docs/post/{dirname}/"+mdf, "r") as f:
                lines = f.readlines()
            if lines[0][:3]=="创建于": lines[0] = lines[0].replace("\n","<br>\n")

            with open(f"docs/post/{dirname}/"+mdf, "w") as f:
                for line in lines: f.write(line)

def title_level_check():
    """
    post mdfile level 1 title should use 2 `#`.
    """
    post_dirs = []
    for string in os.listdir("post"):
        if "." not in string: post_dirs.append(string)
    
    for dirname in post_dirs:
        post_mdfiles = []
        for string in os.listdir(f"post/{dirname}"):
            if string[-3:]==".md": post_mdfiles.append(string)
    
        for mdf in post_mdfiles:
            with open(f"./post/{dirname}/"+mdf, "r") as f:
                text = f.readlines()
    
            for line in text:
                if line[:2] == "# ":
                    raise TitleError(f"""\033[01;31;01m {mdf} {line} Please use 2 '#', {'#'+line}\033[01;31;01m""")

def title_length_check():
    """post title length should not be more than 28 chars. 
    Note: a cn char len eq to double en char len.
    """
    post_dirs = []
    for string in os.listdir("post"):
        if "." not in string: post_dirs.append(string)

    for dirname in post_dirs:
        post_mdfiles = []
        for string in os.listdir(f"post/{dirname}"):
            if string[-3:]==".md": post_mdfiles.append(string)

        post_titles = list(map(lambda x: x.replace("--未完成.md","") if "--未完成" in x else x.replace(".md",""), post_mdfiles))
        for title in post_titles:
            if post_title_stdlen(title) > 28:
                msg = f"`{title}` title length is more than 28 chars! Note: a cn char len eq to double en char len."
                raise LengthError(msg)

def refference_modify():
    """add <br> in refference line, the last char except \n.
    """
    docs_sub = os.listdir("./docs")
    if "post" in docs_sub:
        shutil.rmtree("./docs/post")
    os.system("cp -r ./post ./docs/")
   
    post_dirs = []
    for string in os.listdir("docs/post"):
        if "." not in string: post_dirs.append(string)
    
    for dirname in post_dirs:

        post_mdfiles = []
        for string in os.listdir(f"docs/post/{dirname}"):
            if string[-3:]==".md": post_mdfiles.append(string)
   
        for mdf in post_mdfiles:
            with open(f"./docs/post/{dirname}/"+mdf, "r") as f:
                text = f.readlines()
   
            if "## 参考文献\n" in text:
                index = text.index("## 参考文献\n")
                for i in range(index, len(text)):
                    if text[i][0] == "[":
                        text[i] = text[i][:-1]+"<br>"+"\n"
   
            with open(f"./docs/post/{dirname}/"+mdf, "w") as f:
                for line in text:
                    f.write(line)

if __name__ == "__main__":
    print("==> Starting blog deployment. (updating ./docs/)")

    title_level_check()
   # title_length_check()
    refference_modify()
    gen_sidebar()
    gen_readme()
    modify_tr_operator()
    first_line_add_br()

    print("==> Done. (./docs/ updated!)\n")
    print("You can use `python preview.py` to preview your post locally.\n")
    print("Use `gd && gc 'update' && gp` commit and push to github in time!!!\n")

