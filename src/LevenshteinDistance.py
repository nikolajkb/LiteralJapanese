# adapted from the following implementation:
# https://stackoverflow.com/a/5567464
# result changed to tuple in order to show which operations were performed

from Equality import equals
import Constants


def distance(source, target):
    if source == target:
        return (0,0,0)

    slen, tlen = len(source), len(target)
    dist = [[(0,0,0) for i in range(tlen + 1)] for x in range(slen + 1)]
    for i in range(slen + 1):
        dist[i][0] = (i,0,0)
    for j in range(tlen + 1):
        dist[0][j] = (0,j,0)

    for i in range(slen):
        for j in range(tlen):
            equal = equals(source[i],target[j])
            if Constants.WEIGHTED_SIMILARITY and not equal:
                # similarity approaches 1 as words are more similar.
                similarity = Constants.SIMILARITY.similarity(source[i],target[j])
                cost = (0,0,1-similarity)
            else:
                cost = (0,0,0) if equal else (0,0,1)
            dist[i + 1][j + 1] = min(
                add(dist[i][j + 1], (1,0,0)),  # deletion
                add(dist[i + 1][j], (0,1,0)),  # insertion
                add(dist[i][j], cost)  # substitution
                , key=lambda x: total(x)
            )

    return dist[-1][-1]


def total(tup):
    (a,b,c) = tup
    return a + b + c


def add(tup,tup2):
    (a,b,c) = tup
    (x,y,z) = tup2
    return (a+x,b+y,c+z)
