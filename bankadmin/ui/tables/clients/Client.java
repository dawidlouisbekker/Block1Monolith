package bankadmin.ui.tables.clients;

public class Client {
    
    public String firstname;
    public String middlename;
    public String last_name;
    public String email;
    public String cell_no;
    public String id_number;

    public Client(
        String firstname,
        String middlename,
        String last_name,
        String email,
        String cell_no,
        String id_number 
    ) {
        this.firstname = firstname;
        this.middlename = middlename;
        this.last_name = last_name;
        this.email = email;
        this.cell_no = cell_no;
        this.id_number = id_number;
    };

    public void displayAll(){
        System.out.println("First Name: " + firstname);
        System.out.println("Middle Name: " + middlename);
        System.out.println("Last Name: " + last_name);
        System.out.println("Email: " + email);
        System.out.println("Cell No: " + cell_no);
        System.out.println("ID Number: " + id_number);
    }

    public Client(){

    };

    public String getFirstname() {
        return firstname;
    }

    public void setFirstname(String firstname) {
        this.firstname = firstname;
    }

    public String getMiddlename() {
        return middlename;
    }

    public void setMiddlename(String middlename) {
        this.middlename = middlename;
    }

    public String getLast_name() {
        return last_name;
    }

    public void setLast_name(String last_name) {
        this.last_name = last_name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getCell_no() {
        return cell_no;
    }

    public void setCell_no(String cell_no) {
        this.cell_no = cell_no;
    }

    public String getId_number() {
        return id_number;
    }

    public void setId_number(String id_number) {
        this.id_number = id_number;
    }

}
