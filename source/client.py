import requests
import json
import schedule
import time
import socket
import tkinter as tk
import sys
import os
import _thread
import fnmatch

host = None
port = None
Username = None
Password = None

def Thongbao(str): #thông báo xuất hiện và ấn ok để tắt
    Noti=tk.Tk()
    Noti.title("Thông báo")
    tk.Label(Noti,text=str).pack()
    tk.Button(Noti, text="OK", command=lambda: Noti.destroy(), width=10).place(relx=0.5, rely=0.7,anchor='center')
    #Noti.after(1000,lambda :Noti.destroy())
    Noti.geometry('300x50')
    Noti.mainloop()

def Thongbao_Login(str):   #Thông báo có 2 lựa chọn, chỉ xuất hiện khi nhập sai lúc Login
    Noti=tk.Tk()
    Noti.title("Thông báo")
    tk.Label(Noti,text=str,wraplength=250).place(relx=0.5,rely=0.3, anchor='center')
    tk.Button(Noti,text = "Nhập lại", command = lambda: TryAgain(Noti) , width=10).place(relx=0.2, rely=0.7,anchor='center')
    tk.Button(Noti, text="Đăng ký", command = lambda: GotoSignUp(Noti), width=10).place(relx=0.8, rely=0.7,anchor='center')
    Noti.geometry('300x100')
    Noti.mainloop()

def Thongbao_SignUp(str):   #Thông báo có 2 lựa chọn, chỉ xuất hiện nếu nhập sai trong SignUp
    Noti=tk.Tk()
    Noti.title("Thông báo")
    tk.Label(Noti,text=str,wraplength=250).place(relx=0.5,rely=0.3, anchor='center')
    tk.Button(Noti,text = "Nhập lại", command = lambda: TryAgain(Noti) , width=10).place(relx=0.2, rely=0.7,anchor='center')
    tk.Button(Noti, text="Đăng nhập", command = lambda: GotoLogin(Noti), width=10).place(relx=0.8, rely=0.7,anchor='center')
    Noti.geometry('300x100')
    Noti.mainloop()

def TryAgain(Noti):
    s.sendall('1'.encode('utf8'))
    Noti.destroy()

def GotoSignUp(Noti):
    s.sendall('0'.encode('utf8'))
    Noti.destroy()
    Hide_LoginForm()
    SignUpForm()

def GotoLogin(Noti):
    s.sendall('0'.encode('utf8'))
    Noti.destroy()
    Hide_SignUpForm()
    LoginForm()

def Hide_SignUpForm(): #xóa các ô nhập thông tin SignUp
    UsernameLabel.place_forget()
    UsernameEntry.place_forget()
    PasswordLabel.place_forget()
    PasswordEntry.place_forget()
    Click3.place_forget()

def Hide_LoginForm(): #xóa các ô nhập thông tin login
    UsernameLabel.place_forget()
    UsernameEntry.place_forget()
    PasswordLabel.place_forget()
    PasswordEntry.place_forget()
    Click2.place_forget()

def Hide_Get_IP_port(): #Xóa các ô nhập host và port
    HostLabel.place_forget()
    HostEntry.place_forget()
    PortEntry.place_forget()
    PortLabel.place_forget()
    Click1.place_forget()

def Check_IP_port(): #kiểm tra xem có thể kết nối tới server không
    try:
        s.connect((host, int(port)))
        Hide_Get_IP_port()
        ChooseForm()
    except:
        Thongbao("IP hoặc port không hợp lệ! Vui lòng nhập lại")
        return

def getData(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def Exit():
    s.close()
    root.destroy();

def SignUp():
    Username = UsernameEntry.get()
    Password = PasswordEntry.get()
    if len(Username) != 0 and len(Password) != 0:
        s.sendall(Username.encode('utf8'))
        s.sendall(Password.encode('utf8'))
        check = s.recv(1).decode('utf8')
        if check != '0':
            Thongbao_SignUp('Tài khoản đã tồn tại! Vui lòng thử lại')
        else:
            Hide_SignUpForm()
            tk.Label(root, text="trade").place(relx=0.5, rely=0.5, anchor='center')
            s.sendall('x'.encode('utf8'))
    else:
        Thongbao("Vui Lòng nhập lại!")

def Login():
    Username = UsernameEntry.get()
    Password = PasswordEntry.get()
    if len(Username) != 0 and len(Password) != 0:
        s.sendall(Username.encode('utf8'))
        s.sendall(Password.encode('utf8'))
        check = s.recv(1).decode('utf8')
        if check != '1':
            Thongbao_Login('Sai tên đăng nhập hoặc mật khẩu! Vui lòng thử lại hoặc tạo tài khoản!')
        else:
            Hide_LoginForm()
            tk.Label(root, text="trade").place(relx=0.5, rely=0.5, anchor='center')
            s.sendall('x'.encode('utf8'))
    else:
        Thongbao("Vui Lòng nhập lại!")

def Get_IP_port(HostEntry,PortEntry):
    global host, port
    host = HostEntry.get()
    port = PortEntry.get()
    if len(host) != 0 and len(port) != 0:
        Check_IP_port()
    else:
        Thongbao("Vui Lòng nhập lại!")

def SignUpForm(): #Tạo các ô điền Login
    UsernameLabel.place(relx=0.3, rely=0.5)
    UsernameEntry.place(relx=0.4, rely=0.5)
    PasswordLabel.place(relx=0.3, rely=0.55)
    PasswordEntry.place(relx=0.4, rely=0.55)
    Click3.place(relx=0.4, rely=0.6)

def LoginForm(): #Tạo các ô điền Login
    UsernameLabel.place(relx=0.3, rely=0.5)
    UsernameEntry.place(relx=0.4, rely=0.5)
    PasswordLabel.place(relx=0.3, rely=0.55)
    PasswordEntry.place(relx=0.4, rely=0.55)
    Click2.place(relx=0.4, rely=0.6)

def ChoosoToLogin(LoginButton, SignUpButton):
    LoginButton.destroy() #xóa bỏ lựa chọn Login
    SignUpButton.destroy() #xóa bỏ lựa chọn SignUp
    LoginForm() #Tạo các ô điền Login
    s.sendall('1'.encode('utf8')) #Gửi thông tin cho server

def ChoosoToSignUp(LoginButton, SignUpButton):
    LoginButton.destroy() #xóa bỏ lựa chọn Login
    SignUpButton.destroy() #xóa bỏ lựa chọn SignUp
    SignUpForm() #Tạo các ô điền SignUp
    s.sendall('0'.encode('utf8')) #Gửi thông tin cho server

def ChooseForm(): #Tạo ra lựa chọn cho người dùng sau khi nhập host và port
    LoginButton = tk.Button(root, text="LogIn", height=3, width=10, command=lambda: ChoosoToLogin(LoginButton,SignUpButton))
    LoginButton.place(relx=0.5, rely=0.4, anchor="center")
    SignUpButton = tk.Button(root, text="SignUp", height=3, width=10, command=lambda: ChoosoToSignUp(LoginButton,SignUpButton))
    SignUpButton.place(relx=0.5, rely=0.6, anchor="center")
    ExitButton.place(relx=0.5, rely=0.8, anchor="center")

root = tk.Tk()
#các thông tin tại màn hình chính
tk.Label(root, text=" TỶ GIÁ TIỀN TỆ VIỆT NAM", font=("Arial", 25)).place(relx=0.5, rely=0.25, anchor='center')
HostLabel=tk.Label(root, text="Host")
HostLabel.place(relx=0.3, rely=0.5)
HostEntry = tk.Entry(root)
HostEntry.place(relx=0.4, rely=0.5)
PortLabel= tk.Label(root, text="Port")
PortLabel.place(relx=0.3, rely=0.55)
PortEntry = tk.Entry(root)
PortEntry.place(relx=0.4, rely=0.55)
Click1 = tk.Button(root, text="Submit", command=lambda: Get_IP_port(HostEntry,PortEntry))
Click1.place(relx=0.4, rely=0.6)

#tạo Socket
try: s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    Thongbao('Không kết nối được, vui lòng thử lại sau!')

#Các ô thông tin để đăng nhập hoặc đăng ký
UsernameLabel = tk.Label(root, text="Username")
UsernameEntry = tk.Entry(root)
PasswordLabel = tk.Label(root, text="Password")
PasswordEntry = tk.Entry(root)
Click2 = tk.Button(root, text="LogIn", command=lambda: Login())
Click3 = tk.Button(root, text="SignUP", command=lambda: SignUp())

ExitButton = tk.Button(root, text="Thoát", height=3, width=10, command = lambda: Exit())
root.geometry("600x400")
root.mainloop()
