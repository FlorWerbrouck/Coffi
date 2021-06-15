import RPi.GPIO as GPIO
import time
#GPIO Mode (BOARD / BCM)
class HC204:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        #set GPIO Pins
        self.GPIO_TRIGGER = 20
        self.GPIO_ECHO = 21
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)
  
    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        StartTime = 0
        StopTime = 0

        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.process_time()
    
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.process_time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return round(distance,2)
    
    def distance2(self):

        GPIO.output(self.GPIO_TRIGGER,True)

        time.sleep(0.00001)

        GPIO.output(self.GPIO_TRIGGER,False)

        pulse_start = time.time()
        timeout = pulse_start + 0.04
        while GPIO.input(self.GPIO_ECHO) == 0 and pulse_start < timeout:
            pulse_start = time.time()

        pulse_end = time.time()
        timeout = pulse_end + 0.04
        while GPIO.input(self.GPIO_ECHO) == 1 and pulse_end < timeout:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000

        return distance

    def distanceavg(self):
        values = []
        for x in range(20):
           v = self.distance2()
           values.append(v)
           time.sleep(0.02)
        return sum(values)/len(values)

    def distanceml(self):
        value = self.distanceavg()
        valueml = ((-133 * value)+1907)
        valuemlround = self.myround(valueml)
        return valuemlround
    
    def myround(self, x, base=100):
        value = int(base * round(float(x)/base))
        if value<0: result = 0
        else: result = value
        return result

# u = HC204()
# while True:
#     print(u.distanceml())
#     time.sleep(1)