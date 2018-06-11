import java.io.*;
import java.util.*;
import java.io.File;
import java.io.InputStream;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.google.gson.Gson;
import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.ClientResponse;
import com.sun.jersey.api.client.WebResource;
import com.fasterxml.jackson.databind.ObjectMapper;

public class CSV2JSON {


    public static void main(String[] args) throws Exception {

        Client client = Client.create();

        WebResource webResource = client
                .resource("https://file.io/0LsN2q");

        ClientResponse response = webResource.accept("csv")
                .get(ClientResponse.class);

        if (response.getStatus() != 200) {
            throw new RuntimeException("Failed : HTTP error code : "
                    + response.getStatus());
        }

        String output = response.getEntity(String.class);

        //System.out.println(output);
        //File output = new File("input.csv");
        File outputt = new File("output.json");
        //InputStream in = new FileInputStream(output);
        InputStream in = new ByteArrayInputStream(output.getBytes("UTF-8"));
        CSV csv = new CSV(true, ',', in );
        List < String > fieldNames = null;
        if (csv.hasNext()) fieldNames = new ArrayList < > (csv.next());
            List < Map < String, String >> list = new ArrayList < > ();
            while (csv.hasNext()) {
                List < String > x = csv.next();
                Map < String, String > obj = new LinkedHashMap < > ();
                for (int i = 0; i < fieldNames.size(); i++) {
                    obj.put(fieldNames.get(i), x.get(i));
                }
                list.add(obj);
            }
        ObjectMapper mapperr = new ObjectMapper();
        mapperr.enable(SerializationFeature.INDENT_OUTPUT);
        //mapperr.writeValue(System.out, list);
        System.out.println(list);
        System.out.println(list.get(0).values());
        mapperr.writerWithDefaultPrettyPrinter().writeValue(outputt, list);


        Scanner reader = new Scanner(System.in);  // Reading from System.in
        System.out.println("Enter The column Name you want to Remove: ");
        String n = reader.next(); // Scans the next token of the input as an int.
//once finished
        System.out.println(n);
        reader.close();

        for (int i = 0; i < list.size(); i++) {
            if (list.get(i).containsKey(n)) ;
            list.get(i).remove(n);
        }
        System.out.println(list);

       // ArrayList<list> sampleList = new ArrayList<list>();
        String json = new Gson().toJson(list);
        System.out.println(json);


    }

}
