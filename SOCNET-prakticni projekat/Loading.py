import networkx as nx
from networkx.algorithms import cluster
from networkx.classes.function import neighbors 
import random as rand

def loadGraph():
    graph = nx.DiGraph()
    numbers = [1, 2, 3, 4, 5, 6, 7]

    print("Izaberite graf koji zelite da ucitate: \n"
    "1 -> Epinions \n"
    "2 -> Slashdot \n"
    "3 -> Wiki \n"
    "4 -> Klasterabilan(test) \n"
    "5 -> Neklasterabilan(test) \n"
    "6 -> Random generisan graf\n"
    "7 -> Bitcoinalfa\n")

    num = int(input("Unesite jednu od ponuđenih mogućnosti: "))
    print("\n")

    if num in numbers:
        if num == 1:
            print("---------Analiza mreze Epinions---------\n")
            graph = loadEpinions()
        if num == 2:
            print("---------Analiza mreze Slashdot---------\n")
            graph = loadSlashdot()
        if num == 3:
            print("---------Analiza mreze Wikipedia---------\n")
            graph = loadWiki()
        if num == 4:
            print("---------Analiza klasterabilne mreze---------\n")
            graph = ucitajKlasterabilan()
        if num == 5:
            print("---------Analiza neklasterabilne mreze---------\n")
            graph = loadNeklasterabilan()
        if num == 6:
            print("---------Analiza random nastale mreze---------\n")
            graph = randomGraph1(10000, 0, 1000, 0.5)
        if num == 7:
            print("---------Analiza mreze Bitcoin---------\n")
            graph = loadBitcoin()
    else:
        print("Niste uneli odgovarajuci broj. Unesite ponovo: ")
        loadGraph()
    return graph      


def ucitajKlasterabilan():
    filePath = "klasterabilan.txt"
    g1 = nx.DiGraph()
    f = open(filePath, "r")
    numNode = int(f.readline().strip().split(":")[1].strip().split()[0].strip())
    g1.add_nodes_from(range(numNode))
    f.readline()
    for line in f:
        nodeA = int(line.split("\t")[0].strip())
        nodeB = int(line.split("\t")[1].strip())
        aff = (line.split("\t")[2].strip())
        if aff == "1":
            aff = "positive"
        else:
            aff = "negative"
        g1.add_edge(nodeA, nodeB, affinity=aff)
        br = g1.number_of_nodes()
    grana = g1.number_of_edges()
    print("Graf ima ",br," cvorova.")
    print("Graf ima ",grana," grana")
    f.close()
    return transformFromDirToUndir(g1)

def loadWiki():
    fajl="wiki-RfA.txt"
    g1 = nx.DiGraph()
    with open(fajl, "r", encoding="utf8") as file:
        for line in file:
            if line.startswith("SRC"):
                source = line.split(":")[1].strip()
            elif line.startswith("TGT"):
                target = line.split(":")[1].strip()
            elif line.startswith("RES"):
                res = line.split(":")[1].strip()
                if res == "-1":
                    affinity = "negative"
                else:
                    affinity = "positive"
                g1.add_edge(source, target, affinity = affinity)
    br = g1.number_of_nodes()
    grana = g1.number_of_edges()
    print("Broj cvorova u grafu: ",br)
    print("Broj grana u grafu: ",grana)
    return transformFromDirToUndir(g1)

def loadNeklasterabilan():
    fajl = "neklas.txt"
    g1 = nx.DiGraph()
    with open(fajl, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue
            red = line.split("\t")
            affinity = None
            if "-1" in red[2]:
                affinity = "negative"
            else:
                affinity = "positive"
            g1.add_edge(red[0].strip(), red[1].strip(), affinity = affinity)
    br = g1.number_of_nodes()
    grana = g1.number_of_edges()
    print("Broj cvorova u grafu: ",br)
    print("Broj grana u grafu: ",grana)
    return transformFromDirToUndir(g1)

def loadSlashdot():
    fajl = "soc-sign-slashdot.txt"
    g1 = nx.DiGraph()
    with open(fajl, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue
            red = line.split("\t")
            affinity = None
            if "-1" in red[2]:
                affinity = "negative"
            else:
                affinity = "positive"
            g1.add_edge(red[0].strip(), red[1].strip(), affinity = affinity)
    br = g1.number_of_nodes()
    grana = g1.number_of_edges()
    print("Broj cvorova u grafu: ",br)
    print("Broj grana u grafu: ",grana)
    return transformFromDirToUndir(g1)

def loadEpinions():
    fajl = "soc-sign-epinions.txt"
    g1 = nx.DiGraph()
    with open(fajl, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue
            red = line.split("\t")
            affinity = None
            if "-1" in red[2]:
                affinity = "negative"
            else:
                affinity = "positive"
            g1.add_edge(red[0].strip(), red[1].strip(), affinity = affinity)
    br = g1.number_of_nodes()
    grana = g1.number_of_edges()
    print("Broj cvorova u grafu: ",br)
    print("Broj grana u grafu: ",grana)
    return transformFromDirToUndir(g1)

def loadBitcoin():
    import csv
    fajl = "soc-sign-bitcoinalpha.csv"
    g1 = nx.DiGraph()

    with open(fajl, "r") as file:
        reader = csv.reader(file)
        for line in reader:
            if int(line[2]) > 0:
                aff = "positive"
            else:
                aff = "negative"
            g1.add_edge(line[0], line[1], affinity = aff)
    br = g1.number_of_nodes()
    grana = g1.number_of_edges()
    print("Broj cvorova u grafu: ",br)
    print("Broj grana u grafu: ",grana)
    return transformFromDirToUndir(g1)

    

def transformFromDirToUndir(g1):
    undir = nx.Graph()
    undir.add_edges_from(g1.edges(), affinity="")
    for u, v, d in g1.edges(data=True):
        af1 = g1[u][v]['affinity']
        af2 = ""
        if(v, u) in g1.edges:
            af2 = g1[v][u]['affinity']
        if af1 == "negative" or af2 == "negative":
            undir[u][v]['affinity'] = "negative"
        else:
            undir[u][v]['affinity'] = "positive"
    return undir

def randomGraph1(numNodes, clusterable, numClasters, p):
    graph = nx.Graph()
    graph.add_nodes_from(range(numNodes))

    if clusterable == 1:
        for n in range(numNodes):
            klaster = rand.randint(0, numClasters)
            graph.nodes[n]['c'] = klaster #dodela oznake klastera cvorovima
        
        for i in graph.nodes:
            for j in graph.nodes:
                if graph.nodes[i]['c'] == graph.nodes[j]['c']: #ukoliko se cvorovi nalaze u istom klasteru povezani su pozitivnom granom
                    lista = list(nx.neighbors(graph, i))
                    if len(lista) < 50:
                        affinity = "positive"
                        graph.add_edge(i, j, affinity = 'positive')
                else:
                    x = rand.randint(0, 1)
                    if p > x:
                        lista = list(nx.neighbors(graph, i))
                        if len(lista) < 5:
                            affinity = "negative"
                            graph.add_edge(i, j, affinity = 'negative')

    else:
        for n in range(numNodes):
            klaster = rand.randint(0, numClasters) #oznaka klastera
            graph.nodes[n]['c'] = klaster #dodela oznake covrovima

        for i in graph.nodes:
            for j in graph.nodes:
                x = rand.randint(0, 1)
                
                if graph.nodes[i]['c'] == graph.nodes[j]['c']:
                    if p > x:
                        graph.add_edge(i, j, affinity = 'positive')
                    else:
                        graph.add_edge(i, j, affinity = 'negative')
                else:
                    lista = list(nx.neighbors(graph, i))
                    if len(lista) < 5:
                        affinity = "negative"
                        graph.add_edge(i, j, affinity = 'negative')
    print("Graf je ucitan.")
    br = graph.number_of_nodes()
    grana = graph.number_of_edges()
    print("Broj cvorova u grafu: ",br)
    print("Broj grana u grafu: ",grana)
    return graph