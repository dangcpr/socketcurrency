import requests
import json
import schedule
import time
import socket
import tkinter as tk



def getData(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def Interface_for_Client():





    
if __name__=="__main__":
    #data()
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname_ex(hostname)
    print(hostname)
    print(local_ip)
    Interface_for_Client()
