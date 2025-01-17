#!/bin/bash
echo "Building Micropython for the Eos Pixel Driver"
cd ports/rp2

echo "Checking for existing build directory..."
if [ -d "build-EOS_PIXEL_DRIVER" ]; then
    echo "Build directory found. Removing..."
    rm -rf "build-EOS_PIXEL_DRIVER"
    echo "Build directory removed."
else
    echo "No existing build directory found."
fi

echo "Starting the build process..."
make USER_C_MODULES=../../ulab/code/micropython.cmake BOARD=EOS_PIXEL_DRIVER CFLAGS+=-Wno-unused-function
echo "Build process completed."