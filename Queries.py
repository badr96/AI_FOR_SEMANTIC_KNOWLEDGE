import rdflib
import os 
g = rdflib.Graph()

g.parse("monument.rdf")



Querie1 = """

	   PREFIX vcard:<http://www.w3.org/2001/vcard-rdf/3.0#>

	   SELECT DISTINCT ?name ?categories_name
       WHERE {
         ?a vcard:NAME ?name.
         ?a vcard:CLASS ?categories_name.
       }
    LIMIT 20

"""


Querie2 = """
		 PREFIX vcard:<http://www.w3.org/2001/vcard-rdf/3.0#>


		 SELECT DISTINCT ?name ?categories_name
       	 WHERE {
          ?a vcard:NAME ?name.
          ?a vcard:CLASS ?categories_name. FILTER( ?categories_name = "musée")
        }
	"""

Querie3 = """
    PREFIX vcard:<http://www.w3.org/2001/vcard-rdf/3.0#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?parc (COUNT(?parc) as ?parc_count)
    WHERE{
        ?a vcard:CLASS ?parc. FILTER(?parc = "parc")
      }
     
"""


qres = g.query(Querie1)
for row in qres:
	print(row['name'],'had categorie:',row['categories_name'])

print('\n\t next Querie: [Get Musuem monument]: Press a button')
input()

qres = g.query(Querie2)
for row in qres:
	print(row['name'])

print('\n\t next Querie: [Get Number of Theatre, Hotel and tour]: Press a button')
input()
qres = g.query(Querie3)
for row in qres:
  print('there is:',row['parc_count'],row['parc'],'in Paris')
