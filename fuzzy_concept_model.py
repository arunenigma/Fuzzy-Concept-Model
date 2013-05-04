from ast import literal_eval
import math


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

    def constructScoreDictionaries(self):
        for row in self.query_pi:
            print row
            self.query_pi_dict[row[0]] = float(row[1])

        for row in self.spec_pi:
            self.spec_pi_dict[row[0]] = float(row[1])


    def compareSkeletons(self):
        self.query_skeletons = []
        self.spec_skeletons = []

        for row_q in self.query_fc:
            self.query_skeletons.append([set(literal_eval(row_q[0])), literal_eval(row_q[1])])
        for row_s in self.spec_fc:
            self.spec_skeletons.append([set(literal_eval(row_s[0])), literal_eval(row_s[1])])
        for skeleton_q in self.query_skeletons:
            for skeleton_s in self.spec_skeletons:
                if len(skeleton_q[0].intersection(skeleton_s[0])) == len(skeleton_q[0]):
                    print skeleton_q[0], skeleton_s[0], 1.0
                else:
                    self.compareSkeletonsPartialMatch(skeleton_q, skeleton_s)
            print '*************************************************'

    def compareSkeletonsPartialMatch(self, skeleton_q, skeleton_s):

        for i in range(len(skeleton_q[0]) - 1, 1, -1):
            if len(skeleton_q[0].intersection(skeleton_s[0])) == len(skeleton_q[0]) - i:
                #print skeleton_q[0], skeleton_s[0]
                print '*****************'
                print (float(len(skeleton_q[0]) - i)) / float(len(skeleton_q[0]))
                matched = skeleton_q[0].intersection(skeleton_s[0])
                q_matched_candidates = []
                for q_inf_path in skeleton_q[1]:
                    if matched.intersection(set(tuple(q_inf_path))):
                        relation = list(matched.intersection(set(tuple(q_inf_path))))
                        candidates = q_inf_path
                        indices = []

                        if len(relation) > 1:
                            for node in relation:
                                indices.append(candidates.index(node))
                            if candidates[indices[0]: indices[1] + 1]:
                                q_matched_candidates.append(candidates[indices[0]: indices[1] + 1])
                            else:
                                q_matched_candidates.append(candidates[indices[1]: indices[0] + 1])
                        else:
                            q_matched_candidates.append(relation)

                s_matched_candidates = []
                for s_inf_path in skeleton_s[1]:
                    if matched.intersection(set(tuple(s_inf_path))):
                        relation = list(matched.intersection(set(tuple(s_inf_path))))
                        candidates = s_inf_path
                        indices = []

                        if len(relation) > 1:
                            for node in relation:
                                indices.append(candidates.index(node))
                            if candidates[indices[0]: indices[1] + 1]:
                                s_matched_candidates.append(candidates[indices[0]: indices[1] + 1])
                            else:
                                s_matched_candidates.append(candidates[indices[1]: indices[0] + 1])
                        else:
                            s_matched_candidates.append(relation)

                q_matched_candidates_wo_dup = []
                s_matched_candidates_wo_dup = []
                for item in q_matched_candidates:
                    if not item in q_matched_candidates_wo_dup:
                        q_matched_candidates_wo_dup.append(item)
                for item in s_matched_candidates:
                    if not item in s_matched_candidates_wo_dup:
                        s_matched_candidates_wo_dup.append(item)

                node_pairs = []
                for q_node in q_matched_candidates_wo_dup:
                    for s_node in s_matched_candidates_wo_dup:
                        if q_node == s_node:
                            node_pairs.append([q_node, s_node])
                        elif all(len(x) >= 1 for x in [q_node, s_node]) and not set(q_node).isdisjoint(s_node):
                            node_pairs.append([q_node, s_node])
                for node_pair in node_pairs:
                    print node_pair
                    if len(node_pair[0][0]) == 1 and len(node_pair[1][0]) == 1:
                        print math.fabs(
                            self.query_pi_dict.get(node_pair[0][0]) - self.spec_pi_dict.get(node_pair[1][0]))


                    if len(node_pair[0][0]) == 2 and len(node_pair[0][1]) == 2 :
                        print math.fabs(self.query_pi_dict.get(node_pair[0][0][0]) - self.query_pi_dict.get(node_pair[0][1][0])), math.fabs(self.query_pi_dict.get(node_pair[0][1][0]) - self.query_pi_dict.get(node_pair[0][1][1])),

    def querySpecConceptMap_1_gt1(self):
        pass

    def querySpecConceptMap_2_gt2(self):
        pass
    