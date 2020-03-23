"""
Method that produce the merge list of similar topic of consecutive years
produced according to the chosen approach
"""


def produce_merge_list_similar_topics_consecutive_year(similar_topics):
    result = list()
    insert_yet = list()
    for el in similar_topics:
        years, key1, key2, set_1, set_2, similarity = el
        set_result = set_1.union(set_2)
        if set_result not in insert_yet:
            result.append(set_result)
            insert_yet.append(set_result)
    return result


'''
Method that writes the final result in a file.
The file contains the best pairs of topics of consecutive years based on a specific similarity used.
'''


def write_file_final_result(filename, similar_topics, merged_list, similarity_used, folder):
    with open(folder + filename, 'w') as fw:
        fw.write("similar topics in consecutive years:" + str.upper(similarity_used) + "\n\n")
        for el in similar_topics:
            years, key1, key2, set_1, set_2, similarity = el
            fw.write(years + " --> " + key1 + " <--> " + key2 + "\n")
            fw.write("First set: " + str(set_1) + "\n")
            fw.write("Second set: " + str(set_2) + "\n")
            fw.write(similarity_used + " : " + str(similarity) + "\n\n")

        fw.write("final merged list:\n\n")
        fw.write(str(merged_list))

        fw.close()
