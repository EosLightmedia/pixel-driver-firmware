import time

import gc
from ulab import numpy as np

import os
from cndl import CNDL
import machine

from rgb_logger import RGBLogger
from ws2812 import WS2812


class EPD:
    def __init__(self):
        self.hz = 30
        self.fade_frames = 60
        self.adc0 = machine.ADC(0)
        self.adc1 = machine.ADC(1)
        self.GP1 = machine.Pin(machine.Pin.board.GP1, machine.Pin.OUT)
        self.GP2 = machine.Pin(machine.Pin.board.GP2, machine.Pin.OUT)

        self.logger = RGBLogger()
        
        os.remove('.fastboot') if '.fastboot' in os.listdir() else self.logger.boot_sequence()
        
        with open('.version', 'w') as version_file:
            version_file.write(str(CNDL.version))
            
        try:
            with open('scene.cndl', 'r') as scene_file:
                code = scene_file.read()

            self.cndl = CNDL(code)
            self.driver = WS2812(self.cndl.global_vars['WIDTH'] * self.cndl.global_vars['HEIGHT'], self.cndl.layers_per_pixel)
            
        except Exception as e:
            print(f"Failed to load scene: {e}")
            self.logger.cndl_error()

    def run_scene(self):
        print('Running scene...')
        self.GP1.low()
        self.GP2.low()

        frame_time = 1000 // self.hz
        _t = 0 + frame_time
        delta = frame_time / 1000
        
        in1 = self.read_in1()
        in2 = self.read_in2()
        output = self.cndl.update(delta, in1, in2)
        fade_frames = int(self.fade_frames)
        _elapsed: int = 0
        _bytes = np.array(output * 255 * (1. - (fade_frames / self.fade_frames)), dtype=np.uint8).tobytes()
        _ms = time.ticks_ms
        _sleep = time.sleep_ms
        _diff = time.ticks_diff
        _read_in1 = self.read_in1
        _read_in2 = self.read_in2
        _array = np.array
        
        while True:
            self.logger.processing()
            fade_frames -= 1 if fade_frames > 0 else 0
            in1 = _read_in1()
            in2 = _read_in2()
            self.logger.set_in1(in1)
            self.logger.set_in2(in2)

            self.driver.write_bytes(_array(self.cndl.update(delta, in1, in2) * 255 * (1. - (fade_frames / self.fade_frames)), dtype=np.uint8).tobytes())
            
            gc.collect()
            
            _elapsed = _diff(_ms(), _t)
            delta = _elapsed / 1000
            if _elapsed < frame_time:
                self.logger.idle()
                _sleep(frame_time - _elapsed)
            _t = _ms()

    def read_in2(self):
        return float(self.adc1.read_u16() / 65535) * 2 - 1

    def read_in1(self):
        return float(self.adc0.read_u16() / 65535) * 2 - 1
            
        