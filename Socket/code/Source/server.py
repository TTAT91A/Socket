import socket
import threading
import pyodbc
from datetime import date
import datetime
import json
import requests
import time
from tkinter import *
from tkinter.messagebox import ERROR
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox


HOST="127.0.0.1"
PORT=65432
FORMAT="utf8"
url="https://www.dongabank.com.vn/exchange/export"
MySQL="DRIVER={ODBC Driver 17 for SQL Server}; SERVER=LAPTOP-OB4QSGQ1\SQLEXPRESS; Database=DA_MMT_Socket; UID=TuTrinh; PWD=123456"

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)

root=tk.Tk()
root.title("SEVER")
root.geometry("700x500")

def send_list_data(conn,list): #hàm gửi danh sách 2 chiều
    for item in list:
        for item2 in item:
            if(item2==''):
                item2="$$$$$$"
            conn.sendall(item2.encode(FORMAT))
            conn.recv(1024)
        conn.sendall("end".encode(FORMAT))
        conn.recv(1024)      
    conn.send("x".encode(FORMAT))

def recv_list(conn): # hàm gửi danh sách 1 chiều
    list=[]
    item=conn.recv(1024).decode(FORMAT)
    while (item !="x"):
        conn.sendall(item.encode(FORMAT))
        list.append(item)
        item=conn.recv(1024).decode(FORMAT)
    return list



def check_account(account): # kiểm tra tài khoản đã tồn tại hay chưa 
    connt=pyodbc.connect(MySQL)
    cursor=connt.cursor()
    cursor.execute("select * from Account where username = ?",account[0])
    data=cursor.fetchall() 
    if(data==[]):
        return 0       
    elif(account[1]==data[0][1]):
        return "true"       
    return "false"


def sign_up(conn): # đăng kí 
    account=[]
    account=recv_list(conn)
    accept=check_account(account)
    if accept== 0:
        print("username:",account[0],"accepted !")
        msg="true"
        conn.sendall(msg.encode(FORMAT))
        connt=pyodbc.connect(MySQL)
        cursor=connt.cursor()
        username=account[0]
        password=account[1]
        cursor.execute("insert Account values (?,?)", username, password)
        cursor.commit()
    else:
        print("Tài khoản",account[0],"đăng kí không thành công !")
        msg= "false"
        conn.sendall(msg.encode(FORMAT))
    return accept
def login(conn):  # đăng nhập
    account=[]
    account=recv_list(conn)
    accept=check_account(account)
    if(accept==0):
        accept="false"
    conn.sendall(accept.encode(FORMAT))
    conn.recv(1024)
    if(accept=="true"):
        print("Tài khoản",account[0]," đã đăng nhập!!")
        msg="Đăng nhập thành công !!"       
    else:
        print("user:",account[0]," login failed!!")
        msg="Tên đăng nhập hoặc mật khẩu không đúng !!"       
    conn.sendall(msg.encode(FORMAT))
    return accept

def parse_string(str): # xử lý dữ liệu từ web
    i = 0
    while i < len(str):
        if str[i] != '[':
            str = str[1:]
        else:
            break
    while i < len(str):
        if str[len(str) - 1] != ']':
            str = str[:-1]
        else:
            break
    return str


def get_data(url): # lấy dữ liệu từ web và lưu vào cơ sở dữ liệu
    try: 
        response = requests.get(url)
        decoded_data = response.content.decode('utf-8')
        decoded_data = parse_string(decoded_data)
        data = json.loads(decoded_data)
        i = 0
        while True:
            try:
                connt = pyodbc.connect(MySQL)
                cursor = connt.cursor()
                type = data[i]["type"]
                imageurl = data[i]["imageurl"]
                muatienmat = data[i]["muatienmat"]
                muack = data[i]["muack"]
                bantienmat = data[i]["bantienmat"]
                banck = data[i]["banck"]
                from datetime import date
                ngay = str(date.today())
                from datetime import datetime
                updated = str(datetime.now())
                cursor.execute("insert DU_LIEU_VALUE values (?,?,?,?,?,?,?,?)", type,
                            imageurl, muatienmat, muack, bantienmat, banck, ngay, updated)
                i += 1
                cursor.commit()
            except:
                break
    except:
        messagebox.showerror("Error"," Không thể lấy dữ liệu từ web !!!")





def find_data_type(type): # tìm kiếm theo loại vàng
    connt = pyodbc.connect(MySQL)
    cursor = connt.cursor()
    cursor.execute("select * from DU_LIEU_VALUE where type = ?",type)
    data=cursor.fetchall()
    return data

def find_data_date(date): #tìm kiếm theo ngày tháng năm
    connt = pyodbc.connect(MySQL)
    cursor = connt.cursor()
    cursor.execute("select * from DU_LIEU_VALUE where thoigian = ?",date)
    data=cursor.fetchall()
    return data

def find_data_date_type(date,type): # tìm kiếm theo ngày và loại
    connt = pyodbc.connect(MySQL)
    cursor = connt.cursor()
    cursor.execute("select * from DU_LIEU_VALUE where type=? and thoigian= ?",type,date)
    data=cursor.fetchall()
    return data

def delete_old_data(date): # hàm xóa dữ liệu cùng ngày trước khi cập nhật
    connt = pyodbc.connect(MySQL)
    cursor = connt.cursor()
    cursor.execute("delete from DU_LIEU_VALUE where thoigian=?", date)
    connt.commit()
  

def updateData(): # hàm cập nhật dữ liệu
    from datetime import date
    date =str(date.today())
    start_time = time.time()
    seconds = 30*60
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        current_date = datetime.date.today()

        if (elapsed_time > seconds) or (current_time == start_time):
            if find_data_date(date) != []:
                delete_old_data(str(current_date))
            get_data(url)
            print("Finished iterating in: " +
                str(int(elapsed_time)) + " seconds")
            start_time = current_time
      
       
 
def handle_client(conn,addr): # hàm xử lý yêu cầu của client
    print("client address:",addr)
    print("connect:",conn.getsockname())
    try:
         while True:
            choose=conn.recv(1024).decode(FORMAT)
            conn.sendall(choose.encode(FORMAT))
            if (choose=='SIGNUP'):
                sign_up(conn)
            if(choose=='LOGIN'):  
                login(conn)

            if(choose=='DATE'):
                date=conn.recv(1024).decode(FORMAT)
                newData = []
                newData = find_data_date(date)
                send_list_data(conn,newData)
            if(choose=='TYPE'):
                type=conn.recv(1024).decode(FORMAT)
                newData1 = []
                newData1 = find_data_type(type)
                send_list_data(conn,newData1)
            if(choose=='DATE_TYPE'):
                date=conn.recv(1024).decode(FORMAT)
                conn.sendall(date.encode(FORMAT))
                type=conn.recv(1024).decode(FORMAT)
                newData2 = []
                newData2 = find_data_date_type(date,type)
                send_list_data(conn,newData2)
            if(choose=='QUIT'):
                ip=addr[0]
                port=addr[1]
                tt="Đã ngắt kết nối"
                root.tr.insert("",0,text=0,values=(ip,port,tt))
                conn.close()
                break

    except:
        ip=addr[0]
        port=addr[1]
        tt="Đã ngắt kết nối"
        root.tr.insert("",0,text=0,values=(ip,port,tt))
        conn.close()


print("---------------------SERVER-----------------")
print("IP SERVER:",HOST)
print("PORT SERVER:",PORT)


class App(tk.Tk): # giao diện
    def __init__(master,self): 

        ttitle=tk.Label(self,text='SEVER',font=("time new roman",20,"bold"),foreground="red")
        ttitle.pack()

        # bang 1
        a=tk.Frame(self,borderwidth=4,relief=RIDGE)
        a.place(x=10,y=50,width=700,height=100)
           
        # Cột đầu tiên
        ipserver=tk.Label(a,text="IP SERVER:" + HOST,font=("time new roman",13,"bold"),foreground="red")
        ipserver.grid()
        port=tk.Label(a,text='PORT:'+ str(PORT) ,font=("time new roman",13,"bold"),foreground="red")
        port.grid(sticky='w')
        list_client=tk.Label(a,text='CLIENT:' ,font=("time new roman",13,"bold"),foreground="red")
        list_client.grid(sticky='w')
        # bang 2
        self.b=tk.Frame(self,borderwidth=4,relief=RIDGE)
        self.b.place(x=10,y=150,width=700,height=300)
        self.xsbr=ttk.Scrollbar(self.b,orient='horizontal')
        self.ysbr=ttk.Scrollbar(self.b,orient='vertical')
        self.tr=ttk.Treeview(self.b,columns=('1','2','3'),xscrollcommand=self.xsbr.set,yscrollcommand=self.ysbr.set)
        self.xsbr.pack(side=BOTTOM,fil='x')
        self.ysbr.pack(side=RIGHT,fil='y')
        self.xsbr.config(command=self.tr.xview)
        self.ysbr.config(command=self.tr.yview)
        self.tr.heading('1',text="IP")
        self.tr.heading('2',text='Port')
        self.tr.heading('3',text='TRẠNG THÁI')
        self.tr['show']='headings'
        self.tr.column('1',width=200,anchor=CENTER)
        self.tr.column('2',width=200,anchor=CENTER)
        self.tr.column('3',width=300,anchor=CENTER)
        self.tr.pack()
        c=tk.Frame(self.b)
        c.place(x=250,y=240,width=700,height=30)
        Button1=tk.Button(c,text='Stop',font=("time new roman",10,"bold"),command=lambda: quit())
        Button1.pack()
    
def runServer(): # hàm xử lý kết nối đa luồng
    try:
        while True:
            conn, addr = s.accept()
            ip=addr[0]
            port=addr[1]
            tt="Đang hoạt động"
            root.tr.insert("",0,text=0,values=(ip,port,tt))
            clientThread = threading.Thread(target=handle_client, args=(conn,addr))
            clientThread.daemon = True 
            clientThread.start()
    except:
        s.close()

def quit(): # hàm thoát khoỉ chương trình
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        s.close()
        
# xử lý update dữ liệu bằng 1 luồng 
Thread_update=threading.Thread(target=updateData)
Thread_update.daemon = True
Thread_update.start()
# xử lý đa tiến trình
clientThread = threading.Thread(target=runServer)
clientThread.daemon = True 
clientThread.start()


app=App(root)
root.mainloop()


