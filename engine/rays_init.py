"""

There is  class which initialize rays

Rays are directions which can be attacked
by sliced figures like Queen, Rook or
Bishop

"""


import bitarray as bt


from constants import * 


class RaysInitializer:

    @staticmethod
    def count_north_rays():
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

    @staticmethod
    def count_south_rays():
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

    @staticmethod
    def count_east_rays():
        """
        Count rays in east direction
        for all square on the board

        :return: array of east rays
        """

        east_rays = []
        east_ray = bt.bitarray('0' * 56 + '1' * 7 + '0')

        for i in range(8):
            current_ray = east_ray << i * 8
            mask = ~NULL
            sector = 0

            for j in range(8):
                mask &= ~SECTORS[sector]
                east_rays.append((current_ray << j) & mask)
                sector += 1

        return east_rays

    @staticmethod
    def count_west_rays():
        """
        Count rays in west direction
        for all square on the board

        :return: array of west rays
        """

        west_rays = []
        west_ray = bt.bitarray('0' + '1' * 7 + '0' * 56)

        for i in range(8):
            current_ray = west_ray >> i * 8
            mask = ~NULL
            sector = 7

            for j in range(8):
                mask &= ~SECTORS[sector]
                west_rays.append((current_ray >> j) & mask)
                sector -= 1

        west_rays.reverse()

        return west_rays

    @staticmethod
    def count_north_east_rays():
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
            mask = ~NULL
            sector = 0

            for j in range(8):
                mask &= ~SECTORS[sector]
                north_east_rays.append((current_ray << j) & mask)
                sector += 1

        return north_east_rays

    @staticmethod
    def count_south_east_rays():
        """
        Count rays in south east direction
        for all square on the board

        :return: array of south east rays
        """

        south_east_rays = []
        south_east_ray = bt.bitarray('0' * 14 + '1000000' * 7 + '0')

        for i in range(8):
            current_ray = south_east_ray >> i * 8
            mask = ~NULL
            sector, rank = 0, []

            for j in range(8):
                mask &= ~SECTORS[sector]
                rank.append((current_ray << j) & mask)
                sector += 1

            rank.reverse()
            south_east_rays = south_east_rays + rank

        south_east_rays.reverse()

        return south_east_rays

    @staticmethod
    def count_north_west_rays():
        """
        Count rays in north west direction
        for all square on the board

        :return: array of north west rays
        """

        north_west_rays = []
        north_west_ray = bt.bitarray('0' * 7 + '1000000' * 7 + '0' * 8)

        for i in range(8):
            current_ray = north_west_ray << i * 8
            mask = ~NULL
            sector, rank = 7, []

            for j in range(8):
                mask &= ~SECTORS[sector]
                rank.append((current_ray >> j) & mask)
                sector -= 1

            rank.reverse()

            north_west_rays = north_west_rays + rank

        return north_west_rays

    @staticmethod
    def count_south_west_rays():
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
            mask = ~NULL
            sector = 7

            for j in range(8):
                mask &= ~SECTORS[sector]
                south_west_rays.append((current_ray >> j) & mask)
                sector -= 1

        south_west_rays.reverse()

        return south_west_rays
