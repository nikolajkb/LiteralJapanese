def distance(source, target):
    if source == target:
        return 0

        # Prepare a matrix
    slen, tlen = len(source), len(target)
    dist = [[0 for i in range(tlen + 1)] for x in range(slen + 1)]
    for i in range(slen + 1):
        dist[i][0] = i
    for j in range(tlen + 1):
        dist[0][j] = j

    # Counting distance, here is my function
    for i in range(slen):
        for j in range(tlen):
            cost = 0 if source[i] == target[j] else 1
            dist[i + 1][j + 1] = min(
                dist[i][j + 1] + 1,  # deletion
                dist[i + 1][j] + 1,  # insertion
                dist[i][j] + cost  # substitution
            )
    return dist[-1][-1]
    #return lev_dist_rec(source, len(source), target, len(target))


def lev_dist_rec(source, len_s, target, len_t):
    if len_s == 0:
        return len_t
    if len_t == 0:
        return len_s

    if source[len_s - 1] == target[len_t - 1]:
        cost = 0
    else:
        cost = 1

    return min(lev_dist_rec(source, len_s - 1, target, len_t    ) + 1,
               lev_dist_rec(source, len_s    , target, len_t - 1) + 1,
               lev_dist_rec(source, len_s - 1, target, len_t - 1) + cost)
