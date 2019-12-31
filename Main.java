package aikm;

import java.io.IOException;

public class Main {

	public static void main(String[] args) throws IOException {
		Document doc = new Document();
		doc.readDocuments("predicted_data.csv");
		doc.listStatement();
		doc.saveRdfFile();
	}

}
