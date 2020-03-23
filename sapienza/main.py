import os
from sapienza.dataset_preprocessing import clean_dataset, create_dataset_for_year
from sapienza.utility import graph_builder as gb
from sapienza.utility import visualization as vs

# Folder path
RESULTS_FOLDER = "../ProjectResults/"
GRAPH_FOLDER = "../ProjectResults/GraphImage/"
DATASET_LOC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Datasets/")
DATA_COKEYWORDS = "ds-1.tsv"
DATA_COAUTHORS = "ds-2.tsv"
CLEAN_DATA_COKEYWORDS = "clean_ds-1.tsv"
CLEAN_DATA_COAUTHORS = "clean_ds-2.tsv"
OUTPUT_FOLDER_DS1 = "../ProjectResults/output_ds-1/years_ds1/"
OUTPUT_FOLDER_DS2 = "../ProjectResults/output_ds-2/years_ds2/"

# Data creation
clean_dataset.clean_datasetCoKeywords(DATASET_LOC + DATA_COKEYWORDS, DATASET_LOC + CLEAN_DATA_COKEYWORDS)
clean_dataset.clean_datasetCoKeyAuthors(DATASET_LOC + DATA_COAUTHORS, DATASET_LOC + CLEAN_DATA_COAUTHORS)
create_dataset_for_year.generate_files(DATASET_LOC + CLEAN_DATA_COKEYWORDS, DATASET_LOC + CLEAN_DATA_COAUTHORS,
                                       OUTPUT_FOLDER_DS1, OUTPUT_FOLDER_DS2)

# GENERATE GRAPHS OF TYPE DS1
map_graph_ds1 = gb.graphs_first_dataset(DATASET_LOC, OUTPUT_FOLDER_DS1)
vs.plot_edge_weights(map_graph_ds1['2018'])  # Plot edge weights before normalization

gb.normalize_weights(map_graph_ds1)
vs.plot_edge_weights(map_graph_ds1['2018'])  # Plot edge weights before normalization

print(map_graph_ds1['2001'].edges(data=True))

vs.plot_all_graphs(map_graph_ds1,2000,2019,GRAPH_FOLDER)

###############################  SOLUTION OF THE FIRST TASK  #########################################

# TASK 1 : PART I
top_k = vs.print_topk_over_the_year(map_graph_ds1, 10)  # 10 is the k parameters of top-k keywords

# TASK 1 : PART 2
year = "2018"
topics_for_a_year = vs.print_topics_for_a_year(year, map_graph_ds1, top_k)  # 2018 is the selected year

# TASK 1 : PART 3
vs.print_topics_join_for_a_year(year, topics_for_a_year, 0.55)
all_topics = vs.print_all_topics(map_graph_ds1, top_k)

###############################  SOLUTION OF THE SECOND TASK  #########################################

# TASK 2 : PART 1
most_popular_keywords_over_the_year = vs.print_popular_keywords_over_the_year(all_topics)
vs.plot_popular_keyword(most_popular_keywords_over_the_year)

topics_over_the_year = vs.print_topic_trace_over_the_year(all_topics, 2000, 2018)
vs.print_keywords_for_specific_topic("linear matrix inequality", topics_over_the_year)

most_popular_topics_over_the_year = vs.print_popular_topics_over_the_year(topics_over_the_year)
vs.plot_popular_topics(most_popular_topics_over_the_year)

# TASK 2 : PART 2
similar_topics = vs.print_similar_topics_consecutive_years(all_topics)
similar_topics_subgraphs = vs.print_similar_topics_subgraph_consecutive_years(all_topics, map_graph_ds1)

# TASK 2 : PART 3
vs.save_on_file_merged_list(similar_topics, RESULTS_FOLDER)
vs.save_on_file_merged_subgraphs_list(similar_topics_subgraphs, RESULTS_FOLDER)
