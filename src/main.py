from dbpedia import queryInfluencedBy, queryInfluencedAndInfluencedBy
from graph import generateGraph, saveToFile
from graphviz import Digraph


result = queryInfluencedBy()
dot = generateGraph(result, Digraph(filename="../output/programming", format="svg"))
saveToFile(dot)

result = queryInfluencedAndInfluencedBy("Java (programming language)")
dot = generateGraph(result, Digraph(filename="../output/java", format="svg", engine="dot"))
saveToFile(dot)