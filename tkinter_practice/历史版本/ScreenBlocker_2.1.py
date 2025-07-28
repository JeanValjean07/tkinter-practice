import sys
import tkinter as tk
from doctest import master
from idlelib.help import HelpParser
from tkinter import Toplevel
from tkinter import messagebox
from datetime import datetime
import json
import os
import time
import ctypes
import secrets
import string
import webbrowser
import threading
from xmlrpc.client import boolean
import psutil
import win32gui
import win32con

#多开线程
def taskmgr2():
    while True:
        def enum_func(hwnd, _):
            try:
                if win32gui.GetClassName(hwnd) == 'TaskManagerWindow':
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            except pywintypes.error:
                pass
        win32gui.EnumWindows(enum_func, None)
        time.sleep(1)


taskmgr_threading = threading.Thread(target=taskmgr2, daemon=True)
taskmgr_threading.start()



#配置
CONFIG_FILE = "../config.json"  #读取配置
def initConfig():
    if not os.path.exists(CONFIG_FILE):
        config = {
            "launch_count": 0,
            "EMERGENCY_KEY": "",
            "CoverState": False,
            "PasswordLS": ""
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

#变量集



#解密
decryptedPwd=""

#读DPI
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except AttributeError:
    "未能读取到本机DPI"
user32 = ctypes.windll.user32



class WindowGeo:

    def __init__(self, window):
        self.window = window
        self.native_launch_count = 0
        self.sw = 0
        self.sh = 0
        self.ww = 0
        self.wh = 0

    def PreProcessScreen(self):
        self.sw = user32.GetSystemMetrics(0)  # screen_width
        self.sh = user32.GetSystemMetrics(1)  # screen_height
        self.ww = int((self.sw) * 0.3)
        self.wh = int((self.sh) * 0.8)
        #print(" 预处理程序：本机分辨率:" + str(self.sw) + 'x' + str(self.sh))  # 调试
        return self.ww, self.wh

    def Style1(self):
        if self.native_launch_count == 0:
            self.PreProcessScreen()
            self.native_launch_count += 1

        self.window.geometry(f"{self.ww}x{self.wh}+{int((self.sw // 2)*0.98 - self.ww // 2)}+{int((self.sh // 2) * 0.92 - self.wh // 2)}")


    def Style2(self):
        self.window.attributes('-topmost', True)
        self.window.attributes('-fullscreen', True)
        self.window.overrideredirect(True)
        self.window.configure(bg='white')

    def Style3(self):
        self.window.attributes('-topmost', True)
        self.window.attributes('-fullscreen', True)
        self.window.overrideredirect(True)
        self.window.configure(bg='white')



class Cover:
    def __init__(self):
        self.pwd = ""
        self.inputPwdQ = tk.StringVar()
        self.inputPwdF = tk.StringVar()
        self.coverTSKExist=False

    def checkPasswordSet(self):

        if config["PasswordLS"] == "":
            messagebox.showerror("提示","请先设置密码")
            return False
        return True
    def coverStateSet(self,motion):
        global coverstate
        if motion=="true":
            config["CoverState"]=True
            saveConfig(config)
        else:
            config["CoverState"] = False
            saveConfig(config)

    def switchCoverStyle1(self):
        self.cover.lift()
    def switchCoverTSK(self):
        if self.coverTSKExist==False:
            self.coverStyleTSK()
        self.coverTSK.lift()

    def coverStyle1(self):

        if not self.checkPasswordSet():
            return
        self.coverStateSet("true")

        self.cover = tk.Toplevel()
        window=WindowGeo(self.cover)
        window.Style2()
        self.cover.protocol("WM_DELETE_WINDOW", lambda: None)
        self.cover.lift()

        tk.Label(self.cover, text="您的屏幕已被\"健康使用电脑\"锁定，请输入密码以解锁",
                 relief="solid", width=100, height=8, borderwidth=2,
                 font=("HarmonyOS sans SC", 17)).pack(side="top", pady=60)

        tk.Label(self.cover, text="输入密码以解锁",bg="white").pack(side="top")

        entryQ = tk.Entry(self.cover, textvariable=self.inputPwdQ, show="*")
        entryQ.pack(side="top", padx=5, pady=5)
        entryQ.focus_set()

        tk.Button(self.cover, text="确定", command=self.quitByPwd).pack(side="top", padx=10,pady=10)

        tk.Button(self.cover, text="使用时空密令解锁", command=self.switchCoverTSK).pack(side="left", anchor="sw", padx=10,pady=10)
    def coverStyleTSK(self):

        self.coverTSKExist = True

        self.coverTSK=tk.Toplevel()
        window = WindowGeo(self.coverTSK)
        window.Style2()
        self.coverTSK.protocol("WM_DELETE_WINDOW", lambda: None)
        self.cover.lift()

        tk.Label(self.coverTSK, text="使用时空密令解锁\n\n\n(时空密令是一种基于当前时间，日期，经纬度，天气等因素计算得出的密码。使用时空密令的前提是您已知晓其计算公式)",
                 relief="solid", width=100, height=8, borderwidth=2,
                 font=("HarmonyOS sans SC", 16)).pack(side="top", pady=60)

        tk.Label(self.coverTSK, text="输入时空密令以解锁", bg="white").pack(side="top")

        entryF = tk.Entry(self.coverTSK, textvariable=self.inputPwdF, show="*")
        entryF.pack(side="top", padx=5, pady=5)
        entryF.focus_set()

        tk.Button(self.coverTSK, text="确定", command=self.quitByTSK).pack(side="top", padx=10, pady=10)

        tk.Button(self.coverTSK, text="返回使用密码解锁", command=self.switchCoverStyle1).pack(side="left", anchor="sw", padx=10, pady=10)

    def quitByTSK(self):
        inputpwd = self.inputPwdF.get()

        if inputpwd == "1145141919810":

            print(" 用户触发了\"哼啊啊啊\"解锁")
            self.cover.destroy()
            self.coverTSK.destroy()
            self.coverStateSet("114")
            messagebox.showinfo("恶臭", "哼，啊啊，啊啊啊啊啊啊啊啊啊啊啊啊啊")
            return

        if inputpwd == decryptedPwd:
            time.sleep(0.2)
            self.cover.destroy()
            self.coverTSK.destroy()
            self.coverStateSet("114")
            return
        if len(inputpwd) >= 12:
            messagebox.showerror("您不能退出", "您的输入长度超出", parent=self.coverTSK)
            self.inputPwdF.set('')
            return
        if inputpwd == "":
            messagebox.showerror("您不能退出", "密码不能为空", parent=self.coverTSK)
            return
        if inputpwd != self.pwd:
            messagebox.showerror("您不能退出", "您的密码错误", parent=self.coverTSK)
            self.inputPwdF.set('')
            return
    def quitByPwd(self):
        inputpwd = self.inputPwdQ.get()

        if inputpwd == config["EMERGENCY_KEY"]:
            if config["EMERGENCY_KEY"] == "":
                messagebox.showerror("您不能退出","您的密码不能为空" ,parent=self.cover)
                return
            messagebox.showinfo("紧急恢复","您触发了紧急恢复，您的密码将被删除" ,parent=self.cover)
            self.coverStateSet("False")
            print(" 用户触发了紧急恢复")
            config["PasswordLS"] = ""
            saveConfig(config)
            loadConfig()
            self.cover.destroy()
            return

        if inputpwd == decryptedPwd:
            time.sleep(0.2)
            if self.coverTSKExist==True:
                self.coverTSK.destroy()
                self.coverTSKExist=False
            self.coverStateSet("114")
            self.cover.destroy()
            return
        if len(inputpwd) >=12:
            messagebox.showerror("您不能退出", "您的输入长度超出",parent=self.cover)
            self.inputPwdQ.set('')
            return
        if inputpwd == "":
            messagebox.showerror("您不能退出", "密码不能为空",parent=self.cover)
            return
        if inputpwd != self.pwd:
            messagebox.showerror("您不能退出", "您的密码错误",parent=self.cover)
            self.inputPwdQ.set('')
            return



class Password:
    def __init__(self):
        self.pwdsetOn=False
        self.emkeysetOn=False
        self.SetOrChange = False
    def close(self,name):
        if name == "pwdset":
            self.pwdsetOn = False
            self.pwdset.destroy()
        if name == "emkeyset":
            self.emkeysetOn = False
            self.emkeyset.destroy()

    def PwdSecrete(self):
        global decryptedPwd
        decryptedPwd = self.RawPwd
        print("原始密码"+self.RawPwd)
        encrypted_pwd = ""
        for char in self.RawPwd:
            # 将每个字符的 ASCII 码加 2
            encrypted_char = chr(ord(char) + 2)
            encrypted_pwd += encrypted_char
        print("加密后的密码", encrypted_pwd)
        config["PasswordLS"] = encrypted_pwd
        saveConfig(config)
        loadConfig()
    def PwdSetCheck(self):
        if self.SetOrChange == False:
            pwdOld = self.pwdOld.get()
            pwdNew1 = self.pwdNew1.get()
            pwdNew2 = self.pwdNew2.get()
            if pwdOld == decryptedPwd:
                if len(pwdOld)>12 or len(pwdNew1)>12 or len(pwdNew2)>12:
                    messagebox.showerror("密码修改失败", "密码不能超过12位",parent=self.pwdset)
                    return
                if pwdNew1 == "":
                    messagebox.showerror("密码修改失败", "新密码不能为空",parent=self.pwdset)
                    return
                if pwdNew1 == pwdNew2:
                    self.RawPwd = pwdNew1
                    messagebox.showinfo("密码修改成功", "您的密码已成功修改",parent=self.pwdset)
                    self.PwdSecrete()
                    self.pwdsetOn=False
                    self.pwdset.destroy()
                else:
                    messagebox.showerror("密码修改失败", "两次输入密码不一致",parent=self.pwdset)
            else:
                messagebox.showerror("密码修改失败", "您的原密码错误",parent=self.pwdset)
        if self.SetOrChange == True:
            pwdNew1 = self.pwdNew1.get()
            pwdNew2 = self.pwdNew2.get()
            if len(pwdNew1) > 12 or len(pwdNew2) > 12:
                messagebox.showerror("密码修改失败", "密码不能超过12位", parent=self.pwdset)
                return
            if pwdNew1 == "":
                messagebox.showerror("密码设置失败", "新密码不能为空",parent=self.pwdset)
                return
            if pwdNew1 == pwdNew2:
                self.RawPwd = pwdNew1
                messagebox.showinfo("密码设置成功", "您的密码已成功修改",parent=self.pwdset)
                self.PwdSecrete()
                self.pwdsetOn=False
                self.pwdset.destroy()
            else:
                messagebox.showerror("密码设置失败", "两次输入密码不一致",parent=self.pwdset)
    def pwdSet(self):
        if self.pwdsetOn:
            self.pwdset.lift()
            return
        else:
            self.pwdsetOn=True

        self.pwdset=tk.Toplevel(bg="white")
        window = WindowGeo(self.pwdset)
        window.Style1()
        self.pwdset.title("密码管理")
        self.pwdset.protocol("WM_DELETE_WINDOW", lambda: self.close("pwdset"))
        self.pwdset.grab_set()

        if config["PasswordLS"]=="":
            self.SetOrChange=True
            tk.Label(self.pwdset, text="您目前没有密码，请在此设置密码：",bg="white",height=5,width=60,relief="solid", borderwidth=1,
                 font=("宋体", 12)).pack(side="top", pady=5,padx=5)
        else:
            self.SetOrChange=False

            tk.Label(self.pwdset, text="您已设置密码，正在执行密码修改程序：",bg="white", height=5, width=60, relief="solid", borderwidth=1,
                     font=("宋体", 12)).pack(side="top", pady=5, padx=5)

            tk.Label(self.pwdset, text="输入原密码：",bg="white").pack(side="top", pady=3)
            self.pwdOld = tk.StringVar()
            entry1 = tk.Entry(self.pwdset, textvariable=self.pwdOld)
            entry1.pack(side="top", padx=5, pady=5)
            entry1.focus_set()

        self.pwdNew1 = tk.StringVar()
        tk.Label(self.pwdset, text="输入新密码：",bg="white").pack(side="top", pady=3)
        entry2 = tk.Entry(self.pwdset, textvariable=self.pwdNew1)
        entry2.pack(side="top", padx=5, pady=5)
        if config["PasswordLS"]=="":
            entry2.focus_set()
        self.pwdNew2 = tk.StringVar()
        tk.Label(self.pwdset, text="再次确认新密码：",bg="white").pack(side="top", pady=3)
        entry3 = tk.Entry(self.pwdset, textvariable=self.pwdNew2)
        entry3.pack(side="top", padx=5, pady=5)
        tk.Button(self.pwdset, text="确定", command=self.PwdSetCheck).pack(side="top", padx=10, pady=10)
    def EmKeySet(self):

        def PwdQuestClose():
            self.emkeysetOn=False
            self.emkeyset.destroy()
            self.pwdquest.destroy()
        def PwdQuest():
            self.pwdquest=tk.Toplevel(bg="white")
            window4 = WindowGeo(self.pwdquest)
            window4.Style1()
            self.pwdquest.grab_set()
            self.pwdquest.title("密码验证")
            self.pwdquest.grab_set()
            self.pwdquest.protocol("WM_DELETE_WINDOW", lambda: PwdQuestClose())
            self.pwdquest.lift()
            tk.Label(self.pwdquest, text="验证密码后，可对恢复密钥进行管理", height="3",bg="white").pack(side="top", pady=3)
            tk.Label(self.pwdquest, text="请输入您的密码：",bg="white").pack(side="top", pady=3)
            pwdquestPwd = tk.StringVar()
            entryP = tk.Entry(self.pwdquest, textvariable=pwdquestPwd)
            entryP.pack(side="top", padx=5, pady=5)
            entryP.focus_set()
            tk.Button(self.pwdquest, text="确认", command=lambda:PwdQuestCheck()).pack(side="top", padx=10, pady=10)

            def PwdQuestCheck():
                if pwdquestPwd.get() == decryptedPwd:
                    messagebox.showinfo("提示","您即将进入恢复密钥管理页面，请妥善保存您的恢复密钥",parent=self.pwdquest)
                    self.pwdquest.destroy()
                    self.emkeysetOn=True
                    self.emkeyset.lift()
                    self.emkeyset.grab_set()
                    return
                else:
                    messagebox.showerror("密码错误", "您的密码错误，将退回到设置",parent=self.pwdquest)
                    self.pwdquest.destroy()
                    self.emkeysetOn = False
                    self.emkeyset.destroy()
                    return
        def EmKey(type=""):

            if type == "delete":
                config["EMERGENCY_KEY"] = ""
                saveConfig(config)
                loadConfig()
                messagebox.showinfo("删除密钥", "您的密钥已置空", parent=self.emkeyset)
                self.emkeysetOn = False
                self.emkeyset.destroy()
                return

            if type == "create" or type == "reset":
                characters = string.ascii_uppercase + string.digits
                raw = ''.join(secrets.choice(characters) for _ in range(20))
                key = '-'.join(raw[i:i + 4] for i in range(0, len(raw), 4))
                config["EMERGENCY_KEY"] = key
                saveConfig(config)
                if type == "create":
                    messagebox.showinfo("生成密钥", "您的恢复密钥是：" + key + "\n请务必牢记此密钥", parent=self.emkeyset)
                if type == "reset":
                    messagebox.showinfo("重置密钥", "您的恢复密钥是：" + key + "\n请务必牢记此密钥", parent=self.emkeyset)
            loadConfig()
            self.emkeysetOn = False
            self.emkeyset.destroy()
            return key

        if self.emkeysetOn:
            self.emkeyset.lift()
            return
        else:
            self.emkeysetOn = True

        def check():
            global decryptedPwd
            if decryptedPwd=="":
                messagebox.showerror("无法管理恢复密钥", "您需要先设置密码，才能管理恢复密钥",parent=self.emkeyset)
                self.emkeysetOn = False
                self.emkeyset.destroy()
                return False
            return True

        self.emkeyset=tk.Toplevel(bg="white")
        window3=WindowGeo(self.emkeyset)
        window3.Style1()
        self.emkeyset.title("恢复密钥管理")
        self.emkeyset.protocol("WM_DELETE_WINDOW", lambda: self.close("emkeyset"))

        tk.Label(self.emkeyset, text="恢复密钥", bg="white", width=34, height=6, borderwidth=1,
                    font=("宋体", 17)).pack(side="top", padx=10, pady=10)
        tk.Label(self.emkeyset, text="恢复密钥是一种忘记密码时所使用的恢复密码"
                        "\n\n恢复密钥需要您进行手动生成，程序默认不会产生恢复密钥"
                        "\n\n当您使用恢复密钥解锁后，普通密码会被删除，您需要重新设置密码\n",bg="white").pack()


        if config["EMERGENCY_KEY"]!="":
            tk.Label(self.emkeyset, text="您已设置恢复密钥，可修改", bg="white",height=2,width=60,relief="solid", borderwidth=1,
            font=("宋体", 12)).pack(side="top", pady=10,padx=20)
            tk.Button(self.emkeyset, text="重新生成恢复密钥",command=lambda: EmKey(type="reset")).pack()
            tk.Button(self.emkeyset, text="删除恢复密钥",command=lambda: EmKey(type="delete")).pack()

        if config["EMERGENCY_KEY"]=="":
            tk.Label(self.emkeyset, text="您当前没有恢复密钥", bg="white",height=2,width=60,relief="solid", borderwidth=1,
                 font=("宋体", 12)).pack(side="top", pady=10,padx=20)
            tk.Button(self.emkeyset,text="生成恢复密钥", command=lambda: EmKey(type="create")).pack()

        Continue=check()
        print(Continue)
        if Continue==False:
            return

        PwdQuest()


class Settings:
    def __init__(self):
        global openemkeyset
        global openpwdset
        openemkeyset=None
        openpwdset=None
        self.settingcenterOn=False
    def close(self,name):
        if name==self.settingcenter:
            self.settingcenterOn=False
            self.settingcenter.destroy()
    def openEmKey(self):
        global openemkeyset
        if openemkeyset is None:
            openemkeyset=Password()
        openemkeyset.EmKeySet()
    def openPwdSet(self):
        global openpwdset
        if openpwdset is None:
            openpwdset=Password()
        openpwdset.pwdSet()


    def settingCenter(self):       #设置页需要多开检查
        # 多开检查
        if self.settingcenterOn:
            self.settingcenter.lift()
            return
        else:
            self.settingcenterOn = True

        self.settingcenter = tk.Toplevel(bg="white")
        window = WindowGeo(self.settingcenter)
        window.Style1()
        self.settingcenter.title("设置")
        self.settingcenter.protocol("WM_DELETE_WINDOW", lambda: self.close(self.settingcenter))
        #self.settingcenter.grab_set()


        tk.Label(self.settingcenter, text="设置", bg="white", width=34, height=6, borderwidth=1,
                 font=("HarmonyOS sans SC", 17)).pack(side="top", padx=10, pady=10)
        tk.Button(self.settingcenter, text="  设置密码  ", command=self.openPwdSet).pack()

        tk.Button(self.settingcenter, text="  管理恢复密钥  ", command=self.openEmKey).pack()

        tk.Button(self.settingcenter, text="  关于本程序  ", command=self.about).pack()

        tk.Button(self.settingcenter, text="返回主页", bg='#B3E5FC', fg='black',
                  activebackground='#81D4FA', activeforeground='black',
                  width=60, height=1, font=("HarmonyOS sans SC", 12),
                  borderwidth="1", relief="ridge", command=lambda: self.close(self.settingcenter)).pack(side="bottom",
                                                                                                        padx=5, pady=5)


    def about(self):           #about页面无需多开检查
        aboutcenter=tk.Toplevel(bg="white")
        window = WindowGeo(aboutcenter)  # 把当前tk实例送到windowgeo()函数中
        window.Style1()
        aboutcenter.title("关于")

        def open_github_link():
            webbrowser.open("https://github.com/JeanValjean/GUI_Study")

        tk.Label(aboutcenter, text="关于本程序",bg="white", width=34, height=6, borderwidth=1,
             font=("HarmonyOS sans SC", 17)).pack(side="top", padx=10, pady=10)
        tk.Label(aboutcenter, bg="white",text="本程序为个人项目，无法保证后期支持"
                    "\n\n\n基于Python3.13.5，tkinter GUI"
                    "\n\n\n本程序的源代码已上传至GitHub：https://github.com/JeanValjean/GUI_Study",
                    #"\n\n\n本程序的许可证为MIT许可证。"
                 font=("HarmonyOS sans SC", 9)).pack(side="top", padx=10, pady=10)

        tk.Button(aboutcenter, text="前往页面", command=open_github_link).pack(side="top", padx=10, pady=10)

        tk.Button(aboutcenter, text="      返回设置      ", command=aboutcenter.destroy).pack(side="left",anchor="sw", padx=10, pady=10)



class Main:
    def __init__(self):
        #防多开控制码
        global opensetting
        opensetting=None

    def startCheck(self):         #运行前检查，检查无误才启动主页面
        print("执行运行前检查...")
        #运行前检查
        if config["CoverState"] == True and config["PasswordLS"] == "":
            messagebox.showerror("发生严重错误","发生状态冲突，程序不能在左右脑互博的状态下打开")
            sys.exit()
        print("正在解密上一次的密码...")
        #解密+检查
        global decryptedPwd
        encryptedPwd = config["PasswordLS"]
        decryptedPwd = ""
        for char in encryptedPwd:
            decrypted_char = chr(ord(char) - 2)
            decryptedPwd += decrypted_char
        decryptedPwd=decryptedPwd
        print("解密结果：" + decryptedPwd)
        if config["launch_count"]<3:
            messagebox.showinfo("以管理员身份启动","本程序包含监控任务管理器功能，以管理员身份启动程序才可启用\n"
                                "(此提示只出现3次)")
            config["launch_count"]+=1
            saveConfig(config)


        if len(decryptedPwd) > 12:
            messagebox.showerror("发生严重错误","现有密码不符合规范，请通过配置文件重置")
            sys.exit()

        #开始启动主界面
        self.MainPage()

    def MainPage(self):

        self.mainpage = tk.Tk()
        self.mainpage.config(bg="white")
        window = WindowGeo(self.mainpage)  #把当前tk实例送到windowgeo()函数中
        window.Style1()
        self.mainpage.title("主页")
        self.mainpage.protocol("WM_DELETE_WINDOW", self.preventClose)


        tk.Label(self.mainpage, text="健康使用电脑", bg="white", width=34, height=6, borderwidth=1,
                 font=("宋体", 17)).pack(side="top", padx=10, pady=10)

        tk.Button(self.mainpage, text="启动遮罩", bg='#B3E5FC', fg='black',
                  activebackground='#81D4FA', activeforeground='black',
                  command=self.openCover,
                  width=45, height=3, font=("HarmonyOS sans SC", 14),
                  borderwidth="1", relief="ridge").pack(side="top", padx=10, pady=0)


        tk.Button(self.mainpage, text="设置", bg='white', fg='black', width=5, height=1,
                             command=self.openSetting).pack(side="left", anchor="sw", padx=10, pady=10)

        tk.Button(self.mainpage, text="帮助", bg='white', fg='black', width=5, height=1,
                              command=self.help).pack(side="left", anchor="sw", padx=1, pady=10)

        tk.Button(self.mainpage, text="退出", bg='white', fg='black', width=5, height=1,
                               command=self.mainpage.destroy).pack(side="left", anchor="sw", padx=10, pady=10)

        #主页-启动后检查
        #1.没密码提示先设密码
        if config["PasswordLS"]=="":
            messagebox.showinfo("欢迎使用","欢迎使用\"健康使用电脑\"应用程序，使用前请先设置密码")
            self.openSetting()
        #2.检查是否需要自动开启
        def autoStart():
            if config["CoverState"] == True:
                self.openCover()
        autoStart()

        self.mainpage.mainloop()

    def preventClose(self):     #防止主页被关闭：遮罩启动时不能通过系统关闭主页
        if config["CoverState"]==True:
            pass
        else:
            self.mainpage.destroy()

    def help(self):
        helpcenter = tk.Toplevel(bg="white")
        window = WindowGeo(helpcenter)  # 把当前tk实例送到windowgeo()函数中
        window.Style1()
        helpcenter.title("帮助")
        tk.Label(helpcenter, text="帮助", bg="white", width=34, height=6, borderwidth=1,
                 font=("HarmonyOS sans SC", 17)).pack(side="top", padx=10, pady=10)
        tk.Button(helpcenter, text="      返回主页      ", command=helpcenter.destroy).pack(side="left", anchor="sw",padx=10,pady=10)

    def openCover(self):          #cover不在当前类，通过实例化调用
        covercenter = Cover()      #Cover页面无需禁止防多开
        covercenter.coverStyle1()

    def openSetting(self):      #设置不在当前类，通过实例化调用
        global opensetting         #设置页面需带有防多开
        if opensetting is None:
            opensetting = Settings()
        opensetting.settingCenter()



if __name__ == "__main__":


    Main().startCheck()







# pyinstaller --onefile --noconsole --manifest admin.manifest xxx.py

# pyinstaller --onefile --noconsole --manifest admin.manifest ScreenBlocker_2.1.py



