"""

There is a function for displaying of bitboards


"""


def print_bitboard(bitboard):
    for i in range(8):
        line = bitboard[i * 8: (i + 1) * 8]
        line.reverse()
        print(line)

    print('\n')
