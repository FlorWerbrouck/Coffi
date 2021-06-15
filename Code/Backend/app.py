import time
from RPi import GPIO
import threading
import eventlet
eventlet.monkey_patch()

from helpers.HC204 import HC204
from helpers.WS2812b import WS2812b
from helpers.MCP import MCP
from helpers.Coffee import Coffee
from helpers.DS18B20 import DS18B20

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify
from repositories.DataRepository import DataRepository
from datetime import date, datetime
from datetime import timedelta

distancesensor = HC204()
leds = WS2812b()
LDR = MCP()
knop = Coffee()
temp = DS18B20()
CoffeePlanned = False

# Code voor Hardware
def read_ultrasonor():
    try:
        prevValue = 0
        while True:
            value = distancesensor.distance()
            print(value)
            if (abs(value-prevValue) > 1) and (value > 0):
                prevValue = value
                DataRepository.write_historiek(value, 1)
                status = DataRepository.read_historiek(1)
                socketio.emit('B2F_historiek_1', {'historiek': status}, broadcast=True)
                leds.part_on(int(round(value,0)))
            eventlet.sleep(1)
    except KeyboardInterrupt:
        leds.all_off()
    finally:
        leds.all_off()

def read_temp():
    check = 0
    while check < 30:
        value = temp.read_temp()
        print(value)
        DataRepository.write_historiek(value, 4)
        #status = DataRepository.read_historiek(4)
        #socketio.emit('B2F_historiek_1', {'historiek': status}, broadcast=True)
        eventlet.sleep(1)
        check = check + 1

def read_LDR():
    if (LDR.read_channel(0)<10): 
        coffeemug = True
        print("koffietas staat eronder")
    else: 
        coffeemug = False
        print("koffietas staat er niet onder")
    while True:
        value = LDR.read_channel(0)
        if coffeemug == False:
            if value<10:
                print("Koffie tas is er onder gezet")
                coffeemug = True
                DataRepository.write_historiek(1, 2)
                status = DataRepository.read_historiek(2)
                socketio.emit('B2F_historiek_2', {'historiek': status}, broadcast=True)
                eventlet.sleep(2)
        else:
            if value>50:
                print("koffie tas is er van gehaald")
                coffeemug = False
                DataRepository.write_historiek(0, 2)
                status = DataRepository.read_historiek(2)
                socketio.emit('B2F_historiek_2', {'historiek': status}, broadcast=True)
                eventlet.sleep(2)
        eventlet.sleep(1)

def checkbutton():
    global CoffeePlanned
    if CoffeePlanned == False:
        status = DataRepository.read_coffeeplanned()
        if status == None:
            print("Geen koffie gepland")
            CoffeePlanned = False
        else:
            print("Koffie word gepland")
            planbutton(status["DateTime"])

def planbutton(FutureDate):
    seconds = float((FutureDate - datetime.now()).seconds)
    print("button planned in ", seconds)
    threading.Timer(seconds, pushbuttonplanned).start()
    CoffeePlanned = True

def pushbuttonplanned():
    CoffeeMug = DataRepository.read_historiek(2)
    if (bool(int(CoffeeMug["Value"])) == False): print("Koffie kan niet gemaakt worden, er staat geen koffietas onder de koffiemachine")
    elif (bool(int(CoffeeMug["Value"])) == True): 
        print("Koffie word gezet")
        knop.press() #word vanzelf ook terug uitgezet
    CoffeePlanned = False
    checkbutton()

def pushbutton():
    CoffeeMug = DataRepository.read_historiek(2)
    if (bool(int(CoffeeMug["Value"])) == False): print("Koffie kan niet gemaakt worden, er staat geen koffietas onder de koffiemachine")
    elif (bool(int(CoffeeMug["Value"])) == True): 
        print("Koffie word gezet")
        DataRepository.write_historiek(1, 3)
        knop.press() #word vanzelf terug uitgezet

def read_sensors():
    eventlet.spawn(read_ultrasonor)
    #eventlet.spawn(read_LDR)
    eventlet.spawn(read_temp)
    checkbutton()
    pass
    
read_sensors()

# Code voor Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)


print("**** Program started ****")

# API ENDPOINTS

@app.route('/api/v1')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    # vraag de status op uit de DB
    status1 = DataRepository.read_historiek(1)
    emit('B2F_historiek_1', {'historiek': status1}, broadcast=True)
    status2 = DataRepository.read_historiek(2)
    emit('B2F_historiek_2', {'historiek': status2}, broadcast=True)
    knop = Coffee()

@socketio.on('F2B_buttonpushed')
def buttonpushed():
    pushbutton
      
@socketio.on('F2B_buttonplanned')
def buttonpushed():
    global CoffeePlanned
    if CoffeePlanned == False: checkbutton()


# ANDERE FUNCTIES
if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')