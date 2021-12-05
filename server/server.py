import requests
import json
import schedule
import time
import socket
import tkinter as tk
import sys
import os


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


def runServer(s):
    try:
        conn, addr = s.accept()
        with conn:
            print('Duoc ket noi boi', addr)
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
    except socket.error as err:
        print("Lỗi kết nối: ", err)
        sys.exit(1)


def data():
    url = "https://currency-converter5.p.rapidapi.com/currency/convert"

    querystring = {"format": "json", "from": "AUD", "to": "CAD", "amount": "1"}

    headers = {
        'x-rapidapi-host': "currency-converter5.p.rapidapi.com",
        'x-rapidapi-key': "eeedbfa64emshbdd697d5f8b99b5p13bbcdjsn9ce5e073eaa1"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_object = json.loads(response.text)
    print(json.dumps(json_object, indent=3))
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(json_object, f, ensure_ascii=False, indent=4)


def updateLocalIPEvery30mins():
    data()
    schedule.every(30).minutes.do(data)
    while True:
        schedule.run_pending()
        time.sleep(0)


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

    s.bind((address, port))
    s.listen(1)
    #print('Xin chào các bạn'.encode('utf-16'))
    #exportCurrency()
    runServer(s)