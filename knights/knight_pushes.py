from constants import SECTORS


def north_north_east(knights, empty):
    """
    Count possible squares for push
    to north north east direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param empty: bitarray of empty squares
    :return: bitarray of possible pushes
    """

    nne = (knights << 17) & ~SECTORS['A']
    return nne & empty


def north_east_east(knights, empty):
    """
    Count possible squares for push
    to north east east direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param empty: bitarray of empty squares
    :return: bitarray of possible pushes
    """

    not_a_b = ~SECTORS['A'] & ~SECTORS['B']
    nee = (knights << 10) & not_a_b

    return nee & empty


def south_east_east(knights, empty):
    """
    Count possible squares for push
    to south east east direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param empty: bitarray of empty squares
    :return: bitarray of possible pushes
    """

    not_a_b = ~SECTORS['A'] & ~SECTORS['B']
    see = (knights >> 6) & not_a_b

    return see & empty


def south_south_east(knights, empty):
    """
    Count possible squares for push
    to south south east direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param empty: bitarray of empty squares
    :return: bitarray of possible pushes
    """

    sse = (knights >> 15) & ~SECTORS['A']

    return sse & empty


def north_north_west(knights, empty):
    """
    Count possible squares for push
    to north north west direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param empty: bitarray of empty squares
    :return: bitarray of possible pushes
    """

    nnw = (knights << 15) & ~SECTORS['H']

    return nnw & empty


def north_west_west(knights, empty):
    """
    Count possible squares for push
    to north west west direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param empty: bitarray of empty squares
    :return: bitarray of possible pushes
    """

    not_g_h = ~SECTORS['G'] & ~SECTORS['H']
    nww = (knights << 6) & not_g_h

    return nww & empty


def south_west_west(knights, empty):
    """
    Count possible squares for push
    to south west west direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param empty: bitarray of empty squares
    :return: bitarray of possible pushes
    """

    not_g_h = ~SECTORS['G'] & ~SECTORS['H']
    sww = (knights >> 10) & not_g_h

    return sww & empty


def south_south_west(knights, empty):
    """
    Count possible squares for push
    to south south west direction
    //-----------------------------//
    :param knights: bitarray of knights
    :param empty: bitarray of empty squares
    :return: bitarray of possible pushes
    """

    ssw = (knights >> 17) & ~SECTORS['H']

    return ssw & empty


def knights_push(knights, empty):
    """
    Count possible squares for push
    //-----------------------------//
    :param knights: bitarray of knights
    :param empty: bitarray of empty squares
    :param empty: bitarray of empty squares
    :return: bitarray of possible pushes
    """

    nnw = north_north_west(knights, empty)
    nww = north_west_west(knights, empty)
    sww = south_west_west(knights, empty)
    ssw = south_south_west(knights, empty)
    sse = south_south_east(knights, empty)
    see = south_east_east(knights, empty)
    nee = north_east_east(knights, empty)
    nne = north_north_east(knights, empty)

    pushes = nnw | nww | sww | ssw
    pushes |= sse | see | nee | nne

    return pushes
