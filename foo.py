import pprint

A = [['point'], ['point', 'floating']]
B = [['floating', 'undefined', 'point'], ['point']]
C = []

for a in A:
    for b in B:
        if a == b:
            C.append([a, b])
        elif all(len(x) >= 2 for x in [a, b]) and not set(a).isdisjoint(b):
            C.append([a, b])

pprint.pprint(C)