from ast import literal_eval
from math import fabs, exp
#from numpy import product
from itertools import groupby


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

        self.query_ps_dict = {}
        self.spec_ps_dict = {}

        self.similarity_score = []  # document similarity score

    def constructScoreDictionaries(self):
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

    def skeletonMatch(self, skeleton_q, skeleton_s):
        # matching skeletons
        #print skeleton_q[0], skeleton_s[0]
        if len(skeleton_q[0]) > 1 and len(skeleton_s[0]) > 1:
            self.matched_bones = len(set(skeleton_q[0]).intersection(set(skeleton_s[0])))

        elif len(skeleton_q[0]) == 1 and len(skeleton_s[0]) > 1:
            self.matched_bones = len(set(skeleton_q[0]).intersection(set(skeleton_s[0])))

        elif len(skeleton_q[0]) > 1 and len(skeleton_s[0]) == 1:
            self.matched_bones = len(set(skeleton_q[0]).intersection(set(skeleton_s[0])))

        elif len(skeleton_q[0]) == 1 and len(skeleton_s[0]) == 1:
            self.matched_bones = len(set(skeleton_q[0]).intersection(set(skeleton_s[0])))

        elif type(skeleton_q[0]) is str:
            self.matched_bones = len({skeleton_q[0], }.intersection(set(skeleton_s[0])))

        elif type(skeleton_s[0]) is str:
            self.matched_bones = len(set(skeleton_q[0]).intersection({skeleton_s[0], }))

        else:
            self.matched_bones = None

        #print self.matched_bones, set(skeleton_q[0]).intersection(set(skeleton_s[0]))
        if not self.matched_bones is None:
            for i in range(len(skeleton_q[0])):
                if self.matched_bones == len(skeleton_q[0]) - i and not self.matched_bones == 0:
                    match_ratio = (float(len(skeleton_q[0]) - i)) / float(len(skeleton_q[0]))
                    for q_node in skeleton_q[1]:
                        for s_node in skeleton_s[1]:
                            if len(q_node) == 1 and len(s_node) == 1 and len(set(q_node).intersection(set(s_node))) == 1:
                                print q_node[0], s_node[0]
                                CF = fabs(
                                    self.query_pi_dict.get(q_node[0]) - self.spec_pi_dict.get(q_node[0]))
                                self.similarity_score.append([CF, match_ratio, skeleton_q[0]])
                                print 'CF = ', CF

                            if len(q_node) == 1 and len(s_node) > 1 and len(set(q_node).intersection(set(s_node))) == 1:
                                print q_node[0], s_node[0]
                                CF = fabs(
                                    self.query_pi_dict.get(q_node[0]) - self.spec_pi_dict.get(q_node[0]))
                                self.similarity_score.append([CF, match_ratio, skeleton_q[0]])
                                print 'CF = ', CF

                            if len(q_node) > 1 and len(s_node) > 1 and len(set(q_node).intersection(set(s_node))) > 0:
                                for node_pair in zip(q_node, q_node[1:]):
                                    indices = []
                                    if node_pair[0] in s_node and node_pair[1] in s_node:
                                        print node_pair[0], node_pair[1]
                                        indices.append([s_node.index(node_pair[0]), s_node.index(node_pair[1])])
                                        if s_node[indices[0][0]:indices[0][1] + 1]:
                                            change_in_PI_node_1 = fabs(
                                                self.query_pi_dict.get(node_pair[0]) - self.spec_pi_dict.get(
                                                    node_pair[0]))
                                            change_in_PI_node_2 = fabs(
                                                self.query_pi_dict.get(node_pair[1]) - self.spec_pi_dict.get(
                                                    node_pair[1]))
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
                                            print 'CF = ', CF
                                            self.similarity_score.append([CF, match_ratio, skeleton_q[0]])

                                        else:
                                            print node_pair[0], node_pair[1]
                                            change_in_PI_node_1 = fabs(
                                                self.query_pi_dict.get(node_pair[0]) - self.spec_pi_dict.get(
                                                    node_pair[0]))
                                            change_in_PI_node_2 = fabs(
                                                self.query_pi_dict.get(node_pair[1]) - self.spec_pi_dict.get(
                                                    node_pair[1]))
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
                                            print 'CF = ', CF
                                            self.similarity_score.append([CF, match_ratio, skeleton_q[0]])

                                    if node_pair[0] in s_node and not node_pair[1] in s_node:
                                        print node_pair[0], node_pair[1]
                                        CF = fabs(self.query_pi_dict.get(node_pair[0]) - self.spec_pi_dict.get(node_pair[0]))
                                        self.similarity_score.append([CF, match_ratio, skeleton_q[0]])
                                        print 'CF = ', CF

                                    if node_pair[1] in s_node and not node_pair[0] in s_node:
                                        print node_pair[0], node_pair[1]
                                        CF = fabs(self.query_pi_dict.get(node_pair[1]) - self.spec_pi_dict.get(node_pair[1]))
                                        self.similarity_score.append([CF, match_ratio, skeleton_q[0]])
                                        print 'CF = ', CF

    def key(self, item):
        return [x for x in item[2]]

    def printSimilarityScore(self):
        doc_similarity = []
        for k, v in groupby(self.similarity_score, key=self.key):
            v = dict((x[0], x) for x in v).values()
            concept_score = []
            for score in v:
                concept_score.append(exp(score[0] * score[1]))
            doc_similarity.append(sum(concept_score))
        if not len(doc_similarity) == 0:
            print 'Similarity Score = ', sum(doc_similarity) / self.n_q_skeletons
        else:
            print 'Similarity Score = ', 0