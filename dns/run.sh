#!/bin/bash

# Compile the C++ code using g++
g++ RecursiveResolver.cpp -o ecursiveResolver.out

# Check if the compilation was successful
if [ $? -eq 0 ]; then
    echo "Compilation successful! Running the program..."
    # Run the compiled executable
    ./RecursiveResolver.out
else
    echo "Compilation failed!"
fi
