#!/bin/bash
BOARD_NAME="EOS_PIXEL_DRIVER"

echo "Building Micropython for $BOARD_NAME"
cd ports/rp2

echo "Checking for existing build directory..."
if [ -d "build-$BOARD_NAME" ]; then
    echo "Build directory found. Removing..."
    rm -rf "build-$BOARD_NAME"
    echo "Build directory removed."
else
    echo "No existing build directory found."
fi

echo "Starting the build process..."
make USER_C_MODULES=../../ulab/code/micropython.cmake BOARD=$BOARD_NAME CFLAGS+=-Wno-unused-function
echo "Build process completed."
