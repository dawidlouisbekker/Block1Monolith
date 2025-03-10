package bankadmin;
import javafx.embed.swing.JFXPanel;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import bankadmin.*;

public class AdminSocketActions {



    public AdminSocket socket;
    private JFXPanel panel;

    static public void displayActionResult(String Title, String header,String Text, AlertType type) {
        Alert alert = new Alert(type);  // Type of pop-up
        alert.setTitle(Title);
        alert.setHeaderText(header);
        alert.setContentText(Text);
        alert.showAndWait();  // Display the pop-up and wait for user interaction
    }

    AdminSocketActions(AdminSocket socket, JFXPanel panel) {
        this.socket = socket;
        this.panel = panel;
    }

    public void receiveJson() {
        //JSObject
        String text = this.socket.ReadData();
        System.out.println(text);

    };

    public void receiveText() {

    };

    public void sendJson() {

    }

    public boolean login(String payload){
        try {
            this.socket.sendData(payload);
            String data = this.socket.ReadData();
            if (data.equals(null)) {
                displayActionResult(null, "An error occured.", null, AlertType.ERROR);
                return false;
            }
            displayActionResult(null, data, null, AlertType.INFORMATION);
            return true;
        } catch (Exception e){
            displayActionResult(null, "An error occured.", null, AlertType.ERROR);
            System.err.println(e);
            return false;
        }
    }
}
