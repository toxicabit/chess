from constants import SECTORS
from constants import WHITE


def north_west_one(pawns):
    """
    Move all white pawns forward to north
    west direction for one square
    //----------------------------------//
    :param pawns: bitarray of pawns
    :return: bitarray of possible attacks
    """

    return (pawns << 7) & ~SECTORS[0]


def north_east_one(pawns):
    """
    Move all white pawns forward to north
    east direction for one square
    //----------------------------------//
    :param pawns: bitarray of pawns
    :return: bitarray of possible attacks
    """

    return (pawns << 9) & ~SECTORS[7]


def south_west_one(pawns):
    """
    Move all black pawns forward to south
    west direction for one square
    //----------------------------------//
    :param pawns: bitarray of pawns
    :return: bitarray of possible attacks
    """

    return (pawns >> 9) & ~SECTORS[0]


def south_east_one(pawns):
    """
    Move all black pawns forward to south
    east direction for one square
    //----------------------------------//
    :param pawns: bitarray of pawns
    :return: bitarray of possible attacks
    """

    return (pawns >> 7) & ~SECTORS[7]


def pawns_nwest_attacks(pawns, enemy):
    """
    Calculate all possible north west
    attacks
    //----------------------------------//
    :param pawns: bitarray of white pawns
    :param enemy: bitarray of black figures
    :return: bitarray of possible west attacks
    """

    north_west = north_west_one(pawns)

    return north_west & enemy


def pawns_neast_attacks(pawns, enemy):
    """
    Calculate all possible north east
    attacks
    //----------------------------------//
    :param pawns: bitarray of white pawns
    :param enemy: bitarray of black figures
    :return: bitarray of possible east attacks
    """

    north_east = north_east_one(pawns)

    return north_east & enemy


def pawns_swest_attacks(pawns, enemy):
    """
    Calculate all possible south west
    attacks
    //----------------------------------//
    :param pawns: bitarray of black pawns
    :param enemy: bitarray of white figures
    :return: bitarray of possible west attacks
    """

    south_west = south_west_one(pawns)

    return south_west & enemy


def pawns_seast_attacks(pawns, enemy):
    """
    Calculate all possible south east
    attacks
    //----------------------------------//
    :param pawns: bitarray of black pawns
    :param enemy: bitarray of white figures
    :return: bitarray of possible east attacks
    """

    south_east = south_east_one(pawns)

    return south_east & enemy


def pawns_north_attacks(pawns, enemy):
    """
    Calculate all possible north attacks
    //----------------------------------//
    :param pawns: bitarray of white pawns
    :param enemy: bitarray of black figures
    :return: bitarray of possible north attacks
    """

    west_attacks = pawns_nwest_attacks(pawns, enemy)
    east_attacks = pawns_neast_attacks(pawns, enemy)

    return west_attacks | east_attacks


def pawns_south_attacks(pawns, enemy):
    """
    Calculate all possible south attacks
    //----------------------------------//
    :param pawns: bitarray of black pawns
    :param enemy: bitarray of white figures
    :return: bitarray of possible south attacks
    """

    west_attacks = pawns_swest_attacks(pawns, enemy)
    east_attacks = pawns_seast_attacks(pawns, enemy)

    return west_attacks | east_attacks


def pawns_attacks(pawns, enemy, color):
    """
    Calculate all possible attacks
    //----------------------------------//
    :param pawns: bitarray of pawns
    :param enemy: bitarray of enemy's figures
    :param color: pawns color
    :return: bitarray of possible attacks
    """

    if color == WHITE:
        return pawns_north_attacks(pawns, enemy)

    else:
        return pawns_south_attacks(pawns, enemy)


def pawn_attack(pawns, sector, enemy, color):
    """
    Calculate possible attacks for single
    pawn
    //----------------------------------//
    :param pawns: bitarray of pawns
    :param sector: bitarray for board column
    :param enemy: bitarray of enemy's figures
    :param color: pawns color
    :return: bitarray of possible attacks
    """

    return pawns_attacks(pawns & sector, enemy, color)
