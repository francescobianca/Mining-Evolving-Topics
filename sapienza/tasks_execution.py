import argparse
import os

from sapienza.dataset_preprocessing import clean_dataset, create_dataset_for_year
from sapienza.utility import graph_builder as gb
from sapienza.utility import visualization as vs

DATASET_LOC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Datasets/")
DATA_COKEYWORDS = "ds-1.tsv"
DATA_COAUTHORS = "ds-2.tsv"
CLEAN_DATA_COKEYWORDS = "clean_ds-1.tsv"
CLEAN_DATA_COAUTHORS = "clean_ds-2.tsv"


def tasks_execution(start_year: int, end_year: int, directory: str):
    os.mkdir(directory)  # Not already exists
    OUTPUT_FOLDER_A = directory + "/output_ds-1/"
    OUTPUT_FOLDER_B = directory + "/output_ds-2/"
    os.mkdir(OUTPUT_FOLDER_A)
    os.mkdir(OUTPUT_FOLDER_B)
    OUTPUT_FOLDER_DS1 = OUTPUT_FOLDER_A + "years_ds1/"
    OUTPUT_FOLDER_DS2 = OUTPUT_FOLDER_B + "years_ds2/"
    os.mkdir(OUTPUT_FOLDER_DS1)
    os.mkdir(OUTPUT_FOLDER_DS2)

    # Data creation
    clean_dataset.clean_datasetCoKeywords(DATASET_LOC + DATA_COKEYWORDS, DATASET_LOC + CLEAN_DATA_COKEYWORDS)
    clean_dataset.clean_datasetCoKeyAuthors(DATASET_LOC + DATA_COAUTHORS, DATASET_LOC + CLEAN_DATA_COAUTHORS)
    create_dataset_for_year.generate_files(DATASET_LOC + CLEAN_DATA_COKEYWORDS, DATASET_LOC + CLEAN_DATA_COAUTHORS,
                                           OUTPUT_FOLDER_DS1, OUTPUT_FOLDER_DS2)

    graphs = gb.graphs_by_range(DATASET_LOC, OUTPUT_FOLDER_DS1, start_year, end_year)
    vs.plot_edge_weights(graphs[str(end_year)])  # Plot edge weights before normalization

    gb.normalize_weights(graphs)
    vs.plot_edge_weights(graphs[str(end_year)])  # Plot edge weights before normalization

    vs.graph_comparison(graphs[str(start_year)],graphs[str(end_year)])

    print(graphs[str(end_year)].edges(data=True))
    graph_folder = directory + "/GraphsImage/"
    os.mkdir(graph_folder)
    vs.plot_all_graphs(graphs, start_year, end_year, graph_folder)

    # TASK 1 : PART I
    top_k = vs.print_topk_over_the_year(graphs, 10)  # 10 is the k parameters of top-k keywords

    # TASK 1 : PART 2
    year = str(end_year)
    topics_for_a_year = vs.print_topics_for_a_year(year, graphs, top_k)

    # TASK 1 : PART 3
    vs.print_topics_join_for_a_year(year, topics_for_a_year, 0.55)
    all_topics = vs.print_all_topics(graphs, top_k)

    # TASK 2 : PART 1
    most_popular_keywords_over_the_year = vs.print_popular_keywords_over_the_year(all_topics)
    vs.plot_popular_keyword(most_popular_keywords_over_the_year)

    topics_over_the_year = vs.print_topic_trace_over_the_year(all_topics, start_year, end_year)
    #vs.print_keywords_for_specific_topic("linear matrix inequality", topics_over_the_year)

    most_popular_topics_over_the_year = vs.print_popular_topics_over_the_year(topics_over_the_year)
    vs.plot_popular_topics(most_popular_topics_over_the_year)

    # TASK 2 : PART 2
    similar_topics = vs.print_similar_topics_consecutive_years(all_topics)
    similar_topics_subgraphs = vs.print_similar_topics_subgraph_consecutive_years(all_topics, graphs)

    # TASK 2 : PART 3
    vs.save_on_file_merged_list(similar_topics, directory+"/")
    vs.save_on_file_merged_subgraphs_list(similar_topics_subgraphs, directory+"/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Web&Social Information Extraction Project : execution of the tasks')
    parser.add_argument('-s', '--start',
                        metavar='<start year>',
                        type=int,
                        required=True,
                        help="starting year. Constraints: >= 2000 and <= <end year>")
    parser.add_argument('-e', '--end',
                        metavar='<end year>',
                        type=int,
                        required=True,
                        help="ending year. Constraints: >= <start year> and <= 2018")
    parser.add_argument('--outdir',
                        metavar='<output-dir>',
                        type=str,
                        required=True,
                        help="directory to save out. Constraints: No exists yet")
    args = parser.parse_args()

    tasks_execution(args.start, args.end, args.outdir)
