#!/bin/bash

# Compile the C++ code using g++
g++ tldserver.cpp -o client.out

# Check if the compilation was successful
if [ $? -eq 0 ]; then
    echo "Compilation successful! Running the program..."
    # Run the compiled executable
    ./client.out --port 5056 --tld .com
else
    echo "Compilation failed!"
fi