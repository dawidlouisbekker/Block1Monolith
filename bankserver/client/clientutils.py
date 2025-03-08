import ctypes
from pathlib import Path
import os
import socket
import sys
import ssl
import shutil

HOST = "localhost"
PORT = 21

BASE_PATH_STR = os.getcwd()
BASE_PATH = Path(BASE_PATH_STR) / "client"
WIN_FOPENER_DLL = BASE_PATH / Path("win") / "FileOpener.dll"

file_opener = ctypes.CDLL(str(WIN_FOPENER_DLL))
file_opener.OpenFileDialog.restype = ctypes.c_char_p

def createSSLContext(sock: socket.socket):
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # Use a secure TLS version
        context.load_cert_chain(certfile="client/client_cert.pem", keyfile="client/client_key.pem")
        context.load_verify_locations(cafile="certificates/ca_cert.pem")
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        print("Loaded certs")
        return context.wrap_socket(sock, server_side=False, server_hostname=HOST)
    except Exception as e:
        print("Error creating SSL Context:",e)

def handleOpenFile():
    result = file_opener.OpenFileDialog()
    if result:
        file_path = result.decode("utf-8")
        print(file_path)
        return file_path
    return ""

options : list[str] = []

def printLoader(total: int, current: int):
    cols, _ = shutil.get_terminal_size()
    bar_width = max(1, cols - 10)
    unit_perc = bar_width / total
    filled_width = int(current * unit_perc)

    sys.stdout.write("\r|\033[32m")

    for i in range(bar_width):
        if i < filled_width:
            sys.stdout.write("=")
        elif i == filled_width:
            sys.stdout.write(">")
        else:
            sys.stdout.write(" ")

    sys.stdout.write("\033[0m|")
    if total != current:
        sys.stdout.flush()

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
    
    def makeLarge(self,msg : str) -> str:
        lg = "".join(chr(ord(c) + 0xFEE0) if '!' <= c <= '~' else c for c in msg)
        return lg
    
    def logSuccess(self, message : str):
        print(f"{self.GREEN} {message} {self.RESET}")
        return

    def logGreenAction(self, basemessage : str = "SUCCESS",message : str | None = None, addr : tuple[str,int] | None = None, service : str | None = None):
        prnt = f"{self.GREEN} {basemessage}{self.RESET}"
        if addr is not None:
            prnt = prnt + f": {addr[0]}:{addr[1]}"
        if message is not None:
            prnt = prnt + f" | {message}"

        print(prnt)
        return

    def logRedAction(self, basemessage : str = "ERROR",message : str | None = None, addr : tuple[str,int] | None = None):
        prnt = f"{self.RED} {basemessage}{self.RESET}"
        if addr is not None:
            prnt = prnt + f" {addr[0]}:{addr[1]}"
        if message is not None:
            prnt = prnt + f" | {message}"
        print(prnt)
        return 
    
            
