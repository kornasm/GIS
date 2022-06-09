from time import sleep
from typing import Counter
from igraph import *
import igraph as ig
import csv
import random
import sys
sys.path.append("../")
from graph_functions import *

# read and create graph

inverse_indicies = None

# playersFilename jest w zasadzie niepotrzebne. Tylko do wyświetlenia nazwisk piłkarzy (a i tak tego nie zaimplementowałem)
playersFilename = "../../data/Players.csv"
edgesFilename = "../../scrapers/2019-2020-Ekstraklasa-StatsEdges.csv"

playersFilename = "../../data/samplePlayers"
edgesFilename = "../../data/sampleEdges"
edgesFilename = "genedges"


class Lpa:

    @staticmethod
    def read_graph(edges_file):
        g = Graph_Reader.read_graph(edges_file)
        g.vs["lpalabel"] = list(zip(range(len(g.vs)), g.vs["vertex_color"]))
        g.vs["newlpalabel"] = 0
        g.vs["vertex_color"]
        return g

    @staticmethod
    def solve(g):
        changed = True
        max_iter = 20
        neigh_labels = [None] * len(g.vs)

        #print("\n\nLPA\n")

        iter = 0

        g.vs["vertex_color"] = g.vs["lpalabel"][1]
        g.vs["label"] = g.vs["lpalabel"]

        while changed == True and iter < max_iter:
            iter = iter + 1
            a = 1
            #print("loop")
            changedthisiteration = False
            for vert in g.vs:

                neighbours = g.neighbors(vert)

                if(len(neighbours) > 0):

                    vertidx = vert.index
                    neigh_labels[vertidx] = []

                    for neigh in neighbours:
                        neigh_labels[vertidx].append(g.vs[neigh]["lpalabel"])

                    counted = Counter(neigh_labels[vertidx])
                    newlabel = counted.most_common()

                    #g.vs[vertidx]["vertex_size"] = 30
                    if g.vs[vertidx]["lpalabel"] != newlabel[0][0]:

                        g.vs[vertidx]["newlpalabel"] = newlabel[0][0]
                        #g.vs[vertidx]["vertex_size"] = 60
                        changedthisiteration = True

            changed = changedthisiteration

            g.vs["lpalabel"] = g.vs["newlpalabel"]
            for vert in g.vs:
                vertidx = vert.index
                g.vs[vertidx]["vertex_color"] = g.vs[vertidx]["lpalabel"][1]
                g.vs[vertidx]["label"] = (g.vs[vertidx]["id"], g.vs[vertidx]["lpalabel"][0])

        # stworzenie listy spolecznosci
        done_communities = []
        communities_list = []
        for i in range(len(g.vs)):
            print(str(i) + '   ' + str(g.vs[i]["lpalabel"]))
            community = g.vs[i]["lpalabel"]
            if not community in done_communities:
                done_communities.append(community)
                communities_list.append([])
                for j in range(i, len(g.vs)):
                    if g.vs[j]["lpalabel"] == community:
                        communities_list[-1].append(j)
        
        return communities_list