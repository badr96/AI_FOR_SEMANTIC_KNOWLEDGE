package aikm;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.FileWriter;
//import java.io.IOException;
import java.util.ArrayList;
import java.util.List;


import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.StmtIterator;
import org.apache.jena.vocabulary.VCARD;

import org.apache.jena.rdf.model.*;


public class Document {
	private String ID;
	private String name;
	private String description;
	private String cluster_name;
    public Document() {
    	
    }
	public Document(String iD, String name, String description, String cluster_name) {
		this.ID = iD;
		this.name = name;
		this.description = description;
		this.cluster_name = cluster_name;
	}

	public String getID() {
		return ID;
	}
	
	Model model = ModelFactory.createDefaultModel();
	
	public void readDocuments(String fileName) {
		List<Document> articles = new ArrayList<>();
		BufferedReader br = null;
		String line = "";
		try {
			br = new BufferedReader(new FileReader(fileName));
			while ((line = br.readLine()) != null) {
				String[] attributes = line.split(",");
				String articleURI = "http://Monument/";
				Document article = createDocument(attributes, articleURI);

				articles.add(article);
				line = br.readLine();
			}
		} catch (IOException ioe) {
			ioe.printStackTrace();
		}

		
	}

	public Document createDocument(String[] metadata, String uri) {

		String id = metadata[0];
		String name = metadata[1];
		String description = metadata[2];
		String cluster_name = metadata[4];
		
		this.model.createResource(uri+id).addProperty(VCARD.PRODID, id)
		.addProperty(VCARD.NAME, name)
		.addProperty(VCARD.CATEGORIES, description)
		.addProperty(VCARD.CLASS, cluster_name);

		return new Document(id, name, description, cluster_name);
	}

	public void listStatement() {
		StmtIterator iter = model.listStatements();
		while (iter.hasNext()) {
			Statement stmt      = iter.nextStatement();  
			Resource  subject   = stmt.getSubject();     
			Property  predicate = stmt.getPredicate();   
			RDFNode   object    = stmt.getObject();      

			System.out.print(subject.toString());
			System.out.print(" " + predicate.toString() + " ");
			if (object instanceof Resource) {
				System.out.print(object.toString());
			} else {
				System.out.print(" \"" + object.toString() + "\"");
			}

			System.out.println(" .");
		}
				
	}

	public void writeRDF() {
		this.model.write(System.out, "RDF/XML-ABBREV");
	}

	public void saveRdfFile() throws IOException {
		
		String fileName = "monument.rdf";
		FileWriter out = new FileWriter(fileName);

		try {
			model.write(out, "RDF/XML-ABBREV" );
		}
		finally {
			try {
				out.close();
			}
			catch (IOException closeException) {
				closeException.printStackTrace();
			}
		}

	}

	public void setID(String iD) {
		ID = iD;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public String getCluster_name() {
		return cluster_name;
	}

	public void setCluster_name(String cluster_name) {
		this.cluster_name = cluster_name;
	}

	@Override
	public String toString() {
		return "Document [ID=" + ID + ", name=" + name + ", description=" + description + ", cluster_name="
				+ cluster_name + "]";
	}
}
