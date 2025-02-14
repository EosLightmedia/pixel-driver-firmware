try:
    from pixel_driver import EPD
    EPD().run_scene()
except Exception as e:
    print("Critical Error", e)
    from rgb_logger import RGBLogger
    log = RGBLogger()
    log.system_error()