from machine import Pin

from adc_input import AdcInput
from pixel_driver import PixelDriver
from pixel_logger import PixelLogger

class EosPixelDriver:
    def __init__(self):
        self.input_0 = AdcInput(Pin(26, Pin.IN))
        self.input_1 = AdcInput(Pin(27, Pin.IN))
        self.pixel_driver = PixelDriver(Pin(3, Pin.OUT), Pin(4, Pin.OUT), 24)
        self.logger = PixelLogger(Pin(12, Pin.OUT))
        
    def run(self):
        while True:
            in_0_value = self.input_0.get_value()
            in_1_value = self.input_1.get_value()
            print(in_0_value, in_1_value)
            
            
EosPixelDriver().run()