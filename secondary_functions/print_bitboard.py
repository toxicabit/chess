"""

There is a function for correct
displaying of bitboards

"""


def print_bitboard(bitboard):
    for i in range(8):
        print(bitboard[i * 8: (i + 1) * 8])

    print('\n')
