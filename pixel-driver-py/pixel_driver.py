from machine import Pin
from ulab import numpy as np

class Protocol:
    WS2812 = 'ws2812'

class PixelDriver:
    def __init__(self, d0: Pin, d1: Pin, length: int, channels: int):
        from neopixel import NeoPixel
        self.neopixel = NeoPixel(Pin(d0), length, bbp=channels)
        self.buffer: np.ndarray = np.zeros((length, channels), dtype=np.float16)
        
    def render(self):
        flat_buffer = (self.buffer.flatten() * 255).astype(np.uint8)
        self.neopixel[:] = flat_buffer
        self.neopixel.write()
