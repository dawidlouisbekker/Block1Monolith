package bankadmin;
import java.io.*;
import java.nio.file.*;
import java.security.cert.*;
import java.util.Base64;

public class CertificateLoader {
    public static X509Certificate loadCertificate(String certPath) throws Exception {
        // Read the certificate file
        String certPEM = new String(Files.readAllBytes(Paths.get(certPath)));

        // Remove PEM headers and footers
        certPEM = certPEM.replaceAll("-----BEGIN CERTIFICATE-----", "")
                         .replaceAll("-----END CERTIFICATE-----", "")
                         .replaceAll("\\s", ""); // Remove newlines and spaces

        // Decode Base64
        byte[] decodedCert = Base64.getDecoder().decode(certPEM);

        // Create CertificateFactory and generate X509Certificate
        CertificateFactory factory = CertificateFactory.getInstance("X.509");
        return (X509Certificate) factory.generateCertificate(new ByteArrayInputStream(decodedCert));
    }
}

