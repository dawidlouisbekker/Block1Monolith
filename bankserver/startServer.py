import threading

from server import ActivateServer, newBankAdminForm
#From serverutils
from server import StopServerException, HOST, PORT, ADMIN_PORT, socket, os, createSSLContext, createAdminSSLContext, ConType
import sys
import signal

sock : socket.socket | None = None


def signal_handler(sig, frame):
    print("\nReceived Ctrl+C, shutting down server...\n")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    command : str = ""
    server_thread : threading.Thread | None = None
    server_admin_thread : threading.Thread | None = None
    try:
        sock = createSSLContext(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
        sock.bind((HOST,PORT))

        admin_sock = createAdminSSLContext(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
        admin_sock.bind((HOST,ADMIN_PORT))
        
        server_thread = threading.Thread(target=ActivateServer,args=(sock,ConType.FTP), daemon=True)
        server_admin_thread = threading.Thread(target=ActivateServer,args=(admin_sock,ConType.BANKADMIN,), daemon=True)
        #Set up UDP
        
        server_thread.start()
        server_admin_thread.start()
        
        while True:
            command = input("Enter option: ")
            if command == "exit":
                os.kill(os.getpid(), signal.SIGINT)
                raise StopServerException()
            if command == "new":
                try:
                    newBankAdminForm()
                except Exception as e:
                    print(e)
                    
            
    except StopServerException:
        print("Stopping server...")
        
    except Exception as e:
        print("Error in server start up:",e)
        if server_admin_thread is not None:
            server_admin_thread.join()
            
        if server_thread is not None:
            server_thread.join()
        
    finally:
        if sock is not None:
            sock.close()
            if server_thread is not None:
                server_thread.join()
        print("Server stopped running.")

        