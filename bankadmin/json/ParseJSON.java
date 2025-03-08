package bankadmin.json;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ParseJSON<T> {  // No need for "T extends Object" since all classes implicitly extend Object

    public List<T> data;
    private Class<T> type;

    static class JSONObject {
        String key;
        Object value;
    }

    static class JSONArray {
        String key;
        String[] values;
    }

    private void setPublicFieldValue(T object, String fieldName, Object value) {
        try {
            Field field = object.getClass().getField(fieldName); // Works only for public fields
            field.set(object, value);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            e.printStackTrace();
        }
    }

    static private Map<String, Object> getMap(String payload) {
        Map<String, Object> jsonMap = new HashMap<>();

        Pattern pattern = Pattern.compile("\"(\\w+)\":\\s*(\"[^\"]*\"|\\d+)");
        Matcher matcher = pattern.matcher(payload);

        while (matcher.find()) {
            jsonMap.put(matcher.group(1), matcher.group(2).replaceAll("\"", ""));
        }
        System.out.println("Map:" + jsonMap);
        return jsonMap;
    }
    
    // Fills an array of the class's public fields with the values from the JSON payload
    // Result is accessed through the data field
    public ParseJSON(Class<T> type) {   
        this.type = type;
        this.data = new ArrayList<>();
    }

    public T parseFlatJSON(T object, String jsonPayload) {
        Map<String,Object> valuesMap = new HashMap<>();
   
        valuesMap = getMap(jsonPayload);
        Map<String,String> jsonMap = new HashMap<>();
        Class<?> clazz = object.getClass();
        for (Field field : clazz.getFields()) {
            String strfield = field.getName();
            String typeName = field.getType().getSimpleName();
            jsonMap.put(strfield, typeName);
        }  
        for (String field : jsonMap.keySet()) {
            System.out.println("Field: " + field + " Type: " + jsonMap.get(field));
            try {
                switch (jsonMap.get(field)) {
                    case "String":
                        setPublicFieldValue(object, field, (String)valuesMap.get(field));
                        break;
                    case "String[]":
                        setPublicFieldValue(object, field, (String[])valuesMap.get(field));
                    case "Integer":
                        setPublicFieldValue(object, field, Integer.parseInt((String)valuesMap.get(field)));
                        break;
                    case "Double":
                        setPublicFieldValue(object, field, Double.parseDouble((String)valuesMap.get(field)));
                        break;
                    default:
                        break;
                }
            } catch (Exception e) {
                System.out.println(e);
            }
        }
        this.data.add(object);
        return object;
    }

    public List<T> parseJSONArray(String jsonPayload) {
        String regex = "\\{[^{}]*\\}";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(jsonPayload);
        while (matcher.find()) {
            try {
                T newObj = type.getDeclaredConstructor().newInstance();  // ✅ Create new instance
                String objStr = matcher.group();
                System.out.println("Object: " + objStr);
                parseFlatJSON(newObj, objStr); // Implement this for JSON mapping
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        System.out.println("Parsed JSON Array: " + this.data);
        return this.data;
    }
/* 
    public static void main(String[] args) {
        Sample sampleObject = new Sample();
        ParseJSON<Sample> parser = new ParseJSON<>(sampleObject, "{ \"id\": 42, \"name\": \"John Doe\", \"balance\": 1000.75 }");


        // Set values to public fields
        parser.setPublicFieldValue(sampleObject, "id", 42);
        parser.setPublicFieldValue(sampleObject, "name", "John Doe");

        // Set values to private fields
        parser.setPrivateFieldValue(sampleObject, "balance", 1000.75);
        System.out.println("Private fields: " + parser.getAllPrivateFieldNames(Sample.class)); // Output: [balance]
        // Print results
        System.out.println("id: " + sampleObject.id); // Output: id: 42
        System.out.println("name: " + sampleObject.name); // Output: name: John Doe
        // Access private field using reflection
        try {
            Field balanceField = Sample.class.getDeclaredField("balance");
            balanceField.setAccessible(true);
            System.out.println("balance: " + balanceField.get(sampleObject)); // Output: balance: 1000.75
        } catch (Exception e) {
            e.printStackTrace();
        }
    }*/
}
