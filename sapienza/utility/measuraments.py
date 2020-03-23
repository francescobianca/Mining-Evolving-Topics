"""
A series of similarity metrics and graph algorithms are implemented in this file.
Graph operations are implemented in the networkx library while the formula was simply implemented for metric operations.
"""

import networkx as nx
import collections

'''
Method that calculates the Jaccard Similarity between two sets
'''


def jaccard_similarity(X, Y):
    intersection = X.intersection(Y)
    union = X.union(Y)
    return float(len(intersection) / (len(union)))


'''
Method that calculates the edit distance between two sets
'''


def edit_distance(X, Y):
    m = len(X) + 1
    n = len(Y) + 1

    tbl = {}
    for i in range(m): tbl[i, 0] = i
    for j in range(n): tbl[0, j] = j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if X[i - 1] == Y[j - 1] else 1
            tbl[i, j] = min(tbl[i, j - 1] + 1, tbl[i - 1, j] + 1, tbl[i - 1, j - 1] + cost)

    return tbl[i, j]


'''
Method that calculates the cosine similarity between two sets
'''


def cosine_similarity(X, Y):
    # count word occurrences
    a_vals = collections.Counter(list(X))
    b_vals = collections.Counter(list(Y))

    # convert to word-vectors
    words = list(a_vals.keys() | b_vals.keys())
    a_vect = [a_vals.get(word, 0) for word in words]
    b_vect = [b_vals.get(word, 0) for word in words]

    # find cosine
    len_a = sum(av * av for av in a_vect) ** 0.5
    len_b = sum(bv * bv for bv in b_vect) ** 0.5
    dot = sum(av * bv for av, bv in zip(a_vect, b_vect))
    cosine = dot / (len_a * len_b)
    return cosine


'''
Method that calculates the overlap similarity between two sets
'''


def overlap_similarity(X, Y):
    return len(X.intersection(Y)) / min(len(X), len(Y))


'''
method used to select the top-k keywords based on page rank
:k number of selected keywords (can be 5,10 ..)
return a list of top-k keywords.
'''


def selection_with_pagerank(graph, k):
    result = list()
    page_rank = nx.pagerank(graph)
    if k <= len(graph.nodes):
        for pair in sorted(page_rank.items(), key=lambda x: x[1], reverse=True)[:k]:
            result.append(pair[0])
    else:
        raise Exception("not possible for this value of k!")
    return result


'''
method used to select the top-k keywords based on hubness
'''


def selection_with_hubness(graph, k, iterations):
    result = list()
    hubness, authority = nx.hits(graph, max_iter=iterations)
    if k <= len(graph.nodes):
        for pair in sorted(hubness.items(), key=lambda x: x[1], reverse=True)[:k]:
            result.append(pair[0])
    else:
        raise Exception("not possible for this value of k!")
    return result


'''
method used to select the top-k keywords based on authority
'''


def selection_with_authority(graph, k, iterations):
    result = list()
    hubness, authority = nx.hits(graph, max_iter=iterations)
    if k <= len(graph.nodes):
        for pair in sorted(authority.items(), key=lambda x: x[1], reverse=True)[:k]:
            result.append(pair[0])
    else:
        raise Exception("not possible for this value of k!")
    return result


'''
method used to select the top-k keywords based on closeness centrality
'''


def selection_with_closeness(graph, k):
    result = list()
    closeness = nx.closeness_centrality(graph)
    if k <= len(graph.nodes):
        for pair in sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:k]:
            result.append(pair[0])
    else:
        raise Exception("not possible for this value of k!")
    return result


'''
method used to select the top-k keywords based on betweenness centrality
'''


def selection_with_betweenness(graph, k):
    result = list()
    betweenness = nx.betweenness_centrality(graph, weight='weight')

    if k <= len(graph.nodes):
        for pair in sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:k]:
            result.append(pair[0])
    else:
        raise Exception("not possible for this value of k!")
    return result


'''
method used to select the top-k keywords based on degree centrality
'''


def selection_with_degree(graph, k):
    result = list()
    degree = dict(graph.degree(weight='weight'))

    if k <= len(graph.nodes):
        for pair in sorted(degree.items(), key=lambda x: x[1], reverse=True)[:k]:
            result.append(pair[0])
    else:
        raise Exception("not possible for this value of k!")
    return result
