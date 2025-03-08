# Use official Ubuntu as a base image
FROM ubuntu:latest

# Install essential packages for C++ development
RUN apt update && apt install -y \
    build-essential \
    g++ \
    cmake \
    vim \
    git \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080
EXPOSE 5056
# Set the working directory
WORKDIR /workspace

# Default command (you can replace with your own if needed)
CMD ["bash"]
