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


connectAddress = []
# host = '127.0.0.1'
# port = 65432

def CheckIfExit(Username, Password):
    #User = Username + '_' + Password
    with open ('Account.json', 'r') as f:
        Acc_List = json.load(f)
        if (Username in Acc_List['Account']):
            index = Acc_List['Account'].index(Username)
            if (Acc_List['Pass'][index] == Password):
                return '1'
            else:
                return '0'
        else: return '0'

def SaveAccount(Username, Password):
    #User = Username + '_' + Password
    with open('Account.json', 'r+') as f:
        Acc_list = json.load(f)
        Acc_list['Account'].append(Username)
        Acc_list['Pass'].append(Password)
        f.seek(0)
        json.dump(Acc_list, f, indent = 4)

def SignUp_server(s):
    check = None
    checkAcc = None
    while True:
        Username = s.recv(1024).decode("utf8")
        Password = s.recv(1024).decode("utf8")
        if len(Username) != 0 and len(Password) != 0 and Username != 'x' and Password != 'x': #chỉ xảy ra khi người dùng tắt client lúc đăng ký
            checkAcc = CheckIfExit(Username, Password)
            if checkAcc == '1':
                s.sendall('1'.encode('utf8'))
            elif checkAcc == '0':
                s.sendall('0'.encode('utf8'))
                SaveAccount(Username, Password)
                return
            check = s.recv(1).decode('utf8')
            if check == '0':
                Login_server(s)
                return
        else: return
def Login_server(s):
    check = None
    checkAcc = None
    while True:
        Username = s.recv(1024).decode("utf8")
        Password = s.recv(1024).decode("utf8")
        if len(Username) != 0 and len(Password) != 0:  #chỉ xảy ra khi người dùng tắt client lúc đăng ký
            checkAcc = CheckIfExit(Username, Password)
            if checkAcc == '0':
                s.sendall('0'.encode('utf8'))
                noti = s.recv(1024).decode('utf8')
                print(noti.encode('utf8'))
            else:
                s.sendall('1'.encode('utf8'))
                noti = s.recv(1024).decode('utf8')
                print(noti.encode('utf8'))
                return
            check = s.recv(1).decode('utf8')
            if check == '0':
                SignUp_server(s)
                return
        else:
            return
def closeClient(conn, addr):
    try:
        print(addr, ' da ngat ket noi')
        disAddr = str(addr)
        index = connectAddress.index(conn)
        connectAddress.pop(index)
        dis = ''.join(['Client ', disAddr, ' da thoat'])
        for i in connectAddress:
            i.send(dis.encode('utf8'))
    except:
        print('Error')

def runServer(conn, addr):
    try:
        with conn:
            print('Duoc ket noi boi', addr)
            connectAddress.append(conn)
            print(connectAddress)
            DNDK = conn.recv(1).decode('utf8')
            if DNDK == '1':
                Login_server(conn)
            elif DNDK == '0':
                SignUp_server(conn)
            else:
                closeClient(conn, addr)
                return
            str_data = None
            while str_data != 'x':
                data = conn.recv(1024)
                str_data = data.decode('utf8')
                if not str_data:
                    break
                if(str_data != 'x'):
                    print(str_data)
                    if(str_data == 'search'):
                        conn.sendall('1'.encode('utf8'))
                        x = conn.recv(1024).decode('utf8')
                        currencyUnit = findData(x,'data.json')
                        check = currencyUnit.idxCurrency()
                        if (check == '-1'): conn.sendall('-1'.encode('utf8'))
                        else: exportData(conn, currencyUnit)
                    else:
                        conn.sendall('-1'.encode('utf8'))
                else:
                    break
            closeClient(conn, addr)
    except socket.error as err:
        print("Lỗi kết nối: ", err)
        sys.exit(1)

def threadClient(s):
    while True:
        try:
            conn, addr = s.accept()
            thrr = threading.Thread(target = runServer, args=(conn, addr))
            thrr.daemon = True
            thrr.start()
        except:
            print('Error')


def data():
    apiKey = getAPIKey()

    url = "https://vapi.vnappmob.com/api/v2/exchange_rate/bid?api_key=" + apiKey

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    print('Da update du lieu')
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(json_object, f, ensure_ascii=False, indent=4)

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
    schedule.every(60).seconds.do(data)
    while True:
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
    print(k)
    buy_transfer = currencyUnit.buy_transfer()
    conn.sendall(str(buy_transfer).encode('utf8'))
    k = conn.recv(1024).decode('utf8')
    print(k)
    sell = currencyUnit.sell()
    conn.sendall(str(sell).encode('utf8'))
    k = conn.recv(1024).decode('utf8')
    print(k)

# def exportData():


if __name__ == "__main__":
    port = 65432
    hostname = socket.gethostname()
    address = socket.gethostbyname(hostname)
    thrr = threading.Thread(target = updateData, args=())
    thrr.daemon = True
    thrr.start()
    print(address)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Da tao socket')
    except socket.error as err:
        print('Loi tao socket', err)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((address, port))
    s.listen(5)
    threadClient(s)