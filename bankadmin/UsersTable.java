package bankadmin;
import java.util.ArrayList;
import java.util.List;

import javafx.application.Platform;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;

import javafx.scene.control.TableView;
import javafx.scene.control.Button;
import javafx.scene.control.TableCell;
import javafx.scene.control.TableColumn;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.control.cell.TextFieldTableCell;
import javafx.collections.ObservableList;
import javafx.collections.FXCollections;


public class UsersTable extends VBox {
    private TableView<bankadmin.User> table;
    private HBox actions = new HBox(5);

    private User[] users;
    private List<User> filteredUsers;
    private List<String> companies;
    private String selectedCompany;

    void addUser() {
        System.out.println("Add user.");
    }

    void displayActions(){
        Button addUsers = new Button();
        addUsers.setOnAction((event) -> {
            addUser();
        });
        addUsers.setText("Add User");

        actions.getChildren().add(addUsers);
        this.getChildren().add(actions);
    }



    UsersTable(User[] users, SAV sav) {
        this.users = users;
        this.companies = new ArrayList<>();
        this.companies.add("All");
        for (User usr : users) {
            if (usr.getCompany() != null) {
                String company = usr.getCompany();
                if (!this.companies.contains(company)) {
                    this.companies.add(company);
                }
            }
        }
        this.users = users;
        Platform.runLater(() -> {
            table = new TableView<>();
            table.getStylesheets().add(getClass().getResource("styles/table.css").toExternalForm());
            ObservableList<User> data = FXCollections.observableArrayList(this.users);
            table.setItems(data);
            table.setEditable(true);

            HBox topOptions = new HBox(5);
            for (String company : this.companies) {
                Button companyButton = new Button(company);
                companyButton.setOnAction(event -> {
                    if (company.equals("All")) {
                        table.setItems(FXCollections.observableArrayList(this.users));
                        return;
                    }
                    this.selectedCompany = company;
                    this.filteredUsers = new ArrayList<User>();
                    for (User usr : users) {
                        if (usr.getCompany().equals(company)) {
                            filteredUsers.add(usr);
                        }
                    }
                    table.setItems(FXCollections.observableArrayList(this.filteredUsers));
                });
                topOptions.getChildren().add(companyButton);
            }

            table.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY_ALL_COLUMNS);
            TableColumn<User, String> nameCol = new TableColumn<>("Username");
            nameCol.setCellValueFactory(new PropertyValueFactory<>("username"));
            nameCol.setCellFactory(TextFieldTableCell.forTableColumn());
            nameCol.setOnEditCommit(event -> {
                User user = event.getRowValue();
                user.setUsername(event.getNewValue());
                table.refresh();
            });

            TableColumn<User, String> orgUnitCol = new TableColumn<>("Organization Unit");
            orgUnitCol.setCellValueFactory(new PropertyValueFactory<>("orgUnit"));
            orgUnitCol.setCellFactory(TextFieldTableCell.forTableColumn());
            orgUnitCol.setOnEditCommit(event -> {
                User user = event.getRowValue();
                user.setOrgUnit(event.getNewValue());
                table.refresh();
            });

            TableColumn<User, String> groupCol = new TableColumn<>("Group");
            groupCol.setCellValueFactory(new PropertyValueFactory<>("group")); 
            groupCol.setCellFactory(TextFieldTableCell.forTableColumn());
            groupCol.setOnEditCommit(event -> {
                User user = event.getRowValue();
                user.setGroup(event.getNewValue());

                table.refresh();
                
            });

            TableColumn<User, Button> updateColumn = new TableColumn<>("Action");
            updateColumn.setStyle("-fx-alignment: center;");
            updateColumn.setCellFactory(param -> new TableCell<>() {
                private final Button updateButton = new Button("Update");
    
                {
                    updateButton.setOnAction(event -> {
                        User usr = getTableView().getItems().get(getIndex());
                        usr.resetEdited();
                        getTableView().refresh();
                    });
                }
    
                @Override
                protected void updateItem(Button item, boolean empty) {
                    super.updateItem(item, empty);
                    if (empty || !getTableView().getItems().get(getIndex()).isEdited()) {

                        setGraphic(null);
                    } else {
                        User usr = users[getIndex()];
                        usr.setPrevUsername(); 
                        String json = usr.getJSON();
                        System.out.println(json);
                        sav.sendSAV("update", json);
                        usr.resetEdited();
                        setGraphic(updateButton);
                        
                    }
                }
            });

            table.getColumns().addAll(nameCol, orgUnitCol, groupCol, updateColumn);
            this.getChildren().add(topOptions);
            this.getChildren().add(table);
            
        });
    }
}
