import time
from RPi import GPIO
import threading

from flask.wrappers import Request

from helpers.HC204 import HC204
from helpers.WS2812b import WS2812b
from helpers.MCP import MCP
from helpers.Coffee import Coffee
from helpers.DS18B20 import DS18B20
from helpers.LCD import LCD

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, json, jsonify, request
from repositories.DataRepository import DataRepository
from datetime import date, datetime
from datetime import timedelta
from subprocess import check_output


CORS(app)

distancesensor = HC204()
leds = WS2812b()
LDR = MCP()
knop = Coffee()
temp = DS18B20()
LCD = LCD()
CoffeePlanned = False

# Code voor Database
def write_historiek(value, id):
    DataRepository.write_historiek(value, id)

def read_historiek(id):
    return DataRepository.read_historiek(id)

# Code voor Hardware
def read_ultrasonor():
    prevValue = -2
    while True:
        value = distancesensor.distanceml()
        print(value)
        if (abs(value-prevValue) > 1):
            prevValue = value
            write_historiek(value,1)
            status = read_historiek(1)
            socketio.emit('B2F_historiek_1', {'historiek': status}, broadcast=True)
            leds.part_on(int(round((value/1200)*15,0)))
        time.sleep(5)

def read_temp():
    check = 0
    while check < (6*5):
        value = temp.read_temp()
        print(value)
        write_historiek(value,4)
        #status = read_historiek(4)
        #socketio.emit('B2F_historiek_3', {'historiek': status}, broadcast=True)
        time.sleep(10)
        check = check + 1

def read_LDR():
    if (LDR.read_channel(0)<25): 
        coffeemug = True
        print("koffietas staat eronder")
        write_historiek(1, 2)
        status = read_historiek(2)
        socketio.emit('B2F_historiek_2', {'historiek': status}, broadcast=True)
    else: 
        coffeemug = False
        print("koffietas staat er niet onder")
        write_historiek(0, 2)
        status = read_historiek(2)
        socketio.emit('B2F_historiek_2', {'historiek': status}, broadcast=True)
    while True:
        value = LDR.read_channel(0)
        if coffeemug == False:
            if value<25:
                print("Koffie tas is er onder gezet")
                leds.coffemug_true()
                coffeemug = True
                write_historiek(1, 2)
                status = read_historiek(2)
                socketio.emit('B2F_historiek_2', {'historiek': status}, broadcast=True)
                time.sleep(1)
        else:
            if value>50:
                print("koffie tas is er van gehaald")
                leds.coffemug_false()
                coffeemug = False
                write_historiek(0, 2)
                status = read_historiek(2)
                socketio.emit('B2F_historiek_2', {'historiek': status}, broadcast=True)
                time.sleep(1)
        time.sleep(1)

def checkbutton():
    global CoffeePlanned
    if CoffeePlanned == False:
        status = DataRepository.read_coffeeplanned()
        if status == None:
            print("Geen koffie gepland")
            LCD.lcd_display_string("Nothing planned",2)
            CoffeePlanned = False
        else:
            print("Koffie word gepland")
            planbutton(status["DateTime"],status["MetingID"])
            CoffeePlanned = True

def planbutton(FutureDate, MetingID):
    seconds = float((FutureDate - datetime.now()).seconds)
    print("button planned on ", FutureDate)
    string = str(FutureDate)
    LCDstr = str(FutureDate.day) + "/" + str(FutureDate.month) + " " + string[11:16] + "     "
    LCD.lcd_display_string(LCDstr,2)
    threading.Timer(seconds, pushbuttonplanned).start()

def pushbuttonplanned():
    MetingID = DataRepository.read_coffeeplanned()
    CoffeeMug = read_historiek(2)
    Waterlevel = read_historiek(1)
    if (bool(int(CoffeeMug["Value"])) == False): 
        print("Koffie kan niet gemaakt worden, er staat geen koffietas onder de koffiemachine Koffie word verwijderd uit DB")
        DataRepository.delete_historiek(MetingID["MetingID"])
        time.sleep(1)
    elif (bool(int(CoffeeMug["Value"])) == True): 
        if Waterlevel["Value"] == 0.0: 
            print("Koffie kan niet gemaakt worden, geen water in de koffiemachine")
            DataRepository.delete_historiek(MetingID["MetingID"])
        else:
            print("Koffie word gezet")
            ml = read_historiek(1)
            write_historiek(ml["Value"],5)
            knop.press() #word vanzelf ook terug uitgezet
            threading.Thread(target=read_temp).start()
        
    CoffeePlanned = False
    checkbutton()

def pushbutton():
    CoffeeMug = read_historiek(2)
    Waterlevel = read_historiek(1)
    if (bool(int(CoffeeMug["Value"])) == False): print("Koffie kan niet gemaakt worden, er staat geen koffietas onder de koffiemachine")
    elif (bool(int(CoffeeMug["Value"])) == True):
        print(Waterlevel)
        if Waterlevel["Value"] == 0.0: print("Koffie kan niet gemaakt worden, geen water in de koffiemachine")
        else:
            print("Koffie word gezet")
            write_historiek(1, 3)
            ml = read_historiek(1)
            write_historiek(ml["Value"],5)
            knop.press()
            threading.Thread(target=read_temp).start()

def read_sensors():
    ips = check_output(['hostname', '--all-ip-addresses']).split()
    LCD.lcd_display_string(ips[0].decode())
    print(ips[0].decode())
    
    threading.Thread(target=read_ultrasonor).start()
    time.sleep(2.5)
    threading.Thread(target=read_LDR).start()
    checkbutton()
    

# Code voor Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=True, ping_timeout=1)

read_sensors()

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)


print("**** Program started ****")

# API ENDPOINTS

endpoint = '/api/v1'

@app.route(endpoint)
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route(endpoint + '/nextcoffeeplanned', methods=['GET','POST'])
def nextcoffeeplanned():
    if request.method == 'GET':
        return jsonify(koffie=DataRepository.read_coffeeplanned())
    if request.method == 'POST':
        gegevens = DataRepository.json_or_formdata(request)
        print(gegevens)
        data = DataRepository.plan_coffee(gegevens['datetime'])
        return jsonify(status=data)

@app.route(endpoint + '/futurecoffees', methods=['GET'])
def futurecoffees():
    if request.method == 'GET':
        return jsonify(koffie=DataRepository.read_futurecoffees())

@app.route(endpoint + '/futurecoffees/<MetingID>', methods=['DELETE'])
def deletecoffee(MetingID):
    if request.method == 'DELETE':
        data = DataRepository.delete_historiek(MetingID)
        return jsonify(koffie=data)

@app.route(endpoint + '/totalwater', methods=['GET'])
def totalwater():
    if request.method == 'GET':
        return jsonify(water=DataRepository.read_totalwater())

@app.route(endpoint + '/totalwateravg', methods=['GET'])
def totalwateravg():
    if request.method == 'GET':
        return jsonify(water=DataRepository.read_totalwateravg())

@app.route(endpoint + '/totaltempavg', methods=['GET'])
def totaltempavg():
    if request.method == 'GET':
        return jsonify(temp=DataRepository.read_totaltempavg())

@app.route(endpoint + '/totalwaterall', methods=['GET'])
def totalwaterall():
    if request.method == 'GET':
        return jsonify(water=DataRepository.read_totalwaterall())

@app.route(endpoint + '/totaltempall', methods=['GET'])
def totaltempall():
    if request.method == 'GET':
        return jsonify(temp=DataRepository.read_totaltempall())


@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    # vraag de status op uit de DB
    status1 = read_historiek(1)
    emit('B2F_historiek_1', {'historiek': status1}, broadcast=True)
    status2 = read_historiek(2)
    emit('B2F_historiek_2', {'historiek': status2}, broadcast=True)

@socketio.on('F2B_buttonpushed')
def buttonpushed():
    pushbutton()
      
@socketio.on('F2B_buttonplanned')
def buttonpushed():
    global CoffeePlanned
    print(CoffeePlanned)
    if CoffeePlanned == False: checkbutton()


# ANDERE FUNCTIES
if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')