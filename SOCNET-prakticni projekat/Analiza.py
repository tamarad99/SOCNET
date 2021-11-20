import networkx as nx
from networkx.algorithms import cluster
from networkx.classes import graph
from networkx.classes.function import neighbors
from networkx.linalg.attrmatrix import _edge_value
import Loading as l
import Clustering as c

def density(clusterNet):
    density = nx.density(clusterNet)
    
    return density

def averageDegree(g):
   
    return 2 * nx.number_of_edges(g) / nx.number_of_nodes(g)
    

def diameterOfNet(g):
    
    return nx.diameter(g)
    

def averageDist(g):
    return nx.average_shortest_path_length(g)

def clusterAnalyse(g, score):
    ad = averageDegree(g)
    score[0].append(ad)

    adist = averageDist(g)
    score[1].append(g)

    diam = diameterOfNet(g)
    score[2].append(diam)

    dens = density(g)
    score[3].append(dens)

    return score