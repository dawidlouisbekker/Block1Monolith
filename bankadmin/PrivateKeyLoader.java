package bankadmin;
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
            // If loading as PKCS#8 fails, check if the key is in PKCS#1 format
            if (keyPath.contains("pkcs1")) {
                decodedKey = convertPKCS1ToPKCS8(decodedKey); // Convert to PKCS#8 if it's PKCS#1
                PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(decodedKey);
                KeyFactory keyFactory = KeyFactory.getInstance("RSA");
                return keyFactory.generatePrivate(keySpec);
            } else {
                throw new InvalidKeySpecException("Unable to decode the private key");
            }
        }
    }

    private static byte[] convertPKCS1ToPKCS8(byte[] pkcs1Key) throws GeneralSecurityException {
        // Use BouncyCastle or another library to convert from PKCS#1 to PKCS#8
        // For now, you would need to add the conversion logic here
        throw new UnsupportedOperationException("PKCS#1 to PKCS#8 conversion not implemented");
    }
}


