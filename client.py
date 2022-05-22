import socket
import datetime
import tkinter as tk
import tkinter.messagebox as mbox
from tkinter import ttk
from tkinter.constants import BOTH, BOTTOM, COMMAND, GROOVE, RIDGE, RIGHT, TOP, TRUE
from tkinter.ttk import*
from tkinter import*

PORT=65432
FORMAT="utf8"

def send_list(client,list): #hàm nhận danh sách 1 chiều
    for item in list:
        client.sendall(item.encode(FORMAT))

        client.recv(1024)
    x="x"
    client.sendall(x.encode(FORMAT))

def recv_list_data(client): # hàm nhận 1 danh sách 2 chiều
    list_data=[]
    while (True):
        list=[]
        while(True):
            item = client.recv(1024).decode(FORMAT)
            client.sendall(item.encode(FORMAT))
            if(item=='end'or item=='x'):
                break
            list.append(item)
        if(item=='x'):
            break
        list_data.append(list)
       
    return list_data

        
def check_date(day,month,year): #hàm kiểm tra ngày có hợp lệ hay không
    correctDate = None
    try:
        newDate = datetime.date(int(year),int(month),int(day))
        correctDate = True
    except ValueError:
        correctDate = False
    if(correctDate==True):
        if(datetime.datetime(int(year),int(month),int(day)) > datetime.datetime.now()):
            correctDate = False

    return correctDate

class ConnectFrame(tk.Frame): #giao diện kết nối 
     def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)
        labName = tk.Label(self,text="CONNECT",font=("Arial",15,"italic"),foreground="red")
        label_ip = tk.Label(self, text="IP SERVER")
        
        self.entry_ip = tk.Entry(self,width=20,bg='light yellow')
        self.label_notice = tk.Label(self,text="",font=("Arial",10,"italic"),foreground="red")
        
        button_connect= tk.Button(self,text="CONNECT",command=lambda: connect(ConnectFrame) )     
        button_connect.configure(width=10)
        labName.pack()
        label_ip.pack()
        self.label_notice.pack()
        self.entry_ip.pack()
        button_connect.pack()


class StartPage(tk.Frame): # giao diện đăng nhập
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)
        labName = tk.Label(self,text="ĐĂNG NHẬP",font=("Arial",15,"italic"),foreground="red")
        label_user = tk.Label(self, text="Tài Khoản ")
        label_pswd = tk.Label(self, text="Mật Khẩu ")
        
        self.entry_user = tk.Entry(self,width=20,bg='light yellow')
        self.entry_pswd = tk.Entry(self,width=20,bg='light yellow',show='*')
        self.label_notice = tk.Label(self,text="",font=("Arial",10,"italic"),foreground="red")
        
        button_log = tk.Button(self,text="Đăng Nhập",command=lambda: appController.logIn(self,client) ) 
        button_dangki=tk.Button(self,text="Đăng ký",command=lambda: appController.showPage(HomePage))
        button_quit=tk.Button(self,text="Thoát ",command=lambda: appController.quit(client))

        button_log.configure(width=10)
        button_dangki.configure(width=10)
        button_quit.configure(width=10)

        labName.pack()
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        self.label_notice.pack()
        button_log.pack()
        button_dangki.pack()
        button_quit.pack()

class HomePage(tk.Frame): #giao diện đăng kí
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="ĐĂNG kÝ",font=("Arial",15,"italic"),foreground="red")
        label_tk=tk.Label(self,text="Tài Khoản")
        label_mk=tk.Label(self,text="Mật Khẩu")
        label_mkk=tk.Label(self,text="Nhập lại mật khẩu")
        self.entry_user = tk.Entry(self,width=20,bg='light yellow')
        self.entry_pswd = tk.Entry(self,width=20,bg='light yellow',show="*")
        self.entry_pswdd = tk.Entry(self,width=20,bg='light yellow',show="*")
        self.label_notice = tk.Label(self,text="",font=("Arial",10,"italic"),foreground="red")
        btn_logout = tk.Button(self, text="Tạo tài khoản", command=lambda: appController.signUp(self,client))
        btn_logoutt = tk.Button(self, text="Quay lại", command=lambda: appController.showPage(StartPage))
        btn_logout.configure(width=15)
        btn_logoutt.configure(width=15)

        label_title.pack() 
        label_tk.pack()
        self.entry_user.pack()
        label_mk.pack()
        self.entry_pswd.pack()
        label_mkk.pack()
        self.entry_pswdd.pack()
        self.label_notice.pack()
        btn_logout.pack()
        btn_logoutt.pack()

class SearchFrame(tk.Frame):  #giao diện tìm kiếm
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        title=tk.Label(self,text='BẢNG GIÁ VÀNG',borderwidth=10,relief=GROOVE,font=("time new roman",20,"bold"),background='yellow',foreground="red")
        title.pack(side=TOP,fill='x')
        # bang 1
        self.a=tk.Frame(self,borderwidth=4,relief=RIDGE)
        self.a.place(x=10,y=50,width=800,height=150)
        self.type_verify= StringVar()
        # Cột đầu tiên
        self.entry_search=tk.Entry(self.a)
        self.entry_search.grid(row=1,column=0,padx=10,pady=5,sticky='w')
        self.label_search=tk.Label(self.a,text='Ngày')
        self.label_search.grid(row=0,column=0,padx=10,pady=5,sticky='w')

        Button_search=tk.Button(self.a,text='Search',font=("time new roman",10,"bold"),command=lambda: appController.client_search(self,client))
        Button_search.grid(row=2,column=0,padx=10,pady=5)
        # cột thứ hai

        self.entry_search1=tk.Entry(self.a)
        self.entry_search1.grid(row=1,column=1,padx=10,pady=5,sticky='w')
        self.label_search1=tk.Label(self.a,text='Tháng')
        self.label_search1.grid(row=0,column=1,padx=10,pady=5,sticky='w')

        # cột thứ ba
        self.entry_search2=tk.Entry(self.a)
        self.entry_search2.grid(row=1,column=2,padx=10,pady=5,sticky='w')
        self.label_search2=tk.Label(self.a,text='Năm')
        self.label_search2.grid(row=0,column=2,padx=10,pady=5,sticky='w')
        
        self.label_notice = tk.Label(self,text="",font=("Arial",10,"italic"),foreground="red")
        

        # côt thứ tư
        self.search3=ttk.Combobox(self.a)
        self.search3['value']=("AUD","CAD","CHF","CNY","EUR","GBP","HKD","NZD","SGD","USD","JPY","PNJ","DAB","THB" ,"XAU")
        self.search3.grid(row=1,column=60,padx=10,pady=5,sticky='w')

        self.label_search3=tk.Label(self.a,text='Type')
        self.label_search3.grid(row=0,column=60,padx=10,pady=5,sticky='w')

        # cột thoát 
        self.thoat_buton=tk.Frame(self.a,borderwidth=4)
        self.thoat_buton.place(x=630,y=7,width=100)
        self.thoat_button1=tk.Button(self.thoat_buton,text='Đăng xuất',font=("time new roman",10,"bold"),command=lambda: appController.logout())
        self.thoat_button1.grid(row=0,column=1000,padx=10,pady=20 ,sticky='w')
        #thong bao
        self.c=tk.Frame(self,borderwidth=10)
        self.c.place(x=10,y=200,width=800,height=50)
        self.label_notice = tk.Label(self.c,text="",borderwidth=10,font=("Arial",10,"italic"),foreground="red")
        self.label_notice.pack()

        # bang 2
        self.b=tk.Frame(self,borderwidth=4,relief=RIDGE)
        self.b.place(x=10,y=250,width=800,height=400)
        self.xsbr=ttk.Scrollbar(self.b,orient='horizontal')
        self.ysbr=ttk.Scrollbar(self.b,orient='vertical')
        self.tr=ttk.Treeview(self.b,columns=('1','2','3','4','5','6','7','8'),xscrollcommand=self.xsbr.set,yscrollcommand=self.ysbr.set)
        self.xsbr.pack(side=BOTTOM,fil='x')
        self.ysbr.pack(side=RIGHT,fil='y')
        self.xsbr.config(command=self.tr.xview)
        self.ysbr.config(command=self.tr.yview)
        self.tr.heading('1',text="Type")
        self.tr.heading('2',text='Imageurl')
        self.tr.heading('3',text='Muatienmat')
        self.tr.heading('4',text='muack')
        self.tr.heading('5',text='bantienmat')
        self.tr.heading('6',text='Banck')
        self.tr.heading('7',text='thoigian')
        self.tr.heading('8',text='Update')
        self.tr['show']='headings'
        self.tr.column('1',width=100,anchor=CENTER)
        self.tr.column('2',width=100,anchor=CENTER)
        self.tr.column('3',width=100,anchor=CENTER)
        self.tr.column('4',width=100,anchor=CENTER)
        self.tr.column('5',width=100,anchor=CENTER)
        self.tr.column('6',width=100,anchor=CENTER)
        self.tr.column('7',width=100,anchor=CENTER)
        self.tr.column('8',width=100,anchor=CENTER)
        self.tr.pack()


class App(tk.Tk):
    def __init__(self): 
        tk.Tk.__init__(self)

        self.title("CLIENT")
        self.geometry("500x300")
        self.resizable(width=False, height=False)

        container = tk.Frame()
        container.configure(bg="red")

        container.pack(side="top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, HomePage,SearchFrame,ConnectFrame):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame 

        self.frames[ConnectFrame].tkraise()
    
    def showPage(self, FrameClass): # hiện giao diện
        frame = self.frames[FrameClass]
        if FrameClass==SearchFrame:
            self.geometry("800x700")
        else:
            self.geometry("500x300")
        frame.tkraise()
    
                
    def logIn(self, curFrame,sck): # đăng nhập tài khoản
        try:
            user=curFrame.entry_user.get()
            pswd=curFrame.entry_pswd.get()
            if(user==''or pswd ==''):
                curFrame.label_notice["text"] = "Tên đăng nhập hoặc mật khẩu không được để trống."
            else:
                account=[]
                sck.sendall("LOGIN".encode(FORMAT)) 
                sck.recv(1024)  
                account.append(user)
                account.append(pswd)
                send_list(sck,account)
                accept = sck.recv(1024).decode(FORMAT)
                sck.sendall(accept.encode(FORMAT))
                msg=sck.recv(1024).decode(FORMAT)
                curFrame.label_notice["text"]=msg 
                if(accept =='true'):
                    self.showPage(SearchFrame)
        except:
            mbox.showerror("Error"," Lỗi kết nối !!!")
            sck.close()
    def signUp(self,curFrame,sck): # đăng kí tài khoản
        try: 
            user=curFrame.entry_user.get()
            pswd=curFrame.entry_pswd.get()
            pswdd=curFrame.entry_pswdd.get()
            if(user==''or pswd ==''or pswdd==''):
                curFrame.label_notice["text"] = "Tên đăng nhập hoặc mật khẩu không được để trống."
            elif(pswd!=pswdd):
                curFrame.label_notice["text"] ="Mật khẩu không hợp nhau."
            else:
                account=[]
                account.append(user)
                account.append(pswd)
                sck.sendall("SIGNUP".encode(FORMAT)) 
                sck.recv(1024) 
                send_list(sck,account)
                msg=sck.recv(1024).decode(FORMAT)
                if(msg=="true"):
                    curFrame.label_notice["text"] ="Bạn đã đăng kí tài khoản thành công."
                    self.showPage(StartPage)
                else:
                    curFrame.label_notice["text"] ="Tài khoản đã tồn tại."

        except:
            mbox.showerror("Error"," Lỗi kết nối !!!")
            sck.close()
    def client_search(self,curFrame,sck): # tìm kiếm
        try:
            self.frames[SearchFrame].label_notice['text']=""
            curFrame.tr.delete(*curFrame.tr.get_children())
            day=curFrame.entry_search.get()
            month=curFrame.entry_search1.get()
            year=curFrame.entry_search2.get()
            type=curFrame.search3.get()
            newData = []
            correctDate=True
            if( (day==''or month==''or year=='') and type=='' ):
                correctDate=False
                curFrame.label_notice["text"]="Bạn chưa nhập đủ thông tin cần tìm kiếm."   
            elif(day!=''and month!=''and year!='' and type==''):
                correctDate = check_date(day,month,year)
                if(correctDate==False):
                    curFrame.label_notice["text"]="Ngày bạn cần tìm kiếm thông tin không hợp lệ."
                else:
                    sck.sendall("DATE".encode(FORMAT))
                    sck.recv(1024)
                    newDate = str(datetime.date(int(year),int(month),int(day)))
                    sck.sendall(newDate.encode(FORMAT))
                    newData=[]
                    newData=recv_list_data(sck)
                    
            elif(day ==''and month ==''and year=='' and type!=''):
                sck.sendall("TYPE".encode(FORMAT))
                sck.recv(1024)
                sck.sendall(type.encode(FORMAT))
                newData=[]
                newData=recv_list_data(sck)
            elif(day !=''and month !=''and year!='' and type!=''):
                sck.sendall("DATE_TYPE".encode(FORMAT))
                sck.recv(1024)
                newDate = str(datetime.date(int(year),int(month),int(day)))
                sck.sendall(newDate.encode(FORMAT))
                sck.recv(1024)
                sck.sendall(type.encode(FORMAT))
                newData = []
                newData=recv_list_data(sck)
            if(correctDate==True):
                if(newData==[]):
                    curFrame.label_notice["text"]="Không tồn tại thông tin bạn cần tìm kiếm."  
                else:
                    i=0
                    curFrame.label_notice["text"]="" 
                    while True:
                        try:
                            type = newData[i][0]
                            imageurl = newData[i][1]
                            muatienmat = newData[i][2]
                            muack = newData[i][3]
                            bantienmat = newData[i][4]
                            banck = newData[i][5]
                            ngay = newData[i][6]
                            updated = newData[i][7]
                            curFrame.tr.insert("",i,text=i,values=(type,imageurl,muatienmat,muack,bantienmat,banck,ngay,updated))
                            i+=1
                        except:
                            break
                sck.recv(1024)
        except:
            mbox.showerror("Error"," Lỗi kết nối !!!")
            sck.close()
    def logout(self):  # Đăng xuất 
        self.frames[StartPage].entry_user.delete(0,'end')
        self.frames[StartPage].entry_pswd.delete(0,'end')
        self.frames[StartPage].label_notice['text']=""
        self.frames[SearchFrame].entry_search.delete(0,'end')
        self.frames[SearchFrame].entry_search1.delete(0,'end')
        self.frames[SearchFrame].entry_search2.delete(0,'end')
        self.frames[SearchFrame].search3.delete(0,'end')
        self.frames[SearchFrame].label_notice['text']=""
        self.frames[SearchFrame].tr.delete(*self.frames[SearchFrame].tr.get_children())
        self.showPage(StartPage)
    def quit(self,sck): # Thoát khỏi chương trình 
        if mbox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            sck.sendall("QUIT".encode(FORMAT))
            sck.recv(1024)
            client.close()
            

#---------------------main--------------------------------------      

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
app = App()
def connect(curFrame):
    ip_server=app.frames[curFrame].entry_ip.get()
    if(ip_server==''):
        app.frames[curFrame].label_notice["text"] ="Bạn chưa nhập địa chỉ IP của Server."
    else:
        try:
            client.connect( (ip_server,PORT))
            app.showPage(StartPage)
        except:
            app.frames[curFrame].label_notice["text"]="Không thể kết nối được đến Server."

try:
    app.showPage(ConnectFrame)
    app.mainloop()
except:
    client.close()