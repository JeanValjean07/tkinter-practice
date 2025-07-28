
import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox



def Cover():
    # 创建一个新的窗口
    cover = tk.Toplevel()


    tk.Label(cover, text="您的屏幕已被\"健康使用电脑\"锁定，请输入密码以解锁",
             relief="solid",width=100, height=8, borderwidth=2,
                 font=("HarmonyOS sans SC", 17)).pack(side="top",padx=10, pady=60)

    tk.Label(cover, text="输入密码解除遮罩").pack(side="top",padx=5, pady=5)

    pwd=tk.StringVar()
    entry=tk.Entry(cover,textvariable=pwd)
    entry.pack(side="top",padx=5, pady=5)

    def pwdQuit():
        print("日志：用户点击了确认按钮，密码是"+pwd.get())
        if pwd.get()=="114514":
            cover.destroy()
        else:
            messagebox.showerror("您不能退出", "您的密码错误",parent=cover)


    tk.Button(cover, text="确认",command=pwdQuit).pack(side="top",padx=5, pady=5)

    cover.attributes('-fullscreen', True)
    cover.attributes('-topmost', True)
    cover.overrideredirect(True)

    cover.grab_set()  # 模态
    cover.wait_window()




Center=tk.Tk()
Center.title("健康使用电脑")
Center.geometry("500x700+500+40")
tk.Label(Center, text="欢迎使用\"健康使用电脑\"", width=34, height=6, borderwidth=1,
                 font=("HarmonyOS sans SC", 17)).pack(side="top",padx=10, pady=10)




tk.Button(Center, text="启动遮罩", bg='#B3E5FC', fg='black',
         activebackground='#81D4FA',activeforeground='black',
        width=43, height=3, font=("HarmonyOS sans SC", 14),
        borderwidth="1",relief="ridge",command=Cover).pack(side="top",padx=10, pady=0)



Center.mainloop()











