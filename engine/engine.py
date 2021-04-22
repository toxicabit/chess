import bitarray as bt


"""
              Bitboard scheme:
         f: bit position -> board
     A    B    C    D    E    F    G    H
  +----+----+----+----+----+----+----+----+
8 | 56 | 57 | 58 | 59 | 60 | 61 | 62 | 63 |
  +----+----+----+----+----+----+----+----+
7 | 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 |
  +----+----+----+----+----+----+----+----+
6 | 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 |
  +----+----+----+----+----+----+----+----+
5 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 |
  +----+----+----+----+----+----+----+----+
4 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 |
  +----+----+----+----+----+----+----+----+
3 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
  +----+----+----+----+----+----+----+----+
2 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 |
  +----+----+----+----+----+----+----+----+
1 |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |
  +----+----+----+----+----+----+----+----+
  
                     TERMS
//---------------------------------------------//
RANK - board's row, for example, 1
SECTOR - board's column, for example, A
SLIDING FIGURE - queen, bishop, rook
RAY - direction which sliding figure can attack 
"""


class Grandmaster:

    def count_north_rays(self):
        """
        Count rays in north direction
        for all square on the board

        :return: array of north rays
        """

        north_rays = []
        north_ray = bt.bitarray('00000001' * 7 + '0' * 8)

        for i in range(8):
            current_ray = north_ray << i * 8

            for j in range(8):
                north_rays.append(current_ray << j)

        return north_rays

    def count_south_rays(self):
        """
        Count rays in north direction
        for all square on the board

        :return: array of north rays
        """

        south_rays = []
        south_ray = bt.bitarray('0' * 8 + '10000000' * 7)

        for i in range(8):
            current_ray = south_ray >> i * 8

            for j in range(8):
                south_rays.append(current_ray >> j)

        south_rays.reverse()

        return south_rays

    def count_east_rays(self, sectors, null):  # #reverse SECTORS from GitHub
        """
        Count rays in east direction
        for all square on the board

        :return: array of east rays
        """

        east_rays = []
        east_ray = bt.bitarray('0' * 56 + '1' * 7 + '0')

        for i in range(8):
            current_ray = east_ray << i * 8
            mask = ~null
            sector = 0

            for j in range(8):
                mask &= ~sectors[sector]
                east_rays.append((current_ray << j) & mask)
                sector += 1

        return east_rays

    def count_west_rays(self, sectors, null): # #reverse SECTORS from GitHub
        """
        Count rays in west direction
        for all square on the board

        :return: array of west rays
        """

        west_rays = []
        west_ray = bt.bitarray('0' + '1' * 7 + '0' * 56)

        for i in range(8):
            current_ray = west_ray >> i * 8
            mask = ~null
            sector = 7

            for j in range(8):
                mask &= ~sectors[sector]
                west_rays.append((current_ray >> j) & mask)
                sector -= 1

        west_rays.reverse()

        return west_rays

    def __init__(self):
        pass
