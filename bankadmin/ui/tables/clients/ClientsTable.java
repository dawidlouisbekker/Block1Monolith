package bankadmin.ui.tables.clients;

import bankadmin.com.SAV;
import bankadmin.json.JSONPayload;
import bankadmin.json.JSONPayload.JSONType;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
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


    private JSONPayload payload = new JSONPayload(JSONType.OBJECT);

    public ClientsTable(Client[] clients,SAV sav) {
        this.setAlignment(Pos.TOP_CENTER);
        TableView<Client> table = new TableView<>();
        table.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY_ALL_COLUMNS);
        table.setPrefWidth(700);
        table.setMaxWidth(700);

        TableColumn<Client, String> firstnameCol = new TableColumn<>("Fist Name");
        firstnameCol.setCellValueFactory(new PropertyValueFactory<>("firstname"));
        //firstnameCol.setPrefWidth(100);
        //firstnameCol.setMaxWidth(100);

        TableColumn<Client, String> middlenameCol = new TableColumn<>("Middle name");
        middlenameCol.setCellValueFactory(new PropertyValueFactory<>("middlename"));
        //middlenameCol.setMinWidth(100);
        //middlenameCol.setMaxWidth(100);

        TableColumn<Client,String> last_nameCol = new TableColumn<>("Last Name");
        last_nameCol.setCellValueFactory(new PropertyValueFactory<>("last_name"));
        //last_nameCol.setMinWidth(100);
        //last_nameCol.setMaxWidth(100);

        TableColumn<Client, String> emailCol = new TableColumn<>("Email");
        emailCol.setCellValueFactory(new PropertyValueFactory<>("email"));
        //emailCol.setMinWidth(100);
        //emailCol.setMaxWidth(100);

        TableColumn<Client,String> cell_noCol = new TableColumn<>("Cell Number");
        cell_noCol.setCellValueFactory(new PropertyValueFactory<>("cell_no"));
        //cell_noCol.setMinWidth(100);
        //cell_noCol.setMaxWidth(100);

        TableColumn<Client,String> id_numberCol = new TableColumn<>("ID Number");
        id_numberCol.setCellValueFactory(new PropertyValueFactory<>("id_number"));
        //id_numberCol.setMinWidth(150);
        //id_numberCol.setMaxWidth(150);

        ObservableList<Client> data = FXCollections.observableArrayList(clients);
        table.setItems(data);

        table.getColumns().addAll(firstnameCol,middlenameCol,last_nameCol,emailCol,cell_noCol,id_numberCol);

        HBox actions = new HBox(10);
        actions.setStyle("-fx-alignment: center;");
        actions.setPadding(new Insets(10,0,0,0));
        Button addClient = new Button();
        addClient.setOnAction(e -> {
            TextField firstnameInput = new TextField();
            firstnameInput.setPromptText("First Name");
            //firstnameInput.set
            TextField middlenameInput = new TextField();
            middlenameInput.setPromptText("Middle Name");
            
            TextField emailInput = new TextField();
            emailInput.setPromptText("Email");
            TextField lastnameInput = new TextField();
            lastnameInput.setPromptText("Last Name");
            TextField cellNoInput = new TextField();
            cellNoInput.setPromptText("Cell Number");
            TextField id_numberInput = new TextField();
            id_numberInput.setPromptText("ID Number");
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
                boolean isCompany = isBusiness.isSelected();
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
                if (!isCompany) {
                    sav.setSubject("client");
                    String payloadStr = payload.getPayload();
                    sav.sendSAV("add", payloadStr);
                } else {
                    this.getChildren().clear();
                    
                }

            });
            sendData.setText("Send data");
            Button back = new Button();
            back.setText("Back");
            back.setOnAction(event -> {
                actions.getChildren().clear();
                actions.getChildren().add(addClient);
            });

            actions.getChildren().clear();
            actions.getChildren().addAll(firstnameInput, middlenameInput, lastnameInput, emailInput, cellNoInput, id_numberInput, passwdInput,isBusiness,sendData);

        });
        addClient.setText("Add Client");
        actions.getChildren().add(addClient);

        this.getChildren().addAll(table,actions);


        

    }

}
