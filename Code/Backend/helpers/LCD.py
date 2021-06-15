from RPi import GPIO as io
import time

SDA = 2
SCL = 3

io.setwarnings(False)


class PCF:
    def __init__(self, SDA, SCL, address):
        self.sda = SDA
        self.scl = SCL
        self.__address = address
        self.delay = 0.00001

        # io setup
        self.__setup()

    def write_outputs(self, data):
        # data schrijven
        self.__writebyte(data)
        # ack simuleren door 1 bit te writen
        self.__writebit(1)

    @property
    def address(self):
        return self.__address

    # om het adres van het device te wijzigen
    @address.setter
    def address(self, value):
        self.__address = value

    def __setup(self):
        io.setup(self.sda, io.OUT)
        io.setup(self.scl, io.OUT)

        time.sleep(0.1)

        # startconditie
        self.__start_conditie()
        # adres doorklokken + RW=0 om te schrijven
        self.__writebyte(self.__address << 1)
        # ack
        self.__ack()

    def __start_conditie(self):
        io.output(self.sda, io.HIGH)
        time.sleep(self.delay)
        io.output(self.scl, io.HIGH)
        time.sleep(self.delay)
        io.output(self.sda, io.LOW)
        time.sleep(self.delay)
        io.output(self.scl, io.LOW)
        time.sleep(self.delay)

    def stop_conditie(self):
        io.output(self.scl, io.HIGH)
        time.sleep(self.delay)
        io.output(self.sda, io.HIGH)
        time.sleep(self.delay)

    def __writebit(self, bit):
        # sda bitwaarde geven
        io.output(self.sda, bit)
        time.sleep(self.delay)
        # clock hoog
        io.output(self.scl, io.HIGH)
        time.sleep(self.delay)
        # clock laag na delay
        io.output(self.scl, io.LOW)
        time.sleep(self.delay)

    def __ack(self):
        # setup input + pullup van sda pin
        io.setup(self.sda, io.IN, pull_up_down=io.PUD_UP)
        # klok omhoog brengen
        io.output(self.scl, io.HIGH)
        time.sleep(self.delay)
        # sda pin inlezen: laag = OK
        status = io.input(self.sda) == io.LOW
        # setup output van sda pin
        io.setup(self.sda, io.OUT)
        # klok omlaag
        io.output(self.scl, io.LOW)
        time.sleep(self.delay)
        return status

    def __writebyte(self, byte):
        # 8 keer een bit schrijven
        mask = 0x80
        for i in range(8):
            self.__writebit(byte & (mask >> i))


class LCD:
    def __init__(self):
        self.lcd_device = PCF(SDA, SCL, 0X20)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x02)
        self.lcd_write(0x20 | 0x08 |
                       0x00 | 0x00)
        self.lcd_write(0x08 | 0x04)
        self.lcd_write(0x01)
        self.lcd_write(0x04 | 0x02)
        time.sleep(0.2)

    def lcd_strobe(self, data):
        self.lcd_device.write_outputs(data | 0b00000100 | 0x08)
        time.sleep(.0005)
        self.lcd_device.write_outputs(((data & ~0b00000100) | 0x08))
        time.sleep(.0001)

    def lcd_write_four_bits(self, data):
        self.lcd_device.write_outputs(data | 0x08)
        self.lcd_strobe(data)

    # write a command to lcd
    def lcd_write(self, cmd, mode=0):
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

    # write a character to lcd (or character rom) 0x09: backlight | RS=DR<
    # works!
    def lcd_write_char(self, charvalue, mode=1):
        self.lcd_write_four_bits(mode | (charvalue & 0xF0))
        self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))

    # put string function with optional char positioning
    def lcd_display_string(self, string, line=1, pos=0):
        if line == 1:
            pos_new = pos
        elif line == 2:
            pos_new = 0x40 + pos
        elif line == 3:
            pos_new = 0x14 + pos
        elif line == 4:
            pos_new = 0x54 + pos

        self.lcd_write(0x80 + pos_new)

        for char in string:
            self.lcd_write(ord(char), 0b00000001)

    # clear lcd and set to home
    def lcd_clear(self):
        self.lcd_write(0x01)
        self.lcd_write(0x02)

    # define backlight on/off (lcd.backlight(1); off= lcd.backlight(0)
    def backlight(self, state):  # for state, 1 = on, 0 = off
        if state == 1:
            self.lcd_device.writebyte(0x08)
        elif state == 0:
            self.lcd_device.writebyte(0x00)

    # add custom characters (0 - 7)
    def lcd_load_custom_chars(self, fontdata):
        self.lcd_write(0x40)
        for char in fontdata:
            for line in char:
                self.lcd_write_char(line)