from dbpedia import strictQueryInfluencedBy, queryInfluencedAndInfluencedBy, queryInfluencedAndInfluencedByFor
from graph import generateGraph, saveToFile
from graphviz import Digraph

#Non-strict influenced and influencedBy
result = queryInfluencedAndInfluencedBy()
dot = generateGraph(result, Digraph(filename="../output/programming", format="svg"))
saveToFile(dot)

#Strict influenced and influencedBy
result = strictQueryInfluencedBy()
dot = generateGraph(result, Digraph(filename="../output/programming-strict", format="svg"))
saveToFile(dot)

#Influenced and influencedBy for the programmming language Java
result = queryInfluencedAndInfluencedByFor("Java (programming language)")
dot = generateGraph(result, Digraph(filename="../output/java", format="svg"))
saveToFile(dot)