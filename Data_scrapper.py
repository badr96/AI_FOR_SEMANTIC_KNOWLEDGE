import os
import csv
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from string import Template
import time
import io
import traceback
from collections import defaultdict
#espace vert, urbanisme, musées, resto/bar, monuments, Insolite
#categories = {"Monuments": ["ArchitecturalStructure", "Bridge", "Castle", "Skyscraper", "Monument", "ReligiousBuilding", "Cemetery"], "Museum": ["Museum"]}
#categories = {"Nature" : ["yago:Park108615149", "yago:WikicatFrenchRenaissanceGardens"], "Urban": ["yago:WikicatSquaresInParis", "dbo:Bridge"], "Building": ['yago:Museum103800563'], "Test2": ["dbo:ArchitecturalStructure"], "Test": ["yago:Memorial103743902"]}
#categories = {"Nature" : ["yago:Park108615149", "yago:WikicatFrenchRenaissanceGardens"], "Urban": ["yago:WikicatSquaresInParis", "dbo:Bridge"], "Building": ['yago:Museum103800563', ["yago:Memorial103743902", "dbo:Building"]]}
#yago:WikicatArtMuseumsAndGalleriesInParis
#yago:Garden103417345
#["yago:WikicatMonumentsAndMemorialsInParis", "!yago:Museum103800563"]
#yago:WikicatArtMuseumsAndGalleriesInParis"

categories = {
  "Nature": [
    ["yago:Park108615149", "yago:WikicatFrenchRenaissanceGardens", "yago:WikicatGardensInParis", "yago:Arboretum102733075", "yago:Park108615149", "yago:WikicatBotanicalGardensInFrance", "yago:WikicatParksAndOpenSpacesInParis", "yago:Garden103417345"],
    ["!dbo:Building", "!dbo:Road", "!dbo:Museum"]
  ],
  "Urban": [
    ["yago:WikicatSquaresInParis", ["yago:WikicatMonumentsAndMemorialsInParis", "!yago:Museum103800563"],  "dbo:Road", "dbo:Road"],
    ["!dbo:Building"]
  ],
  "Building": [
    ["yago:WikicatArtMuseumsAndGalleriesInParis", "yago:WikicatHistoryMuseums", "yago:Museum103800563", ["yago:Memorial103743902", "dbo:Building"], "dbo:Museum", "yago:WikicatHistoricHouseMuseums", "yago:WikicatHistoricHouseMuseumsInParis", "dbo:ArchitecturalStructure"],
    ["!dbo:Road", "!dbo:Bridge", "!dbo:SportsTeam"],
  ]
}

i = 0
final = []
tmp = []

def createFilter(rule, extra = False):
  filter = ""
  ext = ""
  if rule.startswith( '!' ):
    rule =  rule.split("!")[1]
    filter += Template("FILTER NOT EXISTS { ?poi rdf:type $type }\n").substitute({'type': rule})
    ext += "Without %s, " % filter
  else:
    filter += Template("FILTER EXISTS { ?poi rdf:type $type }\n").substitute({'type': rule})
    ext += "With %s, " % filter

  if extra == True:
      return ext
  else: 
    return filter


try:
  for categorie in categories:
    for ontologie in categories[categorie][0]:
      globalFilters = categories[categorie][1]
      filtering = ""
      extra = ""
      
      for filter in globalFilters:
          filtering += createFilter(filter) 
          extra += createFilter(filter, True)      

      if type(ontologie) == list:
        extra = "-- "
    
        for filter in ontologie[1:]:
          filtering += createFilter(filter) 
          extra += createFilter(filter, True) 
        
        extra = extra[:-2]
        extra += " --"
        ontologie = ontologie[0]

      print("*** ", ontologie, " ***")

      sparql = SPARQLWrapper("http://dbpedia.org/sparql")
      ask = Template('''
      PREFIX dbpedia: <http://dbpedia.org/resource/>
      PREFIX prop-fr: <http://fr.dbpedia.org/property/>
      PREFIX georss: <http://www.georss.org/georss>
      PREFIX dbpedia-owl:<http://dbpedia.org/ontology/>

      SELECT DISTINCT  ?name, ?wiki_pid, ?image, ?link, ?description_fr, ?description_en, ?longitude, ?latitude

      WHERE {
         <http://dbpedia.org/resource/Paris> geo:geometry ?gm .
  
         ?poi rdf:type $onthologie .
         ?poi rdfs:label ?name .
         ?poi foaf:isPrimaryTopicOf ?link .
         ?poi geo:long|dbp:longitude|prop-fr:longitude ?longitude .
         ?poi geo:lat|dbp:latitude|prop-fr:latitude ?latitude .
         ?poi dbo:wikiPageID ?wiki_pid . 
         $filter
         FILTER (langMatches(lang(?name), 'fr'))
         FILTER (bound(?longitude) && bound(?latitude)) 
         FILTER (xsd:float(?longitude) <= 180 && xsd:float(?longitude) >= -180 &&  xsd:float(?latitude) <= 90 && xsd:float(?latitude) >= -90)
         FILTER (bif:st_intersects ( bif:st_point (xsd:float(?longitude), xsd:float(?latitude) ), ?gm, 20 ) )
         OPTIONAL{?poi dbo:thumbnail ?image }
         OPTIONAL{
            ?poi dbo:abstract ?description_en. 
            FILTER(lang(?description_en)='en')
         }
         OPTIONAL{
            ?poi dbo:abstract ?description_fr. 
            FILTER(lang(?description_fr)='fr')
         }
      }
      LIMIT 10000
      ''')
      query = ask.substitute({ 'onthologie': ontologie, 'filter': filtering})

      sparql.setQuery(query)
      try:
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
          poi = {"complete": True}
          poi["category"] = categorie
          poi["wiki_link"] = result["link"]["value"]
          poi["page_id"] = result["wiki_pid"]["value"]
          poi["name"] = result["name"]["value"]
          poi["longitude"] = result["latitude"]["value"]
          poi["latitude"] = result["longitude"]["value"]
          if "image" in result:
            poi["image"] = result["image"]["value"]
          if "description_fr" in result:
            poi["description_fr"] = result["description_fr"]["value"].replace('\n','')
          if "description_en" in result:
            poi["description_en"] = result["description_en"]["value"].replace('\n','')
          if not all (k in poi for k in ("image","description_fr", "description_en")):
            poi["complete"] = False
          if poi["page_id"] not in tmp:
            i+=1
            final.append(poi)
            print(poi["wiki_link"])
            tmp.append(poi["page_id"])
          
      except Exception as e : 
        print(e)
        break
    print("Nb of results ", i)
  
  print("Size ", len(final))
 
  keys = final[0].keys()
  with io.open("Dataset/poi.csv", "w", newline='\n', encoding="utf-8") as f:
      writer = csv.DictWriter(f, fieldnames=keys)
      writer.writeheader()
      writer.writerows(final)
except Exception as e :  print(traceback.format_exc()) 
