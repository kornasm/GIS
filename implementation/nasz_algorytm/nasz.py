from time import sleep
from igraph import *
from queue import Queue

import sys
sys.path.append('../')
from graph_functions import *

#inverse_indicies = None

edgesFilename = '../../data/sampleEdges'

class Nasz_algorytm:

    @staticmethod
    def read_graph(edgesFile):
        g = Graph_Reader.read_graph(edgesFile)
        g.vs["last_community_tried"] = 0
        g.vs["last_community_added"] = 0
        g.vs["still_in_graph"] = 1
        g.vs["comm_close_id"] = 0
        g.vs["comm_neighbors"] = 0
        g.vs["to_delete"] = 0 # 0 - still in graph, 1 - about to delete (all members in community are deleted at one time), 2 - deleted

        return g

    @staticmethod
    def vertex_should_join(g, vertex_idx, community_size):
        if community_size == 0:
            return True
        no_neigh = len(g.neighbors(vertex_idx))
        n = g.vs[vertex_idx]["comm_neighbors"] / no_neigh
        c = float(g.vs[vertex_idx]["comm_neighbors"]) / community_size

        val = ((n + c) / 2)
        #print('    should join    ' + str(vertex_idx) + '     ' + str(val) + '     ' + str(n) + '   ' + str(c))
        if val >= 0.5:
            return True
        else:
            return False


    @staticmethod
    def should_delete_calc_ratio(g, vertex_idx, comm_num):
        neighbors = g.neighbors(vertex_idx)
        outside_neighbors = 0
        community_neighbors = 0

        for neigh in neighbors:
            if g.vs[neigh]["last_community_added"] == comm_num:
                community_neighbors += 1
            else:
                outside_neighbors += 1

        ratio = float(outside_neighbors) / (community_neighbors + outside_neighbors)
        return ratio

    @staticmethod
    def should_delete_from_graph(g, vertex_idx, comm_num, avg):
        #print('Checking to delete   ' + str(vertex_idx))
        neighbors = g.neighbors(vertex_idx)
        #print(neighbors)
        outside_neighbors = 0
        community_neighbors = 0

        for neigh in neighbors:
            if g.vs[neigh]["last_community_added"] == comm_num:
                community_neighbors += 1
            else:
                outside_neighbors += 1

        ratio = float(outside_neighbors) / (community_neighbors + outside_neighbors)
        #print('         ratio   ' + str(ratio) + '     ' + str(avg))
        if ratio <= avg or ratio < 0.5 :
            g.vs[vertex_idx]["to_delete"] = 1
            #print('     to delete')
            return True
        else:
            #print('     not deleting')
            return False

    @staticmethod
    def add_vertex_to_community(g, comm_num, vertex_idx, communities_by_v, communities_by_c, community_size, queue):
        #print('ADD   ' + str(vertex_idx))
        if g.vs[vertex_idx]["last_community_added"] >= comm_num:
            return
        g.vs[vertex_idx]["last_community_added"] = comm_num
        g.vs[vertex_idx]["vertex_size"] = 25
        communities_by_v[vertex_idx].append(comm_num)
        communities_by_c[comm_num].append(vertex_idx)
        community_size += 1

        neighbors = g.neighbors(vertex_idx)

        for neigh in neighbors:
            #print('neighbors   ', end=' ')
            #print(neighbors)
            # continue if already in community
            if g.vs[neigh]["last_community_added"] == comm_num:
                g.vs[neigh]["comm_neighbors"] += 1
                continue
            if g.vs[neigh]["last_community_tried"] < comm_num:
                g.vs[neigh]["last_community_tried"] = comm_num
                g.vs[neigh]["comm_neighbors"] = 0

            g.vs[neigh]["comm_neighbors"] += 1

            if Nasz_algorytm.vertex_should_join(g, neigh, community_size):
                queue.put(neigh)

    @staticmethod
    def delete_vertex_from_graph(g, vertex_idx):
        edges = g.vs[vertex_idx].all_edges()
        edges = [edge.index for edge in edges]
        g.delete_edges(edges)
        g.vs[vertex_idx]["still_in_graph"] = 0

    @staticmethod
    def solve(g):
        
        communities_by_v = [[] for _ in range(len(g.vs))] # lista ze społecznościami, do których należy vierzchołek
        communities_by_c = [] # lista z wierzchołkami, które należą do danej społeczności
        communities_by_c.append([])

        vertices_left_in_graph = len(g.vs)
        no_vertices = len(g.vs)
        current_community_number = 0
        current_community_size = 0
        
        while vertices_left_in_graph > 0:
            #print('\n\nCOMMUNITY  ' + str(current_community_number))
            # zainicjowanie nowej społeczności
            communities_by_c.append([])
            current_community_number += 1
            current_community_size = 0
            queue = Queue()
            # wybieranie pierwszego kandydata
            starting_idx = -1
            min_edges_start = 1000000
            for vert in g.vs:
                if g.vs[vert.index]["still_in_graph"] == 1:
                    no_neigh = g.degree(vert.index)
                    #print('vertex  ' + g.vs[vert.index]["id"] + '  ' + str(no_neigh))
                    if no_neigh < min_edges_start:
                        min_edges_start = no_neigh
                        starting_idx = vert.index
            #print('community nr  ' + str(current_community_number) + '   started with vertex   ' + g.vs[starting_idx]["id"])
            
            #queue.put(starting_idx)
            Nasz_algorytm.add_vertex_to_community(g, current_community_number, starting_idx, communities_by_v, communities_by_c, current_community_size, queue)

            while queue.empty() == False:
                vertex_to_add = queue.get()
                #print('q front   ' + str(vertex_to_add))
                if Nasz_algorytm.vertex_should_join(g, vertex_to_add, current_community_size):
                    Nasz_algorytm.add_vertex_to_community(g, current_community_number, vertex_to_add, communities_by_v, communities_by_c, current_community_size, queue)
                    current_community_size += 1

                #visual_style["vertex_size"] = g.vs["vertex_size"]
                #plot(g, **visual_style)
                #sleep(1)

            #print('community created')
            #print(communities_by_c[current_community_number])
            sum = 0
            for member in communities_by_c[current_community_number]:
                sum += Nasz_algorytm.should_delete_calc_ratio(g, member, current_community_number)

            avg = sum / len(communities_by_c[current_community_number])
            for member in communities_by_c[current_community_number]:
                Nasz_algorytm.should_delete_from_graph(g, member, current_community_number, avg)

            for member in communities_by_c[current_community_number]:
                if g.vs[member]["to_delete"] == 1:
                    Nasz_algorytm.delete_vertex_from_graph(g, member)
                    vertices_left_in_graph -= 1
            
        communities_by_c.pop(0)
        return communities_by_c