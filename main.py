import base64
import os
import tkinter as tk
from subprocess import Popen
from tkinter import messagebox, filedialog
from win32api import GetFileVersionInfo
import json
from logo import LogoBase64

# 创建主窗口
root = tk.Tk()
root.title("sf登陆器")
with open('tmp.ico', 'wb') as tmp:
    tmp.write(base64.b64decode(LogoBase64))
root.wm_iconbitmap('tmp.ico')
os.remove('tmp.ico')
root.geometry("300x80")
root.resizable(False, False)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

config_path = './sf.conf'
file_name = 'aa.exe'


# 点击事件回调函数
def on_button_click(the_type):
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            f.write(json.dumps([]))
        # 创建新文件

        # file_path = filedialog.askopenfilename(title=title, filetypes=[("Executables", "wow.exe")])
        # version = ''
        # if file_path:
        #     version = show_file_info(file_path)
        # if len(version) == 0:
        #     messagebox.showerror("错误", f"无法读取文件版本信息")
        #     return
    data = json.load(open(config_path, encoding="utf-8-sig"))
    path = ''
    for i in data:
        if i['type'] == the_type:
            path = i['file']
    if len(path) == 0:
        path = init_config(the_type)
    if len(path) == 0:
        return
    directory = os.path.dirname(path)
    if the_type == '3.3.5':
        realmlist = directory + '/realmlist.wtf'
    else:
        realmlist = directory + '/data/zhcn/realmlist.wtf'
    with open(realmlist, 'w') as f:
        f.write('set realmlist cn-logon.stormforge.gg')
    f.close()
    Popen([path])
    root.iconify()
    # 显示文件信息


def init_config(the_type):
    file_path = filedialog.askopenfilename(title=f'请选择{the_type}的{file_name}',
                                           filetypes=[("Executables", "wow.exe")])
    if len(file_path) == 0:
        return ''
    version = show_file_info(file_path)
    if len(version) <= 0:
        messagebox.showerror("错误", f"无法读取文件版本信息")
        return ''
    # 在版本中查找 the_type的关键字
    if version.find(the_type) == -1:
        messagebox.showerror("错误", f"文件版本{version}和版本{the_type}不匹配")
        return ''
    config_data = json.load(open(config_path, encoding="utf-8-sig"))
    config_data.append({'type': the_type, 'file': file_path})
    with open(config_path, 'w') as f:
        # 转换成 json 写入
        json.dump(config_data, f, indent=4)
    f.close()
    return file_path


def show_file_info(file_path):
    try:
        # 获取文件版本信息
        info = GetFileVersionInfo(file_path, '\\')
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
        return version
    except Exception as e:
        # messagebox.showerror("错误", f"无法读取文件信息: {str(e)}")
        return '无法读取文件信息'


# 创建按钮
button1 = tk.Button(root, text="243亚洲", command=lambda: on_button_click('2.4.3'))
button2 = tk.Button(root, text="335亚洲", command=lambda: on_button_click('3.3.5'))

# 使用 grid 布局将按钮并排放置
button1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
button2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# 运行主循环
root.mainloop()
