from pawns_attacks import *
from constants import *


class TestPawnsAttacks:
    """
    Special class to test pawns pushes functions
    """

    def __init__(self):
        pass

    def __test_pawns_attacks(self, pawns, enemy, color, expect):
        """
        Test pawns_push() function
        //------------------------------------//
        :param pawns: bitarray of pawns
        :param enemy: bitarray of enemy figures
        :param color: color of pawns
        :param expect: expected result
        :return:None
        """

        result = pawns_attacks(pawns, enemy, color)

        assert result == expect, f'{result} != {expect}'

    def test_black_attacks(self):
        """
        Test black attacks
        :return: None
        """

        expect = (bpawns >> 9) & ~SECTORS['H']
        expect |= (bpawns >> 7) & ~SECTORS['A']
        self.__test_pawns_attacks(bpawns, ~NULL, BLACK, expect)

        expect = (bknight >> 25) & ~SECTORS['H']
        expect |= (bknight >> 23) & ~SECTORS['A']
        self.__test_pawns_attacks(bknight >> 16, ~NULL, BLACK, expect)

        expect = (bking >> 17) & ~SECTORS['A']
        expect |= (bking >> 15) & ~SECTORS['A']
        self.__test_pawns_attacks(bking >> 8, ~NULL, BLACK, expect)

        expect = (bbishop >> 49) & ~SECTORS['H']
        expect |= (bbishop >> 47) & ~SECTORS['A']
        self.__test_pawns_attacks(bbishop >> 40, ~NULL, BLACK, expect)

    def test_white_attacks(self):
        """
        Test white attacks
        :return: None
        """

        expect = (wpawns << 9) & ~SECTORS['A']
        expect |= (wpawns << 7) & ~SECTORS['H']
        self.__test_pawns_attacks(wpawns, ~NULL, WHITE, expect)

        expect = (wknight << 25) & ~SECTORS['A']
        expect |= (wknight << 23) & ~SECTORS['H']
        self.__test_pawns_attacks(wknight << 16, ~NULL, WHITE, expect)

        expect = (wking << 17) & ~SECTORS['A']
        expect |= (wking << 15) & ~SECTORS['H']
        self.__test_pawns_attacks(wking << 8, ~NULL, WHITE, expect)

        expect = (wbishop << 49) & ~SECTORS['A']
        expect |= (wbishop << 47) & ~SECTORS['H']
        self.__test_pawns_attacks(wbishop << 40, ~NULL, WHITE, expect)
