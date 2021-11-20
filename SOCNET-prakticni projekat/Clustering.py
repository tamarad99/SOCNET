import networkx as nx
from networkx.algorithms import cluster
from networkx.classes import graph
from networkx.classes.function import neighbors

#metoda koja identifikuje komponente povezanosti unutar grafa,
#vraca skup skupova sa cvorovima koji pripadaju istoj komponenti
def identifyComponents(g):
    components = set()
    visited = set()

    for node in g:
        if node not in visited:
            components.add(bfs(visited, g, node))
    numberOfC = str(len(components))
    print("Graf sadrzi " + numberOfC + " klastera.")
    return frozenset(components)


#bfs algoritam, vraca skup skupova koji su u istoj komponenti povezanosti
def bfs(visited, g, node):
    comp = set()
    queue = list()
    comp.add(node)
    visited.add(node)
    queue.append(node)
    
    while queue:
        current = queue.pop(0)
        neighbours = list(nx.neighbors(g, current))

        for neighbour in neighbours:
            a = g.get_edge_data(current, neighbour)
            
            if a['affinity'] == 'negative':
                continue
        
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                comp.add(neighbour)
                
    return frozenset(comp)

#metoda koja proverava balansiranost grafa, za svaku komponentu proverava
#da li sadrzi negativnu granu, ukoliko ima bar jednu, tada graf nije klasterabilan
#metoda daje i informaciju koje grane kvare klasterabilnost
def isClusterable(clusters, g):
    coalitions = list()
    antiCoalitions = list()
    negativeEdges = list()
    ret = list()
    br = 0
    for c in clusters:
        if len(c) > 2:
            n = [(u,v) for (u,v,d) in c.edges(data=True) if c[u][v]['affinity']['affinity'] == 'negative']
            
            if len(n) == 0:
                coalitions.append(c.nodes)
            else:
                antiCoalitions.append(c.nodes)
                negativeEdges.extend(n)
        else:
            coalitions.append(c.nodes)
    if len(antiCoalitions) > 0:
        print("Ovaj graf nije klasterabilan.")
        print("Postoji ",len(negativeEdges)," grana koje narusavaju klasterabilnost.")
        x = (input("Da li zelite da se prikazu? (y/n)"))
        if(x == 'y'):
            print("Treba ukloniti grane:")
            for edge in negativeEdges:
                print(edge)
            print("Prikazane su grane koje narusavaju klasterabilnost grafa (",len(negativeEdges),").")
    else:
        print("Ovaj graf je klasterabilan.")
    ret.append(coalitions)
    ret.append(antiCoalitions)
    return ret

#metoda koja kreira mrezu klastera od skupa klastera
def toNetworkClusters(clusters, g):
    print("Kreiranje mreze klastera...")
    clusterNetwork = nx.Graph()
    count = 1
    for cluster in clusters:
        cluster.graph['name'] = str(count)
        count = count + 1
        clusterNetwork.add_node(cluster)
        
    for cluster1 in clusters:
        for cluster2 in clusters:
            if cluster1 == cluster2:
                continue
            neighbour = False
        
            for node1 in cluster1:
                for node2 in cluster2:
                    if node1 in g.neighbors(node2):
                        neighbour = True
                if neighbour:
                    clusterNetwork.add_edge(cluster1, cluster2)
    nx.set_edge_attributes(clusterNetwork, "negative", "affinity")#cvorovi iz susednih klastera povezani su negativnim linkom
    print("Kreirana je mreza klastera.")
    return clusterNetwork

#metoda koja kreira skup grafova klastera
def makeClusterNetwork(clusters, g):
    setOfClusters = set()
    i = 0
    
    for cluster in clusters:
        graph = nx.Graph()
        for node in cluster:
            graph.add_node(node)#zbog provere suseda, prvo dodam cvor zbog izolovanih
            neighbours = list(nx.neighbors(g, node))
            for node2 in cluster:
                if node == node2:
                    continue
                if node2 in neighbours:
                    graph.add_edge(node, node2, affinity = g.get_edge_data(node, node2))
        setOfClusters.add(graph)
        i = i + 1
    print("Napravljeno je " + str(i) + " grafova klastera.")
    return setOfClusters


#metoda koja iz skupa klastera pronalazi odredjeni
def findGraph(clusterNet, cluster):
    for c in clusterNet:
        if c.nodes == cluster:
            return c