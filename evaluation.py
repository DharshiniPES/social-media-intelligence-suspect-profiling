def precision(tp, fp):

    if tp + fp == 0:
        return 0

    return tp / (tp + fp)


def recall(tp, fn):

    if tp + fn == 0:
        return 0

    return tp / (tp + fn)


def f1_score(p, r):

    if p + r == 0:
        return 0

    return 2 * (p * r) / (p + r)