from argparse import ArgumentError
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from time import sleep

DEFAULT_URL = "https://dbpedia-live.openlinksw.com/sparql"

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

def getResultDict(queryResult):
    """
    Helper method for transforming the query result to a dictionary.
    """
    resultDict = {}
    
    for r in queryResult:
        key = clean(r[0])
        value = clean(r[1])
        if not key in resultDict:
            resultDict[key] = []
        if not value in resultDict[key]:
            resultDict[key].append(value)
    return resultDict

def queryInfluencedBy():
    """
    This method searches for all programming languages and the languages which influenced them.
    The result is a dictionary, which maps the language name onto a list of languages which it was influenced by.
    """
    queryStr = """
SELECT ?label1, ?label2 WHERE {
    SELECT DISTINCT ?label1, ?label2 WHERE {
        ?article1 dbp:wikiPageUsesTemplate dbt:Infobox_programming_language.
        ?article2 dbp:wikiPageUsesTemplate dbt:Infobox_programming_language.
        ?article1 dbo:influencedBy ?article2.
        ?article1 rdfs:label ?label1.
        FILTER(langMatches(LANG(?label1),"EN")).
        ?article2 rdfs:label ?label2.
        FILTER(langMatches(LANG(?label2),"EN")).
    }
    ORDER BY ASC(?label1) ASC(?label2)
}
LIMIT 10000
OFFSET ?offset
"""
    result = queryLiteral(queryStr)
    return getResultDict(result)

def queryInfluenced():
    """
    This method searches for all programming languages and the languages which they influenced.
    The result is a dictionary, which maps the language name onto a list of languages which it was influenced by.
    """
    queryStr = """
SELECT ?label2, ?label1 WHERE {
    SELECT DISTINCT ?label2, ?label1 WHERE {
        ?article1 dbp:wikiPageUsesTemplate dbt:Infobox_programming_language.
        ?article2 dbp:wikiPageUsesTemplate dbt:Infobox_programming_language.
        ?article1 dbo:influenced ?article2.
        ?article1 rdfs:label ?label1.
        FILTER(langMatches(LANG(?label1),"EN")).
        ?article2 rdfs:label ?label2.
        FILTER(langMatches(LANG(?label2),"EN")).
    }
    ORDER BY ASC(?label2) ASC(?label1)
}
LIMIT 10000
OFFSET ?offset
"""
    result = queryLiteral(queryStr)
    return getResultDict(result)


def queryInfluencedAndInfluencedBy():
    """
    Combines the results from influenced() and influencedBy()
    """
    result = queryInfluencedBy()
    result2 = queryInfluenced()
    
    for key in result2:
        if key in result:
            for value in result2[key]:
                if not value in result[key]:
                    result[key].append(value)
        else:
            result[key] = result2[key]
    return result

def strictQueryInfluencedBy():
    """
    This method searches for all programming languages and the languages which influenced them.
    
    To enchance the data quality, a method for reducing the connections is done as follows:
    A, B = Language
    A influencedBy B
    B influenced A
    
    The result is a dictionary, which maps the language name onto a list of languages which it was influenced by.
    """
    queryStr = """
SELECT ?label1, ?label2 WHERE {
    SELECT DISTINCT ?label1, ?label2 WHERE {
        ?article1 dbp:wikiPageUsesTemplate dbt:Infobox_programming_language.
        ?article2 dbp:wikiPageUsesTemplate dbt:Infobox_programming_language.
        ?article1 dbo:influencedBy ?article2.
        ?article2 dbo:influenced ?article1.
        ?article1 rdfs:label ?label1.
        FILTER(langMatches(LANG(?label1),"EN")).
        ?article2 rdfs:label ?label2.
        FILTER(langMatches(LANG(?label2),"EN")).
    }
    ORDER BY ASC(?label1) ASC(?label2)
}
LIMIT 10000
OFFSET ?offset
"""
    result = queryLiteral(queryStr)
    
    return getResultDict(result)

def queryInfluencedAndInfluencedByFor(name):
    """
    The result is the same as from the method "queryInfluencedAndInfluencedBy()"
    The only difference is, its specified for only one language,
    e.g.: given "Java (programming language)" as the language,
    the result is a list of languages which "Java" was influenced by and a list of languages it itself influenced.
    Note that only the "Java" infobox is taken for account.
    """
    influencedByQuery = """
SELECT ?influencedBy WHERE {
    SELECT DISTINCT ?influencedBy WHERE {
        ?article1 dbp:wikiPageUsesTemplate dbt:Infobox_programming_language.
        ?article2 dbp:wikiPageUsesTemplate dbt:Infobox_programming_language.
        ?article1 rdfs:label ?label1.
        FILTER(langMatches(LANG(?label1),"EN")).
        FILTER(STR(?label1) = "?name").
        ?article1 dbo:influencedBy ?article2.
        ?article2 rdfs:label ?influencedBy.
        FILTER(langMatches(LANG(?influencedBy),"EN")).
    }
    ORDER BY ASC(?influencedBy)
}
LIMIT 10000
OFFSET ?offset
"""
    influencedQuery = """
SELECT ?influenced WHERE {
    SELECT DISTINCT ?influenced WHERE {
        ?article1 dbp:wikiPageUsesTemplate dbt:Infobox_programming_language.
        ?article2 dbp:wikiPageUsesTemplate dbt:Infobox_programming_language.
        ?article1 rdfs:label ?label1.
        FILTER(langMatches(LANG(?label1),"EN")).
        FILTER(STR(?label1) = "?name").
        ?article1 dbo:influenced ?article2.
        ?article2 rdfs:label ?influenced.
        FILTER(langMatches(LANG(?influenced),"EN")).
    }
    ORDER BY ASC(?influenced)
}
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
