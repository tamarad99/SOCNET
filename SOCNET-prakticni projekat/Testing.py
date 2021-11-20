import networkx as nx
from networkx.algorithms import cluster
from networkx.classes import graph
from networkx.classes.function import neighbors
from networkx.linalg.attrmatrix import _edge_value
import Loading as l
import Clustering as c
import Analiza as a

g = l.loadGraph()
components = c.identifyComponents(g)
clusterNet = c.makeClusterNetwork(components, g)
coalitionsAndAnti = c.isClusterable(clusterNet, g)
br = nx.number_connected_components(g)
print("Broj povezanih komponenti: ",br)
print("Postoji ",len(coalitionsAndAnti[0]), " koalicija i ",len(coalitionsAndAnti[1])," antikoalicija.")

x = input("Da li zelite da se prikazu koalicije i antikoalicije? (y/n)")

if(x == 'y'):
   print("Koalicije i antikoalicije:")
   if(len(coalitionsAndAnti[0]) > 0):
      print("Koalicije:")
      for coalition in coalitionsAndAnti[0]:
         print(coalition)
   if(len(coalitionsAndAnti[1]) > 0):
      print("Antikoalicije:")
      for anti in coalitionsAndAnti[1]:
         print(anti)

net = c.toNetworkClusters(clusterNet, g)
print("Analiza mreze klastera: ")
print("Broj cvorova: ",net.number_of_nodes())
print("Broj grana: ",net.number_of_edges())
density = a.density(net)
print("Gustina mreze klastera: ",density)
br = nx.number_connected_components(net)
print("Broj povezanih komponenti: ",br)
if br == 1:
   diam = a.diameterOfNet(net)
   print("Dijametar: ",diam)
else:
   print("Nije moguce izracunati dijametar zbog postojanja vise komponenti povezanosti.")

avdeg = a.averageDegree(net)
print("Prosecan stepen: ",avdeg)

y = input("Da li zelite analizu koalicija i antikoalicija? (y/n)")

if(y == 'y'):

   score = [[] for i in range(4)]
   score2 = [[] for i in range(4)]

   for coalition in coalitionsAndAnti[0]:
      graphCoalition = c.findGraph(clusterNet, coalition)
      rez = a.clusterAnalyse(graphCoalition, score)

   for anticoalition in coalitionsAndAnti[1]:
      graphAnti = c.findGraph(clusterNet, anticoalition)
      rez2 = a.clusterAnalyse(graphAnti, score2)

   if sum(rez[0])/len(rez[0]) > sum(rez2[0])/len(rez2[0]):
      print("Koalicije su kohezivnije od antikoalicija.")
   elif sum(rez[0])/len(rez[0]) < sum(rez2[0])/len(rez2[0]):
      print("Antikoalicije su kohezivnije od koalicija.")
   else:
      print("Kohezivnost koalicija i antikoalicija je jednaka.")

   if sum(rez[2])/len(rez[2]) > sum(rez2[2])/len(rez2[2]):
      print("Koalicije imaju veci prosecni dijametar.")
   elif sum(rez[2])/len(rez[2]) < sum(rez2[2])/len(rez2[2]):
      print("Antikoalicije imaju veci prosecni dijametar.")
   else:
      print("Koalicije i antikoalicije imaju jednak prosecni dijametar.")

   if sum(rez[3])/len(rez[3]) > sum(rez2[3])/len(rez2[3]):
      print("Antikoalicije su redje od koalicija.")
   elif sum(rez[3])/len(rez[3]) < sum(rez2[3])/len(rez2[3]):
      print("Koalicije su redje od antikoalicija.")
   else:
      print("Gustina koalicija i antikoalicija je jednaka.")