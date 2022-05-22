# import socket

# HOST = "127.0.0.1"  # loopback
# SERVER_PORT = 56789
# FORMAT = "utf8"

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# print("*****CLIENT*****")

# try:
#     client.connect((HOST, SERVER_PORT))
#     print("Client address:", client.getsockname())

#     msg = None
#     while(msg != "x"):
#         msg = input("talk: ")
#         client.sendall(bytes(msg, FORMAT))
#         msg = client.recv(1024).decode(FORMAT)
#         print("server response:",msg)
# except:
#     print("Error")
# input()


# client.close()

import socket
import datetime
PORT=12345
FORMAT="utf8"

def send_list(client,list):
    for item in list:
        client.sendall(item.encode(FORMAT))

        client.recv(1024)
    x="x"
    client.send(x.encode(FORMAT))

def sign_up(client):
    print("SIGN UP")
    account=[]
    username=input("username:")
    account.append(username)
    password=input("password:")
    account.append(password)
    send_list(client,account)
    msg=client.recv(1024).decode(FORMAT)
    print(msg)

def login(client):    
    print("LOGIN:")
    account=[]
    username=input("username:")
    account.append(username)
    password=input("password:")
    account.append(password)
    send_list(client,account)
    accept = client.recv(1024).decode(FORMAT)
    client.sendall(accept.encode(FORMAT))
    msg=client.recv(1024).decode(FORMAT)
    print(msg)
    return accept
        
def input_date():
    while True:
        print("- DATE:")
        date=[]
        day=input("Input Day:")
        date.append(day)
        month=input("Input Month:")
        date.append(month)
        year=input("Input Year:")
        date.append(year)
        correctDate = None
        try:
            newDate = datetime.date(int(year),int(month),int(day))
            correctDate = True
        except ValueError:
            correctDate = False
        if(datetime.datetime(int(year),int(month),int(day)) > datetime.datetime.now()):
            correctDate = False
        if(correctDate==True):
            send_list(client,date)
            break
    return date

def search(client):
    print("SEARCH:")
    while True:
        print("1.Tra cuu theo ngay:")
        print("2.Tra cuu theo loai:")
        print("3.Tra cuu theo ngay va loai:")
        print("4.Dang xuat")
        choice=input("Choice:")
        client.sendall(choice.encode(FORMAT))
        client.recv(1024)
        if(choice=='1'):
            date=[]
            date=input_date()
            msg=client.recv(1024).decode(FORMAT)
            print(msg)
            
        if(choice=='2'):
            print("- TYPE:")
            type=input("input type:")
            client.sendall(type.encode(FORMAT))
            msg=client.recv(1024).decode(FORMAT)
            print(msg)
        if(choice=='3'):
            date=[]
            date=input_date()
            print("- TYPE:")
            type=input("input type:")
            client.sendall(type.encode(FORMAT))
            msg=client.recv(1024).decode(FORMAT)
            print(msg)

        input()
        if(choice=='4'):
            break
    

def handle_login(client):
    while True: 
        print("1.Sign up")
        print("2.Login")
        print("3.Quit")
        choose=input("Choose:")
        client.sendall(choose.encode(FORMAT)) 
        client.recv(1024)  
        if (choose=='1'):
            sign_up(client)
        if (choose=='2'):
           accept = login(client)
           if(accept=="true"):
               search(client)            
        if(choose=='3'):
            break
        
           



 #----------------main-----------------       
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("---------------------CLIENT-----------------")
ip_server=input("IP SERVER: ")
try:
    client.connect( (ip_server,PORT) )
    print("client address:",client.getsockname())
    handle_login(client)
except:
    print("Connect failed !!! ")  

input()
client.close()