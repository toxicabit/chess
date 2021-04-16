from constants import SECTORS


def one_north(king, empty, taboo):

    north = king << 8

    return north & empty & ~taboo


def one_south(king, empty, taboo):

    south = king >> 8

    return south & empty & ~taboo


def one_west(king, empty, taboo):

    west = king >> 1 & ~SECTORS['H']

    return west & empty & ~taboo


def one_east(king, empty, taboo):

    east = king << 1 & ~SECTORS['A']

    return east & empty & ~taboo


def one_north_west(king, empty, taboo):

    nw = king << 7 & ~SECTORS['H']

    return nw & empty & ~taboo


def one_north_east(king, empty, taboo):

    ne = king << 9 & ~SECTORS['A']

    return ne & empty & ~taboo


def one_south_west(king, empty, taboo):

    sw = king >> 9 & ~SECTORS['H']

    return sw & empty & ~taboo


def one_south_east(king, empty, taboo):

    se = king >> 7 & ~SECTORS['A']

    return se & empty & ~taboo


def king_pushes(king, empty, taboo):

    n = one_north(king, empty, taboo)
    s = one_south(king, empty, taboo)
    w = one_west(king, empty, taboo)
    e = one_east(king, empty, taboo)
    nw = one_north_west(king, empty, taboo)
    ne = one_north_east(king, empty, taboo)
    sw = one_south_west(king, empty, taboo)
    se = one_south_east(king, empty, taboo)

    return n | s | w | e | nw | ne | sw | se
