from igraph import *
import csv
import random


class Graph_Reader:
    def delete_comments(csvfile):
            for row in csvfile:
                raw = row.split('#')[0].strip()
                if raw:
                    yield raw

    def read_graph(edges_file):
        print('reading from file')
        #players = []
        edges = []
        with open(edges_file , 'r') as csvfile:
            csvreader = csv.reader(Graph_Reader.delete_comments(csvfile), delimiter=',')
            edges = list(csvreader)
        print('edges setup')
        edgevertices = list([edge[0] for edge in edges] + [edge[1] for edge in edges])
        edgevertices = list(dict.fromkeys(edgevertices))
        print('vertices')
        #vertices = list([player for player in players if player[0] in edgevertices])
        print('inverse_indicies')
        inverse_indicies = dict(zip(edgevertices, range(len(edgevertices))))
        g = Graph()
        g.add_vertices(len(edgevertices))
        print('no vertices   ' + str(len(edgevertices)))
        g.vs["id"] = [vertex for vertex in edgevertices]
        g.vs["label"] = g.vs["id"]
        g.vs["label"] = list(zip(list(range(len(g.vs))), g.vs["id"]))
        g.vs["vertex_size"] = 8
        #g.vs["comm_label"] = []
        
        
        
        print("setting colors")
        for vert in g.vs:
            vert["vertex_color"] = f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})'
        
        print("creating indicies")
        edges = [(inverse_indicies[edge[0]], inverse_indicies[edge[1]]) for edge in edges]
        print('adding edges')
        try:
            g.add_edges(edges)
        except:
            print("Error occured during graph creating")
            quit()
        Graph.simplify(g)
        #g.es["weigth"] = 1
        print("graph created")
        return g

    def set_visual_style(g):
        visual_style = {}
        visual_style["vertex_size"] = g.vs["vertex_size"]
        visual_style["layout"] = g.layout("kamada_kawai")
        #visual_style["layout"] = g.layout("lgl")
        visual_style["layout"] = g.layout("drl")
        visual_style["vertex_color"] = g.vs["vertex_color"]
        if len(g.vs) > 30:
            visual_style["bbox"] = (1000, 1000)
        else:
            visual_style["bbox"] = (800, 800)
        return visual_style