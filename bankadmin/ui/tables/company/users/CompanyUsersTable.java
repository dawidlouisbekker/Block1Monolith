package bankadmin.ui.tables.company.users;
import java.util.ArrayList;
import java.util.List;

import bankadmin.com.SAV;
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


public class CompanyUsersTable extends VBox {
    private TableView<CompanyUser> table;
    private HBox actions = new HBox(5);

    private CompanyUser[] CompanyUsers;
    private List<CompanyUser> data = new ArrayList<CompanyUser>();
    public List<String> companies;
    private String selectedCompany;

    void addCompanyUser() {
        System.out.println("Add CompanyUser.");
    }

    void displayActions(){

        Button addCompanyUsers = new Button();
        addCompanyUsers.setOnAction((event) -> {
            addCompanyUser();
        });

        addCompanyUsers.setText("Add CompanyUser");

        actions.getChildren().add(addCompanyUsers);
        this.getChildren().add(actions);

    }

    public void setSelectedCompany(String company) {
        this.selectedCompany = company;
        if (company.equals("All")) {
            table.setItems(FXCollections.observableArrayList(this.CompanyUsers));
            return;
        }
        this.selectedCompany = company;
        for (CompanyUser usr : CompanyUsers) {
            if (usr.getCompany().equals(company)) {
                data.add(usr);
            }
        }
        table.setItems(FXCollections.observableArrayList(this.data));
    }

    public CompanyUsersTable(CompanyUser[] CompanyUsers, SAV sav) {
        this.CompanyUsers = CompanyUsers;
        this.companies = new ArrayList<>();
        this.companies.add("All");

        for (CompanyUser usr : CompanyUsers) {
            if (usr.getCompany() != null) {
                String company = usr.getCompany();
                if (!this.companies.contains(company)) {
                    this.companies.add(company);
                }
            }
        }

        this.CompanyUsers = CompanyUsers;
        Platform.runLater(() -> {
            table = new TableView<>();
            table.getStylesheets().add(getClass().getResource("styles/table.css").toExternalForm());
            ObservableList<CompanyUser> data = FXCollections.observableArrayList(this.CompanyUsers);
            table.setItems(data);
            table.setEditable(true);

            HBox topOptions = new HBox(5);
            for (String company : this.companies) {
                Button companyButton = new Button(company);
                companyButton.setOnAction(event -> {
                    if (company.equals("All")) {
                        table.setItems(FXCollections.observableArrayList(this.CompanyUsers));
                        return;
                    }
                    this.selectedCompany = company;
                    for (CompanyUser usr : CompanyUsers) {
                        if (usr.getCompany().equals(company)) {
                            data.add(usr);
                        }
                    }
                    table.setItems(FXCollections.observableArrayList(this.data));
                });
                topOptions.getChildren().add(companyButton);
            }

            table.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY_ALL_COLUMNS);

            TableColumn<CompanyUser, String> nameCol = new TableColumn<>("Username");
            nameCol.setCellValueFactory(new PropertyValueFactory<>("username"));
            nameCol.setCellFactory(TextFieldTableCell.forTableColumn());
            nameCol.setOnEditCommit(event -> {
                CompanyUser CompanyUser = event.getRowValue();
                CompanyUser.setUsername(event.getNewValue());
                table.refresh();
            });

            TableColumn<CompanyUser, String> orgUnitCol = new TableColumn<>("Organization Unit");
            orgUnitCol.setCellValueFactory(new PropertyValueFactory<>("orgUnit"));
            orgUnitCol.setCellFactory(TextFieldTableCell.forTableColumn());
            orgUnitCol.setOnEditCommit(event -> {
                CompanyUser CompanyUser = event.getRowValue();
                CompanyUser.setOrgUnit(event.getNewValue());
                table.refresh();
            });

            /* 
            TableColumn<CompanyUser, String> groupCol = new TableColumn<>("Group");
            groupCol.setCellValueFactory(new PropertyValueFactory<>("group")); 
            groupCol.setCellFactory(TextFieldTableCell.forTableColumn());
            groupCol.setOnEditCommit(event -> {
                CompanyUser CompanyUser = event.getRowValue();
                CompanyUser.setGroup(event.getNewValue());

                table.refresh();
                
            });*/

            TableColumn<CompanyUser,Button> updateColumn = new TableColumn<>("Action");
            updateColumn.setStyle("-fx-alignment: center;");
            updateColumn.setCellFactory(param -> new TableCell<>() {
                private final Button updateButton = new Button("Update");
    
                {
                    updateButton.setOnAction(event -> {
                        CompanyUser usr = getTableView().getItems().get(getIndex());
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
                        CompanyUser usr = CompanyUsers[getIndex()];
                        usr.setPrevUsername(); 
                        String json = usr.getJSON();
                        System.out.println(json);
                        sav.sendSAV("update", json);
                        usr.resetEdited();
                        setGraphic(updateButton);
                    }
                }
            });

            table.getColumns().addAll(nameCol, orgUnitCol, updateColumn); //groupCol,
            this.getChildren().add(topOptions);
            this.getChildren().add(table);
            
        });
    }
}
