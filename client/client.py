import requests
import json
import schedule
import time
import socket
import tkinter as tk
import sys
import os

def SignUp_client(s):
    check = None
    while check != '0':
        Username = input('Điền tên đăng nhập: ')
        s.sendall(Username.encode('utf8'))
        Password = input('Điền mật khẩu: ')
        s.sendall(Password.encode('utf8'))
        check = s.recv(1).decode('utf8')
        if check == '1':
            print('Tài khoản đã tồn tại, hãy thử lại! ')
    print('Đã đăng ký thành công!')

def Login_client(s):
    check = None
    check2 = None
    while check != '1':
        Username = input('Điền tên đăng nhập: ')
        s.sendall(Username.encode('utf8'))
        Password = input('Điền mật khẩu: ')
        s.sendall(Password.encode('utf8'))
        check = s.recv(1).decode('utf8')
        if check != '1':
            check2 = input('Không tồn tại tài khoản! Nhấn 1 để thử lại hoặc ấn 2 để đăng ký:')
            s.sendall(check2.encode('utf8'))
            if check2 == '2':
                SignUp_client(s)
                return
    print('Đã đăng nhập thành công!')

def runClient(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            DNDK = input('Nhập 1 để đăng nhập hoặc nhập 2 để đăng kí: ')
            s.sendall(DNDK.encode('utf8'))
            if DNDK == '1':
                Login_client(s)
            else:
                SignUp_client(s)
            k = None
            while k != 'x':
                # msg = 'Hello World'
                k = input('Client: ')
                s.sendall(k.encode('utf8'))
                print('Da xong')
                data = s.recv(1024)
                print('Received ', data.decode('utf8'))
    except socket.error as err:
        print("Loi ket noi: ", err)
        sys.exit(1)


def getData(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data


# def Interface_for_Client():


# response = requests.request("GET", url, headers=headers, params=querystring)
# json_object = json.loads(response.text)
# print(json.dumps(json_object, indent = 3))
# with open('data.json', 'w' , encoding='utf-8') as f:
# json.dump(json_object, f, ensure_ascii=False, indent=4)


def Example():
    print("Hello")


if __name__ == "__main__":
    # data()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Da tao socket')
    except socket.error as err:
        print('Loi tao socket', err)

    host = input('Host: ')
    port = input('Port: ')
    runClient(host, int(port))
    os.system("pause")