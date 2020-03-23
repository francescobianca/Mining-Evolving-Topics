import copy
from sapienza.first_task import spread_of_influence_algorithm as spread_influence
from sapienza.utility import measuraments as ms

'''
Method used to merge topics. The topic similarity must be grather than the threshold similarity.
'''


def merge_for_year(topic_year, threshold):
    merging_topic = copy.deepcopy(topic_year)

    while True:
        best = 0
        isMerge = False

        for first_keyword, first_set in merging_topic.items():
            for second_keyword, second_set in merging_topic.items():
                if first_keyword != second_keyword:
                    sim = ms.overlap_similarity(first_set, second_set) # Si può cambiare con le altre metriche disponibili.
                    if sim >= best and sim >= threshold:
                        isMerge = True
                        best = sim
                        selected_keywords1 = first_keyword
                        selected_keywords2 = second_keyword

        if not isMerge:
            break
        # effettuo il merging
        merging_topic[selected_keywords1 + "|" + selected_keywords2] = merging_topic[selected_keywords1].union(merging_topic[selected_keywords2])
        merging_topic.pop(selected_keywords1)
        merging_topic.pop(selected_keywords2)
    return merging_topic


'''
Method to create a dictionary of this type -> Key:year value: merging topic of that year. 
It's just a method to apply the merging described in the function above to all the graphs we have.
'''


def generate_all_topics(graphs, top_keywords):
    topics = dict()
    for year, graph in graphs.items():
        topics[year] = spread_influence.calculate_topics_spreading_algorithm(graph, top_keywords[year])
        # Una volta applicato lo spreading algorithm e generati i topics per ogni anno posso fare il merge tramite la funziona precedente
        topics[year] = merge_for_year(topics[year], 0.55)
    return topics
