import time
from datetime import date
ngay = str(date.today())
print(ngay)
from datetime import datetime
updated = str(datetime.now())
print(updated)
import datetime

x = datetime.datetime.now()

print(x.year)
print(x.strftime("%A"))
# start_time = time.time()
# seconds = 3

# while True:
#     current_time = time.time()
#     elapsed_time = current_time - start_time

#     if elapsed_time > seconds:
#         print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
#         start_time = current_time;

