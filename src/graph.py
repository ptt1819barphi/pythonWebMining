from graphviz import Digraph

def count(dict):
    """
    Method used to calculate the amount of influences a language had.
    The number is stored in a dictionary and maped onto the name of the language.
    The resulting dictionary is returned.
    """
    amountDict = {}

    for key in dict:
        if not key in amountDict:
            amountDict[key] = 0
        for value in dict[key]:
            if not value in amountDict:
                amountDict[value] = 0
            amountDict[value] += 1
    return amountDict

def amountToColor(amount):
    """
    Helper method for interpolating the color based on the specified amount.
    """
    if amount >= 10:
        return '0 1 1'
    return str(0.333 -0.0333 * amount) + ' 1 1'

def amountToSize(amount):
    """
    Helper method for interpolating the size based on the specified amount.
    """
    if amount >= 10:
        return '28'
    return str(14 + 1.4 * amount)

def amountToPenWidth(amount):
    """
    Helper method for interpolating the node thickness based on the specified amount.
    """
    if amount >= 10:
        return '4.5'
    return str(3 + 0.15 * amount)

def getAttributes(amount):
    """
    Helper method for returning a dictionary ready to paste as an attribute for
    a node consisting of the calcuated size, color and node thickness.
    """
    return {'penwidth':amountToPenWidth(amount),
            'color':amountToColor(amount),
            'fontsize':amountToSize(amount)}

def generateGraph(dict, dot = Digraph()):
    """
    This method created nodes and edges based on the data in the specified dictionary.
    Thereby, an edge is created between each element in value to it's corresponding key.
    
    The result is the Digraph.
    """
    amountDict = count(dict)
    createdNodes = []
    
    for key in dict:
        if not key in createdNodes:
            dot.node(key, _attributes=getAttributes(amountDict[key]))
            createdNodes.append(key)
        for value in dict[key]:
            if not value in createdNodes:
                dot.node(value, _attributes=getAttributes(amountDict[value]))
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