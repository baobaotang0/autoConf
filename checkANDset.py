import os
import re


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


def change_static_ip(path: str, ip_address: str):
    key_words_list = ["interface eth0", "static ip_address", "static routers", "static domian_name_servers"]
    if check_configuration(path, key_words_list[0]):
        content = ""
        in_key_part = False
        with open(path, "r") as f:
            for line in f:
                if re.match(r' *#', line):
                    continue
                if key_words_list[0] in line:
                    in_key_part = True
                elif in_key_part:
                    if not any([i in line for i in key_words_list[1:]]):
                        in_key_part = False
                        content += line
                else:
                    content += line
        with open(path, "w") as f:
            f.write(content + "\ninterface eth0\nstatic ip_address=" + ip_address + "/24")

    else:
        with open(path, "+a") as f:
            f.write("\ninterface eth0\nstatic ip_address=" + ip_address + "/24")


def system_is_raspberry():
    val = os.popen("cat /etc/issue")
    for i in val.readlines():
        if "Raspbian" in i or "Raspberry Pi OS" in i:
            return True
    return False


if __name__ == '__main__':
    if system_is_raspberry():
        # 链接手柄：树莓派关闭蓝牙增强重传模式
        print("Xbox controller")
        add_configuration("/etc/modprobe.d/bluetooth.conf", 'options bluetooth disable_ertm=Y', "w")
        # 连接odrive：需要打一段代码
        print("odrive")
        add_configuration("/etc/udev/rules.d/91-odrive.rules",
                          'SUBSYSTEM=="usb", ATTR{idVendor}=="1209", ATTR{idProduct}=="0d[0-9][0-9]", MODE="0666"', "w")
        os.system("udevadm control --reload-rules")
        os.system("udevadm trigger")
        # 连接stm32通信：开gpio 8  9 （两根针一个串口）
        print("stm32")
        add_configuration("/boot/config.txt", "dtoverlay=uart4", "a+")
        # 有线网卡配置静态ip - ip怎么配去雷达库readme - 以后树莓派会有两块网卡，留好位置
        print("static ip")
        change_static_ip("/etc/dhcpcd.conf", "10.10.10.100")
        # 计算模块打开usb
        print("usb")
        add_configuration("/boot/config.txt", "dtoverlay=dwc2,dr_mode=host", "a+")
        # 一键安装所有pip依赖库
        print("numpy")
        add_configuration("dependence.txt", "numpy", "a+")
        print("pysdl2")
        add_configuration("dependence.txt", "PySDL2", "a+")
        os.system("pip install -r dependence.txt")
