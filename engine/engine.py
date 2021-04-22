from constants import *
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

    def __count_north_rays(self):
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

    def __count_south_rays(self):
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

    def __count_east_rays(self, sectors, null):  # #reverse SECTORS from GitHub
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

    def __count_west_rays(self, sectors, null):  # #reverse SECTORS from GitHub
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

    def __count_north_east_rays(self, sectors, null):
        """
        Count rays in north east direction
        for all square on the board

        :return: array of north east rays
        """

        north_east_rays = []
        north_east_ray = bt.bitarray('100000000' * 8)

        for i in range(8):
            north_east_ray.pop(-1)

        north_east_ray[-1] = False

        for i in range(8):
            current_ray = north_east_ray << i * 8
            mask = ~null
            sector = 0

            for j in range(8):
                mask &= ~sectors[sector]
                north_east_rays.append((current_ray << j) & mask)
                sector += 1

        return north_east_rays

    def __count_south_east_rays(self, sectors, null):
        """
        Count rays in south east direction
        for all square on the board

        :return: array of south east rays
        """

        south_east_rays = []
        south_east_ray = bt.bitarray('0' * 14 + '1000000' * 7 + '0')

        for i in range(8):
            current_ray = south_east_ray >> i * 8
            mask = ~null
            sector, rank = 0, []

            for j in range(8):
                mask &= ~sectors[sector]
                rank.append((current_ray << j) & mask)
                sector += 1

            rank.reverse()
            south_east_rays = south_east_rays + rank

        south_east_rays.reverse()

        return south_east_rays

    def __count_north_west_rays(self, sectors, null):
        """
        Count rays in north west direction
        for all square on the board

        :return: array of north west rays
        """

        north_west_rays = []
        north_west_ray = bt.bitarray('0' * 7 + '1000000' * 7 + '0' * 8)

        for i in range(8):
            current_ray = north_west_ray << i * 8
            mask = ~null
            sector, rank = 7, []

            for j in range(8):
                mask &= ~sectors[sector]
                rank.append((current_ray >> j) & mask)
                sector -= 1

            rank.reverse()

            north_west_rays = north_west_rays + rank

        return north_west_rays

    def __count_south_west_rays(self, sectors, null):
        """
        Count rays in south west direction
        for all square on the board

        :return: array of south west rays
        """

        south_west_rays = []
        south_west_ray = bt.bitarray('0' * 9 + '100000000' * 7)

        for i in range(8):
            south_west_ray.pop(-1)

        for i in range(8):
            current_ray = south_west_ray >> i * 8
            mask = ~null
            sector = 7

            for j in range(8):
                mask &= ~sectors[sector]
                south_west_rays.append((current_ray >> j) & mask)
                sector -= 1

        south_west_rays.reverse()

        return south_west_rays

    def __init__(self, player_color):

        self.__player_color = player_color
        self.__white = {'pawns': bt.bitarray('0' * 48 + '1' * 8 + '0' * 8),
                        'rook': bt.bitarray('0' * 56 + '1' + '0' * 6 + '1'),
                        'knight': bt.bitarray('0' * 57 + '1' + '0' * 4 + '1' + '0'),
                        'bishop': bt.bitarray('0' * 58 + '1' + '0' * 2 + '1' + '0' * 2),
                        'queen': bt.bitarray('0' * 59 + '1' + '0' * 4),
                        'king': bt.bitarray('0' * 60 + '1' + '0' * 3)}
        self.__black = {'pawns': bt.bitarray('0' * 8 + '1' * 8 + '0' * 48),
                        'rook': bt.bitarray('1' + '0' * 6 + '1' + '0' * 56),
                        'knight': bt.bitarray('0' + '1' + '0' * 4 + '1' + '0' * 57),
                        'bishop': bt.bitarray('0' * 2 + '1' + '0' * 2 + '1' + '0' * 58),
                        'queen': bt.bitarray('0' * 3 + '1' + '0' * 60),
                        'king': bt.bitarray('0' * 4 + '1' + '0' * 59)}
        self.__RANKS = [bt.bitarray('0' * 56 + '1' * 8),
                        bt.bitarray('0' * 48 + '1' * 8 + '0' * 8),
                        bt.bitarray('0' * 40 + '1' * 8 + '0' * 16),
                        bt.bitarray('0' * 32 + '1' * 8 + '0' * 24),
                        bt.bitarray('0' * 24 + '1' * 8 + '0' * 32),
                        bt.bitarray('0' * 16 + '1' * 8 + '0' * 40),
                        bt.bitarray('0' * 8 + '1' * 8 + '0' * 48),
                        bt.bitarray('1' * 8 + '0' * 56)]
        self.__SECTORS = [bt.bitarray('00000001' * 8),
                          bt.bitarray('00000010' * 8),
                          bt.bitarray('00000100' * 8),
                          bt.bitarray('00001000' * 8),
                          bt.bitarray('00010000' * 8),
                          bt.bitarray('00100000' * 8),
                          bt.bitarray('01000000' * 8),
                          bt.bitarray('10000000' * 8)]
        self.__north_rays = self.__count_north_rays()
        self.__north_east_rays = self.__count_north_east_rays(self.__SECTORS, NULL)
        self.__east_rays = self.__count_east_rays(self.__SECTORS, NULL)
        self.__south_east_rays = self.__count_south_east_rays(self.__SECTORS, NULL)
        self.__south_rays = self.__count_south_rays()
        self.__south_west_rays = self.__count_south_west_rays(self.__SECTORS, NULL)
        self.__west_rays = self.__count_west_rays(self.__SECTORS, NULL)
        self.__north_west_rays = self.__count_north_west_rays(self.__SECTORS, NULL)

    def __convert_to_bitboard(self, board_pos):
        """
        This function converts board position,
        which is represented by number from 0 to 63,
        from number to bitarray

        :param board_pos: number from 0 to 63
        :return: bitarray for given position
        """
        try:
            if board_pos < BOTTOM_LEFT or board_pos > TOP_RIGHT:
                raise ValueError

            bit_pos = bt.bitarray('0' * (TOP_RIGHT - board_pos) + '1' + '0' * board_pos)

            return bit_pos

        except ValueError:
            print('ERROR: ' + str(board_pos) + ' is invalid position')
            print('INCORRECT:' + str(BOTTOM_LEFT) + ' <= ' + str(board_pos) + ' <= ' + str(TOP_RIGHT))

            return NULL
