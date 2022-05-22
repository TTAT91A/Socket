import pyodbc
import datetime
import json
import requests
import time


url = "https://www.dongabank.com.vn/exchange/export"
mySQL = 'DRIVER={ODBC Driver 17 for SQL Server}; SERVER=DESKTOP-AFM14RQ\ANHTUAN; Database=TH_Socket; UID=AnhTuan; PWD=TuanNguyenAnh1811'


def readGoldDataSQL():
    connt = pyodbc.connect(mySQL)
    cursor = connt.cursor()
    cursor.execute("select * from DATA")
    data = cursor.fetchall()
    return data


def parse_string(str):
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


def get_data(url):
    response = requests.get(url)
    decoded_data = response.content.decode('utf-8')

    decoded_data = parse_string(decoded_data)
    data = json.loads(decoded_data)
    i = 0
    while True:
        try:
            connt = pyodbc.connect(mySQL)
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
            cursor.execute("insert DATA values (?,?,?,?,?,?,?,?)", type,
                           imageurl, muatienmat, muack, bantienmat, banck, ngay, updated)
            i += 1
            cursor.commit()
        except:
            break


def output_value(data, i):
    print(data[i][0], "|", data[i][1], "|", data[i][2], "|", data[i][3], "|", data[i][4], "|", data[i]
                      [5], "|", data[i][6], "|", data[i][7])


# lọc xem cột ngày có tổng cộng bao nhiêu ngày
def filterDate(data):
    listDate = []
    connt = pyodbc.connect(mySQL)
    cursor = connt.cursor()
    for row in data:
        if row.thoigian not in listDate:
            listDate.append(row.thoigian)
    return listDate


def checkDate(listDate, date):
    if date in listDate:
        return True
    else:
        return False


def searchDate(data, listDate, date, newData):
    i = 0
    if checkDate(listDate, date) == True:
        for data[i] in data:
            if data[i][6] == date:
                newData.append(data[i])
            i += 1
        return newData
    else:
        return False


def filterType(data):
    listType = []
    connt = pyodbc.connect(mySQL)
    cursor = connt.cursor()
    for row in data:
        if row.type not in listType:
            listType.append(row.type)
    return listType


def checkType(listType, type_search):
    if type_search in listType:
        return True
    else:
        return False


def searchType(data, listType, type_search, newData):
    i = 0
    if checkType(listType, type_search) == True:
        for data[i] in data:
            if data[i][0] == type_search:
                newData.append(data[i])
            i += 1
        return newData
    else:
        return False


def search_Date_and_Type(data, listDate, listType, date, type_search, newData):
    i = 0
    if checkDate(listDate, date) == True and checkType(listType, type_search) == True:
        for data[i] in data:
            if (data[i][0] == type_search) and (data[i][6] == date):
                newData.append(data[i])
            i += 1
        return newData
    else:
        return False


def delete_old_data(date):
    connt = pyodbc.connect(mySQL)
    cursor = connt.cursor()
    cursor.execute("delete from DATA where thoigian=?", date)
    connt.commit()


def updateData(listDate):
    start_time = time.time()
    seconds = 30

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        current_date = datetime.date.today()
        if (elapsed_time > seconds) or (current_time == start_time):
            if checkDate(listDate, current_date) == True:
                delete_old_data(current_date)
            get_data(url)
            print("Finished iterating in: " +
                  str(int(elapsed_time)) + " seconds")
            start_time = current_time


# ------------------------main----------------------
get_data(url)
data = readGoldDataSQL()
listDate = filterDate(data)
listType = filterType(data)

day = 15
month = 12
year = 2021

i = 0
newData = []
newData = searchDate(data, listDate, datetime.date(
    int(year), int(month), int(day)), newData)
if (newData == False):
    print("Khong ton tai ngay can tim")
else:
    # In giá trị
    while(i < len(newData)):
        print(i+1, "|", end=" ")
        output_value(newData, i)
        i += 1


type_Search = "AUD"
newData1 = []
newData1 = searchType(data, listType, type_Search, newData1)
# In giá trị
i = 0
if (newData1 == False):
    print("Khong ton tai type can tim")
else:
    # In giá trị
    while(i < len(newData1)):
        print(i+1, "|", end=" ")
        output_value(newData1, i)
        i += 1

newData2 = []
newData2 = search_Date_and_Type(data, listDate, listType, datetime.date(
    int(year), int(month), int(day)), type_Search, newData2)
# In giá trị
i = 0
if (newData2 == False):
    print("Khong ton tai")
else:
    # In giá trị
    while(i < len(newData2)):
        print(i+1, "|", end=" ")
        output_value(newData2, i)
        i += 1












# start_time = time.time()
# seconds = 30

# while True:
#     current_time = time.time()
#     elapsed_time = current_time - start_time
#     current_date = datetime.date.today()
#     # -----------------

#     # -------------------
#     while True:
#         if checkDate(listDate, current_date) == True:
#             delete_old_data(current_date)
       
#         get_data(url)
#         data = readGoldDataSQL()
#         listDate = filterDate(data)
#         listType = filterType(data)
#         while True:
#             day = int(input())
#             month = int(input())
#             year = int(input())

#             i = 0
#             newData = []
#             newData = searchDate(data, listDate, datetime.date(
#                 int(year), int(month), int(day)), newData)
#             if (newData == False):
#                 print("Khong ton tai ngay can tim")
#             else:
#                 # In giá trị
#                 while(i < len(newData)):
#                     print(i+1, "|", end=" ")
#                     output_value(newData, i)
#                     i += 1

#             type_Search = "AUD"
#             newData1 = []
#             newData1 = searchType(data, listType, type_Search, newData1)
#             # In giá trị
#             i = 0
#             if (newData1 == False):
#                 print("Khong ton tai type can tim")
#             else:
#                 # In giá trị
#                 while(i < len(newData1)):
#                     print(i+1, "|", end=" ")
#                     output_value(newData1, i)
#                     i += 1

#             newData2 = []
#             newData2 = search_Date_and_Type(data, listDate, listType, datetime.date(
#                 int(year), int(month), int(day)), type_Search, newData2)
#             # In giá trị
#             i = 0
#             if (newData2 == False):
#                 print("Khong ton tai")
#             else:
#                 # In giá trị
#                 while(i < len(newData2)):
#                     print(i+1, "|", end=" ")
#                     output_value(newData2, i)
#                     i += 1
#             if (elapsed_time > seconds) or (current_time == start_time):
#                 break

#         print("Finished iterating in: " +
#               str(int(elapsed_time)) + " seconds")
#         start_time = current_time





# get_data(url)
# data = readGoldDataSQL()
# listDate = []
# listType = []

# while True:
#     updateData(listDate)
#     data = readGoldDataSQL()
#     listDate = filterDate(data)
#     listType = filterType(data)
#     day = int(input())
#     month = int(input())
#     year = int(input())

#     i = 0
#     newData = []
#     newData = searchDate(data, listDate, datetime.date(
#         int(year), int(month), int(day)), newData)
#     if (newData == False):
#         print("Khong ton tai ngay can tim")
#     else:
#         # In giá trị
#         while(i < len(newData)):
#             print(i+1, "|", end=" ")
#             output_value(newData, i)
#             i += 1

#     type_Search = "AUD"
#     newData1 = []
#     newData1 = searchType(data, listType, type_Search, newData1)
#     # In giá trị
#     i = 0
#     if (newData1 == False):
#         print("Khong ton tai type can tim")
#     else:
#         # In giá trị
#         while(i < len(newData1)):
#             print(i+1, "|", end=" ")
#             output_value(newData1, i)
#             i += 1

#     newData2 = []
#     newData2 = search_Date_and_Type(data, listDate, listType, datetime.date(
#         int(year), int(month), int(day)), type_Search, newData2)
#     # In giá trị
#     i = 0
#     if (newData2 == False):
#         print("Khong ton tai")
#     else:
#         # In giá trị
#         while(i < len(newData2)):
#             print(i+1, "|", end=" ")
#             output_value(newData2, i)
#             i += 1

