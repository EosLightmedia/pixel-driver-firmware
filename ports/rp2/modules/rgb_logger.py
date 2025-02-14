import machine
import time

import math
from neopixel import NeoPixel


class RGBLogger:
    def __init__(self):
        self.pixels = NeoPixel(machine.Pin.board.LED, 3)
    
    @staticmethod
    def colorize_input(value: float):
        blue = 5
        green = int((min(max(value, 0.), 1.) * 10))
        red = int((min(max(value, -1.), 0.) * -10))
        return red, green, blue
 
    def set_in1(self, value: float):
        self.pixels[2] = self.colorize_input(value)
        self.pixels.write()
        
    def set_in2(self, value: float):
        self.pixels[1] = self.colorize_input(value)
        self.pixels.write()
    
    def idle(self):
        self.pixels[0] = (1, 5, 20)
        self.pixels.write()
    
    def processing(self):
        self.pixels[0] = (20, 5, 1)
        self.pixels.write()
    
    def cndl_error(self):
        while True:
            self.pixels[0] = (10, 5, 0)
            self.pixels.write()
            time.sleep_ms(500)
            self.pixels[0] = (0, 0, 0)
            self.pixels.write()
            time.sleep_ms(500)
        
    def system_error(self):
        while True:
            self.pixels.fill((10, 0, 0))
            self.pixels.write()
            time.sleep_ms(500)
            self.pixels.fill((0, 0, 0))
            self.pixels.write()
            time.sleep_ms(500)
    
    def boot_sequence(self):
        delay = 1000 // 11
        self.pixels[0] = (10, 0, 0)
        self.pixels.write()
        time.sleep_ms(delay)
        self.pixels[0] = (2, 0, 0)
        self.pixels[1] = (0, 10, 0)
        self.pixels.write()
        time.sleep_ms(delay)
        self.pixels[0] = (0, 0, 0)
        self.pixels[1] = (0, 5, 0)
        self.pixels[2] = (0, 0, 10)
        self.pixels.write()
        time.sleep_ms(delay)
        self.pixels[1] = (0, 2, 0)
        self.pixels[2] = (0, 10, 10)
        self.pixels.write()
        time.sleep_ms(delay)
        self.pixels[1] = (10, 10, 0)
        self.pixels[2] = (0, 5, 5)
        self.pixels.write()
        time.sleep_ms(delay)
        self.pixels[0] = (10, 0, 10)
        self.pixels[1] = (5, 5, 0)
        self.pixels[2] = (0, 2, 2)
        self.pixels.write()
        time.sleep_ms(delay)
        self.pixels[0] = (10, 10, 10)
        self.pixels[1] = (2, 2, 0)
        self.pixels[2] = (0, 0, 0)
        self.pixels.write()
        time.sleep_ms(delay)
        self.pixels[0] = (5, 5, 5)
        self.pixels[1] = (10, 10, 10)
        self.pixels.write()
        time.sleep_ms(delay)
        self.pixels[0] = (0, 0, 0)
        self.pixels[1] = (5, 5, 5)
        self.pixels[2] = (10, 10, 10)
        self.pixels.write()
        time.sleep_ms(delay)
        self.pixels[1] = (0, 0, 0)
        self.pixels[2] = (5, 5, 5)
        self.pixels.write()
        time.sleep_ms(delay)
        self.pixels[2] = (0, 0, 0)
        self.pixels.write()
        time.sleep_ms(delay)
        time.sleep_ms(delay)
