import numpy
def lpa_overlapping(graph, max_communities, max_iterations, init_graph = True):
    print("Basic lpa with overlapping communities, begin...")
    vertices_count = len(graph.vs)
    counters = [0] * vertices_count
    
    
    if init_graph == True:
        i = 0
        for v in graph.vs:
            v["communities"] = [(i, 1)]
            i += 1
            
    
    convergence = False
    iteration = 0
    while convergence == False and iteration < max_iterations:
        iteration += 1
        convergence = True
        
        for idx in range(vertices_count):
            counters[idx] = 0
            
        for v in graph.vs:
            for com, weight in v["communities"]:
                counters[com] += weight
            
        unique = sum(1 if counter > 0 else 0 for counter in counters)
        print("Iteration " + str(iteration) + ",communities " + str(unique))

        for v in graph.vs:
            current_communities = v["communities"]   
            
            #clear counters
            for idx in range(vertices_count):
                counters[idx] = 0
            
            for e in v.all_edges():     
                if v == e.target_vertex and v == e.source_vertex:
                    print("Warn - out vertex equals current vertex")
                elif v != e.target_vertex:
                    for com, weight in e.target_vertex["communities"]:
                        counters[com] += weight
                elif v != e.source_vertex:
                    for com, weight in e.target_vertex["communities"]:
                        counters[com] += weight
                
            max_value = max(counters)
            sorted_counters = numpy.argsort(counters)[::-1]
            new_communities = []
            
            idx = 0
            
            if max_value == 0:
                continue
                
            normalize_factor = sum(counters)
            while counters[sorted_counters[idx]] / normalize_factor >= 1 / max_communities:
                new_communities.append((sorted_counters[idx], counters[sorted_counters[idx]] / max_value))
                idx += 1
            
            if idx == 0:
                new_communities = current_communities
               
            if len(list(set(new_communities) - set(current_communities))) > 0:
                convergence = False
                
            weight_sum = sum(w for com, w in new_communities)
            for i in range(len(new_communities)):
                new_communities[i] = (new_communities[i][0], new_communities[i][1] / weight_sum)
                
            v["communities"] = new_communities
            
    
    for v in graph.vs:
        normalized = []
        for com, _ in v["communities"]:
            normalized.append(com)
        v["communities"] = normalized