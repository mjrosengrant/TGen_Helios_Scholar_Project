#Reads in Drug Target Rulebase CSV file and converts it into a Neo4j graph

import pandas as pd 
import numpy as np
from py2neo import Graph, Node, Relationship, authenticate


def createDrugs(graph,data):
    uniqueDrugs = np.unique(data["drug"])
    print uniqueDrugs
    nodeCount = 0
    for drug in uniqueDrugs:
        graph.cypher.execute("MERGE (d:Drug {{name:\"{0}\"}})".format(drug))
        nodeCount = nodeCount + 1

def createGenes(graph,data):
    for row_index, row in data.iterrows():
        gene_name = ""
        gene_entrez = ""
        if row["entity_class"] == "biomarker":
            gene_name = row["biomarker_symbol"]
            gene_entrez = row["biomarker_entrez"]
        elif row["entity_class"] == "modifier":
            gene_name = row["modifier_symbol"]
            gene_entrez = row["modifier_entrez"]
        else:
            print"Error in getting genes"
            break
        

        #Query for complete graphs. Doesn't add entity_class to Gene Nodes (stored in aberration instead)
        query = (
            "MATCH (d:Drug {{ name:'{2}'}}) "
            "MERGE (g:Gene {{ name:'{0}', entrez:'{1}'}}) "
            "CREATE UNIQUE (d)-[:TARGETS]->(g) "
        ).format(gene_name, gene_entrez, row["drug"])

        
        # Query for druggene graphs. Adds entity_class attribute to the gene Node
        #query = (
            #"MATCH (d:Drug {{ name:'{2}'}}) "
            #"MERGE (g:Gene {{ name:'{0}', entrez:'{1}', entity_class:'{3}'}}) "
            #"CREATE UNIQUE (d)-[:TARGETS]->(g) "
        #).format(gene_name, gene_entrez, row["drug"], row["entity_class"])


        print query
        graph.cypher.execute(query)

def createAberrations(graph,data):
    for row_index, row in data.iterrows():
        gene_name = ""
        gene_entrez = ""
        ab_type = ""
        ab_value = ""
        
        if row["entity_class"] == "biomarker":
            gene_name = row["biomarker_symbol"]
            gene_entrez = row["biomarker_entrez"]
            ab_type = row["biomarker_aberration_type"]
            ab_value = row["biomarker_aberration_value"]
            
        elif row["entity_class"] == "modifier":
            gene_name = row["modifier_symbol"]
            gene_entrez = row["modifier_entrez"]
            ab_type = row["modifier_aberration_type"]
            ab_value = row["modifier_aberration_value"]
        else:
            print"Error in createAberrations()"
            break

        query = ("MATCH (g:Gene {{name:'{0}', entrez:'{1}'}}), (d:Drug {{name:'{6}'}}) "
                "MERGE (a:Aberration {{ type:'{2}', value:'{3}', gene_entrez:'{4}', entity_class:'{5}' }}) "
                "CREATE UNIQUE (g)-[:HAS_ABERRATION]->(a) "
                "CREATE UNIQUE (d)-[:TARGETS]->(a)"
                ).format(gene_name, gene_entrez, ab_type, ab_value, gene_entrez, row["entity_class"], row["drug"])
        print query
        graph.cypher.execute(query)
    
def createRuleNodes(graph,data):
    for row_index, row in data.iterrows():
        gene_name = ""
        gene_entrez = ""
        ab_type = ""
        ab_value = ""
        
        if row["entity_class"] == "biomarker":
            gene_name = row["biomarker_symbol"]
            gene_entrez = row["biomarker_entrez"]
            ab_type = row["biomarker_aberration_type"]
            ab_value = row["biomarker_aberration_value"]
            
        elif row["entity_class"] == "modifier":
            gene_name = row["modifier_symbol"]
            gene_entrez = row["modifier_entrez"]
            ab_type = row["modifier_aberration_type"]
            ab_value = row["modifier_aberration_value"]
        else:
            print"Error in createAberrations()"
            break
        query = ("MATCH (g:Gene {{name:'{0}', entrez:'{1}'}}), "
                 "(a:Aberration {{ type:'{2}', value:'{3}', gene_entrez:'{4}', entity_class:'{5}' }}), "
                 "(d:Drug {{name:'{6}'}} ) "
                 "Merge (r:Rule {{rulenum:'{7}', evidence:'{8}', pmid:'{9}', evidence_text:\"{10}\" }}) "
                 "CREATE UNIQUE (r)<-[:IS_PART_OF]-(g) "
                 "CREATE UNIQUE (r)<-[:IS_PART_OF]-(a) "
                 "CREATE UNIQUE (r)<-[:IS_PART_OF]-(d) "
                ).format(gene_name, gene_entrez, ab_type, ab_value, gene_entrez, row["entity_class"], 
                         row["drug"], row_index, row["Evidence"], row["PMID"], row["Evidence Text"])
        print query
        graph.cypher.execute(query)

def main():
    print "Starting Main Function"
    data = pd.read_csv('node_info/DrugRulesFixed.csv')

    authenticate("localhost:7474", "neo4j", "qwerty1")
    graph = Graph()
    
    createDrugs(graph,data)
    createGenes(graph,data)
    
    # If building druggene version of graph, comment out createAberrations() and createRuleNodes()
    # Also don't forget to check that the correct query inside createGenes() is uncommented
    createAberrations(graph,data)
    createRuleNodes(graph,data)
main()


# In[ ]:



