package bankadmin.ui;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javafx.animation.ScaleTransition;
import javafx.animation.TranslateTransition;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;
import javafx.util.Duration;
import javafx.util.Pair;

public class LeftSidebar extends VBox {
    private boolean isOpen = false;
    private final TranslateTransition animation;
    private Map<String,Runnable> buttons = new HashMap<>();
    private Map<String,Pair<String,Runnable>[]> dropDowns = new HashMap<>();
    private VBox options = new VBox(10);
    
    public void setButtons(Map<String,Runnable> buttons) {
        this.buttons = buttons;
    }

    public void reRender() {
        options.getChildren().clear();

    };

    private void init(){
        this.toFront();
        options.setPadding(new Insets(50, 0, 0, 0));

        this.setStyle("-fx-background-color: rgba(44, 62, 80, 0.9); -fx-padding: 10px;");
        this.setPrefWidth(200);
        this.setMaxWidth(200);
        this.setAlignment(Pos.TOP_CENTER);
        this.setTranslateX(-200);

        this.setTranslateY(50);
    }



    public LeftSidebar(Map<String,Runnable> buttons) {
        init();
        animation = new TranslateTransition(Duration.millis(300), this);
    }

    public LeftSidebar( Map<String,Runnable> buttons, Map<String,Pair<String,Runnable>[]> dropDowns) {
        init();
        animation = new TranslateTransition(Duration.millis(300), this);

        this.buttons = buttons;
        this.dropDowns = dropDowns;

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

        this.dropDowns.forEach((text,runables) -> {
            Label lbl = new Label();
            lbl.setText(text);
            VBox rnblBox = new VBox(5);
            for (Pair<String,Runnable> runnable : runables) {
                String btnText = runnable.getKey();  
                Runnable action = runnable.getValue(); 
                Button btn = new Button();
                btn.autosize();
                btn.setPrefWidth(Double.MAX_VALUE);
                btn.setText(btnText);
                btn.setOnMousePressed(e -> {

                    ScaleTransition shrink = new ScaleTransition(Duration.millis(200),btn);
                    shrink.setToX(0.9);
                    shrink.setToY(0.9);
                    shrink.play();
                    action.run();
    
                });
    
                btn.setOnMouseReleased(e -> {
    
                    ScaleTransition expand = new ScaleTransition(Duration.millis(200),btn);
                    expand.setToX(1);
                    expand.setToY(1);
                    expand.play();
    
                });
                rnblBox.getChildren().add(btn);
            }
            this.getChildren().add(rnblBox);
        });
        this.getChildren().add(options);

    };

    public void toggleSidebar() {
        animation.setToX(isOpen ? -200 : 0); // Toggle Sidebar Position
        //animation.setByZ();
        isOpen = !isOpen;
        animation.play();
    }
}



