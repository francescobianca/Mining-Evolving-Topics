import copy
import networkx as nx
from sapienza.utility import measuraments as ms

'''
calculate the similar topics in two consecutive years using similarity metrics.
'''


def find_similar_topics_consecutive_years(topics):
    years = list(topics.keys())
    result = list()
    for y in range(len(years) - 1):
        for first_keyword, first_set in topics[years[y]].items():
            max_similarity = 0
            for second_keyword, second_set in topics[years[y + 1]].items():
                sim = ms.overlap_similarity(first_set, second_set)
                if sim >= max_similarity:
                    max_similarity = sim
                    selected_keyword = second_keyword
                    selected_set = second_set
            if max_similarity != 0:
                informations = (
                    years[y] + "-" + years[y + 1], first_keyword, selected_keyword, first_set, selected_set,
                    max_similarity)
                result.append(informations)
    return result


'''
calculate the similar topics in two consecutive years using subgraphs.
'''


def find_similar_topics_node_intersection(topics, graphs):
    years = list(topics.keys())
    result = list()
    for y in range(len(years) - 1):
        for first_keyword, first_set in topics[years[y]].items():
            max_similarity = 0
            for second_keyword, second_set in topics[years[y + 1]].items():
                common = first_set.intersection(second_set)
                if len(common) > 1:
                    first_subgraph = nx.subgraph(graphs[years[y]], common)
                    second_subgraph = nx.subgraph(graphs[years[y + 1]], common)
                    edges_g1 = set(first_subgraph.edges)
                    edges_g2 = set(second_subgraph.edges)
                    if len(edges_g1) != 0 and len(edges_g2) != 0:
                        sim = ms.overlap_similarity(edges_g1, edges_g2)
                        if sim >= max_similarity:
                            max_similarity = sim
                            selected_keyword = second_keyword
                            selected_set = second_set
            if max_similarity != 0:
                informations = (
                    years[y] + "-" + years[y + 1], first_keyword, selected_keyword, first_set, selected_set,
                    max_similarity)
                result.append(informations)
    return result


'''
Method that creates the subgraph with topics for each year.
'''


def create_topics_subgraphs(graphs, all_topics):
    result = dict()
    years = list(all_topics.keys())
    for y in years:
        subgraphs = dict()
        for k, v in all_topics[y].items():
            subgraphs[k] = graphs[y].subgraph(list(v))
        result[y] = copy.deepcopy(subgraphs)
    return result
