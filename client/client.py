import requests
import json
import schedule
import time
import socket
import tkinter as tk
import sys
import os


def runClient(host, port):

    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            #print('Client')
            k = None
            while k!='x':
                #msg = 'Hello World'
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

#def Interface_for_Client():






    #response = requests.request("GET", url, headers=headers, params=querystring)
    #json_object = json.loads(response.text)
    #print(json.dumps(json_object, indent = 3))
    #with open('data.json', 'w' , encoding='utf-8') as f:
        #json.dump(json_object, f, ensure_ascii=False, indent=4)


def Example():
    print("Hello")








    
if __name__=="__main__":
    #data()


    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Da tao socket')
    except socket.error as err:
        print('Loi tao socket', err)
    
    host = input('Host: ')
    port = input('Port: ')
    runClient(host, int(port))
    os.system("pause")