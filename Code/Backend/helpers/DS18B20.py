class DS18B20:
    def __init__(self):
        self.sensor_filename = "/sys/bus/w1/devices/28-01193877f2e9/w1_slave"
    
    def read_temp(self):
        sensorfile = open(self.sensor_filename, 'r')
        for i, line in enumerate(sensorfile):
            if i == 1:  # 2de lijn
                temp = int(line.strip('\n')[line.find('t=')+2:])/1000.0
        sensorfile.close()
        return temp