package bankadmin;
import javax.net.ssl.*;
import java.io.*;
import java.security.*;
import java.security.cert.*;
import java.security.cert.Certificate;


public class AdminSocket {
    protected SSLSocket socket;
    protected String addr;
    protected int port; 
    protected String certPath;
    protected String key;

    public AdminSocket(String addr, int port, String certPath, String keyPath, String ca_cert_path, String passphrase) throws Exception {
        System.out.println("Creating ssl context.");
        SSLContext sslContext = createSSLContext(certPath, keyPath, ca_cert_path, passphrase);
        System.out.println("Getting Socket Factory.");
        SSLSocketFactory factory = sslContext.getSocketFactory();

        System.out.println("Creating Socket.");
        socket = (SSLSocket) factory.createSocket(addr, port);
        System.out.println("Starting handshake.");
        socket.startHandshake(); // Perform TLS handshake
    }

    public OutputStream getOutputStream() throws IOException {
        return socket.getOutputStream();
    }

    public InputStream getInputStream() throws IOException {
        return socket.getInputStream();
    }

    private SSLContext createSSLContext(String certPath, String keyPath, String CAPath, String passphrase) throws Exception {
        // Load client certificate

        if (!CAPath.equals("") && !CAPath.equals("")) {
            X509Certificate caCertificate = CertificateLoader.loadCertificate(CAPath);

            // Create a KeyStore to store the CA certificate
            KeyStore trustStore = KeyStore.getInstance(KeyStore.getDefaultType());
            trustStore.load(null, passphrase.toCharArray()); // Create empty trust store
            trustStore.setCertificateEntry("ca-cert", caCertificate); // Store CA certificate
        
            // Initialize TrustManagerFactory with the truststore (for verifying certificates)
            TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
            tmf.init(trustStore);
        
            System.out.println("CA certificate loaded and trust store initialized.");
        
            System.out.println("Loading client certificate...");
            // Load client certificate
            X509Certificate certificate = CertificateLoader.loadCertificate(certPath);
            System.out.println("Client certificate loaded.");
        
            // Load private key
            PrivateKey privateKey = PrivateKeyLoader.loadPrivateKey(keyPath);
            System.out.println("Private key loaded successfully.");
        
            // Create a KeyStore to hold the cert and key
            KeyStore keyStore = KeyStore.getInstance(KeyStore.getDefaultType());
            keyStore.load(null, null); // Create empty keystore
            keyStore.setKeyEntry("client-key", privateKey, "".toCharArray(), new Certificate[]{certificate});
        
            System.out.println("Initializing KeyManagerFactory...");
            // Initialize KeyManagerFactory with the keystore
            KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
            kmf.init(keyStore, "".toCharArray());
        
            System.out.println("Initializing SSL context...");
            // Initialize SSLContext
            SSLContext sslContext = SSLContext.getInstance("TLS");
            sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), new SecureRandom());
        
            System.out.println("SSL context initialized successfully.");
            return sslContext;
        } else {
            System.out.println("loading cert.");
            X509Certificate certificate = CertificateLoader.loadCertificate(certPath);
            System.out.println("Loaded cert.");
    
            // Load private key
            PrivateKey privateKey = PrivateKeyLoader.loadPrivateKey(keyPath);
            System.out.println("Private key loaded successfully.");
            System.out.println("Creating keystore.");
            // Create a KeyStore to hold the cert and key
            KeyStore keyStore = KeyStore.getInstance(KeyStore.getDefaultType());
            keyStore.load(null, null); // Create empty keystore
            keyStore.setKeyEntry("client-key", privateKey, "".toCharArray(), new Certificate[]{certificate});
    
            System.out.println("Initializing key manager factory.");
            // Initialize KeyManagerFactory with the keystore
            KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
            kmf.init(keyStore, "".toCharArray());
    
            System.out.println("Creating trusted manager.");
            // Create a TrustManager that accepts all certificates (Disables self-signed checks)
            TrustManager[] trustAllCerts = new TrustManager[]{
                new X509TrustManager() {
                    public java.security.cert.X509Certificate[] getAcceptedIssuers() { return null; }
                    public void checkClientTrusted(java.security.cert.X509Certificate[] certs, String authType) {}
                    public void checkServerTrusted(java.security.cert.X509Certificate[] certs, String authType) {}
                }
            };
    
            System.out.println("Initializing ssl context.");
            // Initialize SSLContext
            SSLContext sslContext = SSLContext.getInstance("TLS");
            sslContext.init(kmf.getKeyManagers(), trustAllCerts, new SecureRandom());
    
            return sslContext;
        }

    }


    public void sendData(String data) throws IOException {
        OutputStream output = socket.getOutputStream();
        output.write(data.getBytes());
        output.flush();
    }

    public String ReadData() {
        try {
            InputStream inputStream = socket.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
            System.out.println("Getting response in AdminSocket.ReadData()");
            String line = reader.readLine();
            System.out.println("Response:" + line);
            return line;  // Return the complete response
        } catch (Exception e) {
            e.printStackTrace();
            return "";
        }
    }

    public void close() throws IOException {
        socket.close();
    }
    /* 
    public static void main(String[] args) {
        try {
            AdminSocket adminSocket = new AdminSocket("example.com", 443, "client_cert.pem", "client_key.pem");
            adminSocket.sendData("Hello, Server!");
            adminSocket.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }*/
}


