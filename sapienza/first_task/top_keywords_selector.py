from sapienza.utility import measuraments as ms

'''
Method that select the top k keywords from each graph using a specific metric.
'''


def select_top_keywords_each_graph(graphs, k, metric="degree"):
    top_k = dict()
    for year, graph in graphs.items():
        if metric == "degree":
            top_k[year] = ms.selection_with_degree(graph, k)
        elif metric == "authority":
            iterations = 100
            top_k[year] = ms.selection_with_authority(graph, k, iterations)
        elif metric == "hubness":
            iterations = 100
            top_k[year] = ms.selection_with_hubness(graph, k, iterations)
        elif metric == "betweenness":
            top_k[year] = ms.selection_with_betweenness(graph, k)
        elif metric == "closeness":
            top_k[year] = ms.selection_with_closeness(graph, k)
        elif metric == "pagerank":
            top_k[year] = ms.selection_with_pagerank(graph, k)
    return top_k

