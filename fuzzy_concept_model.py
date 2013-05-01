from ast import literal_eval


class FuzzyConceptModel(object):
    def __init__(self, query_fc, query_pi, query_ps, spec_fc, spec_pi, spec_ps, spec_name):
        self.query_fc = query_fc
        self.query_pi = query_pi
        self.query_ps = query_ps
        self.spec_fc = spec_fc
        self.spec_pi = spec_pi
        self.spec_ps = spec_ps
        self.spec_name = spec_name

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
                print (float(len(skeleton_q[0]) - i)) / float(len(skeleton_q[0]))
                matched = skeleton_q[0].intersection(skeleton_s[0])
                for q_inf_path in skeleton_q[1]:
                    if matched.intersection(set(tuple(q_inf_path))):
                        print list(matched.intersection(set(tuple(q_inf_path)))), q_inf_path
                print '*****************'

                for s_inf_path in skeleton_s[1]:
                    if matched.intersection(set(tuple(s_inf_path))):
                        print list(matched.intersection(set(tuple(s_inf_path)))), s_inf_path
