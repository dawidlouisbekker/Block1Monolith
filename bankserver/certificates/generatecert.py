from cryptography import x509
from cryptography.x509.oid import ExtendedKeyUsageOID
from cryptography.x509.oid import NameOID
from cryptography.x509 import Certificate

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

def gen_admin_cert():
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
                format=serialization.PrivateFormat.PKCS8,
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
                format=serialization.PrivateFormat.PKCS8,
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
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    # Save client certificate
    with open("client_cert.pem", "wb") as f:
        f.write(client_cert.public_bytes(serialization.Encoding.PEM))

    print("Client certificate and key generated successfully.")
    return

if __name__ == "__main__":
    gen_cert()
    
def genClient(ca_cert : Certificate, ca_key : Certificate):
    
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
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    # Save server certificate
    with open("server_cert.pem", "wb") as f:
        f.write(server_cert.public_bytes(serialization.Encoding.PEM))

    print("Server certificate and key generated successfully.")
    
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
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    # Save client certificate
    with open("client_cert.pem", "wb") as f:
        f.write(client_cert.public_bytes(serialization.Encoding.PEM))