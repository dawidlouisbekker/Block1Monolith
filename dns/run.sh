#!/bin/bash

# Compile the C++ code using g++
g++ dnscache.cpp -o dnscache.out

# Check if the compilation was successful
if [ $? -eq 0 ]; then
    echo "Compilation successful! Running the program..."
    # Run the compiled executable
    ./dnscache.out
else
    echo "Compilation failed!"
fi
