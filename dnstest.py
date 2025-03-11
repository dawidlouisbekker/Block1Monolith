import socket

server_address = ('127.0.0.1', 5056)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Send a message to the server
message = 'paratech.top'.encode('ascii')
try:
    # Send the data
    print(f"Sending: {message}")
    sent = sock.sendto(message, server_address)
    print(f"Sent {message}")
    #sock.setblocking(False)
    data, server = sock.recvfrom(128)
    print(f"Received: {data}")

finally:
    print("Closing socket")
    sock.close()
