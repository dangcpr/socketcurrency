import requests
import json
import schedule
import time
import socket
import tkinter as tk



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


    
if __name__=="__main__":
    #data()
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname_ex(hostname)
    print(hostname)
    print(local_ip)
    #createInterface()

