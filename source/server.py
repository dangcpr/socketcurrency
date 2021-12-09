import requests
import json
from requests.api import get
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
    checkAcc = None
    while True:
        Username = s.recv(1024).decode("utf8")
        Password = s.recv(1024).decode("utf8")
        checkAcc = CheckIfExit(Username, Password)
        if checkAcc == '1':
            s.sendall('1'.encode('utf8'))
        else:
            s.sendall('0'.encode('utf8'))
            SaveAccount(Username, Password)
            return


def Login_server(s):
    check = None
    checkAcc = None
    while True:
        Username = s.recv(1024).decode("utf8")
        Password = s.recv(1024).decode("utf8")
        checkAcc = CheckIfExit(Username, Password)
        if checkAcc == '0':
            s.sendall('0'.encode('utf8'))
        else:
            s.sendall('1'.encode('utf8'))
            return
        check = s.recv(1).decode('utf8')
        if check == '2':
            SignUp_server(s)
            return


def runServer(conn, addr):
    try:
        with conn:
            print('Duoc ket noi boi', addr)
            connectAddress.append(conn)
            print(connectAddress)
            DNDK = conn.recv(1).decode('utf8')
            if DNDK == '1':
                Login_server(conn)
            else:
                SignUp_server(conn)
            str_data = None
            while str_data != 'x':
                data = conn.recv(1024)
                str_data = data.decode('utf8')
                if not str_data:
                    break
                print(str_data)
                str_send = 'Mon loz'
                conn.sendall(str_send.encode('utf8'))
            print(addr, ' da ngat ket noi')
            disAddr = str(addr)
            index = connectAddress.index(conn)
            connectAddress.pop(index)
            dis = ''.join(['Client ', disAddr, ' da thoat'])
            for i in connectAddress:
                i.send(dis.encode('utf8'))


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

    #print(response.text)
    json_object = json.loads(response.text)
    
    #print(json.dumps(json_object, indent=3))
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(json_object, f, ensure_ascii=False, indent=4)



def updateData():
    data()
    schedule.every(30).minutes.do(data)
    while True:
        schedule.run_pending()
        time.sleep(0)

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


def exportCurrency():
    with open('currency.json',encoding="utf-16-le") as f:
        json_data = json.load(f)
        print(json.dumps(json_data, indent = 3))




# def exportData():


if __name__ == "__main__":
    port = 65432
    hostname = socket.gethostname()
    address = socket.gethostbyname(hostname)
    print(address)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Da tao socket')
    except socket.error as err:
        print('Loi tao socket', err)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((address, port))
    s.listen(1)
    #print('Xin chào các bạn'.encode('utf-16'))
    #exportCurrency()
    #print(getAPIKey())
    #data()
    threadClient(s)
    print('Không lấy được dữ liệu')
    os.system('pause')