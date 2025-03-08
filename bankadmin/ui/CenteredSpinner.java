package bankadmin.ui;
import bankadmin.AdminSocket;
import javafx.embed.swing.JFXPanel;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.ProgressIndicator;
import javafx.scene.control.Spinner;
import javafx.scene.layout.StackPane;
import javafx.scene.control.ProgressIndicator;

public class CenteredSpinner extends StackPane {

    private ProgressIndicator spinner;
    private JFXPanel panel;

    public void TextOnly(String text) {
        Label msg = new Label();
        msg.setText(text);
        msg.setAlignment(Pos.CENTER);
        // Add the spinner to StackPane (centers it automatically)
        this.getChildren().addAll(spinner,msg);
        Scene scene = new Scene(this, 300, 200);
        this.setStyle("-fx-background: #323232;");
        panel.setScene(scene);
    }

    public void Show(){
        // Create a Spinner with a range from 0 to 100, default value 50
        spinner = new ProgressIndicator();
        spinner.setProgress(ProgressIndicator.INDETERMINATE_PROGRESS); // Keeps spinning

        spinner.setMinWidth(200);
        spinner.setPrefWidth(200);

        spinner.setMinHeight(200);
        spinner.setPrefHeight(200);

        Label msg = new Label();
        msg.setText("Securing connection...");
        msg.setAlignment(Pos.CENTER);
        // Add the spinner to StackPane (centers it automatically)
        this.getChildren().addAll(spinner,msg);
        Scene scene = new Scene(this, 300, 200);
        this.setStyle("-fx-background: #323232;");
        panel.setScene(scene);
    }

    public CenteredSpinner(JFXPanel panel) {
        this.panel = panel;

    }

    // Getter method to access the spinner if needed
    public ProgressIndicator getSpinner() {
        return spinner;
    }    
}
