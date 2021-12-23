import requests
import json
import schedule
import time
import socket
import tkinter as tk
import sys
import os
import threading
import fnmatch

#ClientLogoutServer263
#ClientExitServer555
connectAddress = [] #lưu các conn
AddressOnly = [] #lưu các addr
# host = '127.0.0.1'
# port = 65432

root = tk.Tk()
def Thongbao(str): #thông báo xuất hiện và ấn ok để tắt
    Noti=tk.Toplevel(root)
    Noti.title("Thông báo")
    tk.Label(Noti,text=str).pack()
    tk.Button(Noti, text="OK", command=lambda: [Noti.destroy()], width=10).place(relx=0.5, rely=0.7,anchor='center')
    Noti.after(2000,lambda :Noti.destroy())
    Noti.geometry('300x50')
    #Noti.mainloop()

def Confirm_Shutdown(): #bước đảm bảo trước khi shutdown server
    Noti = tk.Toplevel(root)
    Noti.title("Thông báo")
    tk.Label(Noti, text="Bạn muốn shutdown server?", wraplength=250).place(relx=0.5, rely=0.3, anchor='center')
    tk.Button(Noti, text="Shutdown", command=lambda: Shutdown(), width=10).place(relx=0.2, rely=0.7,
                                                                                     anchor='center')
    tk.Button(Noti, text="Cancel", command=lambda: Noti.destroy(), width=10).place(relx=0.8, rely=0.7,
                                                                                      anchor='center')
    Noti.after(3000, lambda: Noti.destroy())
    Noti.geometry('300x100')

def Confirm_Disconnect(conn, addr): #bước đảm bảo trước khi shutdown server
    Noti = tk.Toplevel(root)
    Noti.title("Thông báo")
    strr = "Bạn muốn ngắt kết nối với " + str(addr) + " ?"
    tk.Label(Noti, text=strr, wraplength=250).place(relx=0.5, rely=0.3, anchor='center')
    tk.Button(Noti, text="Ngắt", command=lambda: closeClient(conn, addr), width=10).place(relx=0.2, rely=0.7,
                                                                                     anchor='center')
    tk.Button(Noti, text="Cancel", command=lambda: Noti.destroy(), width=10).place(relx=0.8, rely=0.7,
                                                                                      anchor='center')
    Noti.after(3000, lambda: Noti.destroy())
    Noti.geometry('300x100')

def CheckIfExist_SignUp(Username, Password): #khi đăng ký chỉ check phần username
    with open ('Account.json', 'r') as f:
        Acc_List = json.load(f)
        if (Username in Acc_List['Account']):
            return '1'
        else:
            return '0'

def CheckIfExist(Username, Password): #check cả username lẫn password khi đăng nhập
    with open ('Account.json', 'r') as f:
        Acc_List = json.load(f)
        if (Username in Acc_List['Account']):
            index = Acc_List['Account'].index(Username)
            if (Acc_List['Pass'][index] == Password):
                return '1'
            else:
                return '0'
        else: return '0'

def CheckIfOnline(Username, Password): #kiểm tra xem tài khoản đó có online không
    with open ('AccountOnline.json', 'r') as f:
        Acc_List = json.load(f)
        if (Username in Acc_List['Account']):
            index = Acc_List['Account'].index(Username)
            if (Acc_List['Pass'][index] == Password):
                return '1'
            else:
                return '0'
        else: return '0'

def SaveAccount(Username, Password): #Lưu account đăng ký
    with open('Account.json', 'r+') as f:
        Acc_list = json.load(f)
        Acc_list['Account'].append(Username)
        Acc_list['Pass'].append(Password)
        f.seek(0)
        json.dump(Acc_list, f, indent = 4)

def Online(Username, Password): #Lưu account đang online
    with open('AccountOnline.json', 'r+') as f:
        Acc_list = json.load(f)
        Acc_list['Account'].append(Username)
        Acc_list['Pass'].append(Password)
        f.seek(0)
        json.dump(Acc_list, f, indent = 4)

def OfflineALL(): #xóa tất cả account đang online, dùng khi shutdowm server
    with open('AccountOnline.json', 'r') as f:
        Acc_list = json.load(f)
        Acc_list['Account'].clear()
        Acc_list['Pass'].clear()
    with open('AccountOnline.json', 'w') as f:
        f.seek(0)
        json.dump(Acc_list, f, indent = 4)

def Offline(Username, Password): #Xóa account khỏi danh sách online
    with open('AccountOnline.json', 'r') as f:
        Acc_list = json.load(f)
        Acc_list['Account'].remove(Username)
        Acc_list['Pass'].remove(Password)
    with open('AccountOnline.json', 'w') as f:
        f.seek(0)
        json.dump(Acc_list, f, indent = 4)

def SignUp_server(s):
    check = None
    checkAcc = None
    while True:
        Username = s.recv(1024).decode("utf8")
        Password = s.recv(1024).decode("utf8")
        if len(Username) != 0 and len(Password) != 0 and Username != 'x' and Password != 'x': #chỉ xảy ra khi người dùng tắt client lúc đăng ký
            checkAcc = CheckIfExist_SignUp(Username, Password)
            if checkAcc == '1':
                s.sendall('1'.encode('utf8'))
            elif checkAcc == '0':
                s.sendall('0'.encode('utf8'))
                SaveAccount(Username, Password)
                Online(Username, Password)
                return Username,Password
            check = s.recv(1).decode('utf8')
            if check == '0':
                return Login_server(s)
                #return Username,Password
        else:
            return Username,Password

def Login_server(s):
    check = None #kiểm tra xem người dùng muốn nhập lại hay chuyển sang đăng kí sau khi đăng nhập sai
    checkAcc = None #kiểm tra tài khoảng có tồn tại hay không
    checkOnline = None #kiểm tra tài khoản có online hay không
    while True:
        Username = s.recv(1024).decode("utf8")
        Password = s.recv(1024).decode("utf8")
        print(Username," ",Password)
        if len(Username) != 0 and len(Password) != 0:  #chỉ xảy ra khi người dùng tắt client lúc đăng ký
            checkAcc = CheckIfExist(Username, Password)
            checkOnline = CheckIfOnline(Username, Password)
            if checkAcc == '0':
                s.sendall('0'.encode('utf8'))
                #noti = s.recv(1024).decode('utf8')
                #print(noti)
            else:
                if checkOnline == '0':
                    s.sendall('1'.encode('utf8'))
                    Online(Username, Password)
                    #noti = s.recv(1024).decode('utf8')
                    #print(noti)
                    return Username,Password
                else:
                    s.sendall('2'.encode('utf8'))

            check = s.recv(1).decode('utf8')
            if check == '0':
                return SignUp_server(s)
                #return Username,Password
        else:
            return Username,Password

def closeClient(conn, addr):
    print(addr, ' da ngat ket noi')
    disAddr = str(addr)
    index = connectAddress.index(conn)
    connectAddress.pop(index)
    index2 = AddressOnly.index(addr)
    AddressOnly.pop(index2)
    global Changed
    Changed = True
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
    #dis = ''.join(['Client ', disAddr, ' da thoat'])
    #for i in connectAddress:
        #i.send(dis.encode('utf8'))

def runServer(conn, addr):
    try:
        with conn:
            print('Duoc ket noi boi', addr)
            strr=str(addr) + ' đã kết nối!'
            Thongbao(strr)
            connectAddress.append(conn)
            AddressOnly.append(addr)
            global Changed
            Changed = True
            print(connectAddress)
            while True:
                DNDK = conn.recv(1024).decode('utf8')
                if DNDK == '1':
                    Username, Password = Login_server(conn)
                elif DNDK == '0':
                    Username, Password = SignUp_server(conn)
                else: #Người dùng chọn thoát, server nhận tín hiệu ClientExitServer555
                    closeClient(conn, addr)
                    return
                if Username == 'ClientExitServer555': #Xảy ra khi người dùng ấn Login/SignUp sau đó ấn thoát, break và ngắt kết nối
                    break
                str_data = None
                while str_data != 'ClientLogoutServer263': #khi server nhận tín hiệu ClientLogoutServer263 sẽ đăng xuất
                    data = conn.recv(1024)
                    str_data = data.decode('utf8')
                    if (not str_data) or (str_data == 'ClientExitServer555'):
                        break
                    if(str_data != 'ClientLogoutServer263'):
                        print(str_data)
                        currencyUnit = findData(str_data, 'data.json')
                        check = currencyUnit.idxCurrency()
                        if (check == '-1'):
                            conn.sendall('-1'.encode('utf8'))
                        else:
                            conn.sendall('1'.encode('utf8'))
                            conn.recv(1024)
                            exportData(conn, currencyUnit)
                            print(currencyUnit.buy_cash)
                            print(currencyUnit.buy_transfer)
                            print(currencyUnit.sell)
                    else:
                        break
                Offline(Username, Password)
            closeClient(conn, addr)
    except socket.error as err:
        print("Lỗi kết nối: ", err)
        sys.exit(1)

def threadClient():
    while True:
        try:
            conn, addr = s.accept()
            thrr = threading.Thread(target = runServer, args=(conn, addr))
            thrr.daemon = True
            thrr.start()
        except:
            print('Error')
            return

def Shutdown():
    OfflineALL()
    s.close()
    root.destroy()
    global Running
    Running = False

def data():
    try:
        apiKey = getAPIKey()

        url = "https://vapi.vnappmob.com/api/v2/exchange_rate/bid?api_key=" + apiKey

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        json_object = json.loads(response.text)
        print('Da update du lieu')
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(json_object, f, ensure_ascii=False, indent=4)
    except:
        print('Không lấy được dữ liệu')

def getAPIKey():
    try:
        url = "https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate"

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        data_dict = json.loads(response.text)

        return data_dict["results"]
    except:
        print('Không lấy được dữ liệu')

def updateData():
    data()
    schedule.every(30).minutes.do(data)
    while Running == True:
        schedule.run_pending()
        time.sleep(0)

def exportCurrency():
    with open('currency.json',encoding="utf-16-le") as f:
        json_data = json.load(f)
        print(json.dumps(json_data, indent = 3))

class findData:
    def __init__(self,currencyUnit,fileName):
        self.name = currencyUnit
        self.file = fileName

    def idxCurrency(self):
        with open(self.file) as file:
            file_Data = json.load(file)

        for i, entry in enumerate(file_Data['results']):
            if entry['currency'] == self.name:
                return i

        return "-1"

    def buy_cash(self):
        idx = self.idxCurrency()

        with open(self.file) as file:
            file_Data = json.load(file)
        return file_Data['results'][idx]["buy_cash"]


    def buy_transfer(self):
        idx = self.idxCurrency()
        with open(self.file) as file:
            file_Data = json.load(file)
        return file_Data['results'][idx]["buy_transfer"]

    def sell(self):
        idx = self.idxCurrency()
        with open(self.file) as file:
            file_Data = json.load(file)
        return file_Data['results'][idx]["sell"]

def exportData(conn, currencyUnit):
    buy_cash = currencyUnit.buy_cash()
    conn.sendall(str(buy_cash).encode('utf8'))
    k = conn.recv(1024).decode('utf8')
    print(buy_cash)
    print(k)
    buy_transfer = currencyUnit.buy_transfer()
    conn.sendall(str(buy_transfer).encode('utf8'))
    k = conn.recv(1024).decode('utf8')
    print(buy_transfer)
    print(k)
    sell = currencyUnit.sell()
    conn.sendall(str(sell).encode('utf8'))
    k = conn.recv(1024).decode('utf8')
    print(sell)
    print(k)

def clear_frame():
   for widgets in ClientFrame.winfo_children():
      widgets.destroy()

def UpdateFrame():
    clear_frame()
    for addr in AddressOnly:
        index = AddressOnly.index(addr)
        tk.Label(ClientFrame, text = addr, width= 50, justify='center',bg='green').grid(row = index, column=0)
        tk.Button(ClientFrame, text = 'Ngắt kết nối', command = lambda: Confirm_Disconnect(connectAddress[index], AddressOnly[index])).grid(row = index, column= 1)

def CheckUpdateFrame():
    global Changed
    while Running == True:
        if Changed == True:
            Changed = False
            UpdateFrame()

tk.Label(root, text=" TỶ GIÁ TIỀN TỆ VIỆT NAM(Server)", font=("Arial", 25)).place(relx=0.5, rely=0.1, anchor='center')
port = 65432
hostname = socket.gethostname()
address = socket.gethostbyname(hostname)
print(address)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((address, port))
    s.listen(5)
    threading.Thread(target=threadClient).start()
    #threading.Thread(target=threadServer).start()
    Thongbao('Đã tạo socket')
    ClientFrame = tk.Frame(root)
    ClientFrame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8, relheight=0.7)
    Changed = False #kiểm tra xem list connectAddress có gì thay đổi không
    Running = True #Kiểm tra xem GUI có còn không, khi GUI bị tắt thì Running = False
    threading.Thread(target=CheckUpdateFrame).start()
    UpdateThread = threading.Thread(target=updateData)
    UpdateThread.start()
    ExitButton = tk.Button(root, text="Shutdown Server", height=3, width=15, command=lambda: Confirm_Shutdown())
    ExitButton.place(relx=0.5, rely=0.9, anchor="center")
except socket.error as err:
    Thongbao('Lỗi không thể tạo socket, vui lòng thử lại!', err)
    root.destroy()
root.protocol("WM_DELETE_WINDOW", Confirm_Shutdown)
root.geometry("600x400")
root.mainloop()