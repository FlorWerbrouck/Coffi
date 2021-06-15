from RPi import GPIO
import time

class Coffee:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.GPIO_LEVELSHIFTER = 16
        GPIO.setup(self.GPIO_LEVELSHIFTER,GPIO.OUT)
        GPIO.output(self.GPIO_LEVELSHIFTER, True)

    def press(self):
        GPIO.output(self.GPIO_LEVELSHIFTER, False)
        time.sleep(0.5)
        GPIO.output(self.GPIO_LEVELSHIFTER, True)

# knop = Coffee()
# knop.press()