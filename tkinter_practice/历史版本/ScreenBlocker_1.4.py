import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox
from datetime import datetime
import json
import os
import ctypes
import secrets
import string
import webbrowser


# 使用dpi感知，dpi不为1时，tkinter不能正确读取分辨率
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except AttributeError:
    "未能读取到本机DPI"



user32 = ctypes.windll.user32
sw = user32.GetSystemMetrics(0)  # screen_width
sh = user32.GetSystemMetrics(1)  # screen_height
print(" 日志：本机分辨率:" + str(sw) + 'x' + str(sh))  # 调试
ww = int(sw * 0.3)
wh = int(sh * 0.8)


##模块1  读取配置
CONFIG_FILE = "../config.json"  #读取配置

def initConfig():
    if not os.path.exists(CONFIG_FILE):
        config = {
            "launch_count": 0,                  #启动次数，暂未使用
            "EMERGENCY_KEY": "EMRG-2025-7D4F-9A3E-1B8C-5F2A-0C7E",   #恢复密钥
            "CoverState": False,             #读取上次的锁屏状态，False为未锁屏，True为已锁屏
            "PasswordExist": False,
            "PasswordLS": ""             # 设置的密码存到json供读取

        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)

    return loadConfig()

def loadConfig():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def saveConfig(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

config = initConfig()      #读取配置


##模块2

isThisTimeSet = False
isThisTimeUsed = False



#防止多窗口-变量合集
setting_window = None
pwdchange_window = None
pwdSet_window = None
about_window = None



def Cover():
    #控制条件集中
    global isThisTimeUsed   #本次运行是否已开过遮罩：如果开过就不再显示记住密码提示
    #should_continue = True  #是否继续：配合messagebox.askyesno使用

    #拒绝开启遮罩的条件
    if config["PasswordExist"] == False:          #条件1：未设置密码（需修改）
        messagebox.showinfo("提示", "您没有设置密码，请先设置密码！")
        SettingCenter()
        return

    if config["PasswordExist"] == False:
        if config["PasswordLS"] != "5F67UW4357JW54Y89" and isThisTimeSet == False and isThisTimeUsed == False:
            response = messagebox.askyesno("提示", "您上次使用程序时修改了密码，请确保您没有忘记此密码！")  #askyesno
            if response==False:
                return


    # 创建遮罩




    config["PasswordExist"] = True
    saveConfig(config)

    cover = tk.Toplevel()

    #拦截窗口关闭事件：点击X，按Alt+F4，在任务栏右键关闭，都不会有反应
    cover.protocol("WM_DELETE_WINDOW", lambda: None)



    tk.Label(cover, text="您的屏幕已被\"健康使用电脑\"锁定，请输入密码以解锁",
             relief="solid", width=100, height=8, borderwidth=2,
             font=("HarmonyOS sans SC", 17)).pack(side="top", padx=10, pady=60)

    tk.Label(cover, text="输入密码解除遮罩").pack(side="top", padx=5, pady=5)
    isThisTimeUsed = True

    pwdIn1 = tk.StringVar()
    entry = tk.Entry(cover, textvariable=pwdIn1, show="*")
    entry.pack(side="top", padx=5, pady=5)

    def pwdQuit():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now + " 日志：用户点击了确认按钮，密码是：" + pwdIn1.get())

        global isNowSet

        pwdQuit = pwdIn1.get()

        if not pwdQuit:
            messagebox.showerror("您不能退出", "您的密码不能为空", parent=cover)
            return
        if pwdQuit == config["EMERGENCY_KEY"]:
            messagebox.showinfo("紧急恢复", "您触发了紧急恢复，密码已重置", parent=cover)
            config["PasswordLS"]="5F67UW4357JW54Y89"
            config["PasswordExist"]=False
            isNowSet=False
            saveConfig(config)
            cover.destroy()
            return
        if len(pwdQuit) > 20:
            messagebox.showerror("您不能退出", "您的密码长度超出", parent=cover)
            return
        if pwdQuit == config["PasswordLS"]:
            cover.destroy()
            config["PasswordExist"] = False
            saveConfig(config)
            return
        else:
            messagebox.showerror("您不能退出", "您的密码错误", parent=cover)

    tk.Button(cover, text="确认", command=pwdQuit).pack(side="top", padx=5, pady=5)

    cover.attributes('-fullscreen', True)
    cover.attributes('-topmost', True)
    cover.overrideredirect(True)

    cover.grab_set()  # 模态
    cover.wait_window()


def SettingCenter():

    isPwdRight = False

    #防止窗口打开多例
    global setting_window
    if setting_window and setting_window.winfo_exists():
        return

    def Setting():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now + " 日志：用户打开-设置")



        def pwdchange():
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now + " 日志：用户请求-修改密码")

            global pwdchange_window
            if pwdchange_window and pwdchange_window.winfo_exists():
                return

            def changepwd1():
                global pwd

                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(now + " 日志：用户确认了密码（未检查）")

                pwdOld = entry1.get()
                pwdA = entry2.get()
                pwdB = entry3.get()

                if not pwdA or not pwdB or not pwdOld:
                    messagebox.showerror("设置失败", "您有至少一个字段未填写", parent=pwdchange)
                    return
                if pwdOld != config["PasswordLS"] and pwdOld != config["EMERGENCY_KEY"]:
                    messagebox.showerror("设置失败", "您的原密码错误", parent=pwdchange)
                    return
                if len(pwdA) > 20 or len(pwdB) > 20 or len(pwdOld) > 20 and pwdOld != config["EMERGENCY_KEY"]:
                    messagebox.showerror("设置失败", "您的密码长度超出，请设置不多于20位字符的密码", parent=pwdchange)
                    return


                if pwdA == pwdB:
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(now + " 日志：设置密码成功：" + pwdA)
                    messagebox.showinfo("设置密码", "密码设置成功", parent=pwdchange)
                    pwd = pwdA
                    config["isPwdSet"] = True
                    config["PasswordLS"] = pwdA
                    saveConfig(config)
                    isThisTimeSet = True
                    # loadConfig()
                    pwdchange.destroy()
                    setting2.destroy()

                else:
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(now + " 日志：设置密码失败：一次：" + pwdA + " 二次：" + pwdB)
                    messagebox.showerror("设置失败", "您输入的两次密码不同", parent=pwdchange)

            pwdchange = tk.Toplevel()
            pwdchange_window = pwdchange
            pwdchange.title("修改密码")
            pwdchange.geometry(f"{ww}x{wh}+{int(sw / 2 - ww / 2)}+{int((sh // 2) * 0.9 - wh // 2)}")
            tk.Label(pwdchange, text="请输入原密码（可使用恢复密钥）", width=70).pack(side="top", padx=5, pady=5)
            entry1 = tk.Entry(pwdchange)
            entry1.pack(side="top", padx=5, pady=5)
            tk.Label(pwdchange, text="请输入新密码", width=70).pack(side="top", padx=5, pady=5)
            entry2 = tk.Entry(pwdchange)
            entry2.pack(side="top", padx=5, pady=5)
            tk.Label(pwdchange, text="再次确认密码", width=70).pack(side="top", padx=5, pady=5)
            entry3 = tk.Entry(pwdchange)
            entry3.pack(side="top", padx=5, pady=5)
            tk.Button(pwdchange, text="确认", command=changepwd1).pack()
            tk.Button(pwdchange, text="取消", command=pwdchange.destroy).pack(side="left", anchor="sw", padx=10, pady=10)

        def pwdSet():
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now + " 日志：用户请求-设置新密码")

            global pwdSet_window
            if pwdSet_window and pwdSet_window.winfo_exists():
                return

            def setpwd1():

                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(now + " 日志：用户确认了密码（未检查）")

                global pwd
                global isThisTimeSet

                pwdA = entry2.get()
                pwdB = entry3.get()
                if not pwdA or not pwdB:
                    messagebox.showerror("设置失败", "您有至少一个字段未填写", parent=pwdset)
                    return
                if len(pwdA) > 20 or len(pwdB) > 20:
                    messagebox.showerror("设置失败", "您的密码长度超出，请设置不多于20位字符的密码)", parent=pwdset)
                    return

                if pwdA == pwdB:
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(now + " 日志：设置密码成功：" + pwdA)
                    messagebox.showinfo("设置密码", "密码设置成功", parent=pwdset)
                    pwd = pwdA
                    config["isPwdSet"] = True
                    config["PasswordLS"] = pwdA
                    saveConfig(config)
                    isThisTimeSet = True
                    # loadConfig()
                    pwdset.destroy()
                    setting2.destroy()



                else:
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(now + " 日志：设置密码失败：一次：" + pwdA + " 二次：" + pwdB)
                    messagebox.showerror("设置失败", "您输入的两次密码不同", parent=pwdset)
                    return

            pwdset = tk.Toplevel()
            pwdSet_window = pwdset
            pwdset.title("设置密码")
            pwdset.geometry(f"{ww}x{wh}+{int(sw / 2 - ww / 2)}+{int((sh // 2) * 0.9 - wh // 2)}")
            tk.Label(pwdset, text="请输入新密码", width=70).pack(side="top", padx=5, pady=5)
            entry2 = tk.Entry(pwdset)
            entry2.pack(side="top", padx=5, pady=5)
            tk.Label(pwdset, text="再次确认密码", width=70).pack(side="top", padx=5, pady=5)
            entry3 = tk.Entry(pwdset)
            entry3.pack(side="top", padx=5, pady=5)

            tk.Button(pwdset, text="确认", command=setpwd1).pack()
            tk.Button(pwdset, text="取消", command=pwdset.destroy).pack(side="left", anchor="sw", padx=10, pady=10)

            return


        if config["PasswordLS"] == "5F67UW4357JW54Y89":
            messagebox.showinfo("设置密码", "您正在执行首次设置密码", parent=setting2)
            pwdSet()
        else:
            messagebox.showinfo("设置密码", "您正在执行已有密码修改", parent=setting2)
            pwdchange()

        return


    def keyReset():

        global isPwdRight

        def pwdcheck():
            pwd2 = pwdin2.get()

            if pwd2 == config["PasswordLS"]:
                isPwdRight = True
            else:
                messagebox.showerror("验证失败", "您输入的密码错误", parent=keyreset)
                return

            if isPwdRight:
                key = generate_secret_key()
                config["EMERGENCY_KEY"] = key
                saveConfig(config)
                messagebox.showinfo("重置紧急密钥", "紧急密钥已重置：" + key, parent=setting2)
                loadConfig()
                keyreset.destroy()

        if config["PasswordLS"]=="5F67UW4357JW54Y89":
            messagebox.showerror("无法操作", "您未设置密码，不需要操作恢复密钥", parent=setting2)
            return



        keyreset = tk.Toplevel()
        keyreset.title("密码验证")
        keyreset.geometry(f"{ww}x{wh}+{int(sw / 2 - ww / 2)}+{int((sh // 2) * 0.9 - wh // 2)}")
        tk.Label(keyreset, text="验证密码后，方可重置紧急恢复密钥。\n\n\n请输入密码：",
                 width=70).pack(side="top", padx=5,pady=20)
        pwdin2 = tk.StringVar()
        entry4 = tk.Entry(keyreset, textvariable=pwdin2)
        entry4.pack(side="top", padx=5, pady=5)
        tk.Button(keyreset, text="确认", command=pwdcheck).pack()
        tk.Button(keyreset, text="取消", command=keyreset.destroy).pack(side="left", anchor="sw", padx=10, pady=10)

    def about():

        global about_window
        if about_window and about_window.winfo_exists():
            return

        def open_github_link():
            webbrowser.open("https://github.com/JeanValjean/GUI_Study")

        about=tk.Toplevel()
        about_window = about
        about.title("关于")
        about.geometry(f"{ww}x{wh}+{int(sw / 2 - ww / 2)}+{int((sh // 2) * 0.9 - wh // 2)}")
        tk.Label(about, text="关于本程序", width=34, height=6, borderwidth=1,
             font=("HarmonyOS sans SC", 17)).pack(side="top", padx=10, pady=10)
        tk.Label(about, text="本程序为个人项目，无法保证后期支持"
                    "\n\n\n基于Python3.13.5，tkinter GUI"
                    "\n\n\n本程序的源代码已上传至GitHub：https://github.com/JeanValjean/GUI_Study",
                    #"\n\n\n本程序的许可证为MIT许可证。"
                 font=("HarmonyOS sans SC", 9)).pack(side="top", padx=10, pady=10)

        tk.Button(about, text="前往页面", command=open_github_link).pack(side="top", padx=10, pady=10)

        tk.Button(about, text="返回", command=about.destroy).pack(side="left",anchor="sw", padx=10, pady=10)




    setting2 = tk.Toplevel()

    setting_window = setting2  # 记录窗口实例

    setting2.title("设置")
    setting2.geometry(f"{ww}x{wh}+{int(sw / 2 - ww / 2)}+{int((sh // 2) * 0.9 - wh // 2)}")
    tk.Label(setting2, text="设置", width=34, height=6, borderwidth=1,
             font=("HarmonyOS sans SC", 17)).pack(side="top", padx=10, pady=10)
    tk.Button(setting2, text="创建/修改密码", command=Setting).pack()

    tk.Button(setting2, text="重置紧急密钥", command=keyReset).pack()

    tk.Button(setting2, text="关于本程序", command=about).pack()

    tk.Button(setting2, text="返回", bg='#B3E5FC', fg='black',
              activebackground='#81D4FA', activeforeground='black',
              width=60, height=2, font=("HarmonyOS sans SC", 12),
              borderwidth="1", relief="ridge", command=setting2.destroy).pack(side="bottom", padx=5, pady=5)




def generate_secret_key(length=20):
    #设置字符池：大写字母+数字+横杠
    characters = string.ascii_uppercase + string.digits
    # 从 characters 中随机选择 length 个字符
    raw = ''.join(secrets.choice(characters) for _ in range(length))

    key = '-'.join(raw[i:i+4] for i in range(0, len(raw), 4))
    return key


#主窗口
Center = tk.Tk()
Center.title("健康使用电脑")
Center.geometry(f"{ww}x{wh}+{int(sw / 2 - ww / 2)}+{int((sh // 2) * 0.9 - wh // 2)}")
tk.Label(Center, text="欢迎使用\"健康使用电脑\"", width=34, height=6, borderwidth=1,
         font=("HarmonyOS sans SC", 17)).pack(side="top", padx=10, pady=10)

tk.Button(Center, text="启动遮罩", bg='#B3E5FC', fg='black',
          activebackground='#81D4FA', activeforeground='black',
          width=43, height=3, font=("HarmonyOS sans SC", 14),
          borderwidth="1", relief="ridge", command=Cover).pack(side="top", padx=10, pady=0)

tk.Button(Center, text="设置", bg='white', fg='black',command=SettingCenter,).pack(side="left", anchor="sw", padx=10, pady=10)

tk.Button(Center, text="退出", bg='white', fg='black',command=Center.destroy).pack(side="left", anchor="sw", padx=1, pady=10)

if config["PasswordExist"] == True:
    Cover()

# if config["launch_count"] == 0:
# messagebox.showinfo("欢迎使用", "首次启动时需要设置密码")
# Setting()
if config["EMERGENCY_KEY"] == "EMRG-2025-7D4F-9A3E-1B8C-5F2A-0C7E":
    messagebox.showinfo("紧急恢复密钥", "将为您生成紧急恢复密钥，忘记密码时需使用密钥解除锁定，请保存好您的密钥")
    key = generate_secret_key()
    config["EMERGENCY_KEY"] = key
    saveConfig(config)
    messagebox.showinfo("紧急恢复密钥", "您的紧急恢复密钥为：" + key)
    print(key)




if config["PasswordLS"]== "5F67UW4357JW54Y89":
    messagebox.showinfo("欢迎使用", "首次使用时，您需要先设置密码")
    isNowSet = True
    SettingCenter()



config["launch_count"] += 1
saveConfig(config)

Center.mainloop()











