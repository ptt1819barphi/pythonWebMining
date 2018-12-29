from argparse import ArgumentError
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from time import sleep

DEFAULT_URL = "https://dbpedia.org/sparql"

def clean(str):
    """
    Helper method for trimming away Wikipedia's additional parentheses specifications.
    e.g.: "Java (programming language)" -> "Java"
    """
    return re.sub("\\s*\\(.*\\)", "", str)

def query(query, url=DEFAULT_URL):
    """
    Method for sending a query to a serer under the specified URL.
    In case no URL was given, the DEFAULT_URL is used.
    
    The query must contain "OFFSET ?offset" and "LIMIT 10000",
    this is ruled by the fact that the query is written especially for the dbpedia.
    """
    if ("OFFSET ?offset" not in query) or ("LIMIT 10000" not in query):
        raise ArgumentError("Please add 'LIMIT 10000' and 'OFFSET ?offset' to the query.")
    
    connection = SPARQLWrapper(url)
    connection.setReturnFormat(JSON)
    
    offset = 0
    result = []
    finished = False
    while not finished:
        tempQuery = query.replace("?offset", str(offset))
        connection.setQuery(tempQuery)
        
        res = []
        
        while res == []:
            try:
                res = connection.query().convert()
            except:
                print("Error! Sleeping ...")
                sleep(10)
                print("... next try.")
        
        result.extend(res["results"]["bindings"])
        finished = len(res["results"]["bindings"]) != 10000
        offset += 10000
    return result

    
def queryLiteral(queryStr, url=DEFAULT_URL):
    """
    Method for converting the query() result to a list of sublists.
    """
    result = query(queryStr, url)
    
    newResult = []
    for row in result:
        newRow = []
        for column in row:
            newRow.append(row[column]["value"])
        newResult.append(newRow)
    return newResult

def queryInfluencedBy(minDepth = 0, maxDepth = 5):
    """
    This method searches for all programming languages and the languages which influenced them.
    
    The parameters "minDepth" and "maxDepth" are there to specify the depth of the subcategories, which are to be checked for language influence.
    
    To enchance the data quality, a method for reducing the connections is done as follows:
    A, B = Language
    A influencedBy B
    B influenced A
    
    The result is a dictionary, which maps the language name onto a list of languages which it was influenced by.
    """
    queryStr = """
SELECT DISTINCT ?name1, ?name2 WHERE {
    ?article1 dct:subject/skos:broader{?minDepth,?maxDepth} dbc:Programming_languages.
    ?article2 dct:subject/skos:broader{?minDepth,?maxDepth} dbc:Programming_languages.
    ?article1 dbo:influencedBy ?article2.
    ?article2 dbo:influenced ?article1.
    ?article1 rdfs:label ?label1.
    FILTER(langMatches(LANG(?label1),"EN")).
    BIND(STR(?label1) AS ?name1).
    ?article2 rdfs:label ?label2.
    FILTER(langMatches(LANG(?label2),"EN")).
    BIND(STR(?label2) AS ?name2).
}
ORDER BY ASC(?name1) ASC(?name2)
LIMIT 10000
OFFSET ?offset
"""
    queryStr = queryStr.replace("?minDepth", str(minDepth)).replace("?maxDepth", str(maxDepth))
    result = queryLiteral(queryStr)
    
    resultDict = {}
    
    for r in result:
        key = clean(r[0])
        value = clean(r[1])
        if not key in resultDict:
            resultDict[key] = []
        resultDict[key].append(value)
    return resultDict

def queryInfluencedAndInfluencedBy(name):
    """
    The result is the same as from the method "queryInfluencedBy()"
    The only difference is, its specified for only one language,
    e.g.: given "Java" as the language,
    the result is a list of languages which "Java" was influenced by and a list of languages it itself influenced.
    
    The same method as in "queryInfluencedBy()" is applied for reducing the results.
    """
    influencedByQuery = """
SELECT DISTINCT ?influencedBy WHERE {
    ?article1 rdfs:label ?label1.
    FILTER(langMatches(LANG(?label1),"EN")).
    FILTER(STR(?label1) = "?name").
    ?article1 dbo:influencedBy ?article2.
    ?article2 dbo:influenced ?article1.
    ?article2 rdfs:label ?label2.
    FILTER(langMatches(LANG(?label2),"EN")).
    BIND(STR(?label2) AS ?influencedBy).
}
ORDER BY ASC(?influencedBy)
LIMIT 10000
OFFSET ?offset
"""
    influencedQuery = """
SELECT DISTINCT ?influenced WHERE {
    ?article1 rdfs:label ?label1.
    FILTER(langMatches(LANG(?label1),"EN")).
    FILTER(STR(?label1) = "?name").
    ?article1 dbo:influenced ?article2.
    ?article2 dbo:influencedBy ?article1.
    ?article2 rdfs:label ?label2.
    FILTER(langMatches(LANG(?label2),"EN")).
    BIND(STR(?label2) AS ?influenced).
}
ORDER BY ASC(?influenced)
LIMIT 10000
OFFSET ?offset
"""
    
    influencedByQuery = influencedByQuery.replace("?name", name)
    influencedQuery = influencedQuery.replace("?name", name)
    
    influencedByResult = queryLiteral(influencedByQuery)
    influencedResult = queryLiteral(influencedQuery)
    resultDict = {}
    name = clean(name)
    
    resultDict[name] = [clean(x[0]) for x in influencedByResult]
    
    for influenced in influencedResult:
        resultDict[clean(influenced[0])] = [name]

    return resultDict