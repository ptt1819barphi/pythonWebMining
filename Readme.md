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
    $ cd src
    $ python main.py
The result is in the "output" directory.
In the "output" directory are three generated files:

* programming.svg which contains all influences between programming languages.
* programming-strict.svg which contains all influences between programming languages but checks if both languages have a reference to each other (A influenced B and B influencedBy A).
* java.svg an example for getting the influences of a specific programming language (java in this example).

The code describing how to use the methods of dbpedia.py and graph.py is in the main.py.
Both dbpedia.py and graph.py also include pythondoc for each method.