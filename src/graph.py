from graphviz import Digraph

def generateGraph(dict, dot = Digraph()):
    """
    This method created nodes and edges based on the data in the specified dictionary.
    Thereby, an edge is created between each element in value to it's corresponding key.
    
    The result is the Digraph.
    """
    createdNodes = []
    
    for key in dict:
        if not key in createdNodes:
            dot.node(key)
            createdNodes.append(key)
        for value in dict[key]:
            if not value in createdNodes:
                dot.node(value)
                createdNodes.append(value)
            dot.edge(value, key)
    
    return dot

def saveToFile(dot, cleanup=True, file = None):
    """
    This method is used to save a Digraph based on its internal settings to a file.
    The internal path of the Digraph is choosen, if no path was specified.
    
    It returns the path to the created file.
    """
    savedAs = ""
    if file is None:
        savedAs = dot.render(cleanup=cleanup)
    else:
        savedAs = dot.render(cleanup=cleanup, filename=file)
        
    print(savedAs + " saved.")
    return savedAs
    