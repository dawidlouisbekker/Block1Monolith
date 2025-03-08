#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>



#define PORT 5057  // Port to bind the socket to
#define SERVER_IP "127.0.0.1"  // IP address of the server (localhost in this case)

int main(int argc, char *argv[]) {
    pid_t pid = fork();

    int port = 0;
    char *tld = NULL;

    static struct option long_options[] = {
        {"port", required_argument, 0, 'p'},
        {"tld", required_argument, 0, 't'},
        {0, 0, 0, 0}
    };

    int opt;
    int option_index = 0;
    while ((opt = getopt_long(argc, argv, "p:t:", long_options, &option_index)) != -1) {
        switch (opt) {
            case 'p':
                port = atoi(optarg);
                break;
            case 't':
                tld = optarg;
                break;
            default:
                fprintf(stderr, "Usage: %s --port <port> --tld <tld>\n", argv[0]);
                exit(EXIT_FAILURE);
        }
    }

    if (port == 0 || tld == NULL) {
        fprintf(stderr, "Usage: %s --port <port> --tld <tld>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    printf("Port: %d\n", port);
    printf("TLD: %s\n", tld);
    if (pid == 0) {
        // Step 1: Create the socket
        int sock = socket(AF_INET, SOCK_DGRAM, 0);  // SOCK_DGRAM for UDP
        if (sock < 0) {
            std::cerr << "Socket creation failed" << std::endl;
            return -1;
        }
        std::cout << "Socket created successfully!" << std::endl;

        // Step 2: Set up the server address
        struct sockaddr_in server_addr;
        memset(&server_addr, 0, sizeof(server_addr));
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(PORT);
        server_addr.sin_addr.s_addr = inet_addr(SERVER_IP);  // Convert IP address to network byte order

        // Step 3: Send a message to the server
        const char *message = "Hello, UDP Server!";
        int send_len = sendto(sock, tld, strlen(message), 0, (struct sockaddr *)&server_addr, sizeof(server_addr));
        if (send_len < 0) {
            std::cerr << "Failed to send message" << std::endl;
            close(sock);
            return -1;
        }
        std::cout << "Message sent to server: " << message << std::endl;

        // Step 4: Receive response from server (optional)
        char buffer[1024];
        socklen_t addr_len = sizeof(server_addr);
        int recv_len = recvfrom(sock, buffer, sizeof(buffer), 0, (struct sockaddr *)&server_addr, &addr_len);
        if (recv_len < 0) {
            std::cerr << "Failed to receive message" << std::endl;
        } else {
            buffer[recv_len] = '\0';  // Null-terminate the received string
            std::cout << "Received message from server: " << buffer << std::endl;
        }

        // Step 5: Close the socket
        close(sock);
    } else {
        int sock = socket(AF_INET, SOCK_DGRAM, 0);  // SOCK_DGRAM for UDP
        if (sock < 0) {
            std::cerr << "Socket creation failed" << std::endl;
            return -1;
        }
        std::cout << "Server socket created successfully!" << std::endl;
    
        // Step 2: Set up the server address structure
        struct sockaddr_in server_addr, client_addr;
        memset(&server_addr, 0, sizeof(server_addr));
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(port);
        server_addr.sin_addr.s_addr = INADDR_ANY;  // Listen on any available network interface
    
        // Step 3: Bind the socket to the address and port
        if (bind(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
            std::cerr << "Main Bind failed" << std::endl;
            close(sock);
            return -1;
        }
    
        // Print server's address and port
        std::cout << "Binding successful! Server is listening on "
                  << inet_ntoa(server_addr.sin_addr) << ":"
                  << ntohs(server_addr.sin_port) << std::endl;
    
        // Step 4: Receive messages from clients
        char buffer[1024];
        socklen_t client_addr_len = sizeof(client_addr);
        while (true) {
            int recv_len = recvfrom(sock, buffer, sizeof(buffer), 0, (struct sockaddr *)&client_addr, &client_addr_len);
            if (recv_len < 0) {
                std::cerr << "Failed to receive message" << std::endl;
                continue;
            }
            buffer[recv_len] = '\0';  // Null-terminate the received string
            std::cout << "Received message: " << buffer << std::endl;
    
            // Step 5: Send a response back to the client
            const char *response = "Message received!";
            sendto(sock, response, strlen(response), 0, (struct sockaddr *)&client_addr, client_addr_len);
        }
    
        // Step 6: Close the socket (this part will never be reached in this example)
        close(sock);
    }

    return 0;
}
