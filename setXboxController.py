import os
# Press the green button in the gutter to run the script.

def check_Xbox_configuration(path="/etc/modprobe.d/"):
    path = path + "bluetooth.conf"
    flag = False
    if os.path.exists(path):
        with open(path, "r") as f:
            info = f.read()
            if 'options bluetooth disable_ertm=Y' in info:
                flag =True
                print("yes")
            else:
                print("not write")
    else:
        print("not exist")
    return flag


def set_up_Xbox_controllers(path="/etc/modprobe.d/"):
    if not check_Xbox_configuration(path):
        with open(path + "bluetooth.conf", "w") as f:
            f.write('options bluetooth disable_ertm=Y')


if __name__ == '__main__':
    set_up_Xbox_controllers("")
    check_Xbox_configuration("")

