import re

regex = re.compile(r'20((0[0-9])|(1[0-8]))')  # regex che verifica gli anni compresi tra 2000 e 2018

'''
method to clean first dataset. Some keywords have values with ???. Also I remove years < 2000 (check with regex)
'''


def clean_datasetCoKeywords(loc, clean_loc):
    with open(loc, 'r', encoding='utf-8') as read_ds1:
        with open(clean_loc, 'w', encoding='utf-8') as write_ds1:
            for l in read_ds1:
                s = l.split('\t')  # splitto per tabulazione
                if (regex.match(s[0]) and not "?" in s[1]
                        and not "?" in s[2]):
                    write_ds1.write(l)
            write_ds1.close()
        read_ds1.close()


'''
method to clean second dataset. I only check the year.
'''


def clean_datasetCoKeyAuthors(loc, clean_loc):
    with open(loc, 'r', encoding='utf-8') as read_ds2:
        with open(clean_loc, 'w', encoding='utf-8') as write_ds2:
            for line in read_ds2:
                s = line.split('\t') # splitto per tabulazione
                if regex.match(s[0]):
                    write_ds2.write(line)
            write_ds2.close()
        read_ds2.close()
