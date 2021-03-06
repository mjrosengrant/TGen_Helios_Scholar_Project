# Modelling-Drug-Gene-Interactions-In-Neo4j

ABSTRACT:
TGen has developed a manually curated rule base that links genomic aberrations to therapeutic selections for use in precision medicine studies. The goal of this project was to model the drug rule base as a network, extend it with protein-protein interactions from the Pathway Commons 2 (PC2) dataset, and store resultant network in a Neo4j graph database. Additionally, network analysis was performed to discover interesting properties associated with drug rule nodes in the network.

We analyzed the combined PC2 drug rule graph for two important node characteristics in biological networks:  betweenness and degree. Biomarkers (drug targets) from the rule base tended to have a higher overall degree then modifiers (non-drug target genes that alter drug response) and the the rest of the nodes in the network. The higher degree indicates that the biomarkers are more connected to other proteins in the larger network. The biomarker nodes also had a higher betweenness centrality than modifiers. The betweenness centrality is a measure of the number of shortest paths that go through a node. To investigate these properties across the whole network, we performed outlier analysis for betweenness and degree. The biomarker category exhibited a greater proportion of outliers than the modifiers. In addition, analysis of the outliers, irrespective of biomarker/modifier status, was performed to identify enriched biological functions associated with those genes. Interesting differences and commonalities were noted across the group of outliers.

In conclusion, we have successfully constructed the drug rule base, integrated  it with the pathway commons 2 resource, and stored it in the Neo4j graph database. We also showed that drug rule related nodes have unique network biological properties. The Neo4j combined database will serve as a central resource used for the further exploration of the network based analysis of drug rule associated genes in the future

*
Drug target data is intellectual property of the Translational Genomics Research Institute in Phoenix AZ

Pathway Commons Data can be found at http://www.pathwaycommons.org/pc2/downloads
File to download from page above is PC.Reactome.EXTENDED_BINARY_SIF.hgnc




*


