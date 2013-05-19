import os
import csv
import time
from fcm_lemmatized import FuzzyConceptModel

if __name__ == '__main__':
    paths = []
    doc_rank = {}
    start_time = time.time()

    for root, directory, files in os.walk('./concept_db'):
        for f in files:
            if f.endswith('.csv'):
                paths.append(os.path.join(root, f))
    for i in range(0, len(paths), 3):
        query_fuzzy_concepts = open('./fuzzy_concepts.csv', 'rU')
        query_fuzzy_concepts_csv = csv.reader(query_fuzzy_concepts)
        query_PI = open('./PI.csv', 'rU')
        query_PI_csv = csv.reader(query_PI)
        query_PS = open('./PS.csv', 'rU')
        query_PS_csv = csv.reader(query_PS)
        spec_fc = paths[i:i + 3][0]
        spec_pi = paths[i:i + 3][1]
        spec_ps = paths[i:i + 3][2]
        spec_name = spec_fc.split('/')[2]
        spec_fuzzy_concepts = open(spec_fc, 'rU')
        spec_fuzzy_concepts_csv = csv.reader(spec_fuzzy_concepts)
        spec_PI = open(spec_pi, 'rU')
        spec_PI_csv = csv.reader(spec_PI)
        spec_PS = open(spec_ps, 'rU')
        spec_PS_csv = csv.reader(spec_PS)
        fcm = FuzzyConceptModel(query_fuzzy_concepts_csv, query_PI_csv, query_PS_csv,
                                spec_fuzzy_concepts_csv, spec_PI_csv, spec_PS_csv,
                                spec_name, doc_rank)
        fcm.constructScoreDictionaries()
        fcm.compareSkeletons()
        fcm.printSimilarityScore()
        query_fuzzy_concepts.close()
        query_PI.close()
        query_PS.close()
        spec_fuzzy_concepts.close()
        spec_PI.close()
        spec_PS.close()
        if (i+3) == len(paths):
            fcm.printSearchResults(start_time)