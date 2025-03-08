#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>



using std::cerr;
using std::cout;
using std::endl;

int main() {
    int socket_adr = socket(AF_INET,SOCK_DGRAM,0);
    int tld_init_socket = socket(AF_INET, SOCK_DGRAM, 0);
    if (tld_init_socket < 0) {
        cerr << "Error creating socket in child" << endl;
        return -1;
    }
    cout << "Child process created socket." << endl;

    struct sockaddr_in tld_server, tld_client_addr;
    try {
        
        memset(&tld_client_addr, 0 , sizeof(tld_client_addr));
        tld_server.sin_family = AF_INET;
        tld_server.sin_port = htons(5096);
        tld_server.sin_addr.s_addr = INADDR_ANY;
    
        if (bind(tld_init_socket , (struct sockaddr *)&tld_server, sizeof(tld_server)) < 0) {
            cerr << "Child bind failed" << endl;
            close(tld_init_socket);
            return -1;
        }
        // Print server's address and port
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
    } catch (...) {

    }

    close(tld_init_socket);
}