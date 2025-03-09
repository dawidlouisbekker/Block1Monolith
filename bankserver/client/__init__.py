import json
from .clientutils import ConsoleColors, os, socket, ssl, sys, Path
from .clientutils import options as cursorOptions, BASE_PATH_STR, handleOpenFile, printLoader ,createSSLContext, HOST, PORT
import readchar
import signal
import time

  




#Globals

#Directory navigation
actionOptions : list[str] = ["Get File", "Send File", "Delete File", "Create Directory", "Delete Directory","Exit"]
options : list[str] = []
currentDir : str = "/"
dirStubs : list[str] = []
name : str | None = None

#
selected_idx = 0
action_idx = 0
choosen_idx : int | None = None 

selected_dir : str | None = None

select_dir : bool = False


select_file : bool = False

#Selecting Send file
send_file : bool = False
sending_file_path : str | None = None
send_file_content : str | None = None
sendFileOptions : list[str] = ["Send","Reselect","Back"]

#File Uploading
upload_file : bool = False

#File selection
sel_file_name : None | str = None

colorsPrinter = ConsoleColors()


def addOptional(arr : list[str], option : str):
    backInt : int | None = None
    try:
        backInt = arr.index(option)
    except ValueError:
        pass
    
    if backInt is None:
        arr.append(option) 


class ClientSocket:
    def __init__(self,sock : ssl.SSLSocket):
        self.socket : ssl.SSLSocket = sock
        self.__currentSendPacket : bytes | None = None
        self.__currentReceivePacket : bytes | None = None
        self.subjectSizes : dict[str,int] = {}
        self.directories : dict[str,list[str]] = {}
        self.files : dict[str,list[str]]  = {}
    
    def __sendPacket(self):
        if self.__currentSendPacket is None:
            raise Exception
        self.socket.send(self.__currentSendPacket)
        return
    
    def recieveFile():
        pass
    
    def __getSubjectSize(self, subject : str) -> int:
        resource_query = { "subject" : subject, "action" : "size"}
        self.sendJson(resource_query)
        msg = self.receiveMessage()
        size = int(msg)
        return size
    
    def sendMessage(self, message : str, encoding : str = "ascii"):
        self.__currentSendPacket = message.encode(encoding=encoding)
        self.__sendPacket()
        
    def recieveJson(self, estSize : int = 512) -> dict:
        jsonpayload = self.socket.recv(estSize)
        self.__currentReceivePacket = jsonpayload
        message = jsonpayload.decode('ascii')
        jsondict : dict = json.loads(message)
        return jsondict

    def receiveMessage(self,estSize : int = 512):
        self.__currentReceivePacket = self.socket.recv(estSize)
        return self.__currentReceivePacket.decode()

    def sendJson(self, content : dict, encoding : str = "ascii"):
        jsonpayload = json.dumps(content)
        self.__currentSendPacket = jsonpayload.encode(encoding=encoding)
        self.__sendPacket()
        
    
    def checkState(self) -> bool:
        try:
            msg = self.socket.recv(64)
            state : dict = json.loads(msg.decode())
            stateTpl = getMsgState(msgdict=state)
            if stateTpl[1] == False:
                colorsPrinter.logRedAction(basemessage="FAILED",message=stateTpl[0])
            elif stateTpl[1] == True:
                colorsPrinter.logGreenAction(basemessage="SUCCESS",message=stateTpl[0])
            return stateTpl[1]
        except Exception as e:
            print("Failed to get message state:",e)
            
        
         
    
    def getSubject(self, subject : str) -> dict[str,list[str]]:
        if subject not in self.subjectSizes.keys():
            try:
                size = self.__getSubjectSize(subject=subject)
                self.subjectSizes[subject] = size
            except Exception as e:
                print(e)
                return
        resource_query = { "subject" : subject, "action" : "get" }
        
        try:
            self.sendJson(content=resource_query)
            msg = self.recieveJson(self.subjectSizes[subject])
            match subject:
                case "entities":
                    self.entities = msg
        except Exception as e:
            print(e)

sock_cls : ClientSocket | None = None

def printAction(action : str):
    print(f"{colorsPrinter.YELLOW}ACTION{colorsPrinter.RESET}: {action}")

def selectSendFile():
    printAction(action="Selecting File to Send")
    global sending_file_path, options, send_file_content, selected_idx, sendFileOptions, sel_file_name
    options = sendFileOptions
    selected_idx = min(max(selected_idx, 0), len(sendFileOptions) - 1)
    prnt : str = ""
    if sending_file_path is not None:
        prnt = f"\n{colorsPrinter.YELLOW}SELECTED FILE{colorsPrinter.RESET}: {sending_file_path}"
        if sending_file_path != "":
            with open(sending_file_path,"r") as file:
                send_file_content = file.read()
                file.close()
        else:
            send_file_content = ""
    else:
        print(f"\n{colorsPrinter.RED}NO{colorsPrinter.RESET} file path")

    if sel_file_name is not None:
        prnt = prnt + f"\t{colorsPrinter.YELLOW}NAME{colorsPrinter.RESET}: {sel_file_name}"
        
    
    if send_file_content is None:
        print(f"{colorsPrinter.RED}NO{colorsPrinter.RESET} file content\n")
    else:
        prnt = prnt + f"\t{colorsPrinter.YELLOW}SIZE{colorsPrinter.RESET}: {len(send_file_content)} bytes\n"
    if prnt != "":
        print(prnt)

    for i, option in enumerate(options):
        if i == selected_idx:
            print(f"> {colorsPrinter.BLUE}{option}{colorsPrinter.RESET} <")
        else:
            print(f"  {option}")
    
    if sending_file_path is None:
        file_path = handleOpenFile()
        sending_file_path = file_path
        path = Path(file_path)
        sel_file_name = path.name
        print_menu()
    return



def selectDir(dirs : list[str]):
    printAction(action="Selecting Directory")
    global options
    global selected_idx

    
    options = dirs
    selected_idx = min(max(selected_idx, 0), len(options) - 1)
    if len(options) > 0:
        print(f"\nPress {colorsPrinter.YELLOW}enter{colorsPrinter.RESET} to {colorsPrinter.RED}DELETE{colorsPrinter.RESET} {options[selected_idx]}")
    
    print("\n--- Options ---")
    if dirs:
        print(f"{colorsPrinter.BLUE}Directories:{colorsPrinter.RESET}")
        for i, directory in enumerate(dirs):
            if i == selected_idx:
                print(f"> {colorsPrinter.BLUE}{directory}{colorsPrinter.RESET} <")
            else:
                print(f"  {directory}")

def connectFTP() -> socket.socket:
    resp = sock_cls.recieveJson()
    print("Response:",resp)

    ftpSock : socket.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("")
    lg = colorsPrinter.makeLarge("CONNECTING")
    msg = f"{colorsPrinter.BLUE}FTP"
    colorsPrinter.logGreenAction(basemessage=lg,message=msg)
    print("")
    try:
        ftpPort = resp["port"]
        ftpSock.connect((HOST,ftpPort))
        colorsPrinter.logGreenAction(basemessage="CONNECTED")
    except Exception as e:
        print(e)
        ftpSock.close() 
    return ftpSock

def selectFile(files : list[str]): 
    printAction(action="Selecting File")
    global options
    global selected_idx
    
    options = files
    selected_idx = min(max(selected_idx, 0), len(options) - 1)
    print("\n--- Options ---")
    if files:
        print(f"{colorsPrinter.BLUE}Files:{colorsPrinter.RESET}")
        for i, file in enumerate(files):
            if i == selected_idx:
                print(f"> {colorsPrinter.BLUE}{file}{colorsPrinter.RESET} <")
            else:
                print(f"  {file}")

def UploadFile():
    global send_file_content
    global upload_file 
    global send_file
    global dirStubs
    
    if send_file_content == "" or send_file_content == None:
        colorsPrinter.logRedAction(basemessage="NO CONTENT",message="No file content.")
        upload_file = False
        send_file = True  
        time.sleep(0.5)
        print_menu(dirs=[],files=[]) 

    if send_file_content != None and send_file_content != "":
        upload_file = False
        send_file = True
        file_size = len(send_file_content)
        sock_cls.sendJson({ "subject" : "file", "action" : "est", "value" : file_size, "name" : sel_file_name, "stubs" : dirStubs })
        
        try:
            ftpSock = connectFTP()
            print("")
            rounds = file_size // 64
            if file_size % 64 != 0:
                rounds += 1
            for i in range(rounds):
                pos = i*64
                cacheLine = send_file_content[pos:(pos+64)]
                ftpSock.sendall(cacheLine.encode('utf-8'))
                printLoader(rounds,i)
            printLoader(rounds,rounds)
            print("\n")
            print("")
            send_file_content = None
            success = sock_cls.checkState()
            print(f" {colorsPrinter.YELLOW}DONE{colorsPrinter.RESET}")
            print("\n Press enter to continue...")
            while True:
                key = readchar.readkey()
                if key == readchar.key.ENTER:
                    break
            print_menu()
        except Exception as e:
            print(e)
        

def receiveFile(file_name : str):
    try:
        sock_cls.sendJson({ "subject" : "file", "action" : "get", "value" : file_name, "stubs" : dirStubs   })
        ftpSock = connectFTP()
        file:  str = ""
        try:
            asc_size = sock_cls.receiveMessage()

            size = int(asc_size)
            file = ""
            rounds = size // 64
            if (rounds % 64) != 0:
                rounds += 1
            for i in range(rounds):
                cacheLine = ftpSock.recv(64)
                file = file + cacheLine.decode('utf-8')
                printLoader(rounds,i)
            printLoader(rounds,rounds)
            print("\n")
            try:
                ftpSock.close()
                if file != "":
                    file_options = ["Download", "Back"]
                    index = 0
                    selected_file_action: int | None = None
                    ret: bool = False

                    # Clear screen
                    os.system('cls' if os.name == 'nt' else 'clear')

                    lg = "FILE"
                    prnt = "\033[33m" + lg + "\033[0m"  # Simulated Yellow color
                    lg = colorsPrinter.makeLarge(file_name)  # Simulating `colorsPrinter.makeLarge(file_name)`
                    prnt = prnt + "  |  \033[34m" + lg + "\033[0m\n"  # Simulated Blue color

                    print(prnt.center(50))
                    print("")

                    # Print file content
                    lines = file.split("\n")
                    for i, line in enumerate(lines):
                        print(f"\u001b[38m {i + 1}{colorsPrinter.RESET}  {line}")

                    print("\n")

                    # Print initial options
                    for i, option in enumerate(file_options):
                        if index == i:
                            print(f"  \033[33m{i + 1}. {option}\033[0m")
                        else:
                            print(f"  {i + 1}. {option}")

                    while not ret:
                        sys.stdout.write(f"\033[{len(file_options)}A") 
                        # Reprint options
                        for i, option in enumerate(file_options):
                            sys.stdout.write("\033[K")
                            if index == i:
                                print(f"  \033[33m{i + 1}. {option}\033[0m")
                            else:
                                print(f"  {i + 1}. {option}")

                        # Read user input
                        key = readchar.readkey()
                        if key == readchar.key.UP and index > 0:
                            index -= 1
                        elif key == readchar.key.DOWN and index < len(file_options) - 1:
                            index += 1
                        elif key == readchar.key.ENTER:
                            downld_path = f"client/downloads/{file_name}"
                            if index == 0:
                                with open(downld_path,'w+') as f:
                                    f.write(file)
                                downld_path = os.getcwd().replace("\\","/") + downld_path
                                colorsPrinter.logGreenAction(basemessage="DOWNLOADED",message=downld_path)
                                time.sleep(1)
                                ret = True
                            else:
                                ret = True
                            
                else:
                    print("NO CONTENT")
            except Exception as e:
                print(e)
        except:
            ftpSock.close()            
    except:
        colorsPrinter.logRedAction(basemessage="FAILED",message="Failed to get file.")


     
def print_menu(dirs: list[str] = [], files: list[str] = []):
    os.system('cls' if os.name == 'nt' else 'clear')
    global selected_idx, action_idx, send_file, select_dir, select_file
    global upload_file
    global dirStubs
    #print("Selected index:",selected_idx)
    prnt = f"{colorsPrinter.BLUE}USERNAME: {colorsPrinter.YELLOW}{name}{colorsPrinter.RESET}\n"
    base = colorsPrinter.makeLarge("CONNECTED")
    colorsPrinter.logGreenAction(basemessage=base, message=prnt)
    full_directory = colorsPrinter.YELLOW
    if len(dirStubs) == 0:
        full_directory += "/"
    else:
        for stub in dirStubs:
            full_directory += f"/  {stub}  "
    full_directory += colorsPrinter.RESET
    print(f"{colorsPrinter.BLUE}CURRENT DIRECTORY: {colorsPrinter.YELLOW}{full_directory}{colorsPrinter.RESET}")
    
    if select_dir:
        selectDir(dirs=dirs) 
    elif select_file:
        selectFile(files=files)
    elif send_file:
        selectSendFile()
    elif upload_file:
        UploadFile()
        
    else:
        global options
        options = files + dirs + actionOptions
        if currentDir != "/":
            backInt : int | None = None
            try:
                backInt = actionOptions.index("Back")
            except ValueError:
                pass
            
            if backInt is None:
                actionOptions.append("Back")
        else:
            backInt : int | None = None
            try:
                backInt = actionOptions.index("Back")
            except ValueError:
                pass
            
            if backInt is not None:
                actionOptions.remove("Back")        

        selected_idx = min(max(selected_idx, 0), len(options) - 1)
        print("\n--- Options ---")

        # Print files
        if files:
            print(f"{colorsPrinter.BLUE}Files:{colorsPrinter.RESET}")
                
            for i, file in enumerate(files):
                if i == selected_idx:
                    print(f"> {colorsPrinter.BLUE}{file}{colorsPrinter.RESET} <")
                else:
                    print(f"  {file}")
        else:
            print("\n NO FILES ")
        # Print directories
        if dirs:
            print(f"{colorsPrinter.BLUE}Directories:{colorsPrinter.RESET}")
                
            for i, directory in enumerate(dirs, start=len(files)):
                if i == selected_idx:
                    print(f"> {colorsPrinter.BLUE}{directory}{colorsPrinter.RESET} <")
                else:
                    print(f"  {directory}")
        else:
            print("\n NO DIRECTORIES")
        print("\n")

        # Print actions
        if actionOptions:
            print(f"{colorsPrinter.BLUE}Actions:{colorsPrinter.RESET}")
            for i, action in enumerate(actionOptions, start=len(files) + len(dirs)):
                if i == selected_idx:
                    print(f"> {colorsPrinter.YELLOW}{action}{colorsPrinter.RESET} <")
                else:
                    print(f"  {action}")



def getMsgState(msgdict : dict) -> tuple[str,bool]:
    try:
        message : str = msgdict.get("message")
        state : bool = msgdict.get("state")
        if message is None:
            raise Exception("No message provided")
        if state is None:
            raise Exception("No state is provided")
        return (message,state)
    except Exception as e:
        print("Error in getting message state:",e)  
        return


class FTPServer:
    def __init__(self):
        pass
        #load cert
        #self.socket = socket.socket



        
        #payload = self.recieveJson(estSize=)
        
        



def connectClient(username : str, password : str | None = None):
    global selected_idx
    global action_idx
    global choosen_idx
    global name
    global options
    
    #Select dir for delete
    global select_dir
    global selected_dir
    
    global select_file
    global currentDir
    
    #select sending file vars
    global sendFileOptions
    global send_file
    global sending_file_path
    global send_file_content

    #send file
    global upload_file
    global sock_cls
    
    name = username
    
    dict_resp : dict | None = None
    client = createSSLContext(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
    client.connect((HOST,PORT))
    sock_cls = ClientSocket(sock=client)
    sock_cls.sendMessage(message=username)
    dict_resp = sock_cls.recieveJson()
    state = getMsgState(dict_resp)
    
    if state[1] == False:
        colorsPrinter.logRedAction(basemessage="FAILED",message=state[0])
        client.close()
        return
    
    colorsPrinter.logGreenAction(basemessage="ESTABLISHED CONNECTION",message=state[0])
    try:
        msg = sock_cls.receiveMessage()
        print(msg)
        size = int(msg)
        entities = sock_cls.recieveJson(estSize=size)
        print(entities)
        sock_cls.files = entities["files"]
        sock_cls.directories = entities["dirs"]
        options  = sock_cls.files[currentDir] + sock_cls.directories[currentDir] + actionOptions
        while options[selected_idx] != "Exit":
            try:
                while choosen_idx is None:
                    try:
                        if not send_file:
                            options = []
                            files = []
                            directories = []
                            total_files = 0
                            total_dirs = 0
                            if sock_cls.files.get(currentDir) is not None:
                                options = sock_cls.files[currentDir]
                                files = sock_cls.files[currentDir]
                                total_files = len(sock_cls.files[currentDir])
                                
                            if sock_cls.directories.get(currentDir) is not None:
                                options = options + sock_cls.directories[currentDir]
                                directories = sock_cls.directories[currentDir]
                                total_dirs = len(sock_cls.directories[currentDir])
                                
                            options = options + actionOptions                        
                            print_menu(files=files, dirs=directories)
                        else:
                            print_menu()
                    except Exception as e:
                        print("Error in top",e)
                        
                    
                    
                    total_options = total_files + total_dirs + len(actionOptions)
                    #print("Len dir:",total_dirs)
                    key = readchar.readkey()
                    #Nav. Actions below
                    if key == readchar.key.UP and selected_idx > 0:
                        selected_idx -= 1
                        
                    if key == readchar.key.DOWN:
                        if select_dir and selected_idx < total_dirs - 1:
                            selected_idx += 1
                            
                        elif select_file and selected_idx < total_files - 1:
                            selected_idx += 1
                            
                        elif send_file and selected_idx < (len(sendFileOptions) - 1):
                            selected_idx += 1
                            
                        elif select_file == False and selected_idx < total_options - 1:
                            selected_idx += 1
                    #All actions. Also processed in display menu's functions
                    elif key == readchar.key.ENTER:
                        try:
                            if select_dir:
                                try:
                                    if len(options) != 0 and sock_cls.directories.get(currentDir) is not None:
                                        selected_dir = options[selected_idx]
                                        print(f"Selected {colorsPrinter.YELLOW}DIRECTORY{colorsPrinter.RESET}:",selected_dir)
                                        sock_cls.sendJson({ "subject" : "directory", "action" : "delete", "value" : selected_dir  })
                                        success = sock_cls.checkState()
                                        if success:
                                            sock_cls.directories[currentDir].remove(selected_dir)
                                        select_dir = False
                                        selected_idx = 0
                                    else:
                                        colorsPrinter.logRedAction(basemessage="NO DIRECTORIES")
                                        time.sleep(1)
                                except Exception as e:
                                    print(e)
                                    time.sleep(1)
                                    
                            elif send_file:
                                match sendFileOptions[selected_idx]:
                                    case "Send":
                                        send_file = False
                                        upload_file = True
                                        
                                    case "Back":
                                        print("Returning")
                                        send_file = False
                                        select_file = False
                                        sending_file_path = None
                                        send_file_content = None
                                        
                                    case "Reselect":
                                        sending_file_path = None
                                        send_file_content = None             
                                       
                            else:
                                if selected_idx >= (total_files + total_dirs):
                                    match options[selected_idx]:
                                        case "Create Directory":
                                            name = input(f"\nEnter {colorsPrinter.YELLOW}DIRECTORY{colorsPrinter.RESET} name: ")
                                            sock_cls.sendJson({ "subject" : "directory", "action" : "create", "value" : name, "stubs" : dirStubs })
                                            success = sock_cls.checkState()
                                            if success:
                                                sock_cls.directories[currentDir].append(name)
                                                sock_cls.files[name] = []
                                                
                                        case "Delete Directory":
                                            print("Select Directory though navigation.")
                                            select_dir = True
                                            selected_idx = 0

                                        case "Send File":
                                            send_file = True
                                            selected_idx = 0
                                        case "Back":
                                            dirStubs.pop()
                                            if len(dirStubs) == 0:
                                                currentDir = "/"
                                            else: 
                                                currentDir = "".join(dirStubs)
                                            sock_cls.sendJson({ "subject" : "directory", "action" : "back"})
                                            
                                            
                                                
                                elif selected_idx < total_files:
                                    try:
                                        file_name = options[selected_idx]
                                        try:
                                            receiveFile(file_name=file_name)
                                        except:
                                            print("Something went wrong.")
                                    except:
                                        print("Invalid file.")
                                        time.sleep(0.5)
                                elif selected_idx < (total_files + total_dirs):
                                    try:
                                        dirStubs.append(options[selected_idx])
                                        currentDir = "".join(dirStubs)
                                        if not sock_cls.directories[currentDir]:
                                            sock_cls.sendJson({ "subject" : "directory", "action" : "next", "value" : options[selected_idx] })
                                            tempdirs = sock_cls.directories
                                            recvd_entities : dict = sock_cls.recieveJson()
                                            files = recvd_entities["files"]
                                            dirs = recvd_entities["dirs"]
                                            for sdir in dirs:
                                                sdir = currentDir + sdir
                                                sock_cls.directories.update({ sdir : [] })
                                            sock_cls.directories.update({ currentDir : dirs })
                                            sock_cls.files.update({ currentDir : files })
                                        sock_cls.directories = tempdirs
                                        selected_idx = 0
                                    except Exception as e:
                                        print(e) 
                                        time.sleep(5)
                                        
                                    
                                    
                        except Exception as e:
                            print("Error in handling selection:",e)
                        finally:
                            time.sleep(0.1)
                            choosen_idx = None
                        try:
                            if options[selected_idx] == "Exit":
                                break
                        except Exception as e:
                            print("Error in exit option:",e)
            except Exception as e:
                print("Error while choosing index:",e)
                
    except Exception as e:
        print("Error:",e)
    finally:
        client.close()
    #client.send(f"lose".encode('ascii'))
    
    

if __name__ == "__main__":
    connectClient()