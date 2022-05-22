import requests
import json
import pyodbc
import datetime
import time
from datetime import datetime

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


url = "https://www.dongabank.com.vn/exchange/export"

response = requests.get(url)
decoded_data = response.content.decode('utf-8')

decoded_data = parse_string(decoded_data)
data = json.loads(decoded_data)
print(type(data))
print(data[0]["type"])
a = datetime.now()
print(a)
i = 0
while True:
    try:
        connt = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=DESKTOP-AFM14RQ\ANHTUAN; Database=TH_Socket; UID=AnhTuan; PWD=TuanNguyenAnh1811')
        cursor = connt.cursor()
        type = data[i]["type"]
        imageurl = data[i]["imageurl"]
        muatienmat = data[i]["muatienmat"]
        muack = data[i]["muack"]
        bantienmat = data[i]["bantienmat"]
        banck = data[i]["banck"]
        from datetime import date
        ngay = date.today()
        updated = datetime.now()
        cursor.execute("insert DATA values (?,?,?,?,?,?,?,?)", type, imageurl, muatienmat, muack, bantienmat, banck, ngay, updated)
        i += 1
        cursor.commit()
    except:
        break

