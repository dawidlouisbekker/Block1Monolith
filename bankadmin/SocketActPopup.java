package bankadmin;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.VBox;
import javafx.stage.Modality;
import javafx.stage.Stage;

public class SocketActPopup {

    public SocketActPopup(String Title) {
        // Create the popup stage
        Stage popupStage = new Stage();
        popupStage.initModality(Modality.APPLICATION_MODAL); // Blocks interaction with other windows
        popupStage.setTitle(Title);

        // Add components to the popup (you can add anything you want)
        Button closeButton = new Button("Close");
        closeButton.setOnAction(e -> popupStage.close());

        VBox layout = new VBox(10);
        layout.getChildren().add(closeButton);

        Scene scene = new Scene(layout, 200, 100);
        popupStage.setScene(scene);

        // Show the popup
        popupStage.showAndWait();
    }

}

