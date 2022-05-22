import pyodbc
import datetime


def readGoldDataSQL():
    connt = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server}; SERVER=DESKTOP-AFM14RQ\ANHTUAN; Database=MMT_Socket; UID=AnhTuan; PWD=TuanNguyenAnh1811')
    cursor = connt.cursor()
    cursor.execute("select * from DU_LIEU_VALUE")
    data = cursor.fetchall()
    return data


def output_value(data, i):
    print(data[i][1], "|", data[i][2], "|", data[i][3], "|", data[i][4], "|", data[i]
                      [5], "|", data[i][6], "|", data[i][7], "|", data[i][8], "|", data[i][9])


# lọc xem cột ngày có tổng cộng bao nhiêu ngày
def filterDate(data):
    listDate = []
    connt = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server}; SERVER=DESKTOP-AFM14RQ\ANHTUAN; Database=MMT_Socket; UID=AnhTuan; PWD=TuanNguyenAnh1811')
    cursor = connt.cursor()
    for row in data:
        if row.day not in listDate:
            listDate.append(row.day)
    return listDate


def searchDate(data, listDate, date, newData):
    i = 0
    if date in listDate:
        for data[i] in data:
            if data[i][6] == date:
                #output_value(data, i)
                newData.append(data[i])
            i += 1
        return newData
    else:
        return False


def filterType(data):
    listType = []
    connt = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server}; SERVER=DESKTOP-AFM14RQ\ANHTUAN; Database=MMT_Socket; UID=AnhTuan; PWD=TuanNguyenAnh1811')
    cursor = connt.cursor()
    for row in data:
        if row.type not in listType:
            listType.append(row.type)
    return listType


def searchType(data, listType, type_search, newData):
    i = 0
    if type_search in listType:
        for data[i] in data:
            if data[i][8] == type_search:
                newData.append(data[i])
            i += 1
        return newData
    else:
        print("Khong ton tai type can tim")


def search_Date_and_Type(data, listDate, listType, date, type_search, newData):
    i = 0
    if (date in listDate) and (type_search in listType):
        for data[i] in data:
            if (data[i][8] == type_search) and (data[i][6] == date):
                newData.append(data[i])
            i += 1
        return newData
    else:
        print("Khong thoa man")


# ------------------------main----------------------
data = readGoldDataSQL()
listDate = filterDate(data)
listType = filterType(data)

day = 8
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

type_Search = "SJC"
newData1 = []
newData1 = searchType(data, listType, type_Search, newData1)
# In giá trị
i = 0
while(i < len(newData1)):
    print(i, "|", end=" ")
    output_value(newData1, i)
    i += 1

newData2 = []
newData2 = search_Date_and_Type(data, listDate, listType, datetime.date(
    int(year), int(month), int(day)), type_Search, newData2)

# # In giá trị
# i = 0
# while(i < len(newData2)):
#     print(i+1, "|", end=" ")
#     output_value(newData2, i)
#     i += 1
