
import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox
from datetime import datetime
import json
import os
import ctypes



#使用dpi感知，dpi不为1时，tkinter不能正确读取分辨率
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except AttributeError:"未能读取到本机DPI"

user32 = ctypes.windll.user32
sw=user32.GetSystemMetrics(0)   #screen_width
sh=user32.GetSystemMetrics(1)  #screen_height
print(" 日志：本机分辨率:"+str(sw)+'x'+str(sh))  #调试
ww=int(sw*0.3)
wh=int(sh*0.8)



CONFIG_FILE = "../config.json"

def initConfig():
    if not os.path.exists(CONFIG_FILE):
        config = {
            "launch_count":0,
            "EMERGENCY_KEY": "EMRG-2025-7D4F-9A3E-1B8C-5F2A-0C7E",
            "pwdLastSave":"5F67UW4357JW54Y89",
            "isPwdSet":False,

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



#主程序-开始
config=initConfig()

isThisTimeSet = False
isNowSet = False
isThisTimeUsed = False



def Cover():

    #控制条件集中放置
    global isThisTimeUsed   #是否已经开启过遮罩：如果开启过就不再显示记住密码提示
    should_continue = True  #是否继续：配合messagebox.askyesno使用

    #拒绝开启遮罩的条件
    if config["pwdLastSave"] == "5F67UW4357JW54Y89":
        messagebox.showinfo("提示", "您没有设置密码，请先设置密码！")
        return

    if config["pwdLastSave"] != "5F67UW4357JW54Y89" and isThisTimeSet==False and isThisTimeUsed==False:
        #messagebox.showinfo("提示", "您上次使用程序时修改了密码，请确保您没有忘记此密码！")
        response = messagebox.askyesno("提示","您上次使用程序时修改了密码，请确保您没有忘记此密码！")
        if not response:
            should_continue = False
            if not should_continue:
                return


    #创建遮罩
    cover = tk.Toplevel()

    tk.Label(cover, text="您的屏幕已被\"健康使用电脑\"锁定，请输入密码以解锁",
             relief="solid",width=100, height=8, borderwidth=2,
                 font=("HarmonyOS sans SC", 17)).pack(side="top",padx=10, pady=60)

    tk.Label(cover, text="输入密码解除遮罩").pack(side="top",padx=5, pady=5)
    isThisTimeUsed=True

    pwdIn1=tk.StringVar()
    entry=tk.Entry(cover,textvariable=pwdIn1,show="*")
    entry.pack(side="top",padx=5, pady=5)

    def pwdQuit():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print( now + " 日志：用户点击了确认按钮，密码是：" + pwdIn1.get())
        pwdQuit=pwdIn1.get()

        if not pwdQuit:
            messagebox.showerror("您不能退出", "您的密码不能为空",parent=cover)
            return
        if pwdQuit == config["EMERGENCY_KEY"]:
            messagebox.showinfo("紧急逃生", "您触发了紧急逃生", parent=cover)
            cover.destroy()
            return
        if len(pwdQuit) > 20:
            messagebox.showerror("您不能退出", "您的密码长度超出",parent=cover)
            return
        if pwdQuit==config["pwdLastSave"]:
            cover.destroy()
            return
        else:
            messagebox.showerror("您不能退出", "您的密码错误",parent=cover)


    tk.Button(cover, text="确认",command=pwdQuit).pack(side="top",padx=5, pady=5)




    cover.attributes('-fullscreen', True)
    cover.attributes('-topmost', True)
    cover.overrideredirect(True)

    cover.grab_set()  # 模态
    cover.wait_window()








def Setting2():
    def Setting():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now + " 日志：用户打开-设置")

        def pwdchange():
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now + " 日志：用户请求-修改密码")

            def changepwd1():
                global pwd

                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(now + " 日志：用户确认了密码（未检查）")


                pwdOld =entry1.get()
                pwdA = entry2.get()
                pwdB = entry3.get()

                if not pwdA or not pwdB or not pwdOld:
                    messagebox.showerror("设置失败", "您有至少一个字段未填写", parent=pwdchange)
                    return
                if len(pwdA) > 20 or len(pwdB) > 20 or len(pwdOld) > 20:
                    messagebox.showerror("设置失败", "您的密码长度超出，请设置不多于20位字符的密码", parent=pwdchange)
                    return
                if pwdOld != config["pwdLastSave"]:
                    messagebox.showerror("设置失败", "您的原密码错误", parent=pwdchange)
                    return

                if pwdA == pwdB:
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(now + " 日志：设置密码成功：" + pwdA)
                    messagebox.showinfo("设置密码", "密码设置成功", parent=pwdchange)
                    pwd = pwdA
                    config["isPwdSet"] = True
                    config["pwdLastSave"] = pwdA
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
            pwdchange.title("修改密码")
            pwdchange.geometry(f"{ww}x{wh}+{int(sw / 2 - ww / 2)}+{int((sh // 2) * 0.9 - wh // 2)}")
            tk.Label(pwdchange, text="请输入原密码", width=70).pack(side="top", padx=5, pady=5)
            entry1 = tk.Entry(pwdchange)
            entry1.pack(side="top", padx=5, pady=5)
            tk.Label(pwdchange, text="请输入新密码", width=70).pack(side="top", padx=5, pady=5)
            entry2 = tk.Entry(pwdchange)
            entry2.pack(side="top", padx=5, pady=5)
            tk.Label(pwdchange, text="再次确认密码", width=70).pack(side="top", padx=5, pady=5)
            entry3 = tk.Entry(pwdchange)
            entry3.pack(side="top", padx=5, pady=5)
            tk.Button(pwdchange, text="确认", command=changepwd1).pack()


        def pwdSet():
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now + " 日志：用户请求-设置新密码")


            def setpwd1():
                global pwd
                global isThisTimeSet
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(now + " 日志：用户确认了密码（未检查）")

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
                    config["pwdLastSave"] = pwdA
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
            pwdset.title("设置密码")
            pwdset.geometry(f"{ww}x{wh}+{int(sw / 2 - ww / 2)}+{int((sh // 2) * 0.9 - wh // 2)}")
            tk.Label(pwdset, text="请输入新密码", width=70).pack(side="top", padx=5, pady=5)
            entry2 = tk.Entry(pwdset)
            entry2.pack(side="top", padx=5, pady=5)
            tk.Label(pwdset, text="再次确认密码", width=70).pack(side="top", padx=5, pady=5)
            entry3 = tk.Entry(pwdset)
            entry3.pack(side="top", padx=5, pady=5)


            
            tk.Button(pwdset, text="确认", command=setpwd1).pack()

            return




        if not config["isPwdSet"]:
            #messagebox.showinfo("设置密码", "您正在执行首次设置密码", parent=setting)
            pwdSet()
        else:
            messagebox.showinfo("设置密码", "您正在执行已有密码修改", parent=setting2)
            pwdchange()


        return


    if isNowSet==True:
        Setting()


    setting2 = tk.Toplevel()
    setting2.title("设置")
    setting2.geometry(f"{ww}x{wh}+{int(sw / 2 - ww / 2)}+{int((sh // 2) * 0.9 - wh // 2)}")
    tk.Label(setting2, text="设置",width=34, height=6, borderwidth=1,
                 font=("HarmonyOS sans SC", 17)).pack(side="top",padx=10, pady=10)
    tk.Button(setting2, text="创建/修改密码", command=Setting).pack()
    tk.Button(setting2, text="返回",bg='#B3E5FC', fg='black',
         activebackground='#81D4FA',activeforeground='black',
        width=60, height=2, font=("HarmonyOS sans SC", 12),
        borderwidth="1",relief="ridge",command=setting2.destroy).pack(side="bottom", padx=5, pady=5)
















Center=tk.Tk()
Center.title("健康使用电脑")
Center.geometry(f"{ww}x{wh}+{int(sw/2-ww/2)}+{int((sh//2)*0.9-wh//2)}")
tk.Label(Center, text="欢迎使用\"健康使用电脑\"", width=34, height=6, borderwidth=1,
                 font=("HarmonyOS sans SC", 17)).pack(side="top",padx=10, pady=10)


tk.Button(Center, text="启动遮罩", bg='#B3E5FC', fg='black',
         activebackground='#81D4FA',activeforeground='black',
        width=43, height=3, font=("HarmonyOS sans SC", 14),
        borderwidth="1",relief="ridge",command=Cover).pack(side="top",padx=10, pady=0)


tk.Button(Center, text="设置", bg='white', fg='black',
          command=Setting2,
          ).pack(side="left",anchor="sw",padx=10, pady=10)



#if config["launch_count"] == 0:
    #messagebox.showinfo("欢迎使用", "首次启动时需要设置密码")
    #Setting()

if config["isPwdSet"] == False:
    messagebox.showerror("欢迎使用", "您需要先设置密码")
    isNowSet = True
    Setting2()



config["launch_count"] += 1
saveConfig(config)




Center.mainloop()











