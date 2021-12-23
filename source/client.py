import requests
import json
import schedule
import time
import socket
import sys
import os
import _thread
import fnmatch
import threading
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter.ttk as exTk
import tkinter as tk

host = None
port = None
Username = None
Password = None

options = ["AUD", "CAD", "CHF", "CNY", "DKK", "EUR", "GBP", "HKD", "JPY", "KRW", "LAK", "MYR", "NOK", "NZD", "RUB",
           "SEK", "SGD", "THB", "TWD", "USD"]
options1 = ["Đô la Úc - AUD", "Đô la Canada - CAD", "Franc Thụy Sĩ - CHF", "Nhân dân tệ - CNY", "Krone Đan Mạch - DKK",
            "Euro - EUR",
            "Bảng Anh - GBP", "Đô la Hồng Kông - HKD", "Yên Nhật - JPY", "Won Hàn Quốc - KRW", "Kip Lào - LAK",
            "Ringgit Malaysia - MYR",
            "Krone Na Uy - NOK", "Đô la New Zealand - NZD", "Rúp Nga - RUB", "Krona Thụy Điển - SEK",
            "Đô la Singapore - SGD",
            "Baht Thái Lan - THB", "Tân Đài tệ - TWD", "Đô la Mỹ - USD"]


def Thongbao(str):  # thông báo xuất hiện và ấn ok để tắt
    Noti = tk.Toplevel(root)
    Noti.title("Thông báo")
    tk.Label(Noti, text=str).pack()
    tk.Button(Noti, text="OK", command=lambda: Noti.destroy(), width=10).place(relx=0.5, rely=0.7, anchor='center')
    Noti.after(2000, lambda: Noti.destroy())
    Noti.geometry('300x50')
    # Noti.mainloop()

def ThongbaoServer(str):  # thông báo từ server
    Noti = tk.Toplevel(root)
    Noti.title("Thông báo")
    tk.Label(Noti, text=str).pack()
    tk.Button(Noti, text="OK", command=lambda: [Noti.destroy(), root.destroy()], width=10).place(relx=0.5, rely=0.7, anchor='center')
    Noti.after(2000, lambda:  [Noti.destroy(), root.destroy()])
    Noti.geometry('300x50')

def Confirm_Exit(): #bước đảm bảo trước khi tắt cliet
    Noti = tk.Toplevel(root)
    Noti.title("Thông báo")
    tk.Label(Noti, text="Bạn muốn thoát?", wraplength=250).place(relx=0.5, rely=0.3, anchor='center')
    tk.Button(Noti, text="thoát", command=lambda: Exit(), width=10).place(relx=0.2, rely=0.7,
                                                                                     anchor='center')
    tk.Button(Noti, text="Cancel", command=lambda: Noti.destroy(), width=10).place(relx=0.8, rely=0.7,
                                                                                      anchor='center')
    Noti.after(2000, lambda: Noti.destroy())
    Noti.geometry('300x100')

def Thongbao_Login(str):  # Thông báo có 2 lựa chọn, chỉ xuất hiện khi nhập sai lúc Login
    Noti = tk.Toplevel(root)
    Noti.title("Thông báo")
    tk.Label(Noti, text=str, wraplength=250).place(relx=0.5, rely=0.3, anchor='center')
    tk.Button(Noti, text="Nhập lại", command=lambda: TryAgain(Noti), width=10).place(relx=0.2, rely=0.7,
                                                                                     anchor='center')
    tk.Button(Noti, text="Đăng ký", command=lambda: GotoSignUp(Noti), width=10).place(relx=0.8, rely=0.7,
                                                                                      anchor='center')
    Noti.after(2000, lambda: TryAgain(Noti))
    Noti.geometry('300x100')
    # Noti.mainloop()


def Thongbao_SignUp(str):  # Thông báo có 2 lựa chọn, chỉ xuất hiện nếu nhập sai trong SignUp
    Noti = tk.Toplevel(root)
    Noti.title("Thông báo")
    tk.Label(Noti, text=str, wraplength=250).place(relx=0.5, rely=0.3, anchor='center')
    tk.Button(Noti, text="Nhập lại", command=lambda: TryAgain(Noti), width=10).place(relx=0.2, rely=0.7,
                                                                                     anchor='center')
    tk.Button(Noti, text="Đăng nhập", command=lambda: GotoLogin(Noti), width=10).place(relx=0.8, rely=0.7,
                                                                                       anchor='center')
    Noti.after(2000, lambda: TryAgain(Noti))
    Noti.geometry('300x100')
    # Noti.mainloop()


def TryAgain(Noti):
    try:
        s.sendall('1'.encode('utf8'))
        Noti.destroy()
    except:
        ThongbaoServer("Không kết nối được với server")


def GotoSignUp(Noti):
    try:
        s.sendall('0'.encode('utf8'))
        Noti.destroy()
        Hide_LoginForm()
        SignUpForm()
    except:
        ThongbaoServer("Server đã ngắt kết nối! Vui lòng thử lại sau!")


def GotoLogin(Noti):
    try:
        s.sendall('0'.encode('utf8'))
        Noti.destroy()
        Hide_SignUpForm()
        LoginForm()
    except:
        ThongbaoServer("Server đã ngắt kết nối! Vui lòng thử lại sau!")


def Hide_SignUpForm():  # xóa các ô nhập thông tin SignUp
    UsernameLabel.place_forget()
    UsernameEntry.place_forget()
    PasswordLabel.place_forget()
    PasswordEntry.place_forget()
    Click3.place_forget()


def Hide_LoginForm():  # xóa các ô nhập thông tin login
    UsernameLabel.place_forget()
    UsernameEntry.place_forget()
    PasswordLabel.place_forget()
    PasswordEntry.place_forget()
    Click2.place_forget()
    # root.place_foget()


def Hide_Get_IP_port():  # Xóa các ô nhập host và port
    HostLabel.place_forget()
    HostEntry.place_forget()
    PortEntry.place_forget()
    PortLabel.place_forget()
    Click1.place_forget()


def Check_IP_port():  # kiểm tra xem có thể kết nối tới server không
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
    try:
        s.sendall('ClientExitServer555'.encode('utf8'))
        s.close()
        root.destroy()
    except:
        ThongbaoServer("Không kết nối được với server.")
        s.close()

def SignUp():
    Username = UsernameEntry.get()
    Password = PasswordEntry.get()
    try:
        if len(Username) != 0 and len(Password) != 0:
            s.sendall(Username.encode('utf8'))
            s.sendall(Password.encode('utf8'))
            check = s.recv(1).decode('utf8')
            if check != '0':
                Thongbao_SignUp('Tài khoản đã tồn tại! Vui lòng thử lại')
            else:
                Thongbao('Đăng ký thành công')
                Hide_SignUpForm()
                mainPage()
        else:
            Thongbao("Vui Lòng nhập lại!")
    except:
        ThongbaoServer("Kết nối đã bị ngắt! Vui lòng thử lại sau!")


def Login():
    Username = UsernameEntry.get()
    Password = PasswordEntry.get()
    try:
        if len(Username) != 0 and len(Password) != 0:
            s.sendall(Username.encode('utf8'))
            s.sendall(Password.encode('utf8'))
            check = s.recv(1).decode('utf8')
            if check == '0':
                Thongbao_Login('Sai tên đăng nhập hoặc mật khẩu! Vui lòng thử lại hoặc tạo tài khoản!')
            elif check == '2':
                Thongbao_Login('Tài khoản này hiện tại đã đăng nhập! Vui lòng truy cập tài khoản khác hoặc đăng ký!')
            else:
                Thongbao('Đăng nhập thành công')
                Hide_LoginForm()
                mainPage()
        else:
            Thongbao("Vui Lòng nhập lại!")
    except:
        ThongbaoServer("Kết nối đã bị ngắt! Vui lòng thử lại sau!")


def searchData():
    try:
        while True:
            k = input("Mời nhập từ khoá search: ")
            s.sendall(k.encode('utf8'))
            t = s.recv(1024).decode('utf8')
            if (t == '1'):
                k = input('Nhập đơn vị: ')
                s.sendall(k.encode('utf8'))
                if (t == '-1'):
                    k = input('Nhập đơn vị: ')
                else:
                    buy_cash = s.recv(1024).decode('utf8')
                    s.sendall('Da nhan buy cash'.encode('utf8'))
                    print("buy_cash: ", buy_cash)
                    buy_transfer = s.recv(1024).decode('utf8')
                    s.sendall('Da nhan buy transfer'.encode('utf8'))
                    print("buy_transfer: ", buy_transfer)
                    sell = s.recv(1024).decode('utf8')
                    s.sendall('Da nhan sell'.encode('utf8'))
                    print("sell: ", sell)
    except:
        ThongbaoServer("Không lấy được dữ liệu")
        s.close()


def Get_IP_port(HostEntry, PortEntry):
    global host, port
    host = HostEntry.get()
    port = PortEntry.get()
    if len(host) != 0 and len(port) != 0:
        Check_IP_port()
    else:
        Thongbao("Vui Lòng nhập lại!")


def SignUpForm():  # Tạo các ô điền Login
    UsernameLabel.place(relx=0.3, rely=0.5)
    UsernameEntry.place(relx=0.4, rely=0.5)
    PasswordLabel.place(relx=0.3, rely=0.55)
    PasswordEntry.place(relx=0.4, rely=0.55)
    Click3.place(relx=0.4, rely=0.6)


def LoginForm():  # Tạo các ô điền Login
    UsernameLabel.place(relx=0.3, rely=0.5)
    UsernameEntry.place(relx=0.4, rely=0.5)
    PasswordLabel.place(relx=0.3, rely=0.55)
    PasswordEntry.place(relx=0.4, rely=0.55)
    Click2.place(relx=0.4, rely=0.6)


def ChoosoToLogin(LoginButton, SignUpButton):
    try:
        LoginButton.destroy()  # xóa bỏ lựa chọn Login
        SignUpButton.destroy()  # xóa bỏ lựa chọn SignUp
        LoginForm()  # Tạo các ô điền Login
        s.sendall('1'.encode('utf8'))  # Gửi thông tin cho server
    except:
        ThongbaoServer("Kết nối đã bị ngắt! Vui lòng thử lại sau!")


def ChoosoToSignUp(LoginButton, SignUpButton):
    try:
        LoginButton.destroy()  # xóa bỏ lựa chọn Login
        SignUpButton.destroy()  # xóa bỏ lựa chọn SignUp
        SignUpForm()  # Tạo các ô điền SignUp
        s.sendall('0'.encode('utf8'))  # Gửi thông tin cho server
    except:
        ThongbaoServer("Kết nối đã bị ngắt! Vui lòng thử lại sau!")


def ChooseForm():  # Tạo ra lựa chọn cho người dùng sau khi nhập host và port
    LoginButton = tk.Button(root, text="LogIn", height=3, width=10,
                            command=lambda: ChoosoToLogin(LoginButton, SignUpButton))
    LoginButton.place(relx=0.5, rely=0.4, anchor="center")
    SignUpButton = tk.Button(root, text="SignUp", height=3, width=10,
                             command=lambda: ChoosoToSignUp(LoginButton, SignUpButton))
    SignUpButton.place(relx=0.5, rely=0.6, anchor="center")
    ExitButton.place(relx=0.5, rely=0.8, anchor="center")


def runClient(atm, cmb, frame, textBox):
    try:
        if atm == '':
            atm = "1"
        if cmb == '':
            cmb = 'USD'
        for i in range(len(options1)):
            if (cmb == options1[i]):
                cmb = options[i]

        s.sendall(cmb.encode('utf8'))
        check = s.recv(1024).decode('utf8')
        if (check == '-1'):
            # s.sendall('Da nhan check'.encode('utf8'))
            Thongbao("Đơn vị tiền tệ không hợp lệ")
            return
        else:
            s.sendall('Da nhan check'.encode('utf8'))
            buy_cash = s.recv(1024).decode('utf8')
            s.sendall('Da nhan buy cash'.encode('utf8'))
            buy_transfer = s.recv(1024).decode('utf8')
            s.sendall('Da nhan buy transfer'.encode('utf8'))
            sell = s.recv(1024).decode('utf8')
            s.sendall('Da nhan sell'.encode('utf8'))
            buy_cash1 = float(atm) * float(buy_cash)
            buy_transfer1 = float(atm) * float(buy_transfer)
            sell1 = float(atm) * float(sell)
            print(sell1)
            textBox.delete(1.0, END)
            textBox.insert(0.0, atm + " " + cmb + "\nTiền mặt          : " + str(buy_cash1) + " VND\nChuyển khoản: " + str(
                buy_transfer1)
                        + " VND\nBán                 : " + str(sell1) + " VND")
    except:
        ThongbaoServer("Không kết nối được với server")

def LogOut(Frame):
    s.sendall('ClientLogoutServer263'.encode('utf8'))
    #s.close()
    root.geometry("600x400")
    Frame.place_forget()
    ChooseForm()
    # pass


def mainPage():
    root.geometry("1000x600")
    MainPage = tk.Frame(root, width=1000, height=600, background="#0A146E")
    MainPage.place(x=0, y=0)
    behind_Frame = tk.Frame(MainPage, width=1000, height=350, background="white")
    behind_Frame.place(x=0, y=250)
    main_Frame = tk.Frame(MainPage, width=800, height=500, background="#FFFABD")
    main_Frame.place(x=100, y=100)

    # label chinh
    lbl = Label(MainPage, text=" TỶ GIÁ TIỀN TỆ VIỆT NAM", background="#0A146E", foreground="white",
                font=("Arial 25 bold")).place(relx=0.5, rely=0.1, anchor='center')

    # label so tien
    amount = Label(main_Frame, text="Số tiền ", background="#FFFABD", foreground="black", font='arial 15')
    amount.place(x=50, y=50)

    # entry nhap so tien
    atm = StringVar()
    amount_entry = Entry(main_Frame, width=20, textvariable=atm)
    amount_entry.place(x=50, y=80)

    # lable Don vi tien te can tra cuu
    odered_currency = Label(main_Frame, text="Đơn vị tiền tệ cần tra cứu", background="#FFFABD", foreground="black",
                            font='arial 15')
    odered_currency.place(x=250, y=50)

    # combobox don vi tien te
    cmb = exTk.Combobox(main_Frame, width=25, font='Time 11', values=options1)
    cmb.place(x=250, y=80)

    VN_currency = Label(main_Frame, text="Đơn vị tiền tệ Việt Nam", background="#FFFABD", foreground="black",
                        font='arial 15')
    VN_currency.place(x=550, y=50)
    VN_curr = Label(main_Frame, text="Việt Nam Đồng - VND", background="#EFE8A8", font='Time 11')
    VN_curr.place(x=550, y=80)

    # Thong tin can tim
    tb = Text(main_Frame, width=35, height=5, background="white", font='Arial 18 bold')
    tb.place(x=165, y=245)

    Search_Btn = tk.Button(main_Frame, text="Tra cứu", background='#0071EB', fg='white', font='arial 18 bold',
                           command=lambda: runClient(atm.get(), cmb.get(), main_Frame, tb))
    Search_Btn.place(x=340, y=140)

    Logout_Btn = tk.Button(MainPage, text="Đăng xuất", background="white", foreground="#0A146E",
                           command=lambda: LogOut(MainPage))
    Logout_Btn.place(x=915, y=10)

    #MainPage.mainloop()


root = tk.Tk()
# các thông tin tại màn hình chính
root.title("Tỷ giá tiền tệ Việt Nam")
root.resizable(0, 0)
mainLabel = tk.Label(root, text=" TỶ GIÁ TIỀN TỆ VIỆT NAM", font=("Arial", 25)).place(relx=0.5, rely=0.25,
                                                                                      anchor='center')
HostLabel = tk.Label(root, text="Host")
HostLabel.place(relx=0.3, rely=0.5)
HostEntry = tk.Entry(root)
HostEntry.place(relx=0.4, rely=0.5)
PortLabel = tk.Label(root, text="Port")
PortLabel.place(relx=0.3, rely=0.55)
PortEntry = tk.Entry(root)
PortEntry.place(relx=0.4, rely=0.55)
Click1 = tk.Button(root, text="Submit", command=lambda: Get_IP_port(HostEntry, PortEntry))
Click1.place(relx=0.4, rely=0.6)

# tạo Socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    Thongbao('Không kết nối được, vui lòng thử lại sau!')
    root.destroy()

# Các ô thông tin để đăng nhập hoặc đăng ký
UsernameLabel = tk.Label(root, text="Username")
UsernameEntry = tk.Entry(root)
PasswordLabel = tk.Label(root, text="Password")
PasswordEntry = tk.Entry(root)
Click2 = tk.Button(root, text="LogIn", command=lambda: Login())
Click3 = tk.Button(root, text="SignUP", command=lambda: SignUp())

ExitButton = tk.Button(root, text="Thoát", height=3, width=10, command=lambda: Confirm_Exit())
root.geometry("600x400")
root.protocol("WM_DELETE_WINDOW", Confirm_Exit)
root.mainloop()