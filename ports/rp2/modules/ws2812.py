import machine


class WS2812:
    def __init__(self, pixel_count: int, bpp: int):
        print(f'Initializing WS2812 driver on SPI 1')
        self.spi = machine.SPI(1, baudrate=3200000, polarity=0, phase=1, mosi=machine.Pin.board.DAT)
        self.output_buffer = bytearray(pixel_count * bpp * 4)
        print(f'Buffer size: {len(self.output_buffer)} bytes, {pixel_count} pixels, {bpp} bytes per pixel')
        self.bpp = bpp
        self.pixel_count = pixel_count
        
    def write_bytes(self, data):
        bpp = self.bpp
        pwm_codes = (0x88, 0x8e, 0xe8, 0xee)
        mask = 0x03
        index = 0
        output_buffer = self.output_buffer
        
        for i in range(0, len(data), bpp):
            channels = [int(data[i + c]) for c in range(bpp)]
            for channel_value in channels:
                output_buffer[index] = pwm_codes[channel_value >> 6 & mask]
                output_buffer[index + 1] = pwm_codes[channel_value >> 4 & mask]
                output_buffer[index + 2] = pwm_codes[channel_value >> 2 & mask]
                output_buffer[index + 3] = pwm_codes[channel_value & mask]
                index += 4

        self.spi.write(output_buffer)