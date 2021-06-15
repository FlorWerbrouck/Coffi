from rpi_ws281x import *
import time
from random import randrange

class WS2812b:
    def __init__(self):
        # LED strip configuration:
        self.LED_COUNT = 15      # Number of LED pixels.
        self.LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        self.LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA = 10      # DMA channel to use for generating signal (try 10)
        self.LED_BRIGHTNESS = 15     # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ,self.LED_DMA,self.LED_INVERT,self.LED_BRIGHTNESS,self.LED_CHANNEL)
        self.strip.begin()

    def all_on(self, r=0, g=0, b=0):
        for x in range(0,self.LED_COUNT):
            self.strip.setPixelColor(x,Color(r,g,b))
        self.strip.show()

    def go_crazy(self):
        while True:
            self.strip.setPixelColor(randrange(0,60),Color(randrange(255),randrange(255),randrange(255)))
            self.strip.show()
            time.sleep(0.1)

    def all_on_line_asc(self, r=0, g=0, b=0):
        for x in range(0,self.LED_COUNT):
            self.strip.setPixelColor(x,Color(r,g,b))
            self.strip.show()
            time.sleep(0.01)
    
    def all_on_line_desc(self, r=0, g=0, b=0):
        for x in range(0,self.LED_COUNT):
            self.strip.setPixelColor(self.LED_COUNT-x,Color(r,g,b))
            self.strip.show()
            time.sleep(0.01)

    def progressbar(self, sec): 
        for x in range(0,self.LED_COUNT):
            for i in range(0,255,5):
                self.strip.setPixelColor(x,Color(0,i,0))
                time.sleep((sec/self.LED_COUNT)/51)
                self.strip.show()
    
    def sunrise1(self): 
        for x in range(0,self.LED_COUNT):
            self.strip.setPixelColor(x,Color(253,244,220))
            self.strip.show()
            time.sleep(1)
    
    def sunrise2(self):
        for x in range(0,self.LED_COUNT):
            self.strip.setPixelColor(x,Color(253,244,220))
            self.strip.show()
        for i in range(255):
            print(i)
            self.LED_BRIGHTNESS = i
            time.sleep(0.1)

    def part_on(self, amount):
        self.all_off()
        for x in range(0,amount):
            self.strip.setPixelColor(x,Color(0,0,255))
        self.strip.show()
    
    def coffemug_true(self):
        for x in range(0,8):
            self.strip.setPixelColor(14-x,Color(0,255,0))
            self.strip.setPixelColor(x,Color(0,255,0))
            self.strip.show()
            time.sleep(0.05)

    def coffemug_false(self):
        for x in range(8,-1,-1):
            self.strip.setPixelColor(14-x,Color(255,0,0))
            self.strip.setPixelColor(x,Color(255,0,0))
            self.strip.show()
            time.sleep(0.05)

    def all_off(self):
        for x in range(0,self.LED_COUNT):
            self.strip.setPixelColor(x,Color(0,0,0))
        self.strip.show()