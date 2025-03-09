package bankadmin.ui.tables.company;


import java.util.List;

import bankadmin.com.SAV;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.VBox;

public class CompaniesTable extends VBox {


    public CompaniesTable(List<Company> companies, SAV sav) {

        //Adding data.
        ObservableList<Company> data = FXCollections.observableList(companies);
        TableView<Company> tableView = new TableView<>();
        tableView.setItems(data);

        TableColumn<Company ,String> nameCol = new TableColumn<>("Name");
        nameCol.setCellValueFactory(new PropertyValueFactory<>("name"));
        tableView.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY_ALL_COLUMNS);
        tableView.getColumns().addAll(nameCol);
        this.getChildren().add(tableView);
    }

}
