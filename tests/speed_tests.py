import time
import sys

sys.path.append('../implementation/')
from graph_functions import *
sys.path.append('../implementation/nasz_algorytm/')
from nasz import *
sys.path.append('../implementation/ext_lpa/')
from lpa2 import *
sys.path.append('../implementation/lpa/')
from lpa import *

def GenerateFootballGraph(teams, players_per_team, min_stayed, transfer_windows):

    #Generate team_labels
    team_labels = []
    for i in range(0,teams):
        lst = [*range(i*players_per_team, (i+1)*players_per_team)]
        team_labels.append(lst)

    #Generate graph
    test_graph = Graph()
    test_graph.add_vertices(teams*players_per_team)
    for t in range(0,teams):
        for i in range(0,players_per_team):
            for j in range(i,players_per_team-1):
                test_graph.add_edges([(i + t * players_per_team ,j+ 1 + t * players_per_team)])


    #Make transfers
    for times in range(0,transfer_windows):
        for i in range(0,teams-1):
            players_chosen = int((len(team_labels[i]) - min_stayed) / 2)
            for j in range(0,players_chosen):
                player_to_transfer = (team_labels[i][random.randint(0, len(team_labels[i]) - 1)])
                team_labels[i].remove(player_to_transfer)
                new_team = random.randint(0,teams-1)
                if new_team == i:
                    new_team += 1
                    new_team %= teams
                team_labels[new_team].append(player_to_transfer)
                for k in team_labels[new_team]:
                    test_graph.add_edges([(player_to_transfer,k)])
    Graph.simplify(test_graph)
    return test_graph

def test_alg(edge_filename):
    g = Nasz_algorytm.read_graph(edge_filename)
    no_edges = len(g.es)
    start = time.time()
    communities_list= Nasz_algorytm.solve(g)
    executionTime = time.time() - start
    print(edge_filename)
    print(str(len(g.vs)) + '   ' + str(no_edges) + '    ' + str(executionTime))
    print('no comm   ' + str(len(communities_list)))
    summ = 0
    for comm in communities_list:
        summ += len(comm)
    print(summ)


def test_lpa_from_file(edge_filename):
    g = Graph_Reader.read_graph(edge_filename)
    no_edges = len(g.es)
    start = time.time()
    result = lpa_overlapping(g, 20, 100)
    executionTime = time.time() - start
    print(edge_filename)
    print(str(len(g.vs)) + '   ' + str(no_edges) + '    ' + str(executionTime))
    print()

def test_lpa_from_graph(g):
    no_edges = len(g.es)
    start = time.time()
    result = lpa_overlapping(g, 100, 100)
    executionTime = time.time() - start
    print(str(len(g.vs)) + '   ' + str(no_edges) + '    ' + str(executionTime))
    print()

# uncomment leagues to be tested
graphs = []
#graphs.append('EkstraklasaEdges.csv')
#graphs.append('CountedSerie-A-StatsEdges.csv')
#graphs.append('CountedBundesliga-StatsEdges.csv')
#graphs.append('CountedSwiss-Super-League-StatsEdges.csv')
#graphs.append('CountedPremier-League-StatsEdges.csv')


# uncomment algorithm to be tested
for graph in graphs:
    graph = '../data/' + graph

    # our algorithm
    #test_alg(graph)

    # lpa (corpa) algorithm
    #test_lpa_from_file(graph)


artificial_graph = GenerateFootballGraph(20, 30, 28, 15)
test_lpa_from_graph(artificial_graph)
