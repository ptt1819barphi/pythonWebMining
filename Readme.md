# Summary
This Repo deals with the following problem:
Creating a graphic represenation of influences between programming languages.

This problem is solved using the following strategies:

* Extract the data from dbpedia with a SPARQL query.
* Generate a graph from the extracted data.
* Save the resulting graph as ".svg". 

# Prerequisites

* Python 3.7
* SPARQLWrapper (https://rdflib.github.io/sparqlwrapper/)
* graphviz (https://pypi.org/project/graphviz/)

# Usage
	$ python main.py
The result is in the "output" directory.