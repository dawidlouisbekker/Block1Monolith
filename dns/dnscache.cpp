#include <iostream>
#include <vector>
#include <cstddef>
#include <string>

#include <sched.h> //For different cores.
#include <thread>

//#include <omp.h> parralel loops


#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <map>

using std::string;
using std::vector;
using std::cout;
using std::cerr;
using std::endl;
using std::map;

#define DNS_PORT 5056
#define TLD_PORT 5057
#define SOCK_SIZE 16

typedef sockaddr_in socketCacheLine[4] __attribute__((aligned(64)));

//Parallel array; 
vector<string> tlds;
vector<vector<socketCacheLine>> tldSockets;

int main() {
    //Fork for 
    pid_t pid = fork();
    if (pid == 0) {
        int tld_init_socket = socket(AF_INET, SOCK_DGRAM, 0);
        if (tld_init_socket < 0) {
            cerr << "Error creating socket in child" << endl;
            return -1;
        }
        cout << "Child process created socket." << endl;

        struct sockaddr_in tld_server, tld_client_addr;

        memset(&tld_client_addr, 0 , sizeof(tld_client_addr));
        tld_server.sin_family = AF_INET;
        tld_server.sin_port = htons(TLD_PORT);
        tld_server.sin_addr.s_addr = INADDR_ANY;

        if (bind(tld_init_socket , (struct sockaddr *)&tld_server, sizeof(tld_server)) < 0) {
            cerr << "Child bind failed" << endl;
            close(tld_init_socket);
            return -1;
        }

        std::cout << "Binding successful! Server is listening on "
                  << inet_ntoa(tld_server.sin_addr) << ":"
                  << ntohs(tld_server.sin_port) << std::endl;

        
        char tldBuffer[20];
        socklen_t tld_client_addr_len = sizeof(tld_client_addr);
        while (true) {
            int tld_recv_len = recvfrom(tld_init_socket,tldBuffer,sizeof(tldBuffer),0,(struct sockaddr *)&tld_client_addr,&tld_client_addr_len);
            if (tld_recv_len < 0) {
                std::cerr << "Failed to receive message" << std::endl;
                continue;
            }
            tldBuffer[tld_recv_len] = '\0';
            cout << "Message recivived: " << tldBuffer << endl;
            const char *response = "child received message.";
            sendto(tld_init_socket, response, strlen(response), 0, (struct sockaddr *)&tld_client_addr, tld_client_addr_len);
        }
        close(tld_init_socket);
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
        server_addr.sin_port = htons(DNS_PORT);
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
