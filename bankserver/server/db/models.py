from sqlalchemy import create_engine, Column, String, Integer, Engine, LargeBinary, ForeignKey, Float, Boolean
from sqlalchemy.orm import declarative_base, Session, sessionmaker
from sqlalchemy.engine import Engine
import os
import cx_Oracle
import sys
import bcrypt


CON_STR_DRIVER = "oracle+cx_oracle://"
CON_STR_HOST = "@DawidBekker2005:1521/XE"

OWNER = os.getenv("OWNER", "c##bank_user:askljnobbDSAi12sSda")

#SQLITE_URI = os.getenv("SQLITE_URI", "sqlite:///users.db")
ORACLE_URI = f"{CON_STR_DRIVER}{OWNER}{CON_STR_HOST}"

try:
    lib_dir = r"C:\instantclient_18_5"
    cx_Oracle.init_oracle_client(lib_dir=lib_dir)
    print("Oracle client initialized successfully.")
except Exception as err:
    print("Failed to initialize Oracle client!")
    print(err)
    sys.exit(1)

# Create SQLAlchemy engine for Oracle
engine = create_engine(ORACLE_URI)

# Declare the base for your models
Base = declarative_base()

# Create sessionmaker for session management
sesh_maker = sessionmaker(bind=engine)

def getOracleDB() -> Session:
    """Returns a new database session."""
    return sesh_maker()
'''
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    hashed_password = Column(String)
    server_cert = Column(String)
    key = Column(String)
    salt = Column(String)
'''

'''
Both intermediary and client ca and keys are kept on client, client uses intermediary to validate server. Both use the same phrase.
priv_enc_key is for the encryption of the data.
'''

CERT_SIZE = 200
KEY_SIZE = 200

class BankAdmin(Base):
    __tablename__ = "bank_admins"
    uuid = Column(String(36),primary_key=True)
    email = Column(String(60),nullable=False)
    
    hashed_password = Column(LargeBinary)
    salt = Column(LargeBinary)
    
    intermedCert = Column(LargeBinary)
    interMedKey = Column(LargeBinary)
    hashed_phrase = Column(LargeBinary)
    
    cert = Column(LargeBinary)
    privateKey = Column(LargeBinary)
    
    server_ca = Column(LargeBinary)
    server_privateKey = Column(LargeBinary)

class Admin(Base):
    __tablename__ = "ftp_admins"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    hashed_password = Column(String(200))
    salt = Column(String(100))
    org_unit = Column(String(60),nullable=True)
    company = Column(String(60),nullable=True)

class BankClient(Base):
    __tablename__ = "clients"
    client_id = Column(Integer, autoincrement=True, primary_key=True)
    firstname = Column(String(70))
    middlename = Column(String(70))
    last_name = Column(String(70))
    email = Column(String(60))
    cell_no = Column(String(13))
    id_number = Column(String) 
    hashed_passwd = Column(LargeBinary)
    salt = Column(LargeBinary)

class Company(Base):
    __tablename__ = "companies"
    company_id = Column(Integer,autoincrement=True,primary_key=True)
    name = Column(String(60))
    hashed_password = Column(LargeBinary)
    intmedCert = Column(LargeBinary)
    hashed_passphrase = Column(LargeBinary)
    intmdPrivKey = Column(LargeBinary)
    salt = Column(LargeBinary)

class Account(Base):
    __tablename__ = "accounts"
    account_id = Column(Integer,autoincrement=True,primary_key=True)
    client_id =  Column(Integer,ForeignKey("clients.client_id"),nullable=True)
    company_id = Column(Integer,ForeignKey("companies.company_id"),nullable=True)
    balance = Column(Float)

class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, autoincrement=True, primary_key=True)
    acount_id = Column(Integer,ForeignKey("accounts.account_id"), nullable=False)
    amount = Column(Float, nullable=False)
    reference = Column(String(100))
    description = Column(String(200))
    ref_transaction = Column(Integer,ForeignKey("transactions.transaction_id"))

class Group(Base):
    __tablename__ = "company_groups"
    group_id = Column(Integer, autoincrement=True, primary_key=True)
    company_id = Column(Integer,  ForeignKey("companies.company_id"))
    group_name = Column(String(60), nullable=False)
    group_code = Column(String(100), nullable=False)

class UserGroup(Base):
    __tablename__ = "user_groups"
    intance_id = Column(Integer,primary_key=True)
    group_id = Column(Integer,ForeignKey("company_groups.group_id"))
    user_uuid = Column(String(36), ForeignKey("company_users.user_id"))
    ftp_login = Column(Boolean)
    ftp_upload = Column(Boolean)
    ftp_download = Column(Boolean)

class CompanyUser(Base):
    __tablename__ = "company_users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36))
    email = Column(String(60), nullable=False)
    
    hashed_password = Column(LargeBinary)
    salt = Column(LargeBinary)
    
    cert = Column(LargeBinary)
    key = Column(LargeBinary)
    
        
'''
    def createGroupsTable(self):
        table_name = f"{self.name}_groups"
        GroupsTable = type(
            table_name,
            (Base,),
            {
                "__tablename__" : table_name,
                "id" : Column(Integer,primary_key=True,autoincrement=True),
                "name" : Column(String(60),nullable=False)
                ""
            }
        )
'''
    

def getAdmin(username : str, password : str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=password.encode("utf-8"), salt=salt)
    newAdmin = Admin(
        username=username,
        hashed_password=hashed_password.decode(encoding="utf-8"),
        salt=salt.decode(encoding="utf-8")
    )
    db = getOracleDB()
    try:
        db.add(newAdmin)
        db.commit()
        db.refresh(newAdmin)
    finally:
        db.close()


def CreateTables():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    try:
        CreateTables()
    finally:
        exit()
        
    add = False
    if add:
        getAdmin(username="dawid",password="123456")
    else:
        try:
            # Test connection
            sesh = getOracleDB()
            try:
                admins = sesh.query(Admin).all()
                for admin in admins:
                    print(admin.username)
                    print(admin.hashed_password)
                print("Connected successfully")
                # Create tables (if not already created)
                #print("Tables created successfully.")
                sesh.close()
            finally:
                sesh.close()
        except Exception as err:
            print("Failed to connect to Oracle database!")
            print(err)
            sys.exit(1)