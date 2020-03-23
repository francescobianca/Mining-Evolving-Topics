"""
method that creates tsv files for each year by dividing by dataset. So I will have 2010 ds1 files and 2010 ds2 files.
the original structure is maintained.
"""


def generate_files(loc_keywords, loc_coauthors, ds1_folder, ds2_folder):
    dictionary_dataset1 = convert_file_to_data_structure(loc_keywords)
    dictionary_dataset2 = convert_file_to_data_structure(loc_coauthors)

    for k in dictionary_dataset1.keys():
        with open(ds1_folder + k + "_ds1.tsv", 'w', encoding='utf-8') as f:
            for line in dictionary_dataset1[k]:
                f.write(line)
            f.close()

    for k in dictionary_dataset2.keys():
        with open(ds2_folder + k + "_ds2.tsv", 'w', encoding='utf-8') as f:
            for line in dictionary_dataset2[k]:
                f.write(line)
            f.close()


'''
method that converts the input dataset into a python data structure (dictionary) to be used for the following phases
'''


def convert_file_to_data_structure(file):
    lines_by_year = dict()
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.split('\t')
            if s[0] not in lines_by_year:  # Se l'anno della linea corrente non è ancora nel dizionario
                lines_by_year[s[0]] = []  # Creo una nuova entry
            lines_by_year[s[0]].append(s[1] + '\t' + s[2] + '\t' + s[3])
    f.close()
    return lines_by_year
