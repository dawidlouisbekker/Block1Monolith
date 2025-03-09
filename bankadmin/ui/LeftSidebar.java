package bankadmin.ui;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

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
    private Map<String,Runnable> buttons = new HashMap<>();
    private VBox options = new VBox(10);
    
    public void setButtons(Map<String,Runnable> buttons) {
        this.buttons = buttons;
    }

    public void reRender() {
        options.getChildren().clear();

    };

    public LeftSidebar(Button toggleButton, Map<String,Runnable> buttons) {
        this.buttons = buttons;
        animation = new TranslateTransition(Duration.millis(300), this);
        this.toFront();
        options.setPadding(new Insets(50, 0, 0, 0));

        this.setStyle("-fx-background-color: rgba(44, 62, 80, 0.9); -fx-padding: 10px;");
        this.setPrefWidth(200);
        this.setMaxWidth(200);
        this.setAlignment(Pos.TOP_CENTER);
        this.setTranslateX(-200);

        this.setTranslateY(50);

        this.buttons.forEach((text,action) -> {
            Button button = new Button();
            button.setText(text);
            button.autosize();
            button.setPrefWidth(Double.MAX_VALUE);
            button.setOnMousePressed(e -> {

                ScaleTransition shrink = new ScaleTransition(Duration.millis(200),button);
                shrink.setToX(0.9);
                shrink.setToY(0.9);
                shrink.play();
                action.run();

            });

            button.setOnMouseReleased(e -> {

                ScaleTransition expand = new ScaleTransition(Duration.millis(200),button);
                expand.setToX(1);
                expand.setToY(1);
                expand.play();

            });
            options.getChildren().add(button);
        });

        this.getChildren().add(options);

    };

    public LeftSidebar(Button toggleButton) {

        options.setPadding(new Insets(50, 0, 0, 0));
    
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



