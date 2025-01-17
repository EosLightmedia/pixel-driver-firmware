#!/bin/bash

cd mpy-cross/ || exit

if [ -d "build" ]; then
  rm -rf build
fi

make