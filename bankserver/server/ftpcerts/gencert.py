from cryptography import x509
from cryptography.x509.oid import ExtendedKeyUsageOID
from cryptography.x509.oid import NameOID
from cryptography.x509 import Certificate

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa

import datetime

COUNTR_NAME = "ZA"
ST_OR_PR_NAME = "Western Cape"
LOC_NAME = "Cape Town"
ORG_NAME = "ABFinances"
COMMON_NAME = "localhost"


subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, COUNTR_NAME),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, ST_OR_PR_NAME),
    x509.NameAttribute(NameOID.LOCALITY_NAME, LOC_NAME),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, ORG_NAME),
    x509.NameAttribute(NameOID.COMMON_NAME, COMMON_NAME),
])

def gen_cert():
# Generate CA private key
    ca_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Create CA certificate


    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=3650))
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True
        )
        .sign(ca_key, hashes.SHA256())
    )

    # Save CA key
    with open("ca_key.pem", "wb") as f:
        f.write(
            ca_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    # Save CA certificate
    with open("ca_cert.pem", "wb") as f:
        f.write(ca_cert.public_bytes(serialization.Encoding.PEM))

    print("CA certificate and key generated successfully.")
    
    server_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )



    server_csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(subject)
        .sign(server_key, hashes.SHA256())
    )

    # Sign the CSR with the CA key
    server_cert = (
        x509.CertificateBuilder()
        .subject_name(server_csr.subject)
        .issuer_name(ca_cert.subject)
        .public_key(server_csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365))  # 1 year
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=True
        )
        .sign(ca_key, hashes.SHA256())
    )

# Save server key
    with open("server_key.pem", "wb") as f:
        f.write(
            server_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    # Save server certificate
    with open("server_cert.pem", "wb") as f:
        f.write(server_cert.public_bytes(serialization.Encoding.PEM))

    print("Server certificate and key generated successfully.")


#def GenClientKey(ca_cert : Certificate, ca_key : Certificate):
    # Generate client private key
    client_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Client certificate signing request (CSR)


    client_csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(subject)
        .sign(client_key, hashes.SHA256())
    )

    # Sign the CSR with the CA key
    client_cert = (
        x509.CertificateBuilder()
        .subject_name(client_csr.subject)
        .issuer_name(ca_cert.subject)
        .public_key(client_csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365))  # 1 year
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.CLIENT_AUTH]), critical=True
        )
        .sign(ca_key, hashes.SHA256())
    )

    # Save client key
    with open("client_key.pem", "wb") as f:
        f.write(
            client_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    # Save client certificate
    with open("client_cert.pem", "wb") as f:
        f.write(client_cert.public_bytes(serialization.Encoding.PEM))

    print("Client certificate and key generated successfully.")
    return




def genClientCert() -> tuple[bytes,bytes]:
        # Load Root CA Private Key
    with open("certificates/admin_ca_key.pem", "rb") as key_file:
        root_private_key = serialization.load_pem_private_key(
            key_file.read(), password=None
        )

    # Load Root CA Certificate
    with open("certificates/admin_ca_cert.pem", "rb") as cert_file:
        root_ca_cert = x509.load_pem_x509_certificate(cert_file.read())
        
    client_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Client certificate signing request (CSR)
    client_csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(subject)
        .sign(client_key, hashes.SHA256())
    )

    # Sign the CSR with the CA key
    client_cert = (
        x509.CertificateBuilder()
        .subject_name(client_csr.subject)
        .issuer_name(root_ca_cert.subject)
        .public_key(client_csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365))  # 1 year
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.CLIENT_AUTH]), critical=True
        )
        .sign(root_private_key, hashes.SHA256())
    )

    # Save client key

    key_bytes = client_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        
    cert_bytes = client_cert.public_bytes(serialization.Encoding.PEM)
    return cert_bytes, key_bytes
    # Save client certificate


def generate_server_cert(intermediate_cert : Certificate, intermediate_private_key : RSAPrivateKey, common_name="localhost"):
    """
    Generates a server certificate signed by the given intermediary CA.
    
    Args:
        intermediate_cert (x509.Certificate): The intermediary CA certificate.
        intermediate_private_key (rsa.RSAPrivateKey): The intermediary CA private key.
        passphrase (str): Passphrase to encrypt the server private key.
        common_name (str): The common name for the server certificate (default: "server.example.com").

    Returns:
        tuple: (server_cert, server_private_key)
    """
    # Generate private key
    server_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Create CSR (Certificate Signing Request)
    server_csr = x509.CertificateSigningRequestBuilder().subject_name(
        x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(common_name)]), critical=False
    ).sign(server_private_key, hashes.SHA256())

    # Issue certificate
    server_cert = (
        x509.CertificateBuilder()
        .subject_name(server_csr.subject)
        .issuer_name(intermediate_cert.subject)  # Issuer is the intermediary CA
        .public_key(server_csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc)  + datetime.timedelta(days=365))  # 1-year validity
        .add_extension(
            x509.KeyUsage(
                digital_signature=True, 
                key_encipherment=True, 
                content_commitment=False,
                key_agreement=False, 
                data_encipherment=False, 
                key_cert_sign=False, 
                crl_sign=False,
                decipher_only=False,
                encipher_only=False
                ), critical=True
        )
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False
        )
        .sign(intermediate_private_key, hashes.SHA256())  # Sign with the intermediary CA
    )

    # Encrypt the private key with no passsphrase.
    private_key_bytes = server_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    server_cert_bytes = server_cert.public_bytes(serialization.Encoding.PEM)
    return server_cert_bytes, private_key_bytes

def generate_client_cert(intermediate_cert : Certificate, intermediate_private_key : RSAPrivateKey, passphrase : str, uuid : str, common_name="localhost"):
    """
    Generates a client certificate signed by the given intermediary CA.
    
    Args:
        intermediate_cert (x509.Certificate): The intermediary CA certificate.
        intermediate_private_key (rsa.RSAPrivateKey): The intermediary CA private key.
        passphrase (str): Passphrase to encrypt the client private key.
        common_name (str): The common name for the client certificate (default: "client@example.com").

    Returns:
        tuple: (client_cert, client_private_key)
    """
    # Generate private key
    client_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Create CSR (Certificate Signing Request)
    client_csr = x509.CertificateSigningRequestBuilder().subject_name(
        x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])
    ).sign(client_private_key, hashes.SHA256())

    # Issue certificate
    client_cert = (
        x509.CertificateBuilder()
        .subject_name(client_csr.subject)
        .issuer_name(intermediate_cert.subject)  # Issuer is the intermediary CA
        .public_key(client_csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365))  # 1-year validity
        .add_extension(
            x509.KeyUsage(digital_signature=True, 
                          key_encipherment=False, 
                          content_commitment=False,
                          key_agreement=False, 
                          data_encipherment=False, 
                          key_cert_sign=False, 
                          crl_sign=False,
                          decipher_only=False,
                          encipher_only=False,
                          ), critical=True
        )
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.CLIENT_AUTH]), critical=False
        )
        .sign(intermediate_private_key, hashes.SHA256())  # Sign with the intermediary CA
    )

    # Encryption is done else where so IV and enc key can be saved.
    key_bytes = client_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Save the certificate and private key
    cert_bytes = client_cert.public_bytes(serialization.Encoding.PEM)
    with open(f'bankadmncerts/{uuid}_cert.pem','wb') as f:
        f.write(cert_bytes)
    with open(f'bankadmncerts/{uuid}_key.pem','wb') as f:
        f.write(key_bytes)   
        
    return cert_bytes, key_bytes

def genIntermed(passphrase : str, uuid : str) -> tuple[bytes,Certificate,bytes,RSAPrivateKey]:
    # Load Root CA Private Key. Add password.
    print("Passphrase:",passphrase)
    with open("certificates/admin_ca_key.pem", "rb") as key_file:
        root_private_key = serialization.load_pem_private_key(
            key_file.read(), password=None
        )

    # Load Root CA Certificate
    with open("certificates/admin_ca_cert.pem", "rb") as cert_file:
        root_ca_cert = x509.load_pem_x509_certificate(cert_file.read())

    # Generate Intermediate CA Private Key
    intermediate_private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048
    )

    # Create Intermediate CA CSR (Certificate Signing Request)
    intermediate_subject = subject

    csr = x509.CertificateSigningRequestBuilder().subject_name(
        intermediate_subject
    ).sign(intermediate_private_key, hashes.SHA256())

    # Create Intermediate CA Certificate
    intermediate_cert = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(root_ca_cert.subject)  # Signed by Root CA
        .public_key(intermediate_private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365 * 5))  # 5 years
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=1), critical=True
        )
        .add_extension(
            x509.KeyUsage(
                key_cert_sign=True,  # Allows the key to be used for signing certificates (used for CAs)
                crl_sign=True,  # Allows the key to be used for signing Certificate Revocation Lists (CRLs)
                digital_signature=True,  # Allows the key to be used for creating digital signatures
                content_commitment=False,  # Disables use for signing content (e.g., email signatures)
                key_encipherment=False,  # Disables use for encrypting symmetric keys (e.g., TLS key exchange)
                data_encipherment=False,  # Disables use for direct data encryption (e.g., encrypting files)
                key_agreement=False,  # Disables use for key agreement protocols (e.g., Diffie-Hellman)
                encipher_only=False,  # Disables use of the key for encryption-only operations
                decipher_only=False  # Disables use of the key for decryption-only operations
            ), critical=True  # Marks this extension as critical (the certificate can't be used without it)
        )
        .sign(root_private_key, hashes.SHA256())  # Signed by Root CA
    )
    key_bytes : bytes = intermediate_private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(password=passphrase.encode('utf-8')),
            )
    
    cert_bytes : bytes = intermediate_cert.public_bytes(serialization.Encoding.PEM)
    with open(f'bankadmncerts/intermediary_{uuid}_cert.pem','wb') as f:
        f.write(cert_bytes)
            
    print("Intermediate CA certificate generated successfully!")
    return cert_bytes, intermediate_cert, key_bytes, intermediate_private_key

if __name__ == "__main__":
    #gen_cert()
    genIntermed()

