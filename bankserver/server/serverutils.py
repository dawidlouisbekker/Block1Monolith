from typing import List
from pathlib import Path

import socket
import ssl
import random
import secrets
import string
import os
import json
import time
from uuid import uuid4
import threading



from cryptography.hazmat.primitives import serialization

from typing import List, Dict, Tuple

from .db.models import getOracleDB, Admin,BankAdmin,bcrypt, Session


CURRENT_DIR_STR = os.getcwd()
SERVER_PASSPHRASE = os.getenv("SERVER_PASSPHRASE")
BASE_PATH = Path(CURRENT_DIR_STR) / Path("server") / Path("files")
HOST = "localhost"
PORT = 21
ADMIN_PORT = 5024

currentFTPPorts : List[int] = []


def createSSLContext(sock: socket.socket):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server/server_cert.pem", keyfile="server/server_key.pem")
    context.load_verify_locations(cafile="certificates/ca_cert.pem")
    return context.wrap_socket(sock, server_side=True)


from cryptography import x509
#I was thinking of creating a temporary file similar to how web browsers create files in a sandbox but after research using ChatGPT (Free version 4o) I found this. 
import tempfile
'''
def crtTempCertAndKeyFls(context : ssl.SSLContext, ):
    with tempfile.NamedTemporaryFile(delete=False) as key_file, \
         tempfile.NamedTemporaryFile(delete=False) as cert_file:
        key_file.write(keyBytes)
        key_file.flush()
        cert_file.write(certBytes)
        cert_file.flush()
        key_file_path = key_file.name
        cert_file_path = cert_file.name
        # Load into SSL context
        context.load_cert_chain(certfile=cert_file_path, keyfile=key_file_path)
'''
def createAdminSSLContext(
    sock: socket.socket,
    certBytes: bytes | None = None,
    keyBytes: bytes | None = None,
    intmdCert: bytes | None = None,
    certFile: str = "server/admin_server_cert.pem",
    keyFile: str = "server/admin_server_key.pem",
    caFile: str | x509.Certificate = "certificates/admin_ca_cert.pem"
):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    try:
        if keyBytes is not None and certBytes is not None:
            with tempfile.NamedTemporaryFile(delete=False) as key_file, \
                tempfile.NamedTemporaryFile(delete=False) as cert_file:
                    
                key_file.write(keyBytes)
                key_file.flush()
                cert_file.write(certBytes)
                cert_file.flush()
                
                key_file_path = key_file.name
                cert_file_path = cert_file.name
                # Load into SSL context
                context.load_cert_chain(certfile=cert_file_path, keyfile=key_file_path)
        else:
            context.load_cert_chain(certfile=certFile, keyfile=keyFile)
        try:
            if intmdCert is not None:
                with tempfile.NamedTemporaryFile(delete=False) as ca_cert:
                    ca_cert.write(intmdCert)
                    ca_cert.flush()
                    ca_file_name = ca_cert.name
                    context.load_verify_locations(cafile=ca_file_name)
            else:
                context.load_verify_locations(cafile=caFile)
                
            return context.wrap_socket(sock, server_side=True)
        except Exception as e:
            print("CA Error:",e)
    except Exception as e:
        print("Key and cert error:",e)

class ConsoleColors:
    def __init__(self):
        self.RED = "\033[31m"
        self.RESET = "\033[0m"
        self.GREEN = "\033[32m"
        self.BLUE = "\033[34m"
        self.YELLOW = "\033[33m"
        
    def logError(self,message : str):
        print(f"{self.RED} {message} {self.RESET}")
        return
        
    def logSuccess(self, message : str):
        print(f"{self.GREEN} {message} {self.RESET}")
        return

    def logGreenAction(self, basemessage : str = "SUCCESS",message : str | None = None, addr : tuple[str,int] | None = None, user : str | None = None):
        prnt = f"{self.GREEN} {basemessage}{self.RESET}"
        if addr is not None:
            prnt = prnt + f" {addr[0]}:{addr[1]}"
        if message is not None:
            prnt = prnt + f" | {message}"
        if user is not None:
            prnt = prnt + f" | {colorsPrinter.YELLOW}USER: {colorsPrinter.BLUE}{user}{colorsPrinter.RESET} "
        print(prnt)
        return

    def logRedAction(self, basemessage : str = "ERROR",message : str | None = None, addr : tuple[str,int] | None = None, user : str | None = None):
        prnt = f"{self.RED} {basemessage}{self.RESET}:"
        if addr is not None:
            prnt = prnt + f" {addr[0]}:{addr[1]}"
        if message is not None:
            prnt = prnt + f" | {message}"
        if user is not None:
            prnt = prnt + f" | {colorsPrinter.YELLOW}USER: {colorsPrinter.BLUE}{user}{colorsPrinter.RESET}"
        print(prnt)
        return 


colorsPrinter = ConsoleColors()


def CheckPathInput(input : str):
    if "./" in input or ".." in input:
        raise Exception("Invalid path. Cannot contain './' or '..'")
    return




def getUserFiles(username : str,entries : List[str]) -> List[str]:
    files : List[str] = []
    try:
        for entry in entries:
            path = Path(username) / Path(entry)
            if os.path.isfile(path=path):
                files.append(entry)   
    except Exception as e:
        colorsPrinter.logRedAction(basemessage="FUNCTION REQUIRES",message=e)

def getFilesAndDirs(username: str, path : Path | None = None) -> tuple[list[str],list[str]]:
    # Construct the correct directory path
    if path is None:
        path = BASE_PATH / username if dir == "/" else BASE_PATH / username / dir

        if not path.exists() or not path.is_dir():
            return {}, {}  # Return empty dictionaries if the path doesn't exist

    entities = list(path.iterdir())  # Use pathlib to list entities

    # Separate files and directories
    files = [entity.name for entity in entities if entity.is_file()]
    dirs = [entity.name for entity in entities if entity.is_dir()]

    return files, dirs 

def GetEntities(username: str, path : Path | None = None ,dir: str = "/") -> Tuple[Dict, Dict]:
    # Construct the correct directory path
    if path is None:
        path = BASE_PATH / username if dir == "/" else BASE_PATH / username / dir

        if not path.exists() or not path.is_dir():
            return {}, {}  # Return empty dictionaries if the path doesn't exist

    entities = list(path.iterdir())  # Use pathlib to list entities

    # Separate files and directories
    files = {dir: [entity.name for entity in entities if entity.is_file()]}
    dirs = {dir: [entity.name for entity in entities if entity.is_dir()]}

    return files, dirs
    

class StopServerException(KeyboardInterrupt):
    pass

class Client:
    def __init__(self,username : str):
        self.username : str = username
        
        #db = getUsersDB()
        #self.dbtTuple : User = db.query(User).filter(User.username == username).first() 
        self.ftpSocket : ssl.SSLSocket | None = None
        self.directories : dict[str,list[str]] = {}
        self.files : dict[str,list[str]] = {}
        entities = GetEntities(username=username)
        self.files.update(entities[0])
        self.directories.update(entities[1])
        for key in self.directories.keys():
            files, directories = GetEntities(username=username,dir=key)
            self.directories.update(directories)
            self.files.update(files)
            
    def CreateFTPSocket(self) -> ssl.SSLSocket:
        pass

class ClientSocketThread():
    def __init__(self, sock : ssl.SSLSocket, addr, debug : bool = True):
        self.debug = debug
        self.addr = addr
        self.socket : ssl.SSLSocket = sock
        self.ftpSocket : ssl.SSLSocket | None = None
        self.highSecPortThread : threading.Thread | None = None
        self.currentDir : str = "/"
        self.__currentSendPacket : bytes | None = None
        self.__currentRecvPacket : bytes | None = None
        self.user : Client | None = None
        self.admin : bool = False
    
    def gen_secure_key(self,length: int = 16) -> str:
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
    
    def randomBind(self, socket : socket.socket):
        success = False
        FTP_PORT : int = 0
        while success == False:
            FTP_PORT = random.randint(19,64000)
            try:
                socket.bind((HOST,FTP_PORT))
                success = True
            except Exception as e:
                print("Error starting ftp:",e)
                prnt = colorsPrinter.YELLOW + "STARTING SERVICE" + colorsPrinter.RESET + "  |  " + colorsPrinter.YELLOW + "PORT: " + colorsPrinter.RESET + str(FTP_PORT)  + "   |  " + colorsPrinter.BLUE + self.user.username + colorsPrinter.RESET + "  |  "  + self.addr[0] + ":" + str(self.addr[1])
                print(prnt)
        return FTP_PORT
    
    def StartFTP(self) -> socket.socket:
        ftpSock : socket.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        FTP_PORT : int = self.randomBind(socket=ftpSock)
        self.ftpSocket = ftpSock
        key = self.gen_secure_key()
        print("Key:",key)
        print("Port:",FTP_PORT)
        self.sendJson(message={ "port" : FTP_PORT, "key" : key })
        return ftpSock
        
    def CloseAndClearResources(self):
        try:
            if self.socket is not None:
                self.socket.close()
                if self.user:
                    colorsPrinter.logGreenAction(basemessage="\n DISCONNECTED",user=self.user.username,addr=self.addr,message="TCP AUTH Socket")
                else:
                    colorsPrinter.logGreenAction(basemessage="\n DISCONNECTED",addr=self.addr,message="TCP AUTH Socket")

            if self.ftpSocket is not None:
                self.ftpSocket.close()
                colorsPrinter.logGreenAction(basemessage="\n DISCONNECTED",addr=self.addr,message="TCP FTP Socket")
             
            if self.user is not None:
                self.user = None
        except Exception as e:
            print("Error closing sockets:",e)
    
    
    #Messaging
    def __sendPacket(self):
        if self.admin:
            packet = self.__currentSendPacket + b"\n"
            self.socket.send(packet)
            print("Sending packet:",self.__currentSendPacket)
            return
        else:
            self.socket.send(self.__currentSendPacket)
            return       
    
    def sendMessage(self, message : str | int, encoding : str = "ascii"):
        try:
            if isinstance(message, str):
                self.__currentSendPacket = message.encode(encoding=encoding)
                self.__sendPacket()
            elif isinstance(message, int):
                self.__currentSendPacket = message.to_bytes(4, byteorder='big')
                self.__sendPacket()
        except Exception as e:
            print("Error in seding message:",e)
    

    def sendJson(self, message : dict | str | list, encoding : str = "ascii"):
        if isinstance(message, dict):
            jsonpayload = json.dumps(message)
            self.__currentSendPacket = jsonpayload.encode(encoding=encoding)
        elif isinstance(message, list):
            jsonpayload = json.dumps(message)
            self.__currentSendPacket = jsonpayload.encode(encoding=encoding)
        elif isinstance(message, str):
            self.__currentSendPacket = message.encode(encoding=encoding)
        else:
            raise ValueError("Invalid message type. Must be a dict or str.")
        self.__sendPacket()
        return
    
    def receiveMessage(self,size : int = 128, logMsg : bool = False, baseMessage : str | None = None) -> str:
        self.__currentRecvPacket = self.socket.recv(size)
        if logMsg:
            message = self.__currentRecvPacket.decode()
            prnt = f"{colorsPrinter.BLUE}{message}{colorsPrinter.RESET}"
            if baseMessage:
                colorsPrinter.logGreenAction(basemessage=baseMessage,message=prnt, addr=self.addr)
            else:
                colorsPrinter.logGreenAction(basemessage="MESSAGE",message=prnt, addr=self.addr)
        return self.__currentRecvPacket.decode()
    
    def recieveJson(self, estSize : int = 512) -> dict:
        jsonpayload = self.socket.recv(estSize)
        self.__currentRecvPacket = jsonpayload
        message = jsonpayload.decode('ascii')
        jsondict : dict = json.loads(message)
        return jsondict
    
    def EstablishUser(self,username : str):
        try:
            self.user = Client(username=username)
            self.sendJson({ "message" : f"Logged in as {colorsPrinter.YELLOW}{username}{colorsPrinter.RESET}", "state" : True})
            jsonbody = { "files" : self.user.files , "dirs" : self.user.directories }
            for direc in self.user.directories["/"]:
                jsonbody["files"].update( { direc : [] } )
                jsonbody["dirs"].update( { direc : [] } )
                
            jsonpayload = json.dumps(jsonbody)
            print(jsonpayload)
            size = len(jsonpayload) * 8
            self.sendMessage(str(size))
            time.sleep(0.1)
            self.sendJson(message=jsonpayload)
            colorsPrinter.logGreenAction(basemessage="SENT",message=f"{colorsPrinter.YELLOW}MESSAGE:{colorsPrinter.RESET} {jsonpayload}", user=username)
        except Exception as e:
            print("Error in establish user con:",e)
        return


        

class ClientSocketsManager:
    def __init__(self):
        self.clients : List[ClientSocketThread] = []
        
    def addClient(self, sock : ClientSocketThread):
        self.clients.append(sock)
        message = f" {colorsPrinter.BLUE}NUMBER CONNECTIONS{colorsPrinter.RESET}: {len(self.clients)}"
        print(message)
    
    def removeClient(self,sock : ClientSocketThread):
        try:
            sock.CloseAndClearResources()
            self.clients.remove(sock)
            message = f" {colorsPrinter.BLUE}NUMBER CONNECTIONS{colorsPrinter.RESET}: {len(self.clients)}"
            print(message)
        except Exception as e:
            print(e)
    
    def closeAllConnections(self):
        for client in self.clients:
            try:
                client.CloseAndClearResources()
            except Exception as e:
                print("Error clearing socket class")
            
clientManager = ClientSocketsManager()



import tkinter as tk
from tkinter import messagebox
from .ftpcerts.gencert import genIntermed, generate_client_cert, generate_server_cert
from .ftpcerts.enc import encrypt_private_key, decrypt_private_key, hashpw, gensalt
 
def genBankUserUUID(db : Session):
    same = True
    uuid = ""
    while same == True:
        uuid = str(uuid4())
        bankAdmin = db.query(BankAdmin.uuid).filter(BankAdmin.uuid == uuid).first()
        if bankAdmin is None:
            same = False
    return uuid
 
 
def show_copyable_message(title, message):
    copy_window = tk.Toplevel()
    copy_window.title(title)
    copy_window.geometry("400x200")

    text_widget = tk.Text(copy_window, wrap="word", height=5)
    text_widget.insert("1.0", message)
    text_widget.config(state="disabled")
    text_widget.pack(pady=10, padx=10, fill="both", expand=True)

    copy_button = tk.Button(copy_window, text="Copy", command=lambda: copy_to_clipboard(message, copy_window))
    copy_button.pack(pady=5)

def copy_to_clipboard(text, window : tk.Toplevel):
    window.clipboard_clear()
    window.clipboard_append(text)
    window.update()  

def newBankAdminForm():
    result : tuple[str,str] | None = None
    def submit() -> tuple[str,str]:
        nonlocal result
        password = password_entry.get()
        
        salt = gensalt()
        hashed_pswd = hashpw(password=password.encode('utf-8'),salt=salt)
        
        email = email_entry.get()
        
        #is only accessible if they know the passphrase.
        intmed_passphrase = pass_phrase_entry.get()
        
        hashed_phrs = hashpw(intmed_passphrase.encode('utf-8'), salt=salt)
        # Do something with the username and email
        result = (email,password)
        #cert_bytes, intermediate_cert, key_bytes, intermediate_private_key

        
        print("Hashed password:",hashed_pswd)
        print("Hashed phrase:",hashed_phrs)
        db = getOracleDB()
        try:
            uuid = genBankUserUUID(db=db)
            #for file name
            cert_bytes, intermediate_cert, key_bytes, intermediate_private_key = genIntermed(passphrase=password,uuid=uuid)
            server_cert_bytes, server_key_bytes = generate_server_cert(intermediate_cert=intermediate_cert,intermediate_private_key=intermediate_private_key)
            client_cert_bytes, client_key_bytes = generate_client_cert(intermediate_cert=intermediate_cert,intermediate_private_key=intermediate_private_key,uuid=uuid,passphrase=intmed_passphrase)
            
            bankAdmin = BankAdmin(
                uuid = uuid,
                email = email,
                hashed_password = hashed_pswd,
                salt = salt,
                
                intermedCert = cert_bytes,
                interMedKey = key_bytes,
                hashed_phrase = hashed_phrs,
                
                cert = client_cert_bytes,
                privateKey = client_key_bytes,
                
                server_ca = server_cert_bytes,
                server_privateKey = server_key_bytes,
            )
            db.add(bankAdmin)
            db.commit()
            db.refresh(bankAdmin)
            
            root.destroy()
            
            show_copyable_message("Form Submission", f"User login id: {uuid}")
        except Exception as e:
            print(e)
        finally:
            db.close()
            
        

    root = tk.Tk()
    root.title("User Form")
    root.geometry("400x300")


    # Create and place the email label and entry
    email_label = tk.Label(root, text="Email:")
    email_label.pack(pady=(10, 0))
    email_entry = tk.Entry(root)
    email_entry.pack(pady=(0, 10))
    
    pass_phrase_label =  tk.Label(root, text="Passphrase:")
    pass_phrase_label.pack(pady=(10, 0))
    pass_phrase_entry = tk.Entry(root)
    pass_phrase_entry.pack(pady=(0, 10))
     
    password_label = tk.Label(root, text="Password:")
    password_label.pack(pady=(10, 0))
    password_entry = tk.Entry(root,show="*")
    password_entry.pack(pady=(0, 10))
    # Create and place the submit button
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack(pady=20)
    

    root.mainloop()
    return result