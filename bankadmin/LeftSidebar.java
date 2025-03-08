package bankadmin;

import javafx.animation.ScaleTransition;
import javafx.animation.TranslateTransition;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.layout.VBox;
import javafx.util.Duration;

public class LeftSidebar extends VBox {
    private boolean isOpen = false;
    private final TranslateTransition animation;
    public LeftSidebar(Button toggleButton) {
        

        this.setStyle("-fx-background-color: rgba(44, 62, 80, 0.9); -fx-padding: 10px;");
        this.setPrefWidth(200);
        this.setMaxWidth(200);
        this.setAlignment(Pos.TOP_CENTER);
        this.setTranslateX(-200);

        // Sidebar Animation
        animation = new TranslateTransition(Duration.millis(300), this);
        this.toFront();

        this.setTranslateY(50);
    }


    public void toggleSidebar() {
        animation.setToX(isOpen ? -200 : 0); // Toggle Sidebar Position
        //animation.setByZ();
        isOpen = !isOpen;
        animation.play();
    }
}



