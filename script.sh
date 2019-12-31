#!/bin/bash

mkdir Dataset
python3 Data_scrapper.py
python3 categoriser.py
java -jar RDF_generator.jar
python3 Queries.py > output_queries.text