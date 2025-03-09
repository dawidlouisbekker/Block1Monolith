package bankadmin;
import javafx.animation.ScaleTransition;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.embed.swing.JFXPanel;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

import javafx.scene.layout.HBox;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.stage.Screen;
import javafx.stage.Stage;
import javafx.util.Duration;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.scene.control.Alert.AlertType;
import bankadmin.com.SAV;
import bankadmin.json.JSONPayload;
import bankadmin.json.ParseJSON;
import bankadmin.ui.CenteredSpinner;
import bankadmin.ui.LeftSidebar;
import bankadmin.ui.tables.clients.Client;
import bankadmin.ui.tables.clients.ClientsTable;
import bankadmin.ui.tables.company.CompaniesTable;
import bankadmin.ui.tables.company.Company;
import bankadmin.ui.tables.company.users.CompanyUser;
import bankadmin.ui.tables.company.users.CompanyUsersTable;

public class Main extends Application {

    static private AdminSocketActions socketActions;

    static private JFrame frame = new JFrame("ABFinances Admins");
    static private JFXPanel jfxPanel = new JFXPanel();
    //static private HBox actions = new HBox(5);
    static private CenteredSpinner spinner;
    static private boolean connError = false;
    static private SAV sav;
    static private CompanyUser[] users;
    static private AdminSocket highSecSock;
    static private VBox tableVbox = new VBox(10);

    static private LeftSidebar leftSidebar;

    static private void AddUser() {
        Platform.runLater(() -> {
            VBox addUserVbox = new VBox(10); // Spacing of 10px
            addUserVbox.setStyle("-fx-alignment: center;");

            addUserVbox.setPrefWidth(100);
            addUserVbox.setMaxWidth(120);

            TextField userNameInput = new TextField();
            userNameInput.setPromptText("Enter username"); // Placeholder text

            userNameInput.setPromptText("Username");
            userNameInput.setMaxWidth(300);

            Button backButton = new Button("Back to Table");
            backButton.setOnAction(event -> showTableUI(users));


            addUserVbox.getChildren().addAll(userNameInput, backButton);

            Scene newScene = new Scene(addUserVbox, 800, 600);
            jfxPanel.setScene(newScene);
        });
    }

    static private void showActions(HBox actions, Button addUser) {
        actions.getChildren().clear();
    
        TextField usernameInput = new TextField();
        usernameInput.setPromptText("Enter Username");

        TextField passwordInput = new TextField();
        passwordInput.setPromptText("Enter Password");

        TextField companyInput = new TextField();
        companyInput.setPromptText("Enter Company");

        TextField orgUnitInput = new TextField();
        orgUnitInput.setPromptText("Enter Organization Unit");

        Label errorLabel = new Label();
        errorLabel.setStyle("-fx-text-fill: red;");

        Button okButton = new Button("OK");

        okButton.setOnAction(okEvent -> {
            String username = usernameInput.getText().trim();
            String password = passwordInput.getText().trim();
            String company = companyInput.getText().trim();
            String orgUnit = orgUnitInput.getText().trim();

            if (username.isEmpty() || password.isEmpty() || company.isEmpty() || orgUnit.isEmpty()) {
                errorLabel.setText("All fields are required.");
            } else {
                System.out.println("New User: " + username);
                JSONPayload payload = new JSONPayload(JSONPayload.JSONType.OBJECT);
                payload.addPair("username", username);
                payload.addPair("password", password);
                payload.addPair("company", company);
                payload.addPair("orgUnit", orgUnit);
                sav.setSubject("admins");
                System.out.println("Payload: " + payload.getPayload());
                sav.sendSAV("add", payload.getPayload());

                actions.getChildren().clear();
                actions.getChildren().add(addUser);
            }
        });

        actions.getChildren().addAll(usernameInput, passwordInput, companyInput, orgUnitInput, okButton, errorLabel);
    }


    static private void showTableUI(CompanyUser[] users) {
        Platform.runLater(() -> {
            
            tableVbox.setStyle("-fx-alignment: center;");
///////////////////// Clients Table ///////////////////////////
            List<Client> clients = List.of(
                new Client("Dawid","Louis","Bekker","dawidbekker123@gmail.com","0605868794","09800987089")
            );
            ClientsTable clientsTable = new ClientsTable(clients, sav);

///////////////////// Users Table /////////////////////////////
            CompanyUsersTable usersTableView = new CompanyUsersTable(users, sav);

            usersTableView.setMaxWidth(700);
            usersTableView.setPrefWidth(700);
            
            List<Company> companies = List.of(
                new Company("Company A"),
                new Company("Company B"),
                new Company("Company C")
            );

            CompaniesTable companiesTableView = new CompaniesTable(companies, sav);
            companiesTableView.setMaxWidth(700);
            companiesTableView.setPrefWidth(700);


            HBox actions = new HBox(5);

            Button addUser = new Button("Add User");
            
            addUser.setOnAction(event -> {
                showActions(actions, addUser);
            });
    
            actions.setAlignment(Pos.CENTER);
            actions.getChildren().add(addUser);
    
            // Root StackPane
            StackPane root = new StackPane();
            root.setStyle("-fx-background-color: #323232;");

            Button toggleButton = new Button("☰");



/////////////////// Left hand side bar //////////////////////////////
            

            Map<String,Runnable> buttons = new HashMap<>() {{
                put("Companies", () -> { 
                    tableVbox.getChildren().clear();
                    tableVbox.getChildren().add(companiesTableView);
                 });
                 put("Company Users", () -> {
                    tableVbox.getChildren().clear();
                    tableVbox.getChildren().addAll(usersTableView, actions);
                 });
                 put("Clients", () -> {
                    tableVbox.getChildren().clear();
                    tableVbox.getChildren().addAll(clientsTable);
                 });
            }};
            
            LeftSidebar leftSidebar = new LeftSidebar(toggleButton,buttons);

            toggleButton.setStyle("-fx-font-size: 20px; -fx-background-color: #3498DB; -fx-text-fill: white;");
            toggleButton.setOnAction(e -> {
                leftSidebar.toggleSidebar();
            });

            StackPane.setAlignment(toggleButton, Pos.TOP_LEFT);
            StackPane.setMargin(toggleButton, new Insets(10));

////////////////////////////// Table VBOX /////////////////////////////////////////

            tableVbox.getChildren().addAll(usersTableView, actions);

            root.getChildren().addAll(toggleButton,leftSidebar,tableVbox);
            toggleButton.setStyle("-fx-background-color:rgb(255, 255, 255)");

            StackPane.setAlignment(leftSidebar, Pos.CENTER_LEFT);
            toggleButton.toFront();

            Scene scene = new Scene(root, 
                Screen.getPrimary().getVisualBounds().getWidth(),
                Screen.getPrimary().getVisualBounds().getHeight()
            );
    
            leftSidebar.toFront();
            jfxPanel.setScene(scene);

        });

    }
    


    static private void LoginUI() {
        Platform.runLater(() -> {
            VBox loginVbox = new VBox(10);
            loginVbox.setStyle("-fx-alignment: center; -fx-background-color: #323232;");
            loginVbox.setMaxWidth(300);
            
            Label loginLabel = new Label();
            loginLabel.setText("Login");
            loginLabel.setStyle("-fx-font-size: 24;");

            TextField idInput = new TextField();
            idInput.setPromptText("Enter id"); 
            idInput.setMaxWidth(200);  
            idInput.setPrefWidth(200); 

            PasswordField passwordInput = new PasswordField();
            passwordInput.setPromptText("Enter password");
            passwordInput.setMaxWidth(200);
            passwordInput.setPrefWidth(200);

            PasswordField phraseInput = new PasswordField();
            phraseInput.setPromptText("Enter phrase");
            phraseInput.setMaxWidth(200);
            phraseInput.setPrefWidth(200);

            Button loginButton = new Button("Login");
            loginButton.setMaxWidth(200); 
            loginButton.setPrefWidth(200); 
        
            loginButton.setOnAction(event -> {
                String id = idInput.getText();
                String password = passwordInput.getText();
                String passphrase = phraseInput.getText();
                JSONPayload payload = new JSONPayload(JSONPayload.JSONType.OBJECT);
                payload.addPair("uuid", id);
                payload.addPair("passphrase", passphrase);
                payload.addPair("password", password);
                boolean success = socketActions.login(payload.getPayload());
                if (success) {
                    try {
                        spinner = new CenteredSpinner(jfxPanel);
                        spinner.Show();
                        try{
                            int port = Integer.parseInt(socketActions.socket.ReadData());
                            String cert_path = "./bankadmin/" + id + "_cert.pem";
                            String key_path = "./bankadmin/" + id + "_key.pem";
                            String ca_cert_path = "./bankadmin/intermediary_" + id + "_cert.pem";
                            highSecSock = new AdminSocket("127.0.0.1", port, cert_path, key_path, ca_cert_path,passphrase);
                            String msg = socketActions.socket.ReadData();
                            if (msg.equals("Connected")) {
                                sav = new SAV(highSecSock.getOutputStream(),highSecSock.getInputStream());
                                sav.setSubject("admins");
                                sav.sendSAV("get");
                                ParseJSON<CompanyUser> parser = new ParseJSON<>(CompanyUser.class);
                                parser.parseJSONArray(sav.data);
                                System.out.println("SAV data: " + sav.data);
                                System.out.println("Parser data: " + parser.data);
                                for (CompanyUser usr : parser.data) {
                                    usr.displayAll();
                                }
                                users = parser.data.toArray(new CompanyUser[0]);
                                showTableUI(users);
                            }
                        } catch (Exception e) {
                            spinner.TextOnly("Connection timed out. Exit and retry login.");
                        }
                        

                    } catch (Exception e) {
                        System.out.println(e);
                    }
                    


                    ///showTableUI(parser.data.toArray(new User[0]));
                }
               // showPopUp();
            });
        
            // Add the TextField, PasswordField, and Button to the VBox
            loginVbox.getChildren().addAll(loginLabel, idInput, phraseInput,passwordInput, loginButton);

            // Create a Scene with the VBox
            Scene scene = new Scene(loginVbox, 300, 200); // Adjust width of the scene as needed
            jfxPanel.setScene(scene); 
        });
    }



    @Override
    public void start(Stage primaryStage) {
        primaryStage.setFullScreen(true); 

        SwingUtilities.invokeLater(() -> {
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setSize(800, 600);
            frame.setExtendedState(JFrame.MAXIMIZED_BOTH);
            frame.add(jfxPanel);
            frame.setVisible(true);

            LoginUI();
        });
        if (connError) {
            Alert alert = new Alert(AlertType.ERROR);  // Type of pop-up
            alert.setTitle("Connection error.");
            alert.setHeaderText("Server might be down.");  // No header
           // alert.setContentText(e.toString());
            alert.showAndWait();  // Display the pop-up and wait for user interaction
        }
    }
    
    public static void main(String[] args) {
        try {
           //(new Sample(), "{ \"id\": 42, \"name\": \"John Doe\", \"balance\": 1000.75 }");
            
            AdminSocket adminSocket = new AdminSocket("localhost", 5024, "./bankadmin/client_cert.pem", "./bankadmin/client_key.pem","","");
            socketActions = new AdminSocketActions(adminSocket,jfxPanel);
            //Public function ins class
            
        } catch (Exception e) {
            connError = true;
        }
        launch(args);
    }
}