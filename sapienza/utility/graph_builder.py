# library to build graphs
import networkx as nx
import os

DATASET_LOC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Datasets/")
OUTPUT_FOLDER_DS1 = "../../ProjectResults/output_ds-1/years_ds1/"
OUTPUT_FOLDER_DS2 = "../../ProjectResults/output_ds-2/years_ds2/"


def nodes_and_edges_first_dataset(file):
    def edges_first_dataset(edge):
        map_edge = dict()
        edge = edge[1:len(edge) - 1].replace(" ", "")
        # Ho entry del tipo: {'d6b6b02e3e9df8e04318548379caabf0497e48c7': 2, '5ab82c9447c47562726b1796f4a442fce611bb82': 2, ...
        s = edge.split(",")  # Splitto per virgola per distinguere gli autori
        for entry in s:
            splitted_entry = entry.split(
                ":")  # Splitto ancora per i : per vedere autore e numero di volte in cui utilizza keywords
            splitted_entry[0] = splitted_entry[0][1:len(splitted_entry[0]) - 1]  # Tolgo le ' '
            map_edge[splitted_entry[0]] = int(splitted_entry[1])
        return map_edge

    nodes = set()
    edges = list()
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip().split('\t')
            if s[0] not in nodes:
                nodes.add(s[0])
            if s[1] not in nodes:
                nodes.add(s[1])
            edges.append((s[0], s[1], edges_first_dataset(
                s[2])))  # Per ogni arco mi salvo un dizionario. Andrò successivamente a definire il peso.
        f.close()
    return nodes, edges


def nodes_and_edges_second_dataset(file):
    nodes = set()
    edges = list()
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip().split('\t')
            if (s[0] not in nodes):
                nodes.add(s[0])
            if (s[1] not in nodes):
                nodes.add(s[1])
            edges.append((s[0], s[1], int(s[2])))  # In questo caso il peso è solamente le collaborazioni
        f.close()
    return nodes, edges


def total_collaborations(file_ds2):
    result = dict()

    def collaborations(file_ds2):
        dictionary_years_authors = dict()
        # calculate pubblications of each author for a specific year
        with open(file_ds2, 'r', encoding='utf-8') as f:
            for line in f:
                s = line.strip().split('\t')
                if 2018 >= int(s[0]) >= 2000:
                    if s[0] not in dictionary_years_authors.keys():
                        dictionary_years_authors[s[0]] = dict()
                    dict_authors = dictionary_years_authors[s[0]]
                    dict_authors[s[1]] = 1 if s[1] not in dict_authors.keys() else dict_authors[
                                                                                       s[1]] + int(
                        s[3])
                    dict_authors[s[2]] = 1 if s[2] not in dict_authors.keys() else dict_authors[
                                                                                       s[2]] + int(
                        s[3])
                    dictionary_years_authors[s[0]] = dict_authors
        f.close()
        return dictionary_years_authors

    authors_collaborations = collaborations(file_ds2)
    years = [x for x in sorted(list(authors_collaborations.keys()))]
    result[years[0]] = authors_collaborations[years[0]]
    for y in range(1, len(years)):
        current = authors_collaborations[years[y]]
        previous = result[years[y - 1]]
        summed_dict = {k: current.get(k, 0) + previous.get(k, 0) for k in current.keys() | previous.keys()}
        result[years[y]] = summed_dict
    return result


def create_weighted_graph_first_dataset(list_of_edges, authors):
    G = nx.Graph()
    for elem in list_of_edges:
        weight = 0
        arg1, arg2, d = elem
        for aut, n in d.items():
            weight += n * (authors[aut] if aut in authors.keys() else 1)
        G.add_edge(arg1, arg2, weight=weight)
    return G


def create_weighted_graph_second_dataset(list_of_edges):
    graph = nx.Graph()
    for elem in list_of_edges:
        arg1, arg2, collaborations = elem
        graph.add_edge(arg1, arg2, weight=collaborations)
    return graph


def graphs_first_dataset(dataset_loc, folder_ds1):
    result = dict()
    tot_pub = total_collaborations(dataset_loc + "ds-2.tsv")  # Utilizzo ds-2 per creare i pesi degli archi
    for year in range(2000, 2019):
        nodes_ds1, edges_ds1 = nodes_and_edges_first_dataset(folder_ds1 + str(year) + "_ds1.tsv")
        authors = tot_pub[str(year)]
        # creazione grafo pesato
        graph_ds1 = create_weighted_graph_first_dataset(edges_ds1, authors)
        result[str(year)] = graph_ds1
    return result


def graphs_by_range(dataset_loc, folder_ds1, start_year, end_year):
    result = dict()
    tot_pub = total_collaborations(dataset_loc + "ds-2.tsv")  # Utilizzo ds-2 per creare i pesi degli archi
    for year in range(start_year, end_year + 1):
        nodes_ds1, edges_ds1 = nodes_and_edges_first_dataset(folder_ds1 + str(year) + "_ds1.tsv")
        authors = tot_pub[str(year)]
        # creazione grafo pesato
        graph_ds1 = create_weighted_graph_first_dataset(edges_ds1, authors)
        result[str(year)] = graph_ds1
    return result


def graphs_second_dataset():
    result = dict()
    for year in range(2000, 2019):
        nodes_ds2, edges_ds2 = nodes_and_edges_second_dataset(OUTPUT_FOLDER_DS2 + str(year) + "_ds2.tsv")
        graph_ds2 = create_weighted_graph_second_dataset(edges_ds2)
        result[str(year)] = graph_ds2
    return result


def normalize_weights(graphs):
    for y, G in graphs.items():
        edge, m = min(dict(G.edges).items(), key=lambda x: x[1]['weight'])
        min_weight = m['weight']
        edge, m = max(dict(G.edges).items(), key=lambda x: x[1]['weight'])
        max_weight = m['weight']
        for edge in G.edges(data=True):
            n1, n2, w = edge
            weight = w['weight']
            # normalizzo i pesi attraverso la minMax normalization
            G.add_edge(n1, n2, weight=(weight - min_weight) / (max_weight - min_weight))
