import threading
from .serverutils import StopServerException, ClientSocketThread, clientManager, colorsPrinter, createSSLContext, socket, os, ssl, createAdminSSLContext
from .serverutils import newBankAdminForm
from .server import handleClient, handleAdmin
from .serverutils import HOST, PORT, ADMIN_PORT



def ActivateServer(sock : ssl.SSLSocket | None, admin : bool = False):
    #context = ssl.create_default_context()
    if sock is None:
        print("No server socket received")
        return
    try:
        sock.listen()
        port = sock.getsockname()[1]
        colorsPrinter.logGreenAction(basemessage="STARTED",message=f"server listening on {HOST}:{port}")
        client_thread : threading.Thread | None = None
        admin_thread : threading.Thread | None = None
        try:
            while sock != None:
                client_sock , addr = sock.accept()
                socket_class = ClientSocketThread(sock=client_sock,addr=addr)
                clientManager.addClient(socket_class)
                if admin:
                    admin_thread = threading.Thread(target=handleAdmin,args=(socket_class,addr,),daemon=True)
                    admin_thread.start()
                else:
                    client_thread = threading.Thread(target=handleClient,args=(socket_class,addr,),daemon=True)
                    client_thread.start()

        except StopServerException:
            pass
        except ssl.SSLError as e:
            colorsPrinter.logRedAction(basemessage="SSL ERROR", message=f"SSL error occurred: {e}")
        except KeyboardInterrupt:
            print("Closing server...")
        except Exception as e:
            print("Error with socket activation:",e)
        finally: 
            if client_thread is not None:
                client_thread.join()
            if admin_thread is not None:
                admin_thread.join()
                
    except Exception as e:
        print(e)
        print("Server thread stopped listening")

