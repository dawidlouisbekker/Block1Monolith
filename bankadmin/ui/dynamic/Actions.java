package bankadmin.ui.dynamic;

import java.util.HashMap;

import javafx.scene.control.Button;
import javafx.scene.layout.HBox;

public class Actions extends HBox {

    private HashMap<String,Runnable> actions;

    public Actions(HashMap<String,Runnable> actions) {
        actions.forEach((text,action) -> {
            Button button = new Button();
            button.setText(text);
            
        });
    }
}
