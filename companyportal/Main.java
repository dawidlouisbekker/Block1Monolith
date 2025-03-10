package companyportal;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

import bankadmin.AdminSocket;
import javafx.application.Application;
import javafx.stage.Stage;

public class Main extends Application {
    
    private JFrame frame;

    @Override
    public void start(Stage primStage) {
        primStage.setFullScreen(true);
        SwingUtilities.invokeLater(() -> {
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setSize(600, 800);
            frame.setExtendedState(JFrame.MAXIMIZED_BOTH);
        });

    }

    public static void main(String[] args) {
        //Might query 'DNS' later for IP.
        AdminSocket adminSocket = new AdminSocket("127.0.0.1", 0, "./certificates/company_server.pem", STYLESHEET_CASPIAN, STYLESHEET_MODENA, STYLESHEET_CASPIAN);
    }
}
