from constants import SECTORS


def north_north_east_attack(knights, enemy):
    """
    Count possible squares for push
    to north north east direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param enemy: bitarray of enemy squares
    :return: bitarray of possible pushes
    """

    nne = (knights << 17) & ~SECTORS['A']
    return nne & enemy


def north_east_east_attack(knights, enemy):
    """
    Count possible squares for push
    to north east east direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param enemy: bitarray of enemy squares
    :return: bitarray of possible pushes
    """

    not_a_b = ~SECTORS['A'] & ~SECTORS['B']
    nee = (knights << 10) & not_a_b

    return nee & enemy


def south_east_east_attack(knights, enemy):
    """
    Count possible squares for push
    to south east east direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param enemy: bitarray of enemy squares
    :return: bitarray of possible pushes
    """

    not_a_b = ~SECTORS['A'] & ~SECTORS['B']
    see = (knights >> 6) & not_a_b

    return see & enemy


def south_south_east_attack(knights, enemy):
    """
    Count possible squares for push
    to south south east direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param enemy: bitarray of enemy squares
    :return: bitarray of possible pushes
    """

    sse = (knights >> 15) & ~SECTORS['A']

    return sse & enemy


def north_north_west_attack(knights, enemy):
    """
    Count possible squares for push
    to north north west direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param enemy: bitarray of enemy squares
    :return: bitarray of possible pushes
    """

    nnw = (knights << 15) & ~SECTORS['H']

    return nnw & enemy


def north_west_west_attack(knights, enemy):
    """
    Count possible squares for push
    to north west west direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param enemy: bitarray of enemy squares
    :return: bitarray of possible pushes
    """

    not_g_h = ~SECTORS['G'] & ~SECTORS['H']
    nww = (knights << 6) & not_g_h

    return nww & enemy


def south_west_west_attack(knights, enemy):
    """
    Count possible squares for push
    to south west west direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param enemy: bitarray of enemy squares
    :return: bitarray of possible pushes
    """

    not_g_h = ~SECTORS['G'] & ~SECTORS['H']
    sww = (knights >> 10) & not_g_h

    return sww & enemy


def south_south_west_attack(knights, enemy):
    """
    Count possible squares for push
    to south south west direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param enemy: bitarray of enemy squares
    :return: bitarray of possible pushes
    """

    ssw = (knights >> 17) & ~SECTORS['H']

    return ssw & enemy


def knights_attack(knights, enemy):
    """
    Count possible squares for push
    //-----------------------------//
    :param knights: bitarray of knights
    :param enemy: bitarray of enemy squares
    :return: bitarray of possible pushes
    """

    nnw = north_north_west_attack(knights, enemy)
    nww = north_west_west_attack(knights, enemy)
    sww = south_west_west_attack(knights, enemy)
    ssw = south_south_west_attack(knights, enemy)
    sse = south_south_east_attack(knights, enemy)
    see = south_east_east_attack(knights, enemy)
    nee = north_east_east_attack(knights, enemy)
    nne = north_north_east_attack(knights, enemy)

    pushes = nnw | nww | sww | ssw
    pushes |= sse | see | nee | nne

    return pushes
