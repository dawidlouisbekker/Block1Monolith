package bankadmin;

import bankadmin.json.JSONPayload;

public class User {
    public String orgUnit;
    public String prevUsername = null;
    public String username = null;
    public String company;
    public String group;
    public boolean edited = false;
    private JSONPayload payload;
    private boolean[] updatedFields;

    public User(String username, String organizationalUnit,  String group) {
        this.orgUnit = organizationalUnit;
        this.username = username;
        this.group = group;
    }

    public User() {
        this.orgUnit = "";
        this.username = "";
        this.group = "";
        this.company = "";
        this.updatedFields = new boolean[]{false, false, false};
        this.payload = new JSONPayload(JSONPayload.JSONType.OBJECT);
    }

    public void resetEdited() {
        for (int i = 0; i < this.updatedFields.length; i++) {
            this.updatedFields[i] = false;
        }   
    }

    public void setPrevUsername() {
        if (this.prevUsername == null) {
            this.prevUsername = this.username;
        }
    }   

    public void setUsername(String username) {
        if (username == null) {
            prevUsername = this.username;
        }
        this.updatedFields[0] = true;
        this.username = username;
    }

    public void setOrgUnit(String orgUnit) {
        this.orgUnit = orgUnit;
        this.updatedFields[1] = true;
    }   

    public void setGroup(String group) {
        this.group = group;
        this.updatedFields[2] = true;
    }

    public String getJSON(){
        this.payload.addPair("prevUsername", this.prevUsername);
        if (this.updatedFields[0]) {
            this.payload.addPair("username", this.username);
        }
        if (this.updatedFields[1]) {
            this.payload.addPair("orgUnit", this.orgUnit);
        }
        if (this.updatedFields[2]) {
            this.payload.addPair("group", this.group);
        }
        return this.payload.getPayload();
    }

    public boolean isEdited() {
        for (boolean field : this.updatedFields) {
            if (field) {
                return true;
            }
        }
        return false;
    }

    public String getOrgUnit() {
        return this.orgUnit;
    }

    public String getUsername() {
        return this.username;
    }

    public String getCompany() {
        return this.company;
    }

    public String getGroup() {
        return this.group;
    }
}
