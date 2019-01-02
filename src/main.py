from dbpedia import strictQueryInfluencedBy, queryInfluencedAndInfluencedBy, queryInfluencedAndInfluencedByFor
from graph import generateGraph, saveToFile
from graphviz import Digraph

result = queryInfluencedAndInfluencedBy()
dot = generateGraph(result, Digraph(filename="../output/programming", format="svg"))
saveToFile(dot)


result = strictQueryInfluencedBy()
dot = generateGraph(result, Digraph(filename="../output/programming-strict", format="svg"))
saveToFile(dot)

result = queryInfluencedAndInfluencedByFor("Java (programming language)")
dot = generateGraph(result, Digraph(filename="../output/java", format="svg", engine="dot"))
saveToFile(dot)
