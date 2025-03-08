package oracleworkbench;

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        try{
            OracleXEConnection oracle = new OracleXEConnection();
        } catch (Exception exception) {
            exception.printStackTrace();
        }

    }

}

    /* 
    public static void main(String[] args) {
        String pipeName = "\\\\.\\pipe\\serverpipe";
        System.out.println("Connecting to named pipe: " + pipeName);

        try (RandomAccessFile pipe = new RandomAccessFile(pipeName, "r")) {
            String line;
            while ((line = pipe.readLine()) != null) {
                System.out.println("Received: " + line);
            }
        } catch (IOException e) {
            System.err.println("Error reading from pipe: " + e.getMessage());
        }

        System.out.println("Client finished.");
    }*/