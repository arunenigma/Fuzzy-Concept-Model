from __future__ import division

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from prettytable import PrettyTable
from itertools import groupby
from ast import literal_eval
#from numpy import product
from math import fabs, exp
from time import time
import operator
import csv
import sys


class FuzzyConceptModel(object):
    def __init__(self, query_fc, query_pi, query_ps, spec_fc, spec_pi, spec_ps, spec_name, doc_rank):
        csv.field_size_limit(sys.maxsize)
        self.query_fc = query_fc
        self.query_pi = query_pi
        self.query_ps = query_ps
        self.spec_fc = spec_fc
        self.spec_pi = spec_pi
        self.spec_ps = spec_ps
        self.spec_name = spec_name

        self.query_pi_dict = {}
        self.spec_pi_dict = {}

        self.query_ps_dict = {}
        self.spec_ps_dict = {}

        self.similarity_score = []  # document similarity score

        self.doc_rank = doc_rank

    def constructScoreDictionaries(self):
        print '> analyzing ' + self.spec_name + '...'
        for row in self.query_pi:
            self.query_pi_dict[row[0]] = float(row[1])

        for row in self.spec_pi:
            self.spec_pi_dict[row[0]] = float(row[1])

        for row in self.query_ps:
            self.query_ps_dict[tuple([row[0], row[1]])] = float(row[2])

        for row in self.spec_ps:
            self.spec_ps_dict[tuple([row[0], row[1]])] = float(row[2])

    def compareSkeletons(self):
        self.query_skeletons = []
        self.spec_skeletons = []
        for row_q in self.query_fc:
            self.query_skeletons.append([literal_eval(row_q[0]), literal_eval(row_q[1])])
        for row_s in self.spec_fc:
            self.spec_skeletons.append([literal_eval(row_s[0]), literal_eval(row_s[1])])

        self.concepts_count = len(self.query_skeletons)

        self.n_q_skeletons = len(self.query_skeletons)

        for skeleton_q in self.query_skeletons:
            for skeleton_s in self.spec_skeletons:
                self.skeletonMatch(skeleton_q, skeleton_s)

    def lemmatizeWords(self, word):
        """
        No Stemmer is used
        Some available NLTK stemmers: Porter, Lancaster and Snowball Stemmer

        Lemmatizer used: WordNetLemmatizer

        :param word: query and spec words
        :return: root or stem word
        """
        l = WordNetLemmatizer()
        snowball = SnowballStemmer('english')
        if not snowball.stem(word) is None:
            return snowball.stem(word)
        else:
            return l.lemmatize(word)

    def skeletonMatch(self, skeleton_q, skeleton_s):
        # matching skeletons
        query_roots = tuple(self.lemmatizeWords(w) for w in skeleton_q[0])
        spec_roots = tuple(self.lemmatizeWords(w) for w in skeleton_s[0])

        if len(skeleton_q[0]) > 0 and len(skeleton_s[0]) > 0:
            self.matched_bones = len(set(query_roots).intersection(set(spec_roots)))

        elif type(skeleton_q[0]) is str:
            self.matched_bones = len({query_roots, }.intersection(set(spec_roots)))

        elif type(skeleton_s[0]) is str:
            self.matched_bones = len(set(query_roots).intersection({spec_roots, }))

        else:
            self.matched_bones = None

        if not self.matched_bones is None:
            for i in range(len(query_roots)):
                if self.matched_bones == len(query_roots) - i and not self.matched_bones == 0:
                    match_ratio = (float(len(query_roots) - i)) / float(len(query_roots))
                    for q_node in skeleton_q[1]:
                        q_node_roots = [self.lemmatizeWords(w) for w in q_node]
                        for s_node in skeleton_s[1]:
                            s_node_roots = [self.lemmatizeWords(w) for w in s_node]
                            if len(q_node_roots) == 1 and len(s_node_roots) == 1 and len(
                                    set(q_node_roots).intersection(set(s_node_roots))) == 1:
                                if self.spec_pi_dict.get(q_node[0]):
                                    CF = fabs(
                                        self.query_pi_dict.get(q_node[0]) - self.spec_pi_dict.get(q_node[0]))
                                    self.similarity_score.append([CF, match_ratio, query_roots])
                                    #print 'CF = ', CF
                                else:
                                    CF = fabs(
                                        self.query_pi_dict.get(q_node[0]) - self.spec_pi_dict.get(s_node[0]))
                                    self.similarity_score.append([CF, match_ratio, query_roots])
                                    #print 'CF = ', CF

                            if len(q_node_roots) == 1 and len(s_node_roots) > 1 and len(
                                    set(q_node_roots).intersection(set(s_node_roots))) == 1:
                                if self.spec_pi_dict.get(q_node[0]):
                                    CF = fabs(
                                        self.query_pi_dict.get(q_node[0]) - self.spec_pi_dict.get(q_node[0]))
                                    self.similarity_score.append([CF, match_ratio, query_roots])
                                    #print 'CF = ', CF
                                else:
                                    CF = fabs(
                                        self.query_pi_dict.get(q_node[0]) - self.spec_pi_dict.get(s_node[0]))
                                    self.similarity_score.append([CF, match_ratio, query_roots])
                                    #print 'CF = ', CF

                            if len(q_node_roots) > 1 and len(s_node_roots) > 1 and len(
                                    set(q_node_roots).intersection(set(s_node_roots))) > 0:
                                node_pair_roots_list = zip(q_node_roots, q_node_roots[1:])
                                node_pair_list = zip(q_node, q_node[1:])
                                for node_pair, node_pair_roots in zip(node_pair_list, node_pair_roots_list):
                                    indices = []
                                    if node_pair_roots[0] in s_node_roots and node_pair_roots[1] in s_node_roots:
                                        indices.append([s_node_roots.index(node_pair_roots[0]),
                                                        s_node_roots.index(node_pair_roots[1])])
                                        if s_node[indices[0][0]:indices[0][1] + 1]:
                                            if self.spec_pi_dict.get(node_pair[0]) and self.spec_pi_dict.get(
                                                    node_pair[1]):
                                                change_in_PI_node_1 = fabs(
                                                    self.query_pi_dict.get(node_pair[0]) - self.spec_pi_dict.get(
                                                        node_pair[0]))
                                                change_in_PI_node_2 = fabs(
                                                    self.query_pi_dict.get(node_pair[1]) - self.spec_pi_dict.get(
                                                        node_pair[1]))
                                            else:
                                                ind_0 = s_node_roots.index(node_pair_roots[0])
                                                ind_1 = s_node_roots.index(node_pair_roots[1])
                                                change_in_PI_node_1 = fabs(
                                                    self.query_pi_dict.get(node_pair[0]) - self.spec_pi_dict.get(
                                                        s_node[ind_0]))
                                                change_in_PI_node_2 = fabs(
                                                    self.query_pi_dict.get(node_pair[1]) - self.spec_pi_dict.get(
                                                        s_node[ind_1]))

                                            if self.query_ps_dict.get(node_pair):
                                                PS_state_1 = self.query_ps_dict.get(node_pair, 1.0)
                                            else:
                                                PS_state_1 = self.query_ps_dict.get(node_pair[::-1], 1.0)
                                            neighbors = s_node[indices[0][0] + 1:indices[0][1]]
                                            PI_neighbors = []
                                            for neighbor in neighbors:
                                                PI_neighbors.append(self.spec_pi_dict.get(neighbor, 1.0))
                                            n_paths = zip(s_node[indices[0][0]:indices[0][1] + 1],
                                                          s_node[indices[0][0]:indices[0][1] + 1][1:])
                                            PS_n_paths = []
                                            for n_path in n_paths:
                                                if self.spec_ps_dict.get(n_path):
                                                    PS_n_paths.append(self.spec_ps_dict.get(n_path, 1.0))
                                                else:
                                                    PS_n_paths.append(self.spec_ps_dict.get(n_path[::-1], 1.0))
                                            change_in_PS = fabs(
                                                PS_state_1 - ((sum(PI_neighbors) * sum(PS_n_paths))))
                                            CF = change_in_PI_node_1 * change_in_PI_node_2 * change_in_PS
                                            #print 'CF = ', CF
                                            self.similarity_score.append([CF, match_ratio, query_roots])

                                        else:
                                            if self.spec_pi_dict.get(node_pair[0]) and self.spec_pi_dict.get(
                                                    node_pair[1]):
                                                change_in_PI_node_1 = fabs(
                                                    self.query_pi_dict.get(node_pair[0]) - self.spec_pi_dict.get(
                                                        node_pair[0]))
                                                change_in_PI_node_2 = fabs(
                                                    self.query_pi_dict.get(node_pair[1]) - self.spec_pi_dict.get(
                                                        node_pair[1]))
                                            else:
                                                ind_0 = s_node_roots.index(node_pair_roots[0])
                                                ind_1 = s_node_roots.index(node_pair_roots[1])
                                                change_in_PI_node_1 = fabs(
                                                    self.query_pi_dict.get(node_pair[0]) - self.spec_pi_dict.get(
                                                        s_node[ind_0]))
                                                change_in_PI_node_2 = fabs(
                                                    self.query_pi_dict.get(node_pair[1]) - self.spec_pi_dict.get(
                                                        s_node[ind_1]))

                                            if self.query_ps_dict.get(node_pair):
                                                PS_state_1 = self.query_ps_dict.get(node_pair, 1.0)
                                            else:
                                                PS_state_1 = self.query_ps_dict.get(node_pair[::-1], 1.0)
                                            neighbors = s_node[indices[0][1] + 1:indices[0][0]]
                                            PI_neighbors = []
                                            for neighbor in neighbors:
                                                PI_neighbors.append(self.spec_pi_dict.get(neighbor, 1.0))
                                            n_paths = zip(s_node[indices[0][1]:indices[0][0] + 1],
                                                          s_node[indices[0][1]:indices[0][0] + 1][1:])
                                            PS_n_paths = []
                                            for n_path in n_paths:
                                                if self.spec_ps_dict.get(n_path):
                                                    PS_n_paths.append(self.spec_ps_dict.get(n_path, 1.0))
                                                else:
                                                    PS_n_paths.append(self.spec_ps_dict.get(n_path[::-1], 1.0))
                                            change_in_PS = fabs(
                                                PS_state_1 - ((sum(PI_neighbors) * sum(PS_n_paths))))
                                            CF = change_in_PI_node_1 * change_in_PI_node_2 * change_in_PS
                                            #print 'CF = ', CF
                                            self.similarity_score.append([CF, match_ratio, query_roots])

                                    if node_pair_roots[0] in s_node_roots and not node_pair_roots[1] in s_node_roots:
                                        if self.spec_pi_dict.get(node_pair[0]):
                                            CF = fabs(self.query_pi_dict.get(node_pair[0]) - self.spec_pi_dict.get(
                                                node_pair[0]))
                                            #print 'CF = ', CF
                                            self.similarity_score.append([CF, match_ratio, query_roots])
                                        else:
                                            CF = fabs(
                                                self.query_pi_dict.get(node_pair[0]) - self.spec_pi_dict.get(s_node[
                                                    s_node_roots.index(node_pair_roots[0])]))
                                            #print 'CF = ', CF
                                            self.similarity_score.append([CF, match_ratio, query_roots])

                                    if node_pair_roots[1] in s_node_roots and not node_pair_roots[0] in s_node_roots:
                                        if self.spec_pi_dict.get(node_pair[1]):
                                            CF = fabs(
                                                self.query_pi_dict.get(node_pair[1]) - self.spec_pi_dict.get(
                                                    node_pair[1]))
                                            #print 'CF = ', CF
                                            self.similarity_score.append([CF, match_ratio, query_roots])
                                        else:
                                            CF = fabs(
                                                self.query_pi_dict.get(node_pair[1]) - self.spec_pi_dict.get(
                                                    s_node[s_node_roots.index(node_pair_roots[1])]))
                                            #print 'CF = ', CF
                                            self.similarity_score.append([CF, match_ratio, query_roots])

    def key(self, item):
        return [x for x in item[2]]

    def printSimilarityScore(self):
        doc_cf = []
        for k, v in groupby(self.similarity_score, key=self.key):
            v = dict((x[0], x) for x in v).values()
            concept_cf = []
            for score in v:
                concept_cf.append(score[0] * score[1])
            doc_cf.append(sum(concept_cf))
        sim_score = exp(sum(doc_cf) / 100) * fabs((len(doc_cf) / self.n_q_skeletons))
        self.doc_rank[self.spec_name] = sim_score

    def printSearchResults(self, start_time):
        sorted_x = sorted(self.doc_rank.iteritems(), key=operator.itemgetter(1))[::-1]
        max_sim_score = max(self.doc_rank.values())
        x = PrettyTable(['Rank', 'Specification Name', 'Similarity Score'])
        x.align['Rank'] = 'c'
        x.align['Specification Name'] = 'l'
        x.align['Similarity Score'] = 'l'
        x.padding_width = 2
        for rank, item in enumerate(sorted_x):
            if not item[1] / max_sim_score == 0:
                x.add_row([rank + 1, item[0], item[1] / max_sim_score])
        print
        print ' > ' + str(len(filter(lambda a: a != 0.0, x))) + ' matches found in ' + str(
            time() - start_time) + ' seconds'
        print x
