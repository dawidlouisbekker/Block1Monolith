package bankadmin.ui.tables.clients;

import java.util.List;
import java.util.function.Function;

import bankadmin.com.SAV;
import bankadmin.json.JSONPayload;
import bankadmin.json.JSONPayload.JSONType;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;

/*
        String firstname,
        String middlename,
        String last_name,
        String email,
        String cell_no,
        String id_number 
 */

public class ClientsTable extends VBox {

    private SAV sav;
    private JSONPayload payload = new JSONPayload(JSONType.OBJECT);

    public ClientsTable(List<Client> clients,SAV sav) {
        this.sav = sav;

        TableView<Client> table = new TableView<>();
        table.setColumnResizePolicy(TableView.UNCONSTRAINED_RESIZE_POLICY);

        TableColumn<Client, String> firstnameCol = new TableColumn<>("Fist Name");
        firstnameCol.setCellValueFactory(new PropertyValueFactory<>("firstname"));
        firstnameCol.setPrefWidth(50);
        firstnameCol.setMinWidth(50);
        
        
        
        
        

        TableColumn<Client, String> middlenameCol = new TableColumn<>("Middle name");
        middlenameCol.setCellValueFactory(new PropertyValueFactory<>("middlename"));
        middlenameCol.setMinWidth(50);
        middlenameCol.setMaxWidth(100);

        TableColumn<Client,String> last_nameCol = new TableColumn<>("Last Name");
        last_nameCol.setCellValueFactory(new PropertyValueFactory<>("last_name"));
        last_nameCol.setMinWidth(50);
        last_nameCol.setMaxWidth(100);

        TableColumn<Client, String> emailCol = new TableColumn<>("Email");
        emailCol.setCellValueFactory(new PropertyValueFactory<>("email"));
        emailCol.setMinWidth(50);
        emailCol.setMaxWidth(100);

        TableColumn<Client,String> cell_noCol = new TableColumn<>("Cell Number");
        cell_noCol.setCellValueFactory(new PropertyValueFactory<>("cell_no"));
        cell_noCol.setMinWidth(50);
        cell_noCol.setMaxWidth(100);

        TableColumn<Client,String> id_numberCol = new TableColumn<>("ID Number");
        id_numberCol.setCellValueFactory(new PropertyValueFactory<>("id_number"));
        id_numberCol.setMinWidth(50);
        id_numberCol.setMaxWidth(100);

        ObservableList<Client> data = FXCollections.observableArrayList(clients);
        table.setItems(data);

        table.getColumns().addAll(firstnameCol,middlenameCol,last_nameCol,emailCol,cell_noCol,id_numberCol);

        HBox actions = new HBox(10);
        actions.setStyle("-fx-alignment: center;");
        Button addClient = new Button();
        addClient.setOnAction(e -> {
            TextField firstnameInput = new TextField();
            firstnameInput.setText("First Name");
            //firstnameInput.set
            TextField middlenameInput = new TextField();
            middlenameInput.setText("Middle Name");
            
            TextField emailInput = new TextField();
            emailInput.setText("Email");
            TextField lastnameInput = new TextField();
            lastnameInput.setText("Last Name");
            TextField cellNoInput = new TextField();
            cellNoInput.setText("Cell Number");
            TextField id_numberInput = new TextField();
            id_numberInput.setText("ID Number");
            PasswordField passwdInput = new PasswordField();
            CheckBox isBusiness = new CheckBox();
            isBusiness.setText("Business");

            Button sendData = new Button();
            sendData.setOnAction(event -> {
                String firstname = firstnameInput.getText();
                String middlename = middlenameInput.getText();
                String lastname = lastnameInput.getText();
                String email = emailInput.getText();
                String cellNo = cellNoInput.getText();
                String idNumber = id_numberInput.getText();
                String password = passwdInput.getText();
                boolean isBusinessClient = isBusiness.isSelected();
                //Do validation
                payload.addPair("firstname", firstname);
                payload.addPair("middlename", middlename);
                payload.addPair("lastname", lastname);
                payload.addPair("email", email);
                payload.addPair("cellNo", cellNo);
                payload.addPair("idNumber", idNumber);
                payload.addPair("password", password);
                //Business checkbox is to determine the next input form.
                //payload.addPair("isBussiness", isBusinessClient);
                sav.setSubject("client");
                String payloadStr = payload.getPayload();
                sav.sendSAV("add", payloadStr);
            });
            sendData.setText("Send data");
            Button back = new Button();
            back.setText("Back");
            back.setOnAction(event -> {
                actions.getChildren().clear();
                actions.getChildren().add(addClient);
            });

            actions.getChildren().clear();
            actions.getChildren().addAll(firstnameInput, middlenameInput, lastnameInput, emailInput, cellNoInput, id_numberInput, passwdInput,sendData);

        });
        addClient.setText("Add Client");
        actions.getChildren().add(addClient);

        this.getChildren().addAll(table,actions);


        

    }

}
