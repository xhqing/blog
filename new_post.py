import os, sys
import time

class TitleError(Exception):
    """TitleError"""

class TitleDuplicated(Exception):
    """Title Duplicated"""

class LengthError(Exception):
    """length too long error"""

def is_cn(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def post_title_stdlen(post_title: str) -> int:

    cn_len = sum(list(map(lambda x: 1 if '\u4e00' <= x <= '\u9fa5' else 0, post_title)))
    return len(post_title) - cn_len + 2*cn_len


def is_en(strs):
    up = "QWERTYUIOPASDFGHJKLZXCVBNM"
    lo = "qwertyuiopasdfghjklzxcvbnm"
    assert len(up) == 26
    assert len(lo) == 26

    is_enf = True
    for s in strs:
        if (s in up) or (s in lo) or (s==" "):
            continue
        else:
            is_enf = False
            break
    return is_enf

# def write_keywords():
#     with open(f"./post/{post_title}.md", "a") as f:
#         f.write("关键词: " + ", ".join(keywords_list) + ".")

def write_createtime(dirname):
    with open(f"./post/{dirname}/{post_title}.md", "w") as f:
        f.write("创建于 " + time.strftime("%Y-%m-%d", time.localtime()) + "\n")

def choose_post_dir():
    post_dirs = []
    for string in os.listdir("post"): 
        if "." not in string: post_dirs.append(string)
    
    msg = f"请问您想将此博文放到以下哪个栏目?\n"
    for i in range(len(post_dirs)):
        msg += f"{i}. {post_dirs[i]}\n"
    # msg = msg[:-2] + "\n"
    msg += "请输入相应的栏目序号或输入'q'退出, 并按回车确定: "
    ans = input(msg)
    if ans=="q":
        sys.exit(0)
    return post_dirs[int(ans)]

if __name__ == "__main__":
    try:
        post_title = sys.argv[1]
    except IndexError:
        raise TitleError(f"""\033[01;31;01m no title, `python new_post.py your_post_title`\033[01;31;01m""")

    if post_title[-3:]==".md": 
        raise TitleError(f"""\033[01;31;01m use `{post_title[:-3]}` as post title instead.`\033[01;31;01m""")
    
    dirname = choose_post_dir()
    post_mdfiles = os.listdir(f"./post/{dirname}")
    if f"{post_title}.md" in post_mdfiles:
        raise TitleDuplicated(f"""\033[01;31;01m {post_title}.md has already exist in ./post/{dirname}, please choose another one. \033[01;31;01m""")

    # if post_title_stdlen(post_title) > 28:
    #    msg = "title length is more than 28 chars! Note: a cn char len eq to double en char len."
    #    raise LengthError(msg)

    os.system(f"touch post/{dirname}/{post_title}.md")
    
    write_createtime(dirname)
    with open(f"./post/{dirname}/{post_title}.md", "a") as f:
        f.write("关键词: ")
    
    os.system(f"open ./post/{dirname}/{post_title}.md")
