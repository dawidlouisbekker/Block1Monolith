package oracleworkbench;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class OracleXEConnection {
    public OracleXEConnection(String url, String username, String password) {
        // JDBC URL for OracleXE (default port: 1521)
        //String url = "jdbc:oracle:thin:@DawidBekker2005:1521/XE";
        //String username = "C##bank_user"; // Replace with your DB username
        //String password = "askljnobbDSAi12sSda"; // Replace with your DB password

        try {
            // Load Oracle JDBC Driver (not needed in Java 6+ but good practice)
            Class.forName("oracle.jdbc.OracleDriver");

            // Establish the connection
            Connection connection = DriverManager.getConnection(url, username, password);
            System.out.println("Connected to Oracle XE!");

            // Execute a simple query
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery("SELECT SYSDATE FROM DUAL");

            // Print the result
            while (resultSet.next()) {
                System.out.println("Current Date from Oracle: " + resultSet.getString(1));
            }

            // Close resources
            resultSet.close();
            statement.close();
            connection.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

