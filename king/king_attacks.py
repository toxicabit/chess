from constants import SECTORS


def one_north(king, enemy, taboo):

    north = king << 8

    return north & enemy & ~taboo


def one_south(king, enemy, taboo):

    south = king >> 8

    return south & enemy & ~taboo


def one_west(king, enemy, taboo):

    west = king >> 1 & ~SECTORS['H']

    return west & enemy & ~taboo


def one_east(king, enemy, taboo):

    east = king << 1 & ~SECTORS['A']

    return east & enemy & ~taboo


def one_north_west(king, enemy, taboo):

    nw = king << 7 & ~SECTORS['H']

    return nw & enemy & ~taboo


def one_north_east(king, enemy, taboo):

    ne = king << 9 & ~SECTORS['A']

    return ne & enemy & ~taboo


def one_south_west(king, enemy, taboo):

    sw = king >> 9 & ~SECTORS['H']

    return sw & enemy & ~taboo


def one_south_east(king, enemy, taboo):

    se = king >> 7 & ~SECTORS['A']

    return se & enemy & ~taboo


def king_pushes(king, enemy, taboo):

    n = one_north(king, enemy, taboo)
    s = one_south(king, enemy, taboo)
    w = one_west(king, enemy, taboo)
    e = one_east(king, enemy, taboo)
    nw = one_north_west(king, enemy, taboo)
    ne = one_north_east(king, enemy, taboo)
    sw = one_south_west(king, enemy, taboo)
    se = one_south_east(king, enemy, taboo)

    return n | s | w | e | nw | ne | sw | se
