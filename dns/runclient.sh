#!/bin/bash

# Compile the C++ code using g++
g++ RootNameServer.cpp -o RootNameServer.out

# Check if the compilation was successful
if [ $? -eq 0 ]; then
    echo "Compilation successful! Running the program..."
    # Run the compiled executable
    ./RootNameServer.out --port 5056 --tld .com
else
    echo "Compilation failed!"
fi