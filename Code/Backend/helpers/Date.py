from datetime import date, datetime
from datetime import timedelta
import threading

def deltatime(FutureDate):
    return((FutureDate - datetime.now()).total_seconds())

def pushbutton():
    print("button pressed on ", str(datetime.now()))

futuredate = datetime.strptime("6/06/21 00:50:00", "%d/%m/%y %H:%M:%S")
print(deltatime(futuredate))
threading.Timer(deltatime(futuredate), pushbutton).start()