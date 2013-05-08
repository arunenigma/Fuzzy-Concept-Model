from ast import literal_eval
import math
from numpy import product


class FuzzyConceptModel(object):
    def __init__(self, query_fc, query_pi, query_ps, spec_fc, spec_pi, spec_ps, spec_name):
        self.query_fc = query_fc
        self.query_pi = query_pi
        self.query_ps = query_ps
        self.spec_fc = spec_fc
        self.spec_pi = spec_pi
        self.spec_ps = spec_ps
        self.spec_name = spec_name

        self.query_pi_dict = {}
        self.spec_pi_dict = {}

        self.similarity_score = []  # document similarity score

    def constructScoreDictionaries(self):
        for row in self.query_pi:
            self.query_pi_dict[row[0]] = float(row[1])

        for row in self.spec_pi:
            self.spec_pi_dict[row[0]] = float(row[1])

    def compareSkeletons(self):
        self.query_skeletons = []
        self.spec_skeletons = []
        for row_q in self.query_fc:
            self.query_skeletons.append([literal_eval(row_q[0]), literal_eval(row_q[1])])
        for row_s in self.spec_fc:
            self.spec_skeletons.append([literal_eval(row_s[0]), literal_eval(row_s[1])])

        self.concepts_count = len(self.query_skeletons)

        for skeleton_q in self.query_skeletons:
            concept_match_score = []  # each query skeleton is equivalent to a concept
            print '***********************************'
            for skeleton_s in self.spec_skeletons:
                self.skeletonMatch(skeleton_q, skeleton_s)

    def skeletonMatch(self, skeleton_q, skeleton_s):
        # matching skeletons
        if not len(skeleton_q[0]) == 1 and not len(skeleton_s[0]) == 1:
            self.matched_bones = len(set(skeleton_q[0]).intersection(set(skeleton_s[0])))

        if type(skeleton_q[0]) is str:
            self.matched_bones = len({skeleton_q[0], }.intersection(set(skeleton_s[0])))

        if type(skeleton_s[0]) is str:
            self.matched_bones = len(set(skeleton_q[0]).intersection({skeleton_s[0], }))

        for i in range(len(skeleton_q[0])):
            if self.matched_bones == len(skeleton_q[0]) - i and not self.matched_bones == 0:
                match_ratio = (float(len(skeleton_q[0]) - i)) / float(len(skeleton_q[0]))
                node_pairs = []

                for q_node in skeleton_q[1]:
                    for s_node in skeleton_s[1]:
                        if len(q_node) == 1 or len(s_node) == 1 and len(set(q_node).intersection(set(s_node))) == 1:
                            print q_node, s_node, match_ratio

                        if len(q_node) > 1 and len(s_node) > 1 and len(set(q_node).intersection(set(s_node))) > 1:
                            print q_node, s_node, match_ratio
























    '''
                # *********** Calculating Change Factor ***********
                print node_pairs
                for node_pair in node_pairs:

                    print '==============='
                    print node_pair[0], node_pair[1]
                    if len(node_pair[0]) == len(node_pair[1]):
                        CS = self.querySpecPerfectMatch(node_pair[0], node_pair[1], match_ratio)
                        self.similarity_score.append(CS)

                    if len(node_pair[0]) == 1 and len(node_pair[1]) > 1 and set(map(tuple, node_pair[0])) <= set(
                            map(tuple, node_pair[1])):
                        self.querySpecConceptMap_1_gt1(node_pair[0][0], node_pair[1][0], match_ratio)

                    if len(node_pair[0]) == 2 and len(node_pair[1]) == 2 and set(map(tuple, node_pair[0])) <= set(
                            map(tuple, node_pair[1])):
                        print math.fabs(self.query_pi_dict.get(node_pair[0][0]) - self.spec_pi_dict.get(
                            node_pair[1][0])), math.fabs(
                            self.query_pi_dict.get(node_pair[1][0]) - self.spec_pi_dict.get(node_pair[1][1]))

                    if len(node_pair[0]) == 2 and len(node_pair[1]) > 2 and set(map(tuple, node_pair[0])) <= set(
                            map(tuple, node_pair[1])):
                        self.querySpecConceptMap_2_gt2(node_pair[0], node_pair[1], match_ratio)

    def querySpecPerfectMatch(self, x, y, match_ratio):
        print 'Perfect match'
        len_x = len(x)
        pi_change_inf_path = []
        for i in range(len_x):
            print x[i], y[i]
            pi_change_node = math.fabs(self.query_pi_dict.get(x[i]) - self.spec_pi_dict.get(y[i]))
            pi_change_inf_path.append(pi_change_node)
            #print pi_change_inf_path
        CF = product(pi_change_inf_path)
        print match_ratio, CF

    def querySpecConceptMap_1_gt1(self, x, y, match_ratio):
        print match_ratio, math.fabs(self.query_pi_dict.get(x) - self.spec_pi_dict.get(y))

    def querySpecConceptMap_2_gt2(self, x, y, match_ratio):
        print x, y
        indices = []
        for node in x:
            indices.append(y.index(node))
        swipe = (indices[1] - indices[0]) - 1
        print math.fabs(self.query_pi_dict.get(x[0]) - self.spec_pi_dict.get(x[0])), math.fabs(
            self.query_pi_dict.get(x[1]) - self.spec_pi_dict.get(x[1]))
        for i in range(swipe):
            print y[i + 1], self.spec_pi_dict.get(y[i + 1])


    def querySpecConceptMap_gt2_gt2(self, x, y):
        pass

    def printSimilarityScore(self):
        pass
    '''