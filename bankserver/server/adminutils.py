from .serverutils import Admin, BankAdmin, ClientSocketThread, colorsPrinter, getOracleDB,  createAdminSSLContext
from .serverutils import ssl, threading, socket ,time


class AdminSocketThread(ClientSocketThread):
    def __init__(self,sock_thread : ClientSocketThread, dbadmin : Admin):
        super().__init__(addr=sock_thread.addr,sock=sock_thread.socket)
        self.dbadmin : Admin = dbadmin
        self.admin = True
        self.sendMessage(message="Success")
        
    def newUser():
        pass
    
class BankAdminSocketThread(ClientSocketThread):
    def __init__(self,sock_thread : ClientSocketThread, bankAdmin : BankAdmin, passphrase : str):
        super().__init__(addr=sock_thread.addr,sock=sock_thread.socket)
        
        self.bankAdmin = bankAdmin
        
        self.admin = True
        highSecPort =  createAdminSSLContext(socket.socket(socket.AF_INET,socket.SOCK_STREAM),certBytes=bankAdmin.server_ca,keyBytes=bankAdmin.server_privateKey,intmdCert=bankAdmin.intermedCert)
        PORT : int = self.randomBind(socket=highSecPort)
        colorsPrinter.logGreenAction(basemessage="BANK ADMIN LOGIN",user=bankAdmin.uuid)
        self.highSecPort : ssl.SSLSocket = highSecPort 
        
        #badmn = Bank Admin.
        self.badmn_connect : bool = False
        
        self.highSecPortThread = threading.Thread(target=self.startHighSec,args=(highSecPort,),daemon=True)
        self.highSecPortThread.start()
        self.sendMessage("Success")
        self.sendMessage(str(PORT))
        self.waitForConnection()
        
        
    def waitForConnection(self):
        amnttime : float = 0
        while not self.badmn_connect:
            time.sleep(0.1)
            amnttime += 0.1
            if amnttime >= 10:
                self.highSecPort.close()
                self.socket.close()
                self.highSecPortThread.join()
                colorsPrinter.logRedAction("TOOK TO LONG",user=self.bankAdmin.uuid)
                return
        
    def startHighSec(self, sock : ssl.SSLSocket):
        sock.listen(1)
        colorsPrinter.logGreenAction("BANK ADMIN PORT LISTENING",user=self.bankAdmin.uuid)
        try:
            badmn_socket, badmn_addr = sock.accept()
            self.sendMessage("Connected")
            self.socket.close()
            self.socket = badmn_socket
            self.addr = badmn_addr
            colorsPrinter.logGreenAction("BANK ADMIN CONNECTED",user=self.bankAdmin.uuid)
            self.badmn_connect = True
        except Exception as e:
            pass
        return
        
        
    
    
    
    