import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx
from sapienza.first_task import top_keywords_selector as topK
from sapienza.first_task import spread_of_influence_algorithm as lm
from sapienza.first_task import topics_merging as merge
from sapienza.second_task import topic_tracing as tracing
from sapienza.second_task import consecutive_year_tracing as consecutive_year_tracing
from sapienza.second_task import topic_final_list as final_merging

'''
method to plot and save all graphs
'''


def plot_all_graphs(map_graph, start_year, end_year, folder):
    for year in range(start_year, end_year):
        plt.title("Graph" + str(year), fontsize=15)
        nx.draw_random(map_graph[str(year)], with_labels=False, node_size=100, node_color=[(0.73, 0.09, 0.19)],
                       node_cmap=cm.get_cmap("viridis"), edge_cmap=cm.get_cmap("binary"))
        plt.savefig(folder + "Graph" + str(year) + ".png", format="PNG")
        plt.show()


'''
method to plot edge weights of a particular graph
'''


def plot_edge_weights(g):
    m = g.number_of_edges()
    n = g.number_of_nodes()

    def nsum(ui):
        w = 0
        for vi in g[ui]:
            w += g[vi][ui]["weight"]
        return w

    weights = [w for u, v, w in g.edges.data("weight")]
    weights.sort()

    neighboursums = [nsum(ui) for ui in g.nodes]
    neighboursums.sort()

    plt.subplot(1, 2, 1)
    plt.scatter(range(m), weights, s=1.5 * 1.5, color=[(0.73, 0.09, 0.19)])
    plt.xlabel("edges")
    plt.ylabel("weight")
    plt.title("Edge Weights")

    plt.subplot(1, 2, 2)
    plt.xlabel("nodes")
    plt.ylabel("in-neighbor sum")
    plt.title("Weighted In-neighbors Sums")
    plt.scatter(range(n), neighboursums, s=1.5 * 1.5, color=[(0.73, 0.09, 0.19)])
    plt.tight_layout()
    plt.show()


'''
method to plot graph comparison
'''


def graph_comparison(first_graph, second_graph):
    edge_color = {(ui, vi): -1 for ui, vi in first_graph.edges()}
    for ui, vi in second_graph.edges():
        if (ui, vi) in edge_color:
            edge_color[(ui, vi)] = 0
        else:
            edge_color[(ui, vi)] = 1
    graph = nx.Graph(first_graph)
    graph.add_edges_from(second_graph.edges())
    nx.set_edge_attributes(graph, edge_color, "color")
    edge_color = [c for ui, vi, c in graph.edges(data="color")]
    nx.draw_networkx(
        graph,
        arrows=False,
        node_size=40,
        edge_color=edge_color,
        edge_cmap=cm.get_cmap("tab10"),
        linewidths=0,
        width=0.25,
        with_labels=False)
    plt.show()


'''
method to plot most popular keywords
'''


def plot_popular_keyword(popular_keywords):
    plt.barh(range(len(popular_keywords)), list(popular_keywords.values()), color=[(0.73, 0.09, 0.19)])
    plt.yticks(range(len(popular_keywords)), list(popular_keywords.keys()), fontsize=7)
    plt.xticks(fontsize=15)
    plt.title("Top-10 keywords", fontsize=15)
    plt.xlabel("number appearances", fontsize=15)
    plt.rcParams["figure.figsize"] = (8, 6)
    plt.plot()
    plt.show()


'''
method to plot most popular topics
'''


def plot_popular_topics(popular_topics):
    plt.barh(range(len(popular_topics)), list(popular_topics.values()), color=[(0.73, 0.09, 0.19)])
    plt.yticks(range(len(popular_topics)), list(popular_topics.keys()), fontsize=7)
    plt.xticks(fontsize=15)
    plt.title("Top-10 topics", fontsize=15)
    plt.xlabel("number appearances", fontsize=15)
    plt.rcParams["figure.figsize"] = (8, 6)
    plt.plot()
    plt.show()


'''
method to print top-k keywords over the year
'''


def print_topk_over_the_year(map_graph, k):
    top_k = topK.select_top_keywords_each_graph(map_graph, k, metric="degree", iterations=10000)
    for year, keywords in top_k.items():
        print("Top " + str(k) + " keywords of " + year + " are: ", keywords)
    return top_k


'''
method to print results of Spread of Influence algorithm
'''


def print_topics_for_a_year(year, map_graph, top_k):
    print("Spread of Influence Algorithm for " + year + ": ")
    result = lm.calculate_topics_spreading_algorithm(map_graph[year], top_k[year])
    for k, v in result.items():
        print("Keyword: " + k)
        print("Influenced elements:\n", v)
        print()
    return result


'''
 All these methods are necessary to visualize the results.
'''


def print_topics_join_for_a_year(year, topics, threshold):
    print("Produced topic join for " + year + ": ")
    result = merge.merge_for_year(topics, threshold)
    for k, v in result.items():
        print("Keyword: " + k)
        print("Influenced elements:\n", v)
        print()


def print_all_topics(map_graph, top_k):
    result = merge.generate_all_topics(map_graph, top_k)
    for k in result.keys():
        print("year: " + k)
        for key, value in result.items():
            print(value)
            print()
    return result


def print_popular_keywords_over_the_year(topics):
    most_popular_keywords = tracing.keyword_that_appears_more_times(topics)
    most_popular_keywords = dict(sorted(most_popular_keywords.items(), key=lambda x: x[1], reverse=True)[:10])
    print(most_popular_keywords)
    return most_popular_keywords


def print_topic_trace_over_the_year(topics, start_year, end_year):
    result = tracing.trace_all_topics_time_interval(topics, start_year, end_year)
    print(result)
    return result


def print_keywords_for_specific_topic(topic_name, topics):
    print("Specific topic: " + topic_name)
    for y, t in topics[topic_name].items():
        print("In year " + y + " : " + str(len(t)) + " keywords")


def print_popular_topics_over_the_year(topics):
    result = tracing.number_topic_appears(topics)
    result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:10])
    print(result)
    return result


def print_similar_topics_consecutive_years(topics):
    result = consecutive_year_tracing.find_similar_topics_consecutive_years(topics)
    print("second task part two with similarity measure : similar topic consecutive year\n")
    for el in result:
        years, key1, key2, first_set, second_set, similarity = el
        print(years + " --> " + key1 + " <--> " + key2)
        print("first set: ", first_set)
        print("second set: ", second_set)
        print("Overlap similarity: ", similarity)
        print()
    return result


def print_similar_topics_subgraph_consecutive_years(topics, map_graph):
    result = consecutive_year_tracing.find_similar_topics_node_intersection(topics, map_graph)
    print("second task part two with subgraphs : similar topic consecutive year\n")
    for el in result:
        years, key1, key2, first_set, second_set, similarity = el
        print(years + " --> " + key1 + " <--> " + key2)
        print("first set: ", first_set)
        print("second set: ", second_set)
        print("edge subgraphs similarity: ", similarity)
        print()
    return result


def save_on_file_merged_list(similar_topics, folder):
    result = final_merging.produce_merge_list_similar_topics_consecutive_year(similar_topics)
    final_merging.write_file_final_result("result_overlapping_similarity", similar_topics, result,
                                          "overlapping similarity", folder)


def save_on_file_merged_subgraphs_list(similar_topics_subgraphs, folder):
    result = final_merging.produce_merge_list_similar_topics_consecutive_year(similar_topics_subgraphs)
    final_merging.write_file_final_result("result_subgraphs_edges_similarity", similar_topics_subgraphs, result,
                                          "edges subgraphs overlapping similarity", folder)
