# cmake file for Eos Pixel Driver
list(APPEND PICO_BOARD_HEADER_DIRS ${MICROPY_BOARD_DIR})
set(PICO_BOARD "eos-pixel-driver")
set(PICO_PLATFORM "rp2040")
set(MICROPY_FROZEN_MANIFEST ${MICROPY_BOARD_DIR}/manifest.py)
