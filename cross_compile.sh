#!/bin/bash

echo "Changing directory to mpy-cross/"
cd mpy-cross/ || exit

if [ -d "build" ]; then
  echo "Existing build directory found."
  echo "Removing existing build directory..."
  rm -rf build
fi

echo "Running make..."
make
echo "Build process completed."