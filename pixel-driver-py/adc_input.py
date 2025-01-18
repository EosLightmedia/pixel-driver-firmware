from machine import Pin
from machine import ADC

class AdcInput:
    def __init__(self, pin: Pin):
        self.adc = ADC(pin)
        
    def get_value(self):
        return float(self.adc.read_u16() / ((2 ** 16) - 1))