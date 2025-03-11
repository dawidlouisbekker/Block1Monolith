from .serverutils import ClientSocketThread,clientManager, colorsPrinter,os, getOracleDB,  bcrypt, socket, BASE_PATH, GetEntities, getFilesAndDirs, time, gensalt, hashpw
from .serverutils import BankAdmin, Admin, BankClient
from .adminutils import AdminSocketThread,BankAdminSocketThread
from pathlib import Path

CURRENT_DIR_STR = os.getcwd()
BASE_PATH = Path(CURRENT_DIR_STR) / Path("server") / Path("files")

#Changed to currentDir
def CreateDirectory(username: str, directoryName: str, currentDir: str | Path = "/") -> tuple[str, bool]:
    if "/" in directoryName:
        return (f"{colorsPrinter.RED}INVALID NAME{colorsPrinter.RESET}. No '/' or './' in the name", False)
    create_path = currentDir / directoryName
    print("Creating path:",create_path)
    if os.path.exists(create_path):
        return ("Path already exists.", False)
    
    os.mkdir(create_path)
    return (f"Created path: {directoryName}", True)
        
def DeleteDirectory(username: str, directoryName: str, currentDir: str = "/", delete_path : Path | None = None)  -> tuple[str, bool]:
    if "/" in directoryName:
        return (f"{colorsPrinter.RED}INVALID NAME{colorsPrinter.RESET}. No '/' or './' in the name", False)
    if delete_path is None:
        delete_path = BASE_PATH / username / directoryName
    print("Deleting path:",delete_path)
    if os.path.exists(delete_path):
        os.rmdir(path=delete_path)
        return (f"Deleted path {directoryName}", True)
    else:
        return ("Path does not exist.", False)


def getPath( name : str, stubs : list[str], file_name : str | None = None) -> Path:
    base = BASE_PATH / name 
    for stub in stubs:
        base = base / stub
    if file_name is not None:
        base = base / file_name
    return base

def handleClient(client : ClientSocketThread, addr):
    message : str | None = None
    colorsPrinter.logGreenAction(addr=addr,basemessage="CONNECTED",message="TCP AUTH socket")
    ftpSock : socket.socket | None = None
    
    
    def handle_invalid_value():
        client.sendJson(message={"message": "Invalid value.", "state": False})
        return False
    
    checkVal = lambda x: True if x is not None else handle_invalid_value()
    
    try:
        message = client.receiveMessage(baseMessage="LOGGEDIN",logMsg=True)
        try:
            client.EstablishUser(username=message)
            currentDir : Path = BASE_PATH / client.user.username
            try:
                while True:
                    msgdict = client.recieveJson()
                    print(msgdict)
                    print("Current directory:",currentDir)
                    subject = msgdict.get("subject")
                    action = msgdict.get("action")
                    if subject and action:
                        match subject:
                            case "directory":
                                if action == "back":
                                    currentDir = currentDir.parent
                                else:
                                    value = msgdict.get("value")
                                    
                                    if action == "create" and checkVal(value):
                                        try:                     
                                            result = CreateDirectory(username=client.user.username,directoryName=value,currentDir=currentDir)
                                            client.sendJson(message={ "message" : result[0], "state" : result[1] })
                                        except Exception as e:
                                            print(e)
                                            client.sendJson(message={ "message" : "Failed to create directory.", "state" : False })                                         
                                    #Required permission

                                    if action == "delete" and checkVal(value):
                                        try:
                                            del_dir = currentDir / value
                                            result = DeleteDirectory(username=client.user.username,directoryName=value,delete_path=del_dir)
                                            client.sendJson(message={ "message" : result[0], "state" : result[1] })
                                        except Exception as e:
                                            print(e)
                                            client.sendJson(message={ "message" : "Failed to create directory.", "state" : False })
                                            
                                    if action == "next" and checkVal(value):
                                        currentDir = currentDir / value
                                    
                                    if action == "get" and checkVal(value):
                                        files, dirs = getFilesAndDirs(username=client.user.username,path=currentDir)
                                        payload = { "files" : files, "dirs" : dirs }
                                        client.sendJson(payload)
                                        
                            case "file":
                                if action == "est":
                                    #create 
                                    value = msgdict.get("value")
                                    if value is not None:
                                        size : int = 0
                                        try:
                                            file_name : str | None = None
                                            try:
                                                file_name : str = msgdict.get("name")
                                                if "/" in file_name:
                                                    client.sendJson(message={ "message" : "Invalid name file name (No '/' allowed).", "state" : False })
                                                    file_name = None
                                            except:
                                                client.sendJson(message={ "message" : "Invalid name file name.", "state" : False })
                                                file_name = None

                                            if file_name != None:
                                                size = int(value)
                                                ftpSock = client.StartFTP()
                                                try:
                                                    ftpSock.listen()
                                                    ftp_client, addr = ftpSock.accept()
                                                    try:
                                                        file : str = ""
                                                        rounds = size // 64
                                                        if (rounds % 64) != 0:
                                                            rounds += 1
                                                        for i in range(rounds):
                                                            cacheLine = ftp_client.recv(64)
                                                            file = file + cacheLine.decode('utf-8')
                                                        #print(file)
                                                        try:    
                                                            file_path = currentDir / file_name
                                                            print("PATH:",file_path)
                                                            with open(file_path,"w+") as f:
                                                                f.write(file)
                                                                f.close()
                                                            client.sendJson(message={ "message" : "Recieved file.", "state" : True })
                                                        except:
                                                            client.sendJson(message={ "message" : "Failed to save file.", "state" : False })
                                                    except:
                                                        print("Error receiving file.")
                                                        client.sendJson(message={ "message" : "File transfer failed.", "state" : False })
                                                    finally:
                                                        ftp_client.close()
                                                        ftpSock.close()
                                                        msgdict = {}
                                                except Exception as e:
                                                    print("Error in accepting client:",e)
                                                    ftpSock.close()
                                                
                                                    
                                        except Exception as e:
                                            print(e)
                                            client.sendJson(message={ "message" : "Invalid file size.", "state" : False })

                                    else:
                                        client.sendJson(message={ "message" : "Did not receive file size.", "state" : False })
                                elif action == "get":
                                    try:
                                        file_name : str = msgdict.get("value")
                                        print("File:",file_name)
                                        if '/' in file_name:
                                            
                                            client.sendJson(message={ "message" : "Invalid name file name (No '/' allowed).", "state" : True })
                                            file_name = None
                                        
                                        if file_name is not None:
                                            
                                            ftpSock = client.StartFTP()
                                            ftpSock.listen()
                                            
                                            try:
                                                ftp_client, addr = ftpSock.accept()
                                                try:
                                                    file_path = currentDir / file_name
                                                    size = os.path.getsize(file_path)
                                                    with open(file_path, "rb") as file:
                                                        client.sendMessage(str(size))
                                                        while chunk := file.read(64):
                                                            ftp_client.sendall(chunk) 
                                                     
                                                except Exception as e:
                                                    print(e)
                                                    ftp_client.close()
                                                    ftpSock.close()
                                            except Exception as e:
                                                print(e)
                                                ftpSock.close()
                                        else:
                                            client.sendJson(message={ "message" : "Invalid file name.", "state" : False }) 
                                    except:
                                        client.sendJson(message={ "message" : "Failed to get file.", "state" : False })
                                        
                            case _:
                                client.sendJson(message={ "message" : "Invalid arguments.", "state" : False })
                        #client.sendJson()
                    else:
                        client.sendJson(message={"message" : "Insuffucient data.", "state" : False})
                    
            except Exception as e:
                print("Error in handle client:",e)
        except Exception as e: 
            client.sendJson({ "message" : e, "state" : False})
            
    except Exception as e:
        colorsPrinter.logRedAction(message=e)
    finally:
        clientManager.removeClient(client)

        
        

def handleAdmin(client_thread : ClientSocketThread, addr):
    messagedct : dict | None = None
    colorsPrinter.logGreenAction(addr=addr,basemessage="CONNECTED",message="TCP AUTH socket")
    try:
        def handle_invalid_value():
            client_thread.sendJson(message={"message": "Invalid value.", "state": False})
            return False
        checkVal = lambda x: True if x is not None else handle_invalid_value()
        try:
            messagedct = client_thread.recieveJson()
            uuid : str = messagedct.get('uuid')
            passphrase : str = messagedct.get('passphrase')
            password : str = messagedct.get('password')
            db = getOracleDB()
            admin = db.query(BankAdmin).filter(BankAdmin.uuid == uuid).first()
            
            if admin is None:
                colorsPrinter.logRedAction(basemessage="FAILED LOGGIN",message=f"user {colorsPrinter.YELLOW}{uuid}{colorsPrinter.RESET} tried to login.")
                client_thread.socket.close()
                return
            
            
            salt : bytes = admin.salt
            hashed_password : bytes = bcrypt.hashpw(password=password.encode("utf-8"),salt=salt)
            hashed_dbpassword : bytes = admin.hashed_password
            if hashed_password != hashed_dbpassword:
                colorsPrinter.logRedAction("INCORRECT PASSWORD",user=uuid)
                colorsPrinter.logRedAction(basemessage="ADMIN FAILED LOGIN",user=uuid)
                client_thread.socket.close()
                return

            hashed_phrase : bytes = bcrypt.hashpw(password=passphrase.encode('utf-8'),salt=salt)
            if hashed_phrase != admin.hashed_phrase:
                colorsPrinter.logRedAction("INCORRECT PHRASE",user=uuid)
                colorsPrinter.logRedAction(basemessage="ADMIN FAILED LOGIN",user=uuid)
                client_thread.socket.close()
                return   
            
            colorsPrinter.logGreenAction(basemessage="ADMIN LOGGEDIN",user=uuid)
            admin_sock = BankAdminSocketThread(sock_thread=client_thread,bankAdmin=admin,passphrase=passphrase)
            #client.EstablishUser(username=message)
            try:
                while True:
                    msgdict = admin_sock.recieveJson()
                    print("admins msg:",msgdict)
                    subject = msgdict.get("subject")
                    action = msgdict.get("action")
                    if subject and action:
                        match subject:
                            case "client":
                                if action == "action":
                                    value : dict = msgdict.get("value")
                                    firstname = value.get("firstname")
                                    middlename = value.get("middlename")
                                    lastname = value.get("lastname")
                                    email = value.get("email")
                                    cellNo = value.get("cellNo")
                                    idNumber = value.get("idNumber")
                                    password = value.get("password")
                                    print(f"Firstname: {firstname}, Middlename: {middlename}, Lastname: {lastname}, Email: {email}, Cell No: {cellNo}, ID Number: {idNumber}, Password: {password}")
                                    db = getOracleDB()
                                    salt = gensalt()
                                    hashed_password = hashpw(password=password.encode('utf-8'),salt=salt)
                                    try:
                                        client = BankClient(
                                            firstname=firstname,
                                            middlename=middlename,
                                            last_name=lastname,
                                            email=email,
                                            cell_no=cellNo,
                                            id_number=idNumber,
                                            hashed_passwd = hashed_password,
                                            salt=salt
                                        )
                                        db.add(client)
                                        db.commit()
                                        db.refresh(client)
                                        
                                    except Exception as e:
                                        print(e)
                                    finally:
                                        db.close()
                                elif action == "get":
                                    db = getOracleDB()
                                    try:
                                        clients = db.query(BankClient).all()
                                        clients_payload : dict = {}
                                        for client in clients:
                                            client_payload : dict = {
                                                "firstname" : client.firstname,
                                                "middlename" : client.middlename,
                                                "last_name" : client.last_name,
                                                "email" : client.email,
                                                "cell_no" : client.cell_no,
                                                "id_number" : client.id_number
                                            }
                                            clients_payload.update(client_payload)
                                        admin_sock.sendJson(clients_payload)
                                    except Exception as e:
                                        print(e)
                                    finally:
                                        db.close()
                                        
                            case "directory":
                                value = msgdict.get("value")
                                if action == "create" and checkVal(value):
                                    try:
                                        result = CreateDirectory(username=admin_sock.user.username,directoryName=value)
                                        admin_sock.sendJson(message={ "message" : result[0], "state" : result[1] })
                                    except Exception as e:
                                        print(e)
                                        admin_sock.sendJson(message={ "message" : "Failed to create directory.", "state" : False })

                                if action == "delete" and checkVal(value):
                                    try:
                                        result = DeleteDirectory(username=admin_sock.user.username,directoryName=value)
                                        admin_sock.sendJson(message={ "message" : result[0], "state" : result[1] })
                                    except Exception as e:
                                        print(e)
                                        admin_sock.sendJson(message={ "message" : "Failed to create directory.", "state" : False })
 
                            case "admins":
                                match action:
                                    case "get":
                                        admins = db.query(Admin.username,Admin.company,Admin.org_unit).all()
                                        print(admins)
                                        adminslist : list[dict[str,str]] = []
                                        for admin in admins:
                                            print(admin.tuple())
                                            admins_obj : dict = {
                                                "username" : admin.tuple()[0],
                                                "company" : admin.tuple()[1],
                                                "orgUnit" : admin.tuple()[2],
                                            }
                                            
                                            adminslist.append(admins_obj)
                                        admin_sock.sendJson(message=adminslist)
                                    case "add":
                                        value : dict = msgdict.get("value")
                                        if checkVal(value):
                                            db = getOracleDB()
                                            try:
                                                username : str = value.get("username")
                                                password : str = value.get("password")
                                                org_unit : str = value.get("orgUnit")
                                                company : str = value.get("company")
                                                salt : bytes = bcrypt.gensalt()
                                                hashed_password = bcrypt.hashpw(password=password.encode("utf-8"),salt=salt)
                                                admin = Admin(username=username,hashed_password=hashed_password.decode("utf-8"),org_unit=org_unit,salt=salt.decode("utf-8"),company=company)
                                                db.add(admin)
                                                db.commit()
                                                db.refresh(admin)
                                                admin_sock.sendJson(message={ "message" : "Admin added successfully.", "state" : True})
                                            except Exception as e:
                                                print(e)
                                            finally:
                                                db.close()
                                    case "update":
                                        value : dict = msgdict.get("value")
                                        if checkVal(value):
                                            org_unit = value.get("orgUnit")
                                            company = value.get("company")
                                            username = value.get("username")
                                            prevUsername = value.get("prevUsername")
                                            if prevUsername is not None:
                                                db = getOracleDB()
                                                try:
                                                    admn = db.query(Admin).filter(Admin.username == prevUsername).first()
                                                    if admn is not None:
                                                        Change = False
                                                        if org_unit is not None:
                                                            admn.org_unit = org_unit
                                                            Change = True
                                                        if company is not None:
                                                            admn.company = company
                                                            Change = True
                                                        
                                                        if Change == True:
                                                            print("Updating admin")
                                                            db.commit()
                                                            db.refresh(admn)
                                                        admin_sock.sendJson(message={ "message" : "Admin updated successfully.", "state" : True})
                                                    else:
                                                        admin_sock.sendJson(message={ "message" : "Admin not found.", "state" : False})
                                                finally:
                                                    db.close()
                                            else:
                                                admin_sock.sendJson(message={ "message" : "Invalid arguments.", "state" : False})
                                                
                            case _:
                                admin_sock.sendJson(message={ "message" : "Invalid arguments.", "state" : False })
                        #client.sendJson()
                    else:
                        admin_sock.sendJson(message={"message" : "Insuffucient data.", "state" : False})      
            except Exception as e:
                print("Error in handle client:",e)
                
        except Exception as e: 
            print(e)
            client_thread.sendJson({ "message" : "Error", "state" : False})
            
    except Exception as e:
        colorsPrinter.logRedAction(message=e)
    finally:
        clientManager.removeClient(client_thread)
        


        

    