"""
Method that starting from all topics and dates returns a dictionary
with KEY: keyword that represents a topic VALUE: dictionary
consisting of year (Key) - topic related (Value)
"""


def trace_all_topics_time_interval(topics, start_date, end_date):
    if start_date > end_date:
        raise (Exception("Error: start date is greater than end date!"))
    result = dict()
    for year in range(start_date, end_date + 1):
        for k, t in topics[str(year)].items():
            split = k.split("|")
            for s in split:
                if s not in result:
                    result[s] = dict()
                result[s][str(year)] = t
    return result


"""
Method that calculates the number of times that a keywords appears in the topic set
"""


def keyword_that_appears_more_times(all_topics):
    years = list(all_topics.keys())
    result = dict()
    # per ogni anno scorro ogni topic e per ogni topic scorro ogni keyword per calcolare il punteggio finale.
    for y in years:
        for k, s in all_topics[y].items():
            for w in list(s):
                if w not in result:
                    result[w] = 1
                result[w] += 1
    return result


'''
Method that calculate the number of times that a topic appears
'''


def number_topic_appears(topic_over_years):
    res = dict()
    for k, d in topic_over_years.items():
        res[k] = 0
        for y, s in d.items():
            res[k] += 1
    return res
