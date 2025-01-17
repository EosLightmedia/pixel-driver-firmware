#!/bin/bash

cd ports/rp2

make USER_C_MODULES=../../ulab/code/micropython.cmake BOARD=EOS_PIXEL_DRIVER