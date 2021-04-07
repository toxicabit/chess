from constants import RANKS
from constants import WHITE


def north_one(pawns):
    """
    Move all white pawns forward for one
    square
    //----------------------------------//
    :param pawns: bitarray of pawns
    :return: bitarray of possible pushes
    """

    return pawns << 8


def north_two(pawns, rank):
    """
    Move all white pawns forward for two
    squares
    //----------------------------------//
    :param pawns: bitarray of pawns
    :param rank: rank's bitarray
    :return: bitarray of possible pushes
    """

    return (pawns & rank) << 16


def south_two(pawns, rank):
    """
    Move all black pawns forward for two
    squares
    //----------------------------------//
    :param pawns: bitarray of pawns
    :param rank: rank's bitarray
    :return: bitarray of possible pushes
    """

    return (pawns & rank) >> 16


def south_one(pawns):
    """
    Move all black pawns forward for one
    square
    //----------------------------------//
    :param pawns: bitarray of pawns
    :return: bitarray of possible pushes
    """

    return pawns >> 8


def pawns_single_push(pawns, empty, color):
    """
    Count all possible single pushes forward
    for pawn's bitboard
    //------------------------------------//
    :param pawns: bitarray of pawns
    :param empty: bitarray empty squares
    :param color: color of pawns
    :return: bitarray of possible pushes
    """

    if color == WHITE:
        return north_one(pawns) & empty

    else:
        return south_one(pawns) & empty


def pawns_double_push(pawns, empty, color):
    """
    Count all possible double pushes forward
    for pawn's bitboard
    //------------------------------------//
    :param pawns: bitarray of pawns
    :param empty: bitarray empty squares
    :param color: color of pawns
    :return: bitarray of possible pushes
    """

    if color == WHITE:
        rank = RANKS[1]
        return north_two(pawns, rank) & empty

    else:
        rank = RANKS[6]
        return south_two(pawns, rank) & empty


def pawns_push(pawns, empty, color):
    """
    Count all possible pushes forward for
    pawn's bitboard
    //------------------------------------//
    :param pawns: bitarray of pawns
    :param empty: bitarray empty squares
    :param color: color of pawns
    :return: bitarray of possible pushes
    """

    single = pawns_single_push(pawns, empty, color)
    return single | pawns_double_push(pawns, empty, color)
