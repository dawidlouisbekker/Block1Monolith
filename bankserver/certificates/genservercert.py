from cryptography.x509.oid import ExtendedKeyUsageOID
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
# Generate server private key
server_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Server certificate signing request (CSR)
server_subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Server"),
    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
])

server_csr = (
    x509.CertificateSigningRequestBuilder()
    .subject_name(server_subject)
    .sign(server_key, hashes.SHA256())
)

# Sign the CSR with the CA key
server_cert = (
    x509.CertificateBuilder()
    .subject_name(server_csr.subject)
    .issuer_name(ca_cert.subject)
    .public_key(server_csr.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))  # 1 year
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
