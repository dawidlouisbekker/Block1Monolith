import socket
import requests
# Replace with your domain name
domain_name = "google.com"

# Resolving the domain name to an IP address
ip_address = socket.gethostbyname(domain_name)

print(f"The IP address for {domain_name} is: {ip_address}")


# Replace with your domain name or URL
url = "https://google.com"

# Making a GET request (DNS resolution happens here)
response = requests.get(url)

# Print the requested URL
print(f"Requested URL: {url}")

# Using urllib3 to get the connection details
# The response object has the connection to the server, and we can get the peername
server_ip = response.raw._connection.sock.getpeername()[0]
print(f"Server IP: {server_ip}")