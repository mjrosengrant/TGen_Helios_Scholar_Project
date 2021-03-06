import csv
import numpy as np
import pandas as pd
from py2neo import Graph, Node, Relationship, authenticate


def loadBetweennessData():
    return pd.read_csv('node_info/pc2_druggene_allnode_info.csv')
 
def writeFile(filename, nodeList, graph, bDict):
    with open(filename, 'a') as f:
        writer = csv.writer(f)            
        header = [ "id", "name", "betweenness" ]
        writer.writerows([header])

        for row in nodeList:
            new_row = [ row["id"], row["name"], bDict[row["id"]] ]
            writer.writerows([new_row])

def main():
    #Export results to CSV file
    authenticate("localhost:7474", "neo4j", "qwerty1")
    graph = Graph()
    
    #Run query to get list of all biomarker IDs
    biomarker_query = (
		"MATCH (n:Gene)-[:HAS_ABERRATION]->(a:Aberration {entity_class:'biomarker'}) " 
		"WHERE NOT( (n)-[:HAS_ABERRATION]->({entity_class:'modifier'} ) ) "
		"RETURN DISTINCT ID(n) as id, n.name as name order by name"
   		)

    biomarker_query = "MATCH (n:Gene {entity_class:'biomarker'}) RETURN DISTINCT ID(n) as id, n.name as name order by name"
    
    #Run second query to get list of all modifier IDs
    modifier_query = (
		"MATCH (n:Gene)-[:HAS_ABERRATION]->(a:Aberration {entity_class:'modifier'}) " 
		"WHERE NOT( (n)-[:HAS_ABERRATION]->({entity_class:'biomarker'} ) ) "
		"RETURN DISTINCT ID(n) as id, n.name as name order by name"
   		)
    modifier_query = "MATCH (n:Gene {entity_class:'modifier'}) RETURN DISTINCT ID(n) as id, n.name as name order by name"

    bio_mod_query = (
        "MATCH (n:Gene)-[:HAS_ABERRATION]->(a:Aberration {entity_class:'modifier'}) " 
        "WHERE ( (n)-[:HAS_ABERRATION]->({entity_class:'biomarker'} ) ) "
        "RETURN DISTINCT ID(n) as id, n.name as name order by name"
        )
    bio_mod_query = ("MATCH (n:Gene {entity_class:'modifier'}) RETURN DISTINCT ID(n) as id, n.name as name order by name "
        "UNION MATCH (n:Gene {entity_class:'biomarker'}) RETURN DISTINCT ID(n) as id, n.name as name order by name "
        )

    drug_query = "MATCH (d:Drug) RETURN DISTINCT ID(d) as id, d.name as name order by name"
    gene_query = "MATCH (g:Gene) RETURN DISTINCT ID(g) as id, g.name as name order by name"
    allNode_query = "MATCH n RETURN DISTINCT ID(n) as id, n.name as name order by name"
    aberration_query = "MATCH a RETURN DISTINCT ID(a) as id, a.name as name order by name"

    print "Executing Queries..."
    biomarkers = graph.cypher.execute(biomarker_query)
    modifiers = graph.cypher.execute(modifier_query)
    bio_mods = graph.cypher.execute(bio_mod_query)
    drugs = graph.cypher.execute(drug_query)
    genes = graph.cypher.execute(gene_query)
    allNodes = graph.cypher.execute(allNode_query)
    aberrations = graph.cypher.execute( aberration_query )

    #Load betweenness data and create Dictionary matching id to betweenness value
    nodeData = loadBetweennessData()
    # bdict maps a node id as an index to its betweenness value, for easy access in the writeFile function.
    bdict = dict(zip(nodeData["id"], nodeData["betweenness"]))

    #Make http request to neo4j to get degree for each.
    print "Writing to Files..."
    writeFile("pc2_druggene_biomarker_betweenness.csv",biomarkers,graph,bdict)
    writeFile("pc2_druggene_modifier_betweenness.csv",modifiers,graph,bdict)
    writeFile("pc2_druggene_bio_mod_degrees.csv",bio_mods,graph,bdict)
    writeFile("pc2_druggene_drug_betweenness.csv",drugs,graph,bdict)
    writeFile("pc2_druggene_gene_betweenness.csv",genes,graph,bdict)
    writeFile("pc2_druggene_allnode_betweenness.csv",allNodes,graph,bdict)
    #writeFile("pc2_aberration_degrees.csv",aberrations,graph,bdict)

    print "Done"



main()




