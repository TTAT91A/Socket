# import socket
# import pyodbc

# HOST = "127.0.0.1"  # loopback
# SERVER_PORT = 56789
# FORMAT = "utf8"

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# s.bind((HOST, SERVER_PORT))
# s.listen()

# print("*****SERVER*****")
# print("server", (HOST, SERVER_PORT))
# print("Waiting for client")

# try:
#     conn, addr = s.accept()
#     print("Client address:", addr)
#     print("conn:", conn.getsockname())

#     msg = None
#     while(msg != "x"):
#         msg = conn.recv(1024).decode(FORMAT)
#         print("client", addr, "says", msg)
#         msg = input("server response: ")
#         conn.sendall(bytes(msg,FORMAT))
# except:
#     print("Error")
# input()

import socket
import threading
import pyodbc

HOST="127.0.0.1"
PORT=12345
FORMAT="utf8"

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)
def recv_list(conn):
    list=[]
    item=conn.recv(1024).decode(FORMAT)
    while (item !="x"):
        conn.sendall(item.encode(FORMAT))
        list.append(item)
        item=conn.recv(1024).decode(FORMAT)
    return list


def check_account(account):
    connt=pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=LAPTOP-OB4QSGQ1\SQLEXPRESS; Database=DA_MMT_Socket; UID=TuTrinh; PWD=123456')
    cursor=connt.cursor()
    cursor.execute("select * from Account where username = ?",account[0])
    data=cursor.fetchall() #check user name
    cursor.commit()
    if(data==[]):
        return 0       #check tai khoan co ton tai hay khong
    elif(account[1]==data[0][1]):
        return "true"        #check password
    return "false"

def sign_up(conn):
    account=[]
    account=recv_list(conn)
    accept=check_account(account)
    if accept== 0:
        print("username:",account[0],"accepted !")
        msg="Sign up successfully !!"
        conn.sendall(msg.encode(FORMAT))
        connt=pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=LAPTOP-OB4QSGQ1\SQLEXPRESS; Database=DA_MMT_Socket; UID=TuTrinh; PWD=123456')
        cursor=connt.cursor()
        username=account[0]
        password=account[1]
        cursor.execute("insert Account values (?,?)", username, password)
        cursor.commit()
    else:
        print("username:",account[0],"not accepted !")
        msg="Sign up failed !!"
        conn.sendall(msg.encode(FORMAT))

def login(conn):
    account=[]
    account=recv_list(conn)
    accept=check_account(account)
    if(accept==0):
        accept="false"
    conn.sendall(accept.encode(FORMAT))
    conn.recv(1024)
    if(accept=="true"):
        print("user:",account[0]," login successfully !!")
        msg="Login successfully !!"       
    else:
        print("user:",account[0]," login failed!!")
        msg="Login failed !!"       
    conn.sendall(msg.encode(FORMAT))

    
def handle_client(conn,addr):
    print("client address:",addr)
    print("connect:",conn.getsockname())
    try:
        choose=conn.recv(1024).decode(FORMAT)
        conn.sendall(choose.encode(FORMAT))
        while (choose=='1'):
            print("SIGN UP")
            sign_up(conn)
            choose=conn.recv(1024).decode(FORMAT)
            conn.sendall(choose.encode(FORMAT))
        accept = "false"
        while(choose=='2' and (accept=="false")):  
            print("LOGIN:")  
            login(conn)
            choose=conn.recv(1024).decode(FORMAT)
            conn.sendall(choose.encode(FORMAT)) 
            accept=conn.recv(1024).decode(FORMAT)
    except:
        print("client address:",addr,"disconnected!!!")
        conn.close()



print("---------------------SERVER-----------------")
print("IP SERVER:",HOST)
print("PORT SERVER:",PORT)
try:
    print(HOST)
    print("Waiting for Client")
    while True:
        conn, addr = s.accept()
        clientThread = threading.Thread(target=handle_client, args=(conn,addr))
        clientThread.daemon = True 
        clientThread.start()
        
        #handle_client(conn, addr)
except KeyboardInterrupt:
    s.close()
    print("error")   
   
finally: 
    s.close()  
    print("end")

input()

