import networkx as nx
import random
import copy

'''
Method that modifies the Spread of Influence Algorithm(Linear Threshold Model).
modification of the algorithm presented in the course slides
'''


def calculate_topics_spreading_algorithm(graph, keywords):
    if not graph.is_directed():
        graph = graph.to_directed()

    for n in nx.nodes(graph):
        r = random.random() # random threshold ad ogni nodo.
        graph.nodes[n]['threshold'] = r

    # topics is the dictionary of infected
    topics = {}
    for n in keywords:
        topics[n] = set()
        topics[n].add(n)
    active = copy.deepcopy(keywords)
    # until convergence condition is met
    while True:
        # reset the currently added nodes
        added = []

        for n in nx.nodes(graph):
            # check only inactive nodes
            if n not in active:
                # initialize dictionary of influence
                influence = dict()
                for k in topics.keys():
                    influence[k] = 0
                # check all incoming edges
                for edge in graph.in_edges(n, data=True):
                    # if the edge comes from an active node
                    for k, s in topics.items():
                        if edge[0] in s:

                            # add edge weight to influence
                            influence[k] += float(edge[2]['weight'])

                            # if active weights reach threshold
                            if influence[k] >= graph.nodes[n]['threshold']:
                                # add node to active nodes
                                active.append(n)
                                topics[k].add(n)
                                # add node to the list of newly
                                # added nodes
                                added.append(n)

        # if there are no newly added nodes
        # then we have reached the convergence
        # condition;
        # otherwise trace the added nodes in
        # the current wave
        if len(added) == 0:
            break

    return topics
