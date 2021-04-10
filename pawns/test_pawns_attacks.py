from test_figure_property import TestFigureProperty
from pawns_attacks import *
from constants import *


class TestPawnsAttacks(TestFigureProperty):
    """
    Special class to test pawns pushes functions
    """

    def __init__(self):
        super().__init__()

    def test_figure_property(self, pawns, enemy, color, expect):
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

    def test_black(self):
        """
        Test black attacks
        :return: None
        """

        expect = (bpawns >> 9) & ~SECTORS['H']
        expect |= (bpawns >> 7) & ~SECTORS['A']
        self.test_figure_property(bpawns, ~NULL, BLACK, expect)

        expect = (bknight >> 25) & ~SECTORS['H']
        expect |= (bknight >> 23) & ~SECTORS['A']
        self.test_figure_property(bknight >> 16, ~NULL, BLACK, expect)

        expect = (bking >> 17) & ~SECTORS['A']
        expect |= (bking >> 15) & ~SECTORS['A']
        self.test_figure_property(bking >> 8, ~NULL, BLACK, expect)

        expect = (bbishop >> 49) & ~SECTORS['H']
        expect |= (bbishop >> 47) & ~SECTORS['A']
        self.test_figure_property(bbishop >> 40, ~NULL, BLACK, expect)

    def test_white(self):
        """
        Test white attacks
        :return: None
        """

        expect = (wpawns << 9) & ~SECTORS['A']
        expect |= (wpawns << 7) & ~SECTORS['H']
        self.test_figure_property(wpawns, ~NULL, WHITE, expect)

        expect = (wknight << 25) & ~SECTORS['A']
        expect |= (wknight << 23) & ~SECTORS['H']
        self.test_figure_property(wknight << 16, ~NULL, WHITE, expect)

        expect = (wking << 17) & ~SECTORS['A']
        expect |= (wking << 15) & ~SECTORS['H']
        self.test_figure_property(wking << 8, ~NULL, WHITE, expect)

        expect = (wbishop << 49) & ~SECTORS['A']
        expect |= (wbishop << 47) & ~SECTORS['H']
        self.test_figure_property(wbishop << 40, ~NULL, WHITE, expect)
