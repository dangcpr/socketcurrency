import requests
import json
import schedule
import time
import socket
import tkinter as tk
import sys
import os

#host = '127.0.0.1'
#port = 65432
hostname = socket.gethostname()
address = socket.gethostbyname(hostname)

def createSocket(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Da tao socket')
    except socket.error as err:
        print('Loi tao socket', err)

    try:
        s.bind((host, port))
        s.listen()

        conn, addr = s.accept()
        with conn:
            print('Duoc ket noi boi', addr)
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

    querystring = {"format":"json","from":"AUD","to":"CAD","amount":"1"}

    headers = {
        'x-rapidapi-host': "currency-converter5.p.rapidapi.com",
        'x-rapidapi-key': "eeedbfa64emshbdd697d5f8b99b5p13bbcdjsn9ce5e073eaa1"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_object = json.loads(response.text)
    print(json.dumps(json_object, indent = 3))
    with open('data.json', 'w' , encoding='utf-8') as f:
        json.dump(json_object, f, ensure_ascii=False, indent=4)
def local_ip():
    localip = socket.gethostname()
    print(localip)
def updateLocalIPEvery30mins():
    data()
    schedule.every(10).seconds.do(data)
    while True:
        schedule.run_pending()
        time.sleep(0)

    
if __name__=="__main__":
    #data()
    
    #local_ip = socket.gethostbyname_ex(hostname)
    #local_ip()
    #updateLocalIPEvery30mins()
    #host = '127.0.0.1'
    port = 65432
    hostname = socket.gethostname()
    address = socket.gethostbyname(hostname)
    print(address)
    createSocket(address, port)

