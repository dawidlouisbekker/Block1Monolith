package bankadmin;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;

public class SAV {



    private String subject;

    private InputStream in;
    private OutputStream out;

    public String data = null;

    SAV (OutputStream out, InputStream in) {
        this.in = in;
        this.out = out;
    };

    public void setSubject(){};

    public void setSubject(String subject){
        this.subject = subject;
    };


    private String getResponse() {
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(this.in));
            System.out.println("Getting response");
            String line = reader.readLine();
            return line;
        } catch (Exception e) {
            System.out.println(e);
            //Add error display
            return null;
        }
    }

    public void setStreams(InputStream in, OutputStream out) {
        this.in = in;
        this.out = out;
    }

    public void sendSAV(String action){
        try {
            String query = "{  \"subject\": \"" + this.subject + "\" ,\"action\": \"" + action + "\" }";
            this.out.write((query).getBytes());
            this.data = getResponse();
        } catch (Exception e) {
            System.out.println(e);

        }
    };

    public void sendSAV(String action ,String value){
        try {
            String query = "{ \"action\": \""+ action + "\", \"subject\": \"" + this.subject + "\", \"value\": " + value + " }";
            System.out.println("Sending: " + query);
            this.out.write((query).getBytes());
        } catch (Exception e) {
            System.out.println(e);
        }
    };
    
}; 
