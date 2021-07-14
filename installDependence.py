import os
import re
import pip


def check_configuration(path: str, content: str):
    flag = False
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                if re.match(r' *#', line):
                    continue
                if content in line:
                    flag = True
                    print('yes')
            if not flag:
                print("not write")
    else:
        print("not exist")
    return flag


def add_configuration(path: str, content: str, mode):
    if not check_configuration(path, content):
        with open(path, mode) as f:
            f.write("\n" + content)


def dependence_head(package_list:list):
    if os.path.exists("dependence.txt"):
        os.remove("dependence.txt")
    for i in package_list:
        add_configuration("dependence.txt", i, "a+")
    return os.system("pip install -r dependence.txt")


if __name__ == '__main__':
    """不能用sudo安装"""
    # 一键安装所有pip依赖库
    if os.path.exists("dependence.txt"):
        os.remove("dependence.txt")
    for i in ["numpy", "vtk", "PyQt5"]:
        print(i)
        add_configuration("dependence.txt", i, "a+")
    os.system("pip3 install -r dependence.txt")


