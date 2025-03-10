package companyportal.tlscontext;
import java.nio.file.*;
import java.security.*;
import java.security.spec.*;
import java.util.Base64;

public class PrivateKeyLoader {

    public static PrivateKey loadPrivateKey(String keyPath) throws Exception {
        // Read the key file
        String keyPEM = new String(Files.readAllBytes(Paths.get(keyPath)));

        // Remove PEM headers and footers
        keyPEM = keyPEM.replaceAll("-----BEGIN (RSA )?PRIVATE KEY-----", "")
                       .replaceAll("-----END (RSA )?PRIVATE KEY-----", "")
                       .replaceAll("\\s", ""); // Remove newlines and spaces

        // Decode Base64
        byte[] decodedKey = Base64.getDecoder().decode(keyPEM);

        try {
            // Attempt to load the key as PKCS#8
            PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(decodedKey);
            KeyFactory keyFactory = KeyFactory.getInstance("RSA");
            return keyFactory.generatePrivate(keySpec);
        } catch (InvalidKeySpecException e) {
                throw new InvalidKeySpecException("Unable to decode the private key. Set to PKCS#8 when generating the key.");
        }
    }

}


