package bankadmin.json;

public class JSONPayload {
    private String payload;
    private int pairs;
    private JSONType type;
    public enum JSONType {
        ARRAY,
        OBJECT,
        NONE
    }

    public JSONPayload(JSONType type){
        switch (type) {
            case ARRAY:
                this.payload = "[";
                break;
            case OBJECT:
                this.payload = "{";
                break;
            case NONE:
                this.payload = "";
                break;
            default:
                break;
        }
        this.type = type;
    }

    public void addPair(String key, String value){
        if (this.type == JSONType.ARRAY) {
            throw new IllegalArgumentException("Cannot add key value pair to array type");
        }
        if (this.pairs > 0){
            this.payload += ", ";
        }
        if (this.type == JSONType.OBJECT){
            this.payload += "\"" + key + "\": \"" + value + "\"";
        } else if (this.type == JSONType.ARRAY){
            this.payload += "\"" + value + "\"";
        }
        this.pairs++;

    }
    public String getPayload(){
        switch (this.type) {
            case JSONType.ARRAY:
                return this.payload + "]";
            case JSONType.OBJECT:
                return this.payload + "}";
            default:
                return this.payload;
        }
    }




}
