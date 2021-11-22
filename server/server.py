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
def createInterface():
    root = tk.Tk()
    root.title("Currency Converter")
    root.geometry("300x300")
    root.resizable(False, False)
    root.configure(background='#f2f2f2')
    label = tk.Label(root, text="Currency Converter", font=("Helvetica", 16), bg="#f2f2f2")
    label.pack()
    label = tk.Label(root, text="Enter amount:", font=("Helvetica", 12), bg="#f2f2f2")
    label.pack()
    amount = tk.Entry(root)
    amount.pack()
    label = tk.Label(root, text="From:", font=("Helvetica", 12), bg="#f2f2f2")
    label.pack()
    from_ = tk.Entry(root)
    from_.pack()
    label = tk.Label(root, text="To:", font=("Helvetica", 12), bg="#f2f2f2")
    label.pack()
    to_ = tk.Entry(root)
    to_.pack()
    button = tk.Button(root, text="Convert", command=lambda: convert(amount.get(), from_.get(), to_.get()))
    button.pack()
    root.mainloop()
    
if __name__=="__main__":
    #data()
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname_ex(hostname)
    print(hostname)
    print(local_ip)
    createInterface()

